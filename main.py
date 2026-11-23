import argparse

from engine import advise
from knowledge_base import KnowledgeBase


def print_results(results, trace=None):
    eligible = [r for r in results if r[1]]
    print("\n=== Eligibility report ===")
    for branch, ok, reason in results:
        print(f"[{'YES' if ok else 'NO '}] {reason}")
    names = ", ".join(r[0] for r in eligible) or "none"
    print(f"\nEligible branches: {names}")

    if trace:
        print("\n=== Forward-chaining trace (pass, rule, derived fact) ===")
        for n, rule_name, fact, _ in trace:
            print(f"pass {n}: {rule_name} -> {fact}")


def main():
    kb = KnowledgeBase()
    cats = [c.name for c in kb.categories()]

    parser = argparse.ArgumentParser(description="College Admission Eligibility Advisor")
    parser.add_argument("--marks", type=float, help="percentage marks (0-100)")
    parser.add_argument("--rank", type=int, help="entrance exam rank")
    parser.add_argument("--category", help="one of: " + ", ".join(cats))
    parser.add_argument("--trace", action="store_true", help="show the forward-chaining trace")
    args = parser.parse_args()

    try:
        marks = args.marks if args.marks is not None else float(input("Marks (%): "))
        rank = args.rank if args.rank is not None else int(input("Entrance rank: "))
        category = args.category or input(f"Category ({'/'.join(cats)}): ")
        results, trace = advise(marks, rank, category.strip(), kb)
    except ValueError as err:
        print(f"Input error: {err}")
        return

    print_results(results, trace if args.trace else None)


if __name__ == "__main__":
    main()
