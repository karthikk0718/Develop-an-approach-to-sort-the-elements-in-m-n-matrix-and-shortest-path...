import tkinter as tk
from collections import deque

# Global variables
grid = []
buttons = []
start = None
target = None
rows, cols = 5, 5

# Create grid
def create_grid():
    global buttons, grid
    for widget in frame.winfo_children():
        widget.destroy()

    buttons = []
    grid = [[0]*cols for _ in range(rows)]

    for r in range(rows):
        row = []
        for c in range(cols):
            btn = tk.Button(frame, width=4, height=2, bg="white",
                            command=lambda r=r, c=c: on_click(r, c))
            btn.grid(row=r, column=c)
            row.append(btn)
        buttons.append(row)

# Handle clicks
def on_click(r, c):
    global start, target

    if start is None:
        start = (r, c)
        buttons[r][c].config(bg="green")  # Start
    elif target is None:
        target = (r, c)
        buttons[r][c].config(bg="red")    # Target
    else:
        if (r, c) != start and (r, c) != target:
            grid[r][c] = -1
            buttons[r][c].config(bg="black")  # Obstacle

# BFS algorithm
def bfs():
    if not start or not target:
        result_label.config(text="Select start and target!")
        return

    q = deque([(start, 0)])
    visited = {start}
    parent = {}

    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    while q:
        (r, c), dist = q.popleft()

        if (r, c) == target:
            result_label.config(text=f"Steps: {dist}")
            show_path(parent)
            return

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if (0 <= nr < rows and 0 <= nc < cols and
                (nr, nc) not in visited and grid[nr][nc] != -1):

                visited.add((nr, nc))
                parent[(nr, nc)] = (r, c)
                q.append(((nr, nc), dist + 1))

    result_label.config(text="Target unreachable")

# Animate robot movement
def animate_path(path):
    if not path:
        return

    r, c = path.pop(0)

    if (r, c) != start and (r, c) != target:
        buttons[r][c].config(bg="yellow")

    root.after(300, lambda: animate_path(path))

# Build path and animate
def show_path(parent):
    path = []
    node = target

    while node != start:
        path.append(node)
        node = parent[node]

    path.reverse()
    animate_path(path)

# Reset grid
def reset():
    global start, target
    start = None
    target = None
    create_grid()
    result_label.config(text="")

# UI setup
root = tk.Tk()
root.title("Warehouse Robot Simulator")

frame = tk.Frame(root)
frame.pack(pady=10)

create_grid()

tk.Button(root, text="Find Path", command=bfs).pack(pady=5)
tk.Button(root, text="Reset", command=reset).pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
result_label.pack(pady=10)

root.mainloop()
