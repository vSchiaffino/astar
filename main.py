from types import LambdaType
from typing import List
import pygame
from pygame import draw, scrap
from pygame.locals import *
from node import Node
from queue import PriorityQueue
green = (46, 204, 113)
red = (231, 76, 60)
black  = (44, 62, 80)
white = (236, 240, 241)
purple = (142, 68, 173)
orange = (230, 126, 34)
blue = (52, 152, 219)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def h(node1: Node , node2: Node):
    pos1:List(int) = node1.get_pos()
    pos2:List(int) = node2.get_pos()
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    return abs(dx) + abs(dy)

def astar(draw, grid):
    start = None
    end = None
    for row in grid:
        for node in row:
            node.update_neighbors(grid)
            if node.is_start():
                start = node
            elif node.is_end():
                end = node

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start, end)

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            print("termine")
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] =  temp_g_score + h(neighbor, end)
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()
        
    return False


    



def handle_events():
    global s, ppn, grid
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                astar(lambda: draw(s, grid, ppn), grid)

    p = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    x = pos[0] // ppn
    y = pos[1] // ppn
    if p[0]:
        if len(poner) > 0:
            p = poner.pop()
            if p == "start":
                grid[x][y].make_start()
            elif p == "end":
                grid[x][y].make_end()
        else:
            if grid[x][y].is_free():
                grid[x][y].make_barrier()
    elif p[2]:
        if grid[x][y].is_barrier():
            grid[x][y].reset()
        if grid[x][y].is_end() or grid[x][y].is_start():
            poner.append(grid[x][y].tipo)
            grid[x][y].reset()

poner = []
grid = []
size = (900, 900)
ppn = 10
n_horizontal_nodes = 90
n_vertical_nodes = 90
for x in range(n_horizontal_nodes):
    row = []
    for y in range(n_vertical_nodes):
        row.append(Node(x, y, [n_horizontal_nodes, n_vertical_nodes]))
    grid.append(row)

grid[0][0].make_start()
grid[0][1].make_end()


s = pygame.display.set_mode(size)

def draw(s, grid, ppn):
    colores = {
        "start": blue,
        "end": orange,
        "barrier": black,
        "": white,
        "open": red,
        "closed": green,
        "path": purple
    }
    s.fill(0)
    for row in grid:
        for node in row:
            pygame.draw.rect(s, colores[node.tipo], (node.x * ppn, node.y * ppn, ppn, ppn))

while True:
    if handle_events(): break
    draw(s, grid, ppn)
    pygame.display.flip()

