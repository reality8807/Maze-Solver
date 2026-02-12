from main import GridPayload


class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def remove(self):
        if self.is_empty():
            raise Exception
        node = self.frontier.pop()
        return node

    def is_contains(self, state):
        return state not in [node.state for node in self.frontier]

    def is_empty(self):
        return len(self.frontier) != 0


grid = GridPayload.grid

print(grid)
initial, final = False
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if not initial and grid[i][j] == "A":
            start_pos = (i, j)
            initial = True
        elif not final and grid[i][j] == "B":
            end_pos = (i, j)
            final = True

    if initial and final:
        break


algo = StackFrontier()
algo.add(Node(start_pos, None, Node))
explored_set = []

while algo.frontier:
    node = algo.remove()
    explored_set.append(node.state)

    i = node.state[0]
    j = node.state[1]

    if grid[i][j] == "B":
        print("Found")
        backtrack = []
        actions = []
        while node:
            backtrack.append(node.state)
            actions.append(node.action)
            node = node.parent

        print(backtrack.reverse())
        print(actions.reverse())
        break

    # up
    if i != 0 and grid[i - 1][j] != "boundary" and (i - 1, j) not in explored_set and algo.is_contains((i - 1, j)):
        up_node = Node((i-1, j), node, "up")
        algo.add(up_node)

    # down
    if i != len(grid)-1 and grid[i+1][j] != "boundary" and (i + 1, j) not in explored_set and algo.is_contains((i + 1, j)):
        down_node = Node((i+1, j), node, "down")
        algo.add(down_node)

    # left
    if j != 0 and grid[i][j-1] != "boundary" and (i, j - 1) not in explored_set and algo.is_contains((i, j - 1)):
        left_node = Node((i, j-1), node, "left")
        algo.add(left_node)

    # right
    if j != len(grid[0]) - 1 and grid[i][j+1] != "boundary" and (i, j + 1) not in explored_set and algo.is_contains((i, j + 1)):
        right_node = Node((i, j+1), node, "right")
        algo.add(right_node)
