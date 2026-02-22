from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
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

BASE_DIR = Path(__file__).resolve().parent
app.mount("/frontend", StaticFiles(directory=BASE_DIR / "frontend"), name="frontend")

@app.get("/")
def read_index():
    return FileResponse(BASE_DIR / "frontend" / "index.html")


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
    a_star = A_star(grid).solve()

    return {"dfs": dfs, "bfs": bfs, "greedy": greedy, "a_star": a_star}
