from search_algorithms.nodes import Node
from search_algorithms.dfs import DFS

class BFS(DFS):
    def __init__(self, grid: list[list[str]]):
        super().__init__(grid)

    def remove(self) -> Node:
        if self.is_empty():
            raise Exception

        node = self.frontier.pop(0)
        return node