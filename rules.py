def _value(wm, name):
    """Return the value of a given fact like ("marks", 85)."""
    for fact in wm:
        if fact[0] == name:
            return fact[1]
    return None


# RULE 1

def rule_marks_check(wm, kb):
    marks = _value(wm, "marks")
    cat = kb.category(_value(wm, "category"))
    if marks is None or cat is None:
        return []
    relax = cat.get("marks_relaxation", 0)
    out = []
    for b in kb.branches():
        base = b.get("min_marks")
        need = base - relax
        note = f" ({base} minus {relax} relaxation for {cat.name})" if relax else ""
        if marks >= need:
            out.append((("marks_ok", b.name), f"marks {marks} meet the minimum of {need}{note}"))
        else:
            out.append((("marks_fail", b.name), f"marks {marks} are below the minimum of {need}{note}"))
    return out


# RULE 2

def rule_rank_check(wm, kb):
    rank = _value(wm, "rank")
    cat = kb.category(_value(wm, "category"))
    if rank is None or cat is None:
        return []
    out = []
    for b in kb.branches():
        for pool in kb.seat_routes(cat):
            cutoff = kb.cutoff(b.name, pool)
            where = f"{pool} category" if pool == cat.name else "General open seats"
            if rank <= cutoff:
                out.append((("rank_ok", b.name, pool),
                            f"rank {rank:,} is within the cutoff of {cutoff:,} for {where}"))
            else:
                out.append((("rank_fail", b.name, pool),
                            f"rank {rank:,} is above the cutoff of {cutoff:,} for {where}"))
    return out


# RULE 3

def rule_decide(wm, kb):
    cat = kb.category(_value(wm, "category"))
    if cat is None:
        return []
    pools = kb.seat_routes(cat)
    out = []
    for b in kb.branches():
        marks_ok = ("marks_ok", b.name) in wm
        marks_fail = ("marks_fail", b.name) in wm
        decided = all(("rank_ok", b.name, p) in wm or ("rank_fail", b.name, p) in wm for p in pools)
        if not (marks_ok or marks_fail) or not decided:
            continue 

        ok_pools = [p for p in pools if ("rank_ok", b.name, p) in wm]
        if marks_ok and ok_pools:
            reasons = [wm[("rank_ok", b.name, ok_pools[0])], wm[("marks_ok", b.name)]]
            out.append((("eligible", b.name), f"Eligible for {b.name}: " + "; ".join(reasons)))
        else:
            reasons = []
            if marks_fail:
                reasons.append(wm[("marks_fail", b.name)])
            reasons += [wm[("rank_fail", b.name, p)] for p in pools if ("rank_fail", b.name, p) in wm]
            out.append((("not_eligible", b.name), f"Not eligible for {b.name}: " + "; ".join(reasons)))
    return out


ALL_RULES = [rule_marks_check, rule_rank_check, rule_decide]
