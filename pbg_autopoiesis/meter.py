"""The autopoiesis meter — operational closure over a set of process interfaces.

    autopoietic_gap(S) = requires(S) \\ provides(S) \\ boundary

For the network processes S (their typed input/output ports) and a declared
boundary (what the environment supplies), the gap is everything the network
needs but cannot make itself. The system is operationally closed -- a cell --
when the gap is empty. Building a whole cell = driving the gap down to
{nutrients, energy}.

This is the same provides/requires reasoning as the capability-catalog spike,
turned into a closure metric: the catalog is the autopoiesis meter.
"""
from __future__ import annotations


def operational_closure(network, boundary_inputs):
    """Compute the autopoietic gap.

    Args:
        network: iterable of (name, inputs_dict, outputs_dict) for the
                 SELF-PRODUCING processes (exclude pure boundary/environment
                 processes -- their products are boundary inputs).
        boundary_inputs: iterable of port/store names the environment supplies
                 (e.g. the outputs of the supply/environment processes).

    Returns a dict: provides, requires, boundary, gap, closed.
    """
    provides: set[str] = set()
    requires: set[str] = set()
    for _name, ins, outs in network:
        requires |= set(ins)
        provides |= set(outs)
    boundary = set(boundary_inputs)
    gap = requires - provides - boundary
    return {
        "provides": sorted(provides),
        "requires": sorted(requires),
        "boundary": sorted(boundary),
        "gap": sorted(gap),
        "closed": not gap,
        "self_produced": sorted(requires & provides),
        "n_required": len(requires),
        "n_self_produced": len(requires & provides),
    }


def interface_of(proc):
    """(name, inputs, outputs) for a process-bigraph process/step instance."""
    return (type(proc).__name__, proc.inputs(), proc.outputs())


def report(closure: dict) -> str:
    """One-line-per-fact human summary of a closure result."""
    lines = [
        f"operational closure: {'CLOSED' if closure['closed'] else 'OPEN'}  "
        f"(self-produces {closure['n_self_produced']}/{closure['n_required']} required types)",
        f"  boundary  (imported): {{{', '.join(closure['boundary']) or '∅'}}}",
        f"  gap   (not yet made): {{{', '.join(closure['gap']) or '∅'}}}",
    ]
    return "\n".join(lines)
