from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from search_algorithms.dfs import DFS
from search_algorithms.bfs import BFS
from search_algorithms.greedy import Greedy
from search_algorithms.a_star import A_star

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class GridPayload(BaseModel):
    grid: list[list[str]]


@app.post("/")
async def receive_grid(payload: GridPayload) -> dict | None:
    grid = payload.grid

    dfs = DFS(grid).solve()
    if dfs is None:
        return None

    bfs = BFS(grid).solve()
    greedy = Greedy(grid).solve()
    a_star = A_star(grid).solve()

    return {"dfs": dfs, "bfs": bfs, "greedy": greedy, "a_star": a_star}
