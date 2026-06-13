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
from . import viz

WS = Path(__file__).resolve().parent.parent
STUDY_DIR = WS / "studies" / "study-1-membrane-metabolism-loop"
STUDY_YAML = STUDY_DIR / "study.yaml"

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


def sync():
    measures, context = compute_measures()
    study = _yaml.load(STUDY_YAML.read_text(encoding="utf-8"))
    outcomes = evaluate(study, measures)
    verdict = gate_evaluator(outcomes)

    study["runs"] = [{
        "name": "autopoiesis-meter",
        "status": "completed",
        "composite": "membrane-metabolism-loop",
        "outcomes": {t: dict(o) for t, o in outcomes.items()},
    }]
    study["pipeline_gate"]["gate_evaluator"] = verdict
    study["findings"] = _findings(context, outcomes)

    with STUDY_YAML.open("w", encoding="utf-8") as f:
        _yaml.dump(study, f)
    _copy_figures()

    print(f"autopoiesis spine → verdict: {verdict['result'].upper()}")
    for t, o in outcomes.items():
        print(f"  {o['result']:4s}  {t:28s} observed={o['observed']}")
    return verdict


if __name__ == "__main__":
    sync()
