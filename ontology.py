class Node:
    def __init__(self, name, parent=None, **attrs):
        self.name = name
        self.parent = parent
        self.attrs = attrs
        self.children = []
        if parent is not None:
            parent.children.append(self)

    def get(self, attr, default=None):
        """Return the attribute from this node, or the nearest ancestor that has it."""
        node = self
        while node is not None:
            if attr in node.attrs:
                return node.attrs[attr]
            node = node.parent
        return default

    def is_a(self, name):
        """True if this node is, or descends from, the node called `name`."""
        node = self
        while node is not None:
            if node.name == name:
                return True
            node = node.parent
        return False

    def leaves(self):
        """All nodes at the bottom of the tree under this node (the actual branches/categories)."""
        if not self.children:
            return [self]
        result = []
        for child in self.children:
            result.extend(child.leaves())
        return result

    def path(self):
        names, node = [], self
        while node is not None:
            names.append(node.name)
            node = node.parent
        return " -> ".join(reversed(names))

    def __repr__(self):
        return f"Node({self.name})"
