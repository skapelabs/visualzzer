import pygame
import random
import math
from collections import deque

pygame.init()

# Window
WIDTH, HEIGHT = 1200, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tree Visualizer - Inorder / Preorder / Postorder")

# Layout
LEFT_W = 760               # left drawing area width
RIGHT_W = WIDTH - LEFT_W   # right code panel width
CODE_PANEL_X = LEFT_W + 10
LOG_PANEL_H = 140          # bottom log height
TOP_MARGIN = 80

# Colors
WHITE = (255, 255, 255)
BG = (245, 245, 245)
BLACK = (20, 20, 20)
BLUE = (100, 149, 237)
RED = (220, 50, 50)
GREEN = (50, 180, 50)
GREY = (180, 180, 180)
CODE_HL = (255, 245, 200)

# Fonts
FONT = pygame.font.SysFont("consolas", 18)
BIG = pygame.font.SysFont("consolas", 28)

# Node radius
R = 24

# Limit logs
MAX_LOGS = 8


# ====== Tree node ======
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


# ====== Utility: build example tree ======
def build_sample_tree():
    # Build a sample tree stable each run so layout is consistent
    # structure:
    #         50
    #       /    \
    #     30      70
    #    /  \    /  \
    #   20  40  60  90
    root = Node(50)
    root.left = Node(30)
    root.right = Node(70)
    root.left.left = Node(20)
    root.left.right = Node(40)
    root.right.left = Node(60)
    root.right.right = Node(90)
    return root


