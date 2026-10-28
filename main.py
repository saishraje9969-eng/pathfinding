import pygame
import heapq
import time
from collections import deque

# ------------------------------------------------------------
# Pathfinding Visualizer - Python + Pygame
# Controls:
#   Left-click / drag: draw walls
#   Right-click: erase walls
#   S: choose start cell, E: choose end cell
#   1: BFS, 2: DFS, 3: Dijkstra, 4: A*
#   SPACE: run selected algorithm
#   C: clear walls and search results
#   R: reset everything
#   ESC: quit
# ------------------------------------------------------------

pygame.init()
pygame.display.set_caption("DSA Pathfinding Visualizer")

WIDTH, HEIGHT = 1000, 720
PANEL_H = 120
GRID_TOP = 145
ROWS, COLS = 25, 35
CELL = min(WIDTH // COLS, (HEIGHT - GRID_TOP - 10) // ROWS)
GRID_W, GRID_H = COLS * CELL, ROWS * CELL

# Colors
BG = (20, 24, 33)
PANEL = (29, 35, 47)
GRID_LINE = (55, 64, 79)
EMPTY = (239, 243, 248)
WALL = (47, 54, 68)
START = (46, 204, 113)
END = (231, 76, 60)
VISITED = (105, 174, 245)
PATH = (255, 205, 70)
WHITE = (245, 247, 250)
MUTED = (185, 194, 207)
ACCENT = (91, 110, 225)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 18)
small_font = pygame.font.SysFont("arial", 14)
title_font = pygame.font.SysFont("arial", 26, bold=True)

start = (2, 2)
goal = (ROWS - 3, COLS - 3)
walls = set()
visited = set()
path = set()
selected_algorithm = "BFS"
choosing = None
running_search = False
search_generator = None
search_start_time = 0.0
elapsed_ms = 0.0
visited_count = 0
result_message = "Draw walls, choose an algorithm, then press SPACE."
status = "Ready"

ALGORITHMS = {"1": "BFS", "2": "DFS", "3": "Dijkstra", "4": "A*"}

def label(text, x, y, color=WHITE, use_font=font):
    surface = use_font.render(text, True, color)
    screen.blit(surface, (x, y))

def cell_at_mouse(pos):
    x, y = pos
    if y < GRID_TOP or x >= GRID_W or y >= GRID_TOP + GRID_H:
        return None
    row = (y - GRID_TOP) // CELL
    col = x // CELL
    if 0 <= row < ROWS and 0 <= col < COLS:
        return (row, col)
    return None

def neighbors(node):
    r, c = node
    # Four-direction movement
    for nr, nc in ((r-1,c), (r+1,c), (r,c-1), (r,c+1)):
        nxt = (nr, nc)
        if 0 <= nr < ROWS and 0 <= nc < COLS and nxt not in walls:
            yield nxt

def heuristic(a, b):
    # Manhattan distance for a four-direction grid
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def reconstruct_path(parent, target):
    route = set()
    current = target
    while current in parent:
        route.add(current)
        current = parent[current]
    if current == start:
        route.add(start)
    return route

def search_steps(algorithm):
    """Yield (visited_cell, current_path, finished, message) for animation."""
    parent = {}
    discovered = set()
    distances = {start: 0}
    explored = set()

    if algorithm == "BFS":
        frontier = deque([start])
        discovered.add(start)
        while frontier:
            current = frontier.popleft()
            if current == goal:
                route = reconstruct_path(parent, goal)
                yield (None, route, True, "Path found!")
                return
            for nxt in neighbors(current):
                if nxt not in discovered:
                    discovered.add(nxt)
                    parent[nxt] = current
                    frontier.append(nxt)
            explored.add(current)
            yield (current, set(), False, "")
    elif algorithm == "DFS":
        frontier = [start]
        discovered.add(start)
        while frontier:
            current = frontier.pop()
            if current == goal:
                route = reconstruct_path(parent, goal)
                yield (None, route, True, "Path found!")
                return
            # Reverse order gives a consistent visual direction
            for nxt in reversed(list(neighbors(current))):
                if nxt not in discovered:
                    discovered.add(nxt)
                    parent[nxt] = current
                    frontier.append(nxt)
            explored.add(current)
            yield (current, set(), False, "")
    else:
        counter = 0
        if algorithm == "Dijkstra":
            frontier = [(0, counter, start)]
        else:
            frontier = [(heuristic(start, goal), counter, start)]
        discovered.add(start)

        while frontier:
            priority, _, current = heapq.heappop(frontier)
            if current in explored:
                continue
            if current == goal:
                route = reconstruct_path(parent, goal)
                yield (None, route, True, "Path found!")
                return
            explored.add(current)
            for nxt in neighbors(current):
                new_cost = distances[current] + 1
                if new_cost < distances.get(nxt, float("inf")):
                    distances[nxt] = new_cost
                    parent[nxt] = current
                    counter += 1
                    score = new_cost
                    if algorithm == "A*":
                        score += heuristic(nxt, goal)
                    heapq.heappush(frontier, (score, counter, nxt))
                    discovered.add(nxt)
            yield (current, set(), False, "")

    yield (None, set(), True, "No path found. Try removing some walls.")

