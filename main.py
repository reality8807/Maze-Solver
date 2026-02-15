from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from search import DFS, BFS, Greedy

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
async def receive_grid(payload: GridPayload) -> dict | None:
    grid = payload.grid

    dfs = DFS(grid).solve()
    if dfs is None:
        return None

    bfs = BFS(grid).solve()
    greedy = Greedy(grid).solve()

    return {"dfs": dfs, "bfs": bfs, "greedy": greedy}
