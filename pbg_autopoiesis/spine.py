"""The autopoiesis spine — the biological schema framework driving the study.

Runs the membrane/metabolism loop, computes the autopoiesis meter (operational
closure) and the precariousness measures, applies the study's AUTHORED behavior-test
bands to those computed measures, and WRITES the results into the study's spine fields
(``runs`` outcomes, ``pipeline_gate.gate_evaluator``, ``findings``) — plus the figures.

The result is a dashboard study whose verdict the schema framework *computed*. This is
the same authored-band / computed-measure split as the real spine, with the autopoiesis
meter as the measure source.

    PYTHONPATH=. <pb-venv>/bin/python -m pbg_autopoiesis.spine
"""
from __future__ import annotations

import shutil
from pathlib import Path

from ruamel.yaml import YAML

from .loop import build_loop, run_trajectory, closure_of_loop
from . import viz, spatial

WS = Path(__file__).resolve().parent.parent
STUDY_DIR = WS / "studies" / "study-1-membrane-metabolism-loop"
STUDY_YAML = STUDY_DIR / "study.yaml"
STUDY2_DIR = WS / "studies" / "study-2-spatial-containment"

_yaml = YAML()
_yaml.preserve_quotes = True
_yaml.allow_unicode = True
_yaml.width = 100


# --- the measures the meter produces --------------------------------------

def compute_measures():
    """Run the loop + meter; return the derived scalars the behavior tests read."""
    closure = closure_of_loop()
    fed = run_trajectory(build_loop(supply_rate=2.0), steps=160)
    starved = run_trajectory(build_loop(supply_rate=0.0), steps=160)
    measures = {
        "closure_gap_size": float(len(closure["gap"])),
        "precariousness_ratio": (starved[-1] / fed[-1]) if fed[-1] else 1.0,
        "fed_volume_growth": (fed[-1] / fed[0]) if fed[0] else 0.0,
    }
    context = {"closure": closure, "fed": fed, "starved": starved}
    return measures, context


# --- apply an authored pass_if band to a computed measure -----------------

def _passes(pass_if, value) -> bool:
    op = pass_if["op"]
    if op == "range":
        return pass_if["low"] <= value <= pass_if["high"]
    thr = pass_if["value"]
    return {
        "<=": value <= thr, "<": value < thr,
        ">=": value >= thr, ">": value > thr,
        "==": value == thr, "!=": value != thr,
    }[op]


def evaluate(study, measures):
    """For each authored behavior test, look up its computed measure + apply its band."""
    outcomes = {}
    for test in study.get("behavior_tests", []):
        field = test["measure"]["field"]
        value = measures[field]
        outcomes[test["name"]] = {
            "result": "PASS" if _passes(test["pass_if"], value) else "FAIL",
            "observed": round(float(value), 4),
        }
    return outcomes


def gate_evaluator(outcomes):
    """The verdict rule (matches study_verdict): passed iff no FAIL and >=1 PASS."""
    results = [o["result"] for o in outcomes.values()]
    fails = [t for t, o in outcomes.items() if o["result"] == "FAIL"]
    if fails:
        result = "failed"
    elif "PASS" in results:
        result = "passed"
    else:
        result = "not_started"
    return {"result": result, "blocked_by": fails, "evaluated_by": "code",
            "diverges_from_authored": False}


