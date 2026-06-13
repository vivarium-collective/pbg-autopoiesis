# Roadmap — from autopoiesis to agency to evolution

> The investigation builds one thing, elaborating itself: a **precarious identity** that
> first bounds itself, then holds itself together in space, then acts to survive, then
> reproduces and is selected. Every new capability is **in service of maintaining the
> identity** — this is the enactivist life→mind→evolution continuity, built as composable
> studies and measured by the schema framework.

Each study is an increment in the dashboard investigation; its acceptance is a *computed*
metric (the autopoiesis meter and its spatial/viability extensions), its behavior test is a
form of **precariousness** (does the capability, when withdrawn, dissolve the identity?), and
its evidence is a gallery of figures.

---

## The spine

| # | Study | The capability gained | Enactivist role | Status |
|---|---|---|---|---|
| 1 | Minimal membrane/metabolism loop | **self-bounding** — operational closure + precariousness | *autopoiesis* (a self) | **DONE** ✅ |
| 2 | Spatial containment | **individuation** — the membrane counters diffusion; the individual is held together | *the spatial individual* | this turn |
| 3 | Adaptive chemotaxis | **agency** — move toward food to survive | *sense-making / adaptivity* | planned |
| 4 | Growth & division | **reproduction** — heterogeneous daughters → a population | *the lineage* | planned |
| 5 | Selection | **evolution** — differential survival under pressure | *natural selection* | planned |
| R | Biological realism (parallel) | fold in real v2ecoli metabolism | *grounding* | parallel track |

---

## Study 2 — Spatial containment *(building now)*

**The question study 1 left open.** In study 1 "inside" was a scalar volume. In a real medium the
self-produced molecules would **diffuse away** — the individual would dissolve into the environment.
So what *holds the individual together*? The membrane, as a **spatial permeability barrier**: it keeps
the self-produced interior IN while letting nutrient cross. And it is itself **made by the metabolism it
contains** — so containment is self-produced. This is the autopoiesis of containment.

**Model.** A 1-D lattice (a row of bins) is the medium. The cell occupies an interior region bounded by
membrane. Interior molecules **diffuse** along the lattice; the membrane **gates the cross-boundary flux**
(permeability falls as membrane coverage rises). Metabolism (study 1's loop) runs inside and produces the
lipids that build the membrane that reduces the leak that would otherwise dissolve the metabolism.

**Acceptance (computed).**
- **containment** — the interior/exterior concentration ratio is maintained against diffusion (with the
  self-produced membrane) and collapses without it. *Behavior test:* `containment_ratio` high with membrane,
  → 1 (dispersed) without.
- **precariousness, spatial edition** — stop the metabolism → the membrane decays → permeability rises →
  the interior disperses → the individual dissolves. The identity is held together only as a process.

**Evidence.** The concentration profile over space and time: a contained peak (membrane) vs. a spreading,
flattening profile (no membrane / starved). The dissolution of a starved individual.

**Substrate note.** Built minimally here (a hand-rolled 1-D diffusion + membrane gate). The ecosystem's
`spatio_flux` package (spatial process-bigraph) is the path to richer 2-D fields and is the natural
"compose an existing part" upgrade for later spatial studies.

---

## Study 3 — Adaptive chemotaxis (agency)

**The capability.** The individual **moves toward food to survive**. A nutrient gradient in the environment;
the agent senses it and biases its motion up-gradient. Crucially, the gradient is not "information" in the
abstract — it is **meaningful from the perspective of the precarious identity**: up-gradient = viable,
down-gradient = dissolution. This is Di Paolo's **adaptivity** (the system actively regulates its coupling
to stay viable) and Varela's **sense-making** (significance arises for a self that has something at stake).

**Model.** The cell from study 2 placed in a nutrient field with a gradient. A **sensorimotor loop**: sense
local nutrient (or its temporal change), modulate a motility variable (tumble/run bias, as in bacterial
chemotaxis), move. The nutrient feeds metabolism feeds the membrane feeds survival.

