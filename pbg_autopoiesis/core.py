"""build_core() — the bigraph-schema core with the autopoiesis loop processes
registered, so the dashboard (and our own runner) can resolve `local:Name`."""
from __future__ import annotations

from bigraph_schema import allocate_core

from .processes import Supply, Metabolism, Membrane, Boundary

_PROCS = (("Supply", Supply), ("Metabolism", Metabolism),
          ("Membrane", Membrane), ("Boundary", Boundary))


def build_core():
    core = allocate_core()
    for name, cls in _PROCS:
        core.register_link(name, cls)
    return core
