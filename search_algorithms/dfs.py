from search_algorithms.nodes import Node

class DFS():
    def __init__(self, grid: list[list[str]]):
        self.grid = grid
        self.frontier = []
        self.explored_set = []

    def add(self, node: Node) -> None:
        self.frontier.append(node)

    def remove(self) -> Node:
        if self.is_empty():
            raise Exception
        node = self.frontier.pop()
        return node

    def not_in_frontier(self, state: tuple) -> bool:
        return state not in [node.state for node in self.frontier]

    def is_empty(self) -> bool:
        return len(self.frontier) == 0

    def find_a(self) -> Node:
        for i, row in enumerate(self.grid):
            for j, col in enumerate(row):
                if col == "A":
                    return Node((i, j), None, None)

        raise ValueError("Invalid Starting Position")

    def solve(self) -> list | None:
        self.add(self.find_a())

        while True:
            if self.is_empty():
                return None

            node = self.remove()
            row = node.state[0]
            col = node.state[1]

            if self.grid[row][col] == "B":
                return self.goal_found(node)

            self.explored_set.append(node.state)
            self.add_paths(row, col, node)

    def goal_found(self, node: Node) -> list:
        backtrack = []
        actions = []
        while node.parent is not None:
            backtrack.append(node.state)
            actions.append(node.action)
            node = node.parent

        return [backtrack[::-1], actions[::-1], self.explored_set[1::]]

    def add_paths(self, r: int, c: int, node: Node) -> None:
        # up
        if r != 0 and self.grid[r-1][c] != "boundary" and (r-1, c) not in self.explored_set and self.not_in_frontier((r-1, c)):
            up_node = Node((r-1, c), node, "up")
            self.add(up_node)

        # down
        if r != len(self.grid)-1 and self.grid[r+1][c] != "boundary" and (r+1, c) not in self.explored_set and self.not_in_frontier((r+1, c)):
            down_node = Node((r+1, c), node, "down")
            self.add(down_node)

        # left
        if c != 0 and self.grid[r][c-1] != "boundary" and (r, c-1) not in self.explored_set and self.not_in_frontier((r, c-1)):
            left_node = Node((r, c-1), node, "left")
            self.add(left_node)

        # right
        if c != len(self.grid[0])-1 and self.grid[r][c+1] != "boundary" and (r, c+1) not in self.explored_set and self.not_in_frontier((r, c+1)):
            right_node = Node((r, c+1), node, "right")
            self.add(right_node)
