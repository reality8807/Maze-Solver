from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import sys

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class GridPayload(BaseModel):
    grid: list[list[str]]


@app.post("/grid")
def receive_grid(payload: GridPayload):
    grid = payload.grid
    # result = subprocess.run([sys.executable, 'search.py'], capture_output=True, text=True)
    # print("Received grid:")
    # for row in grid:
    #     print(row)

    # now you can run algorithms on it
    res = func(grid)
    print(res)
    print(type(res[0]))
    print(type(res[1]))
    print(type(res[2]))

    return {"backtrack": res[0], "actions": res[1][1::], "explored": res[2]}


def func(grid):
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
            return len(self.frontier) == 0

    print(grid)
    initial = False
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "A":
                start_pos = (i, j)
                initial = True
                break

        if initial:
            break

    algo = StackFrontier()
    algo.add(Node(start_pos, None, Node))
    explored_set = []

    while algo.frontier:
        # print(algo.frontier)
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

            print(backtrack[::-1])
            print(actions[::-1])
            return [backtrack[::-1], actions[::-1], explored_set]

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
