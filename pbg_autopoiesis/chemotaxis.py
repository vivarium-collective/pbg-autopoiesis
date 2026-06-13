"""Study 3 — adaptive chemotaxis: move toward food to survive.

The cell is placed in an environment with a nutrient gradient (a food source). It
senses the local nutrient and runs-and-tumbles — biasing motion up-gradient by
tumbling less when the sensed nutrient is rising (bacterial chemotaxis). The nutrient
feeds the metabolism that maintains the membrane that keeps it alive. A chemotactic
agent climbs the gradient, finds food, and survives; a blind agent random-walks,
starves, and dissolves.

This is where life becomes mind: the gradient is MEANINGFUL from the perspective of
the precarious identity — up-gradient is viable, down-gradient is dissolution. The
value (food = good) is grounded in the cell's own viability, not assigned from
outside. Agency is in service of self-maintenance (Di Paolo's adaptivity, Varela's
sense-making).
"""
from __future__ import annotations

import numpy as np

L = 100.0          # 1-D environment length
X_FOOD = 80.0      # the food source position
SIGMA = 20.0       # food gradient width


def nutrient(x):
    return np.exp(-((x - X_FOOD) ** 2) / (2.0 * SIGMA ** 2))


def simulate(chemotactic=True, n_agents=80, steps=900, *, v=0.7, base_tumble=0.20,
             alpha=16.0, uptake=0.06, maintenance=0.016, V0=1.5, start=(38.0, 56.0), seed=0):
    """Run a population of run-and-tumble agents. Returns trajectories + survival."""
    rng = np.random.default_rng(seed)
    x = rng.uniform(start[0], start[1], n_agents)   # start where the gradient is just sensible
    d = rng.choice([-1.0, 1.0], n_agents)
    V = np.full(n_agents, float(V0))              # viability (membrane/energy)
    alive = np.ones(n_agents, bool)
    N_prev = nutrient(x)

    X = [x.copy()]; VV = [V.copy()]; AL = [alive.copy()]; Nexp = []
    for _ in range(steps):
        Nx = nutrient(x)
        dN = Nx - N_prev
        if chemotactic:
            p_tumble = np.clip(base_tumble * (1.0 - alpha * dN), 0.02, 0.95)
        else:
            p_tumble = np.full(n_agents, base_tumble)     # blind: fixed tumble rate
        tumble = rng.random(n_agents) < p_tumble
        d = np.where(tumble, rng.choice([-1.0, 1.0], n_agents), d)
        x = np.clip(x + v * d * alive, 0.0, L)            # dead agents stop moving

        V = np.clip(V + uptake * nutrient(x) - maintenance, 0.0, 2.0)
        alive = alive & (V > 0.0)                         # viability gone → dissolved
        N_prev = Nx
        X.append(x.copy()); VV.append(V.copy()); AL.append(alive.copy())
        Nexp.append(float((nutrient(x) * alive).sum() / max(alive.sum(), 1)))
    return {
        "X": np.array(X), "V": np.array(VV), "alive": np.array(AL),
        "survival": float(alive.mean()),
        "mean_nutrient": float(np.mean(Nexp)),     # mean food experienced by survivors
    }


def chemotaxis_metrics(n_seeds=12):
    """The study-3 measures (the meter extended to agency / viability), replicated
    across ``n_seeds`` (chemotactic vs blind at matched seeds).

    Reported measures are the cross-seed MEAN; the context carries a ``robustness``
    summary (per-measure mean / std / range + the seed list) so the study is a
    distribution, not a single run, plus a representative seed-0 run for figures.
    The blind agent is a matched motile-but-non-sensing negative control."""
    per = {"chemotaxis_survival": [], "survival_advantage": [], "gradient_advantage": []}
    blind_survival = []
    chemo0 = blind0 = None
    for s in range(n_seeds):
        chemo = simulate(chemotactic=True, seed=s)
        blind = simulate(chemotactic=False, seed=s)
        if s == 0:
            chemo0, blind0 = chemo, blind
        per["chemotaxis_survival"].append(chemo["survival"])
        per["survival_advantage"].append(chemo["survival"] / max(blind["survival"], 1e-9))
        per["gradient_advantage"].append(chemo["mean_nutrient"] / max(blind["mean_nutrient"], 1e-9))
        blind_survival.append(blind["survival"])
    measures = {k: float(np.mean(v)) for k, v in per.items()}
    robustness = {
        "n_replicates": int(n_seeds),
        "seeds": list(range(n_seeds)),
        "parameter_sweep": False,
        "per_measure": {k: {"mean": float(np.mean(v)), "std": float(np.std(v)),
                            "min": float(np.min(v)), "max": float(np.max(v))}
                        for k, v in per.items()},
        "control_blind_survival_mean": float(np.mean(blind_survival)),
        "seeds_with_advantage": int(sum(1 for a in per["survival_advantage"] if a > 1.0)),
    }
    return measures, {"chemo": chemo0, "blind": blind0, "robustness": robustness}


if __name__ == "__main__":
    m, _ = chemotaxis_metrics()
    for k, val in m.items():
        print(f"{k:22s} {val:.3f}")
