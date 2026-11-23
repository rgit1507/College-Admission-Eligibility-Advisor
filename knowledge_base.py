from ontology import Node


class KnowledgeBase:
    def __init__(self):
        
        self.branch_root = Node("Branch")
        engineering = Node("Engineering", self.branch_root, min_marks=60)
        computing = Node("Computing", engineering, min_marks=75)
        core = Node("Core", engineering)  # inherits min_marks=60

        Node("CSE", computing)
        Node("AIML", computing)
        Node("ECE", core)
        Node("ME", core)
        Node("CE", core)

        
        self.category_root = Node("Category")
        openc = Node("Open", self.category_root, marks_relaxation=0)
        reserved = Node("Reserved", self.category_root, marks_relaxation=5)

        Node("General", openc)
        Node("EWS", reserved)
        Node("OBC", reserved)
        Node("SC", reserved)
        Node("ST", reserved)

        
        self.cutoffs = {
            
            "CSE":  {"General": 6000,  "EWS": 7500,  "OBC": 9500,  "SC": 20000, "ST": 28000},
            "AIML": {"General": 9000,  "EWS": 11000, "OBC": 14000, "SC": 28000, "ST": 38000},
            "ECE":  {"General": 15000, "EWS": 18000, "OBC": 23000, "SC": 42000, "ST": 55000},
            "ME":   {"General": 25000, "EWS": 29000, "OBC": 36000, "SC": 60000, "ST": 75000},
            "CE":   {"General": 32000, "EWS": 37000, "OBC": 45000, "SC": 72000, "ST": 90000},
        }

    
    def branches(self):
        return self.branch_root.leaves()

    def categories(self):
        return self.category_root.leaves()

    def category(self, name):
        for c in self.categories():
            if c.name.lower() == str(name).lower():
                return c
        return None

    def cutoff(self, branch_name, category_name):
        return self.cutoffs[branch_name][category_name]

    def seat_routes(self, category):
        """Seat pools an applicant can compete in: own category, plus General open seats if reserved."""
        routes = [category.name]
        if category.is_a("Reserved"):
            routes.append("General")
        return routes
