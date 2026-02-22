from search_algorithms.nodes import A_star_node


class A_star:
    def __init__(self, grid: list[list[str]]):
        self.grid = grid
        self.frontier = []
        self.explored_set = []
        self.cell_distance = []
        self.explored_set_d = []

    def add(self, node: A_star_node, d: int) -> None:
        self.frontier.append(node)
        self.cell_distance.append(d)

    def remove(self) -> A_star_node:
        if self.is_empty():
            raise Exception("No Solution")

        min_distance = self.cell_distance[0]
        min_distance_pos = 0
        for i, d in enumerate(self.cell_distance):
            if d < min_distance:
                min_distance = d
                min_distance_pos = i

        self.cell_distance.pop(min_distance_pos)
        node = self.frontier.pop(min_distance_pos)
        return node

    def is_empty(self) -> bool:
        return len(self.frontier) == 0

    def not_in_frontier(self, state: tuple) -> bool:
        return state not in [node.state for node in self.frontier]

    def find_points(self) -> tuple:
        found_a, found_b = False, False
        for i, row in enumerate(self.grid):
            for j, col in enumerate(row):
                if col == "A":
                    found_a = True
                    a_pos = (i, j)
                elif col == "B":
                    found_b = True
                    b_pos = (i, j)

                if found_a and found_b:
                    return (A_star_node(a_pos, None, None, 0), b_pos)

        raise ValueError("Invalid Starting/Ending Position")

    def solve(self) -> list | None:
        starting_node, b_pos = self.find_points()
        d = abs(b_pos[1] - starting_node.state[1]) + abs(b_pos[0] - starting_node.state[0])
        self.add(starting_node, d)

        while True:
            if self.is_empty():
                return None

            node = self.remove()
            row = node.state[0]
            col = node.state[1]

            if (row, col) == b_pos:
                return self.goal_found(node)

            self.explored_set.append(node.state)
            self.explored_set_d.append(abs(b_pos[1] - col) + abs(b_pos[0] - row) + node.cost)
            self.add_paths(row, col, node, b_pos)

    def add_paths(self, r: int, c: int, node: A_star_node, b: tuple) -> None:
        # up
        if r != 0 and self.grid[r-1][c] != "boundary" and (r-1, c) not in self.explored_set and self.not_in_frontier((r-1, c)):
            up_node = A_star_node((r-1, c), node, "up", node.cost+1)
            d = abs(b[1] - c) + abs(b[0] - (r-1))
            self.add(up_node, d+node.cost+1)

        # down
        if r != len(self.grid)-1 and self.grid[r+1][c] != "boundary" and (r+1, c) not in self.explored_set and self.not_in_frontier((r+1, c)):
            down_node = A_star_node((r+1, c), node, "down", node.cost+1)
            d = abs(b[1] - c) + abs(b[0] - (r+1))
            self.add(down_node, d+node.cost+1)

        # left
        if c != 0 and self.grid[r][c-1] != "boundary" and (r, c-1) not in self.explored_set and self.not_in_frontier((r, c-1)):
            left_node = A_star_node((r, c-1), node, "left", node.cost+1)
            d = abs(b[1] - (c-1)) + abs(b[0] - r)
            self.add(left_node, d+node.cost+1)

        # right
        if c != len(self.grid[0])-1 and self.grid[r][c+1] != "boundary" and (r, c+1) not in self.explored_set and self.not_in_frontier((r, c+1)):
            right_node = A_star_node((r, c+1), node, "right", node.cost+1)
            d = abs(b[1] - (c+1)) + abs(b[0] - r)
            self.add(right_node, d+node.cost+1)

    def goal_found(self, node: A_star_node | None) -> list:
        backtrack = []
        actions = []
        while node:
            backtrack.append(node.state)
            actions.append(node.action)
            node = node.parent

        return [backtrack[-2:0:-1], actions[::-1], self.explored_set[1::], self.explored_set_d[1::]]