def start_search():
    global running_search, search_generator, visited, path
    global search_start_time, elapsed_ms, visited_count, result_message, status
    if start in walls or goal in walls:
        result_message = "Start and destination cannot be walls."
        return
    visited = set()
    path = set()
    visited_count = 0
    elapsed_ms = 0.0
    search_generator = search_steps(selected_algorithm)
    search_start_time = time.perf_counter()
    running_search = True
    status = "Searching..."
    result_message = f"Running {selected_algorithm}..."

def clear_search():
    global visited, path, running_search, search_generator, elapsed_ms, visited_count, status, result_message
    visited = set()
    path = set()
    running_search = False
    search_generator = None
    elapsed_ms = 0.0
    visited_count = 0
    status = "Ready"
    result_message = "Search cleared. Press SPACE to run again."

def draw_button(rect, text, active=False):
    color = ACCENT if active else (57, 66, 83)
    pygame.draw.rect(screen, color, rect, border_radius=7)
    pygame.draw.rect(screen, (95, 108, 132), rect, 1, border_radius=7)
    txt = small_font.render(text, True, WHITE)
    screen.blit(txt, txt.get_rect(center=rect.center))

def draw():
    screen.fill(BG)
    pygame.draw.rect(screen, PANEL, (0, 0, WIDTH, PANEL_H))
    label("Pathfinding Visualizer", 20, 12, WHITE, title_font)
    label("DSA Project  |  Python + Pygame", 22, 47, MUTED, small_font)

    label(f"Algorithm: {selected_algorithm}", 22, 73, WHITE, font)
    label(f"Visited: {visited_count}", 245, 73, WHITE, font)
    label(f"Time: {elapsed_ms:.2f} ms", 380, 73, WHITE, font)

    # Legend
    legend = [
        (START, "Start"), (END, "Destination"), (WALL, "Wall"),
        (VISITED, "Explored"), (PATH, "Path")
    ]
    lx = 580
    for color, name in legend:
        pygame.draw.rect(screen, color, (lx, 16, 14, 14), border_radius=3)
        label(name, lx + 20, 14, MUTED, small_font)
        lx += 82

    # Algorithm buttons
    draw_button(pygame.Rect(20, 103, 95, 28), "1 BFS", selected_algorithm == "BFS")
    draw_button(pygame.Rect(122, 103, 95, 28), "2 DFS", selected_algorithm == "DFS")
    draw_button(pygame.Rect(224, 103, 125, 28), "3 Dijkstra", selected_algorithm == "Dijkstra")
    draw_button(pygame.Rect(356, 103, 95, 28), "4 A*", selected_algorithm == "A*")
    draw_button(pygame.Rect(462, 103, 100, 28), "SPACE Run", running_search)
    draw_button(pygame.Rect(573, 103, 90, 28), "C Clear")
    draw_button(pygame.Rect(674, 103, 100, 28), "R Reset")

    # Grid
    for r in range(ROWS):
        for c in range(COLS):
            node = (r, c)
            rect = pygame.Rect(c * CELL, GRID_TOP + r * CELL, CELL, CELL)
            color = EMPTY
            if node in walls:
                color = WALL
            if node in visited:
                color = VISITED
            if node in path:
                color = PATH
            if node == start:
                color = START
            if node == goal:
                color = END
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRID_LINE, rect, 1)

    # Footer
    footer_y = GRID_TOP + GRID_H + 8
    label(result_message, 20, footer_y, WHITE, small_font)
    label("Left-click/drag: wall  |  Right-click: erase  |  S: set start  |  E: set destination  |  ESC: quit",
          20, HEIGHT - 23, MUTED, small_font)

    pygame.display.flip()

