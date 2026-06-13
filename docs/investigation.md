# Investigation — Autopoiesis through composition

> A multipart investigation, built up gracefully and compositionally, **driven by the
> biological schema framework**. Each increment is a *study*; the schema framework
> computes each study's *acceptance*; the visualizations are each study's *evidence*.

## Research question

Can a **precarious, self-bounding identity** — a cell that produces its own boundary —
be assembled by composing existing parts, and *how much of itself does each increment
produce*? Progress is measured, not asserted: by **operational closure** (the autopoiesis
meter) and by **precariousness** (does the identity dissipate when self-production stops?).

## How the biological schema framework drives it

This is the same investigation framework as the rest of the ecosystem (investigation →
studies → baselines/runs → acceptance → findings → verdicts), but its **acceptance criteria
are computed by the biological schema framework**, not authored:

| Spine slot | Here, it is… |
|---|---|
| baseline composite | the increment's composed model (membrane/metabolism, then + parts) |
| acceptance criterion | a **closure target** from the autopoiesis meter: `gap = requires \ provides \ boundary` shrinks to a stated set |
| behavior test | **precariousness**: fed → the boundary persists; starved → it dissipates |
| verdict | does this increment achieve its targeted closure *and* stay precarious? |
| finding | which type moved from imported → self-produced; which part was needed |
| evidence | the figures (`figures/`) — the dynamics, the emergent boundary, the closure cycle |

The typed `molecular_species` vocabulary and the capability catalog (provides/requires) are
not plumbing — they *are* the acceptance computation. The catalog is the autopoiesis meter.

## The studies (the increments)

Each study folds one part inside the already-self-bounding unit, moving a component-type
from imported → self-produced and shrinking the boundary inward.

| # | Study | Part folded in | Acceptance (closure target) | Precariousness | Status |
|---|---|---|---|---|---|
| **1** | Minimal membrane/metabolism loop | — (the membrane, built new) | self-produce the **boundary** (volume, membrane); `gap = ∅`, boundary = `{nutrient}` | fed persists · starved dissipates | **PASS** ✅ |
| 2 | Real metabolic interior | v2ecoli metabolism (FBA) | self-produce the **building blocks**; boundary → `{glucose, ions, energy}` | maintained under real metabolism | planned |
| 3 | Self-produced machinery | expression (transcription/translation) | the enzymes/machinery are **made, not given** | maintained | planned |
| 4 | Reproduction | replication / division | the genome copies → the closed unit reproduces | maintained across division | planned |

**Investigation verdict** = the final study reaches **operational closure**: the gap set is
just `{nutrients, energy}`. The cell makes everything else, including itself.

## Study 1 — result

The minimal membrane/metabolism co-construction loop **PASSES**:

- **Operational closure: CLOSED** — the network self-produces 5/5 required types
  (`nutrient, precursor, lipid, membrane_lipids, volume`); `gap = ∅`; boundary = `{nutrient}`.
- **Precariousness holds** — fed, the emergent boundary grows and is self-maintained
  (volume 3 → 10); starved, it dissipates (volume 3 → 0.2). The identity is a *process*,
  not a container.
- **The boundary emerges** — `volume = geometry(membrane lipids)`, derived every tick,
  never declared.
- **The volume coupling is load-bearing** — lipid synthesis is bimolecular, so it runs on
  `concentration = count / volume`; the cell self-regulates its size through dilution.

Evidence: `figures/index.html` (6 figures). Tests: `tests/test_loop.py` (6/6).

## Connection to the dashboard investigation framework

This document is the investigation in narrative form. The natural next step is to wire it
into the actual framework — each study as a `study.yaml` whose acceptance criterion calls
the autopoiesis meter, so closure and precariousness roll up automatically into the
investigation verdict and surface in the dashboard, with the figures as the study report.
That makes the schema framework *literally* drive the spine. (Increment 1 is built and
green; the framework wiring is the next graceful step.)
