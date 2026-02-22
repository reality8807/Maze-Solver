class Node:
    def __init__(self, state: tuple, parent: Node | None, action: str | None):
        self.state = state
        self.parent = parent
        self.action = action


class A_star_node(Node):
    def __init__(self, state: tuple, parent: A_star_node | None, action: str | None, cost: int):
        super().__init__(state, parent, action)
        self.cost = cost
