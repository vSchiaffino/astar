from typing import List


class Node():
    def __init__(self, x: int, y: int, size: List[int]):
        self.x = x
        self.y = y
        self.tipo = ""
        self.neighbors = []
        self.total_size = size

    def click(self):
        pass

    def get_pos(self):
        return [self.x, self.y]

    def is_start(self):
        return self.tipo == "start"
    
    def is_end(self):
        return self.tipo == "end"
    
    def is_barrier(self):
        return self.tipo == "barrier"
    
    def is_open(self):
        return self.tipo == "open"
    
    def is_closed(self):
        return self.tipo == "closed"

    def is_free(self):
        return self.tipo == ""

    def reset(self):
        self.tipo = ""
    
    def make_open(self):
        if self.tipo != "barrier":
            self.tipo = "open"
    
    def make_closed(self):
        if self.tipo != "barrier":
            self.tipo = "closed"
    
    def make_barrier(self):
        self.tipo = "barrier"
    
    def make_end(self):
        self.tipo = "end"
    
    def make_start(self):
        self.tipo = "start"
    
    def make_path(self):
        self.tipo = "path"

    def update_neighbors(self, grid):
        self.neighbors.clear()
        if self.is_barrier():
            return
        # limites
        limit_derecha = self.x == self.total_size[0] - 1
        limit_abajo = self.y == self.total_size[1] - 1
        limit_izquierda = self.x == 0
        limit_arriba = self.y == 0
        # derecha
        if not limit_derecha and not grid[self.x + 1][self.y].is_barrier():
            self.neighbors.append(grid[self.x + 1][self.y])
        if not limit_abajo and not grid[self.x][self.y + 1].is_barrier():
            self.neighbors.append(grid[self.x][self.y + 1])
        if not limit_izquierda and grid[self.x - 1][self.y].is_barrier():
            self.neighbors.append(grid[self.x - 1][self.y])
        if not limit_arriba and grid[self.x][self.y - 1].is_barrier():
            self.neighbors.append(grid[self.x][self.y - 1])

    def __lt__(self, other):
        return False