**Acceptance (computed).**
- **survival** — a cell that chemotaxes maintains viability (membrane above the dissolution threshold) under
  a moving/depleting food source that a non-chemotactic cell cannot.
- **adaptivity** — the motor response is *regulated by viability*: the bias strengthens when the interior is
  depleting. (Not a fixed reflex — a viability-serving regulation.)
- **precariousness** — disable sensing → the agent cannot find food → it dissolves. Agency is in service of
  self-maintenance.

**Evidence.** Trajectories: chemotactic agent climbing the gradient and surviving vs. a blind agent drifting
and dissolving; viability over time; the sensorimotor loop diagram.

**Why this is the deep step.** This is where *life becomes mind*: the same self-production now reaches into
the environment and makes it matter. Chemotaxis is the minimal cognition — a value (food/poison) grounded in
the precarious identity's own viability, not assigned from outside.

---

## Study 4 — Growth & division (the lineage)

**The capability.** The individual **grows** (membrane area, interior volume) and, past a threshold,
**divides** into two daughters — with **heterogeneous compositions** (stochastic / asymmetric partitioning of
the interior molecules and membrane). One individual becomes a **population** of non-identical individuals.

**Model.** Study 2/3's cell with a growth→division rule: when the membrane/volume crosses a size threshold,
split into two, partitioning the interior stochastically. Track a population of cells, each with its own
composition and viability, in the shared environment.

**Acceptance (computed).**
- **reproduction** — the lineage persists across divisions (the closed, precarious identity is *inherited*).
- **heterogeneity** — daughters differ measurably (composition variance > 0); the population is diverse.
- **precariousness across division** — a daughter that inherits too little membrane/metabolism dissolves —
  division has a viability cost; not every daughter survives.

**Evidence.** A lineage tree; the population's composition distribution; viability across generations.

---

## Study 5 — Selection (evolution)

**The capability.** With heterogeneous individuals (study 4) competing for a **limited** resource, those whose
composition/behavior better maintains viability **out-survive and out-reproduce** the rest. The population
**evolves** — not by an external fitness function, but by **differential persistence of precarious identities**.
Fitness *is* viability; selection *is* the autopoietic meter applied across a population under scarcity.

**Model.** A population (study 4) in a finite environment with depleting/competed food and heritable variation
(e.g. in chemotactic bias, metabolic rates, division threshold — passed noisily to daughters). Run long;
observe the distribution of traits shift toward more-viable strategies.

**Acceptance (computed).**
- **selection** — the trait distribution shifts toward higher viability over generations (vs. a neutral
  control with no scarcity).
- **the throughline closes** — every level (closure → containment → agency → reproduction → selection) is the
  *same precarious self-maintenance* operating at a wider scope. The autopoiesis meter, applied to a
  population under pressure, *is* natural selection.

**Evidence.** Trait distributions over generations; survival curves; the selection differential vs. the
neutral control.

---

## What stays constant across all five

- **Precariousness is the test at every level.** Each capability, when withdrawn, dissolves the identity —
  proving the capability is *constitutive of staying alive*, not decoration.
- **The schema framework computes acceptance.** The autopoiesis meter generalizes: closure (1) → containment
  ratio (2) → viability/survival (3) → reproduction+heterogeneity (4) → selection differential (5). Each is a
  *measured* verdict, not an authored one.
- **Composition, not monolith.** Each study composes the previous one with a new part (a diffusion field, a
  sensorimotor loop, a division rule, an environment) — the same "build up from existing parts" method,
  rendered as dashboard studies with figures.

## Parallel track R — biological realism

Folding in real v2ecoli metabolism (the heavy FBA, the bulk pool) grounds the toy interior in real
biochemistry. It is **orthogonal** to the capability arc (which is about emergent agency, not biochemical
detail) and carries real friction (sim_data, the opaque `bulk_array`). It runs as a parallel track that can
replace the toy interior of any study once the capability is demonstrated — realism follows capability, not
the other way around.
