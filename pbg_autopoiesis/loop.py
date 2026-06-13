"""Increment 1 — build and run the minimal membrane/metabolism loop.

Wires Supply, Metabolism, Membrane, Boundary onto shared stores so the network
closes on itself except for the nutrient inflow. Provides:

  * build_loop(supply_rate)   -> a runnable Composite
  * run_trajectory(c, steps)  -> [volume per tick]
  * closure_of_loop()         -> the autopoiesis meter on this network
  * main()                    -> fed-vs-starved demo + the meter
"""
from __future__ import annotations

from process_bigraph import Composite

from .core import build_core as _core
from .processes import Supply, Metabolism, Membrane, Boundary, membrane_volume
from .meter import operational_closure, interface_of, report


def _proc_node(address, config, wires_in, wires_out, interval=1.0):
    return {
        "_type": "process",
        "address": f"local:{address}",
        "config": config,
        "interval": interval,
        "inputs": wires_in,
        "outputs": wires_out,
    }


def build_loop(supply_rate=2.0, *, seed_membrane=40.0, seed_precursor=10.0):
    """A Composite of the minimal autopoietic loop. supply_rate=0 starves it."""
    core = _core()
    state = {
        # --- shared molecular stores (toy counts) ---
        "nutrient": 0.0,
        "precursor": float(seed_precursor),
        "lipid": 0.0,
        "membrane_lipids": float(seed_membrane),
        "volume": membrane_volume(seed_membrane),   # initial emergent boundary

        # --- the network ---
        "supply": _proc_node(
            "Supply", {"rate": supply_rate},
            {}, {"nutrient": ["nutrient"]}),
        "metabolism": _proc_node(
            "Metabolism", {},
            {"nutrient": ["nutrient"], "precursor": ["precursor"],
             "lipid": ["lipid"], "volume": ["volume"]},
            {"nutrient": ["nutrient"], "precursor": ["precursor"],
             "lipid": ["lipid"]}),
        "membrane": _proc_node(
            "Membrane", {},
            {"lipid": ["lipid"], "membrane_lipids": ["membrane_lipids"]},
            {"lipid": ["lipid"], "membrane_lipids": ["membrane_lipids"]}),
        "boundary": _proc_node(
            "Boundary", {},
            {"membrane_lipids": ["membrane_lipids"], "volume": ["volume"]},
            {"volume": ["volume"]}),
    }
    return Composite({"state": state}, core=core)


def run_trajectory(composite, steps=160):
    """Run one tick at a time, recording the volume (the size of the identity)."""
    vols = [composite.state["volume"]]
    for _ in range(steps):
        composite.run(1.0)
        vols.append(composite.state["volume"])
    return vols


def closure_of_loop():
    """The autopoiesis meter for this network. Supply is the environment: its
    product (nutrient) is the boundary input; the rest is the self-producing network."""
    core = _core()
    network = [interface_of(Metabolism({}, core=core)),
               interface_of(Membrane({}, core=core)),
               interface_of(Boundary({}, core=core))]
    boundary = Supply({}, core=core).outputs().keys()   # {'nutrient'} -- supplied from outside
    return operational_closure(network, boundary)


def main():
    print("=" * 64)
    print(" pbg-autopoiesis — increment 1: membrane/metabolism loop")
    print("=" * 64)
    print(report(closure_of_loop()))
    print()

    fed = run_trajectory(build_loop(supply_rate=1.0))
    starved = run_trajectory(build_loop(supply_rate=0.0))
    v0 = fed[0]
    print(f" initial volume (emergent boundary): {v0:.4f}")
    print(f" FED     (nutrient flowing): volume {v0:.4f} -> {fed[-1]:.4f}   "
          f"({'persists/grows' if fed[-1] >= v0 * 0.9 else 'shrinks'})")
    print(f" STARVED (nutrient = 0):     volume {v0:.4f} -> {starved[-1]:.4f}   "
          f"({'dissipates' if starved[-1] < v0 * 0.5 else 'holds'})")
    print()
    print(" => the identity is PRECARIOUS: it persists only through continuous")
    print("    self-production; cut the inflow and the self-produced boundary decays.")
    print("=" * 64)


if __name__ == "__main__":
    main()
