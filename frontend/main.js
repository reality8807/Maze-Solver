const frame = document.getElementById("frame");
const CELL_SIZE = 40;

let gridData = [];
let mouseDown = false;

let mode = "boundary";

let start_flag = true;
let end_flag = true;

// ---------- Build Grid ----------
function buildGrid() {
  const cols = Math.floor(frame.clientWidth / CELL_SIZE);
  const rows = Math.floor(frame.clientHeight / CELL_SIZE);

  frame.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
  frame.style.gridTemplateRows = `repeat(${rows}, 1fr)`;

  frame.innerHTML = "";
  gridData = [];
  start_flag = true;
  end_flag = true;

  for (let r = 0; r < rows; r++) {
    let rowArr = [];
    for (let c = 0; c < cols; c++) {
      const cell = document.createElement("div");
      cell.className = "cell";
      cell.dataset.row = r;
      cell.dataset.col = c;

      cell.addEventListener("mousedown", handleCell);
      cell.addEventListener("mouseenter", handleCell);

      frame.appendChild(cell);
      rowArr.push("");
    }
    gridData.push(rowArr);
  }
}

// ---------- Paint / Select Logic ----------
function handleCell(e) {
  if (e.type === "mouseenter" && !mouseDown) return;

  const cell = e.target;
  const r = cell.dataset.row;
  const c = cell.dataset.col;

  // remove all color classes first
  function clearCellVisual() {
    cell.classList.remove("boundary", "start", "end");
  }

  if (mode === "boundary") {
    if (gridData[r][c] !== "") return;

    cell.classList.add("boundary");
    gridData[r][c] = "boundary";
  } else if (mode === "erase") {
    if (gridData[r][c] === "A") start_flag = true;
    else if (gridData[r][c] === "B") end_flag = true;

    clearCellVisual();
    gridData[r][c] = "";
  } else if (mode === "start" && start_flag) {
    if (gridData[r][c] === "B") return;

    clearCellVisual();
    cell.classList.add("start");
    gridData[r][c] = "A";
    start_flag = false;
  } else if (mode === "end" && end_flag) {
    if (gridData[r][c] === "A") return;

    clearCellVisual();
    cell.classList.add("end");
    gridData[r][c] = "B";
    end_flag = false;
  }
}

// ---------- Mouse Tracking ----------
document.addEventListener("mousedown", (e) => {
  if (e.button === 0) mouseDown = true;
});
document.addEventListener("mouseup", () => (mouseDown = false));

// ---------- Buttons ----------
let btn_frame = document.getElementById("controls");
let boundary_btn = document.getElementById("boundary");
let start_btn = document.getElementById("start");
let end_btn = document.getElementById("end");
let erase_btn = document.getElementById("erase");

let buttons = [boundary_btn, start_btn, end_btn, erase_btn];

document.getElementById("export").onclick = sendGridToPython;

btn_frame.addEventListener("click", function (e) {
  let target_btn = e.target.closest("button");
  if (!target_btn) return;

  id_name = target_btn.id;

  for (let btn of buttons) {
    if (btn.id === id_name) {
      btn.classList.add("clicked");
      btn.disabled = true;
      mode = btn.id;
    } else if (btn.disabled == true) {
      btn.disabled = false;
      btn.classList.remove("clicked");
    }
  }
});

let solved_grid = null;

function sendGridToPython() {
  fetch("http://localhost:8000/grid", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      grid: gridData,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data === null) {
        alert("No Solution!");
        return;
      }
      solved_grid = data;
      document.getElementById("searches").classList.remove("hidden");
    });
}

dfs_btn = document.getElementById("dfs");
bfs_btn = document.getElementById("bfs");
greedy_btn = document.getElementById("greedy");
a_star_btn = document.getElementById("a_star");

dfs_btn.onclick = () => show_solution(solved_grid.dfs);
bfs_btn.onclick = () => show_solution(solved_grid.bfs);
greedy_btn.onclick = () => show_solution(solved_grid.greedy);
a_star_btn.onclick = () => show_solution(solved_grid.a_star);

function show_solution(search_type) {
  const old_path = frame.querySelectorAll(".cell.path");
  old_path.forEach((cell) => {
    cell.classList.remove("path");
    cell.textContent = null;
  });

  // for (row of search_type[2]) {
  //   let data_cell = frame.querySelector(`[data-row="${row[0]}"][data-col="${row[1]}"]`);
  //   data_cell.classList.add("path");
  // }
  if (search_type.length === 4) {
    for ([index, row] of search_type[2].entries()) {
      let data_cell = frame.querySelector(`[data-row="${row[0]}"][data-col="${row[1]}"]`);
      data_cell.classList.add("path");
      data_cell.textContent = search_type[3][index];
    }
  } else {
    for (row of search_type[2]) {
      let data_cell = frame.querySelector(`[data-row="${row[0]}"][data-col="${row[1]}"]`);
      data_cell.classList.add("path");
      data_cell.textContent = null;
    }
  }
}

// ---------- Resize Observer ----------
new ResizeObserver(buildGrid).observe(frame);

buildGrid();
