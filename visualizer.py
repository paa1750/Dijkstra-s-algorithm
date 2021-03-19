import pygame, sys, random, math
from collections import deque
from tkinter import messagebox, Tk
size = (width, height) = 640, 480

pygame.init()
win = pygame.display.set_mode(size)
pygame.display.set_caption("Dijkstra Visualizer")
clock = pygame.time.Clock()
cols, rows = 64, 48
w = width // cols
h = height // rows
board = []
queue, visited = deque(), []
final = []


class Cell:

    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.neighbours = []
        self.prev = None
        self.wall = False
        self.visited = False
        self.f, self.g, self.h = 0, 0, 0

    def show(self, wi, col, shape=1):
        if self.wall:
            col = (0, 0, 0)
        if shape == 1:
            pygame.draw.rect(wi, col, (self.r * w, self.c * h, w - 1, h - 1))
        else:
            pygame.draw.circle(wi, col, (self.r * w + w // 2,
                                         self.c * h + h // 2), w // 3)

    def add_neighbours(self, b):
        if self.r < cols - 1:
            self.neighbours.append(b[self.r + 1][self.c])
        if self.r > 0:
            self.neighbours.append(b[self.r - 1][self.c])
        if self.c < rows - 1:
            self.neighbours.append(b[self.r][self.c + 1])
        if self.c > 0:
            self.neighbours.append(b[self.r][self.c - 1])


def select_wall(p, s):
    x = p[0] // w
    y = p[1] // h
    board[x][y].wall = s


def place(p):
    x = p[0] // w
    y = p[1] // h
    return x, y


for i in range(cols):
    array = []
    for j in range(rows):
        array.append(Cell(i, j))
    board.append(array)


for i in range(cols):
    for j in range(rows):
        board[i][j].add_neighbours(board)


start = board[7][24]
end = board[57][24]
start.wall = False
end.wall = False

queue.append(start)
start.visited = True


def main():
    f = False
    not_f = True
    start_f = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if pygame.mouse.get_pressed()[0]:
                    select_wall(pygame.mouse.get_pos(), True)
                if pygame.mouse.get_pressed()[2]:
                    select_wall(pygame.mouse.get_pos(), False)
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    select_wall(pygame.mouse.get_pos(), True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_f = True

        if start_f:
            if len(queue) > 0:
                curr = queue.popleft()
                if curr == end:
                    temp = curr
                    while temp.prev:
                        final.append(temp.prev)
                        temp = temp.prev
                    if not f:
                        f = True
                        print("Done!")
                    elif f:
                        continue
                if not f:
                    for n in curr.neighbours:
                        if not n.visited and not n.wall:
                            n.visited = True
                            n.prev = curr
                            queue.append(n)
            else:
                if not_f and not f:
                    Tk().wm_withdraw()
                    messagebox.showinfo("no solution", "there was no solution")
                    not_f = False
                else:
                    continue

        win.fill((0, 20, 20))
        for r in range(cols):
            for c in range(rows):
                s = board[r][c]
                s.show(win, (44, 62, 80))
                if s in final:
                    s.show(win, (192, 57, 43))
                elif s.visited:
                    s.show(win, (39, 174, 96))
                if s in queue:
                    s.show(win, (44, 62, 80))
                    s.show(win, (39, 174, 96), 0)
                if s == start:
                    s.show(win, (0, 255, 200))
                if s == end:
                    s.show(win, (39, 120, 255))

        pygame.display.flip()


main()