def _findings(context, outcomes):
    closure = context["closure"]
    fed, starved = context["fed"], context["starved"]
    return [
        {"id": "F-01", "kind": "structural", "status": "confirms",
         "statement": (f"The network is operationally closed: it self-produces "
                       f"{closure['n_self_produced']}/{closure['n_required']} required types "
                       f"({', '.join(closure['self_produced'])}); only nutrient crosses the "
                       f"boundary. The cell produces its own boundary."),
         "evidence": {"from_test": "operational-closure",
                      "observed": outcomes["operational-closure"]["observed"],
                      "units": "types in gap"}},
        {"id": "F-02", "kind": "biological", "status": "confirms",
         "statement": (f"The identity is precarious — a process, not a container. Fed, the "
                       f"self-produced boundary grows and is maintained (volume "
                       f"{fed[0]:.2f} → {fed[-1]:.2f}); starved of nutrient it dissipates "
                       f"({starved[0]:.2f} → {starved[-1]:.3f}). It persists only through "
                       f"continuous self-production."),
         "evidence": {"from_test": "precariousness",
                      "observed": outcomes["precariousness"]["observed"],
                      "units": "starved/fed volume ratio"}},
    ]


def _copy_figures():
    viz.main()
    charts = STUDY_DIR / "charts"
    charts.mkdir(exist_ok=True)
    for png in sorted((WS / "figures").glob("*.png")):
        shutil.copy(png, charts / png.name)
    return charts


def _spatial_findings(context, outcomes):
    held, leaky = context["held"], context["leaky"]
    return [
        {"id": "F-01", "kind": "structural", "status": "confirms",
         "statement": (f"The membrane holds the individual together against diffusion: the "
                       f"interior stays {held['containment']:.0f}× more concentrated than the "
                       f"medium with the self-produced membrane, vs {leaky['containment']:.1f}× "
                       f"with metabolism alone. The membrane — not metabolism — is what contains."),
         "evidence": {"from_test": "membrane-counters-diffusion",
                      "observed": outcomes["membrane-counters-diffusion"]["observed"],
                      "units": "containment fold vs no-membrane"}},
        {"id": "F-02", "kind": "biological", "status": "confirms",
         "statement": (f"Containment is precarious: starved, the membrane decays, the boundary "
                       f"leaks, and the individual disperses — retaining only "
                       f"{outcomes['spatial-precariousness']['observed']*100:.0f}% of its "
                       f"containment. The individual is held together only as a process."),
         "evidence": {"from_test": "spatial-precariousness",
                      "observed": outcomes["spatial-precariousness"]["observed"],
                      "units": "starved/held containment fraction"}},
    ]


def _apply_meter(study_path, measures, context, findings_fn, run_name, composite):
    """Generic: apply the study's authored bands to the computed measures, write the
    run outcomes + gate_evaluator + findings. The schema framework driving the spine."""
    study = _yaml.load(study_path.read_text(encoding="utf-8"))
    outcomes = evaluate(study, measures)
    verdict = gate_evaluator(outcomes)
    study["runs"] = [{"name": run_name, "status": "completed", "composite": composite,
                      "outcomes": {t: dict(o) for t, o in outcomes.items()}}]
    study["pipeline_gate"]["gate_evaluator"] = verdict
    study["findings"] = findings_fn(context, outcomes)
    with study_path.open("w", encoding="utf-8") as f:
        _yaml.dump(study, f)
    _report(study_path.parent.name, verdict, outcomes)
    return verdict


def _report(slug, verdict, outcomes):
    print(f"{slug} → verdict: {verdict['result'].upper()}")
    for t, o in outcomes.items():
        print(f"  {o['result']:4s}  {t:30s} observed={o['observed']}")


def sync():
    """Study 1 — the membrane/metabolism loop (operational closure + precariousness)."""
    measures, context = compute_measures()
    v = _apply_meter(STUDY_YAML, measures, context, _findings,
                     "autopoiesis-meter", "membrane-metabolism-loop")
    _copy_figures()
    return v


def sync_study2():
    """Study 2 — spatial containment (the membrane holds the individual together)."""
    measures, context = spatial.containment_metrics()
    v = _apply_meter(STUDY2_DIR / "study.yaml", measures, context, _spatial_findings,
                     "containment-meter", "spatial-containment")
    viz.spatial_main(STUDY2_DIR / "charts")
    return v


def sync_all():
    sync()
    sync_study2()


if __name__ == "__main__":
    sync_all()
