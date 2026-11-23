# College Admission Eligibility Advisor

Team Syntax Error. A rule-based expert system that takes an applicant's marks, entrance rank and category, applies admission rules by forward chaining, and lists the branches they are eligible for, with a reason for every decision.

Only the Python 3 standard library is used (Tkinter is needed only for the optional window).

## Run it

```
python main.py                                          # asks for inputs
python main.py --marks 85 --rank 4500 --category General
python main.py --marks 85 --rank 4500 --category OBC --trace   # also prints the rule firings
python ui.py                                            # optional Tkinter window
python -m unittest -v                                   # run the tests
```

## How it works

| File | Role |
|---|---|
| `ontology.py` | `Node` class: a class hierarchy where children inherit attributes from parents |
| `knowledge_base.py` | The ontology of branches and categories, plus the cutoff table |
| `rules.py` | IF-THEN rules written as functions |
| `engine.py` | Forward-chaining loop and the `advise()` function |
| `main.py` / `ui.py` | Command-line and Tkinter interfaces |
| `test_advisor.py` | Unit tests |

**Ontology.** `Branch -> Engineering -> Computing -> CSE`. `min_marks` is set on `Engineering` (60) and overridden on `Computing` (75), so `ECE` inherits 60 and `CSE` gets 75. Categories are `Open -> General` and `Reserved -> EWS, OBC, SC, ST`; `Reserved` carries a 5-mark relaxation that all its children inherit.

**Forward chaining.** The engine starts with the applicant's facts and fires every rule. Each rule adds new facts, each with a reason. The loop stops when a full pass adds nothing new.

1. `rule_marks_check`: marks vs branch minimum gives `marks_ok` or `marks_fail`
2. `rule_rank_check`: rank vs closing rank gives `rank_ok` or `rank_fail`. Reserved applicants are checked against their own category and the General open seats.
3. `rule_decide`: uses the facts from rules 1 and 2 to derive `eligible` or `not_eligible`, with the combined reason

## Extending it

- **New branch:** add one `Node(...)` line under the right group in `knowledge_base.py` and one row in `cutoffs`.
- **New category:** add one `Node(...)` line and one value in every cutoff row.
- **New rule:** write a function `rule_x(wm, kb)` in `rules.py` that returns `(fact, reason)` pairs, and add it to `ALL_RULES`.

The cutoffs and minimum marks are sample numbers. Replace them with your college's real data.

## Course outcomes

- **CO2 (Understand):** knowledge representation using an ontology, and how forward chaining derives conclusions from facts
- **CO4 (Apply):** a working rule engine and expert system applied to a real admission problem