def reset_all():
    global start, goal, walls, visited, path, selected_algorithm, choosing
    global running_search, search_generator, elapsed_ms, visited_count, status, result_message
    start = (2, 2)
    goal = (ROWS - 3, COLS - 3)
    walls = set()
    visited = set()
    path = set()
    selected_algorithm = "BFS"
    choosing = None
    running_search = False
    search_generator = None
    elapsed_ms = 0.0
    visited_count = 0
    status = "Ready"
    result_message = "Grid reset. Draw walls and press SPACE."

def handle_cell(cell, button):
    global start, goal
    if cell is None:
        return
    if choosing == "start":
        if cell != goal:
            walls.discard(cell)
            start = cell
        return
    if choosing == "end":
        if cell != start:
            walls.discard(cell)
            goal = cell
        return
    if cell == start or cell == goal:
        return
    if button == 1:
        walls.add(cell)
    elif button == 3:
        walls.discard(cell)

def main():
    global running_search, search_generator, visited, path, visited_count
    global elapsed_ms, status, result_message, selected_algorithm, choosing

    alive = True
    while alive:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    alive = False
                elif event.key == pygame.K_SPACE:
                    start_search()
                elif event.key == pygame.K_c:
                    clear_search()
                elif event.key == pygame.K_r:
                    reset_all()
                elif event.key == pygame.K_s:
                    choosing = "start"
                    result_message = "Click a grid cell to set the start point."
                elif event.key == pygame.K_e:
                    choosing = "end"
                    result_message = "Click a grid cell to set the destination."
                elif event.unicode in ALGORITHMS:
                    selected_algorithm = ALGORITHMS[event.unicode]
                    clear_search()
                    result_message = f"{selected_algorithm} selected. Press SPACE to run."

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 103 <= y <= 131:
                    if 20 <= x <= 115:
                        selected_algorithm = "BFS"
                    elif 122 <= x <= 217:
                        selected_algorithm = "DFS"
                    elif 224 <= x <= 349:
                        selected_algorithm = "Dijkstra"
                    elif 356 <= x <= 451:
                        selected_algorithm = "A*"
                    elif 462 <= x <= 562:
                        start_search()
                    elif 573 <= x <= 663:
                        clear_search()
                        walls.clear()
                        result_message = "Walls and search results cleared."
                    elif 674 <= x <= 774:
                        reset_all()
                    clear_search() if not running_search else None
                    continue
                if running_search:
                    continue
                cell = cell_at_mouse(event.pos)
                if event.button in (1, 3):
                    handle_cell(cell, event.button)
                    if choosing is not None and cell is not None:
                        choosing = None
                    clear_search()

            elif event.type == pygame.MOUSEMOTION and not running_search:
                if event.buttons[0]:
                    handle_cell(cell_at_mouse(event.pos), 1)
                    clear_search()
                elif event.buttons[2]:
                    handle_cell(cell_at_mouse(event.pos), 3)
                    clear_search()

        if running_search and search_generator is not None:
            # Process several cells per frame for a smooth but reasonably fast animation.
            for _ in range(4):
                try:
                    node, found_path, finished, message = next(search_generator)
                    if node is not None and node not in (start, goal):
                        visited.add(node)
                        visited_count += 1
                    if found_path:
                        path = found_path
                    if finished:
                        running_search = False
                        elapsed_ms = (time.perf_counter() - search_start_time) * 1000
                        status = "Finished"
                        result_message = message
                        break
                except StopIteration:
                    running_search = False
                    elapsed_ms = (time.perf_counter() - search_start_time) * 1000
                    status = "Finished"
                    result_message = "Search finished."
                    break
            if running_search:
                elapsed_ms = (time.perf_counter() - search_start_time) * 1000

        draw()

    pygame.quit()

if __name__ == "__main__":
    main()
