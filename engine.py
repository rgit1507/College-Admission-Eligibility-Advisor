from knowledge_base import KnowledgeBase
from rules import ALL_RULES


def forward_chain(initial_facts, kb, rules=ALL_RULES):
    """Return (working_memory, trace). trace lists each rule firing in order."""
    wm = {fact: "given by applicant" for fact in initial_facts}
    trace = []
    changed = True
    passes = 0
    while changed:
        changed = False
        passes += 1
        for rule in rules:
            for fact, reason in rule(wm, kb):
                if fact not in wm:  # only genuinely new facts count
                    wm[fact] = reason
                    trace.append((passes, rule.__name__, fact, reason))
                    changed = True
    return wm, trace


def advise(marks, rank, category, kb=None):
    """Run the expert system. Returns (results, trace).

    results: list of (branch_name, eligible: bool, reason: str), one per branch.
    """
    kb = kb or KnowledgeBase()
    cat = kb.category(category)
    if cat is None:
        raise ValueError(f"Unknown category '{category}'. Choose from: "
                         + ", ".join(c.name for c in kb.categories()))
    if not 0 <= marks <= 100:
        raise ValueError("Marks must be between 0 and 100.")
    if rank < 1:
        raise ValueError("Rank must be 1 or more.")

    facts = [("marks", marks), ("rank", rank), ("category", cat.name)]
    wm, trace = forward_chain(facts, kb)

    results = []
    for b in kb.branches():
        if ("eligible", b.name) in wm:
            results.append((b.name, True, wm[("eligible", b.name)]))
        else:
            results.append((b.name, False, wm[("not_eligible", b.name)]))
    return results, trace