# ====== Compute node positions for pretty layout ======
def compute_positions(root, x, y, dx, positions):
    if root is None:
        return
    positions[root.val] = (x, y)
    # reduce dx each level
    if root.left:
        compute_positions(root.left, x - dx, y + 100, dx // 2, positions)
    if root.right:
        compute_positions(root.right, x + dx, y + 100, dx // 2, positions)


# ====== Draw tree with highlighting ======
def draw_tree_surface(surface, root, positions, highlight=None, visited=set(), path_edges=set()):
    # background for left area
    pygame.draw.rect(surface, BG, (0, 0, LEFT_W, HEIGHT - LOG_PANEL_H))
    # draw edges first
    if root:
        stack = [root]
        while stack:
            node = stack.pop()
            if node.left:
                u = positions[node.val]
                v = positions[node.left.val]
                color = RED if (node.val, node.left.val) in path_edges else BLACK
                pygame.draw.line(surface, color, u, v, 3)
                stack.append(node.left)
            if node.right:
                u = positions[node.val]
                v = positions[node.right.val]
                color = RED if (node.val, node.right.val) in path_edges else BLACK
                pygame.draw.line(surface, color, u, v, 3)
                stack.append(node.right)
    # draw nodes
    if root:
        stack = [root]
        while stack:
            node = stack.pop()
            x, y = positions[node.val]
            if node.val == highlight:
                col = RED
            elif node.val in visited:
                col = GREEN
            else:
                col = BLUE
            pygame.draw.circle(surface, col, (int(x), int(y)), R)
            text = FONT.render(str(node.val), True, WHITE)
            surface.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)


# ====== Code panels for three traversals ======
INORDER_CODE = [
    "function inorder(node):",
    "  if node == null:",
    "    return",
    "  inorder(node.left)",
    "  visit(node)",
    "  inorder(node.right)"
]

PREORDER_CODE = [
    "function preorder(node):",
    "  if node == null:",
    "    return",
    "  visit(node)",
    "  preorder(node.left)",
    "  preorder(node.right)"
]

POSTORDER_CODE = [
    "function postorder(node):",
    "  if node == null:",
    "    return",
    "  postorder(node.left)",
    "  postorder(node.right)",
    "  visit(node)"
]


# ====== Draw code panel and highlight current line ======
def draw_code_panel(surface, code_lines, current_line):
    # background
    pygame.draw.rect(surface, WHITE, (LEFT_W, 0, RIGHT_W, HEIGHT - LOG_PANEL_H))
    # title
    title = BIG.render("Algorithm", True, BLACK)
    surface.blit(title, (LEFT_W + 14, 8))
    # code block area
    block_x = LEFT_W + 10
    block_y = 44
    line_h = 24
    for i, line in enumerate(code_lines):
        y = block_y + i * line_h
        # highlight background for current line
        if i == current_line:
            pygame.draw.rect(surface, CODE_HL, (block_x, y - 2, RIGHT_W - 20, line_h))
        txt = FONT.render(line, True, BLACK)
        surface.blit(txt, (block_x + 6, y))
    # controls at bottom of panel
    controls = [
        "Controls:",
        "SPACE to step",
        "A to toggle autoplay",
        "R to reset to menu",
        "M to go to menu",
        "ESC to quit"
    ]
    for idx, c in enumerate(controls):
        surface.blit(FONT.render(c, True, BLACK), (LEFT_W + 14, HEIGHT - LOG_PANEL_H - 120 + idx * 20))


# ====== Log console ======
def draw_logs(surface, logs):
    y0 = HEIGHT - LOG_PANEL_H
    pygame.draw.rect(surface, (30, 30, 30), (0, y0, WIDTH, LOG_PANEL_H))
    menu = BIG.render("Trace / Log", True, WHITE)
    surface.blit(menu, (12, y0 + 6))
    # draw each log line
    for i, line in enumerate(logs[-MAX_LOGS:]):
        txt = FONT.render(line, True, (220, 220, 220))
        surface.blit(txt, (12, y0 + 40 + i * 18))


# ====== Traversal generators. Each yield returns (lineno_index, action, node_val, log_msg, optional_edge) ======
def inorder_steps(node):
    # code lines indexes align with INORDER_CODE list
    if node is None:
        return
    # going left
    yield (3, "go_left", node.val, f"Going left from {node.val}", None)
    if node.left:
        for step in inorder_steps(node.left):
            yield step
    # visit
    yield (4, "visit", node.val, f"Visiting {node.val}", None)
    # going right
    yield (5, "go_right", node.val, f"Going right from {node.val}", None)
    if node.right:
        for step in inorder_steps(node.right):
            yield step


def preorder_steps(node):
    if node is None:
        return
    # visit
    yield (3, "visit", node.val, f"Visiting {node.val}", None)
    # left
    yield (4, "go_left", node.val, f"Going left from {node.val}", None)
    if node.left:
        for step in preorder_steps(node.left):
            yield step
    # right
    yield (5, "go_right", node.val, f"Going right from {node.val}", None)
    if node.right:
        for step in preorder_steps(node.right):
            yield step


def postorder_steps(node):
    if node is None:
        return
    # left
    yield (3, "go_left", node.val, f"Going left from {node.val}", None)
    if node.left:
        for step in postorder_steps(node.left):
            yield step
    # right
    yield (4, "go_right", node.val, f"Going right from {node.val}", None)
    if node.right:
        for step in postorder_steps(node.right):
            yield step
    # visit
    yield (5, "visit", node.val, f"Visiting {node.val}", None)


# ====== Simple helper: highlight an edge when moving between parent and child ======
def edge_between(parent_val, child_val):
    return (parent_val, child_val)


# ====== App main ======
def main():
    clock = pygame.time.Clock()
    run = True
    state = "menu"     # menu or visualize
    traversal = None   # "inorder", "preorder", "postorder"
    autoplay = False

    # scene variables
    root = None
    positions = {}
    generator = None
    current_highlight = None
    visited = set()
    logs = []
    path_edges = set()

    while run:
        WIN.fill(BG)

        # MENU SCREEN
        if state == "menu":
            # left: title and options
            pygame.draw.rect(WIN, BG, (0, 0, LEFT_W, HEIGHT - LOG_PANEL_H))
            title = BIG.render("Tree Visualizer", True, BLACK)
            WIN.blit(title, (40, 18))
            instr = [
                "Choose traversal type and press SPACE to start",
                "1 - In-order",
                "2 - Pre-order",
                "3 - Post-order",
                "A - toggle autoplay when visualizing",
                "R - Reset to Menu at any time",
                "ESC - Quit"
            ]
            for i, t in enumerate(instr):
                WIN.blit(FONT.render(t, True, BLACK), (40, 80 + i * 28))
            # right: show algorithm preview for selection or default
            draw_code_panel(WIN, INORDER_CODE if traversal != "preorder" and traversal != "postorder" else (PREORDER_CODE if traversal == "preorder" else POSTORDER_CODE), -1)
            # logs
            draw_logs(WIN, logs)

        # VISUALIZATION SCREEN
        elif state == "visualize":
            # draw tree area with highlights
            draw_tree_surface(WIN, root, positions, highlight=current_highlight, visited=visited, path_edges=path_edges)
            # draw code panel according to traversal
            code_lines = INORDER_CODE if traversal == "inorder" else (PREORDER_CODE if traversal == "preorder" else POSTORDER_CODE)
            # current_line derived from last yielded step; map to safe index
            current_line = last_line if 'last_line' in locals() else -1
            draw_code_panel(WIN, code_lines, current_line)
            # draw logs
            draw_logs(WIN, logs)

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                # global keys
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_r:
                    # reset everything to menu
                    state = "menu"
                    traversal = None
                    autoplay = False
                    root = None
                    positions = {}
                    generator = None
                    current_highlight = None
                    visited = set()
                    logs = []
                    path_edges = set()
                if state == "menu":
                    # select traversal
                    if event.key == pygame.K_1:
                        traversal = "inorder"
                    elif event.key == pygame.K_2:
                        traversal = "preorder"
                    elif event.key == pygame.K_3:
                        traversal = "postorder"
                    # start visualization
                    if event.key == pygame.K_SPACE and traversal:
                        # build tree and positions
                        root = build_sample_tree()
                        positions = {}
                        compute_positions(root, LEFT_W // 2, TOP_MARGIN + 20, 220, positions)
                        # init state
                        visited = set()
                        logs = []
                        path_edges = set()
                        current_highlight = None
                        # create generator
                        if traversal == "inorder":
                            generator = inorder_steps(root)
                        elif traversal == "preorder":
                            generator = preorder_steps(root)
                        else:
                            generator = postorder_steps(root)
                        state = "visualize"
                        autoplay = False
                elif state == "visualize":
                    # toggle autoplay
                    if event.key == pygame.K_a:
                        autoplay = not autoplay
                    # step when space and not autoplay
                    if event.key == pygame.K_SPACE and not autoplay:
                        if generator:
                            try:
                                step = next(generator)
                                # a step tuple: (lineno_index, action, node_val, log_msg, optional_edge)
                                lineno, action, node_val, log_msg, _ = step
                                # record last line to highlight
                                last_line = lineno
                                # enact action
                                if action == "visit":
                                    visited.add(node_val)
                                    current_highlight = node_val
                                elif action in ("go_left", "go_right"):
                                    # highlight movement: mark parent as highlight briefly, add log
                                    current_highlight = node_val
                                logs.append(log_msg)
                                if len(logs) > 200:
                                    logs = logs[-200:]
                            except StopIteration:
                                logs.append("Traversal finished")
                                autoplay = False
                                generator = None
                    # autoplay stepping
                    # handled in main loop below
        # autoplay logic: take steps automatically at lower FPS
        if state == "visualize" and autoplay and generator:
            # control speed with tick time
            # step roughly once per 600ms
            # using clock.get_time is noisy, so use pygame.time.get_ticks
            if not hasattr(main, "_last_auto"):
                main._last_auto = 0
            now = pygame.time.get_ticks()
            if now - main._last_auto > 600:
                try:
                    step = next(generator)
                    lineno, action, node_val, log_msg, _ = step
                    last_line = lineno
                    if action == "visit":
                        visited.add(node_val)
                        current_highlight = node_val
                    elif action in ("go_left", "go_right"):
                        current_highlight = node_val
                    logs.append(log_msg)
                    if len(logs) > 200:
                        logs = logs[-200:]
                except StopIteration:
                    logs.append("Traversal finished")
                    autoplay = False
                    generator = None
                main._last_auto = now

        # limit frame rate
        clock.tick(60)
        # update screen
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
