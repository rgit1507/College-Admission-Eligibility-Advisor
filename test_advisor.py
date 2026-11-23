import unittest

from engine import advise
from knowledge_base import KnowledgeBase
from ontology import Node


def eligible(results):
    return {b for b, ok, _ in results if ok}


class TestOntology(unittest.TestCase):
    def test_inheritance(self):
        kb = KnowledgeBase()
        by_name = {b.name: b for b in kb.branches()}
        self.assertEqual(by_name["CSE"].get("min_marks"), 75)  
        self.assertEqual(by_name["ME"].get("min_marks"), 60)   
        self.assertTrue(kb.category("SC").is_a("Reserved"))
        self.assertFalse(kb.category("General").is_a("Reserved"))

    def test_leaves(self):
        self.assertEqual(len(KnowledgeBase().branches()), 5)


class TestAdvisor(unittest.TestCase):
    def test_general_good_rank(self):
        results, _ = advise(85, 4500, "General")
        self.assertEqual(eligible(results), {"CSE", "AIML", "ECE", "ME", "CE"})
        cse = [r for r in results if r[0] == "CSE"][0]
        self.assertIn("rank 4,500 is within the cutoff of 6,000 for General category", cse[2])

    def test_rank_too_high_for_cse(self):
        results, _ = advise(85, 12000, "General")
        self.assertEqual(eligible(results), {"ECE", "ME", "CE"})

    def test_low_marks_blocks_computing(self):
        results, _ = advise(70, 1000, "General")  
        self.assertEqual(eligible(results), {"ECE", "ME", "CE"})

    def test_reserved_marks_relaxation(self):
        results, _ = advise(70, 1000, "SC")  
        self.assertIn("CSE", eligible(results))

    def test_reserved_uses_open_seats(self):
        
        results, _ = advise(90, 9000, "OBC")
        self.assertIn("CSE", eligible(results))
        results, _ = advise(90, 20000, "OBC")
        self.assertNotIn("CSE", eligible(results))

    def test_reason_for_rejection(self):
        results, _ = advise(85, 12000, "General")
        cse = [r for r in results if r[0] == "CSE"][0]
        self.assertFalse(cse[1])
        self.assertIn("above the cutoff of 6,000", cse[2])

    def test_forward_chaining_trace(self):
        _, trace = advise(85, 4500, "General")
        rules_fired = [t[1] for t in trace]
        
        self.assertLess(rules_fired.index("rule_marks_check"), rules_fired.index("rule_decide"))
        self.assertLess(rules_fired.index("rule_rank_check"), rules_fired.index("rule_decide"))

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            advise(85, 4500, "Martian")
        with self.assertRaises(ValueError):
            advise(150, 4500, "General")
        with self.assertRaises(ValueError):
            advise(85, 0, "General")


if __name__ == "__main__":
    unittest.main()
