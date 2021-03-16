import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* Pathfinding Visualization")

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,255,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQUOISE = (64,224,208)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED
    def is_open(self):
        return self.color == GREEN
    def is_blocked(self):
        return self.color == BLACK
    def is_start(self):
        return self.color==ORANGE
    def is_end(self):
        return self.color==TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED
    def make_open(self):
        self.color = GREEN
    def make_blocked(self):
        self.color = BLACK
    def make_start(self):
        self.color = ORANGE
    def make_end(self):
        self.color = TURQUOISE
    def make_path(self):
        self.color = PURPLE
        
    def draw(self,win):
        pygame.draw.rect(win, self.color, (self.x, self.y,self.width,self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # Down
        if self.row<self.total_rows -1 and not grid[self.row +1][self.col].is_blocked():
            self.neighbors.append(grid[self.row+1][self.col])
        # Right
        if self.col<self.total_rows -1 and not grid[self.row ][self.col+1].is_blocked():
            self.neighbors.append(grid[self.row][self.col+1])
        # Up
        if self.row>0 and not grid[self.row -1][self.col].is_blocked():
            self.neighbors.append(grid[self.row-1][self.col])
        # Left
        if self.col>0 and not grid[self.row ][self.col-1].is_blocked():
            self.neighbors.append(grid[self.row][self.col-1])
       # print(self.neighbors)

    def __lt__(self,other):
        return False

def h(p1, p2):
    x1,y1 = p1
    x2,y2 = p2
    return abs(x1-x2)+abs(y1-y2)


def reconstruct_path(prev,cur, draw):
    while cur in prev:
        cur = prev[cur];
        cur.make_path()
        draw()


def algorithm(draw, grid, start, end):
    print("algo started")
    count = 0
    pq = PriorityQueue()
    pq.put((0, start))
    prev = {}
    # g_score --> dis from the starting node
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0;


    # Hashset to tell tell which nodes are present in queue
    items_in_pq = {start}

    while not pq.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        cur = pq.get()[1]
        items_in_pq.remove(cur)

        if cur== end:
            reconstruct_path(prev,end,draw)
            end.make_end()
            start.make_start()
            return True

        #print(cur.neighbors)
        for neighbor in cur.neighbors:
            temp_g = g_score[cur]+1
            if temp_g < g_score[neighbor]:
                prev[neighbor] = cur
                g_score[neighbor] = temp_g
                if neighbor not in items_in_pq:
                    count+=1
                    pq.put((g_score[neighbor],neighbor))
                    items_in_pq.add(neighbor)
                    neighbor.make_open()

        draw()

        if cur!=start:
            cur.make_closed()

    return False
            

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i,j,gap,rows)
            grid[i].append(node);

    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0,i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j*gap,0), ( j*gap, width))
            

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y,x = pos
    row = y // gap
    col = x // gap

    return row, col

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None
    
    run = True
    while run:
        draw(win, grid, ROWS, width);
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                #do this
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                #print(row, col)
                node = grid[row][col]
                if not start and node!=end:
                    start = node
                    start.make_start();
                elif not end and node!=start:
                    end = node
                    end.make_end();
                elif node!=end and node!=start:
                    node.make_blocked()
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node==start:
                    start = None
                elif node==end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key== pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS,width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
    pygame.quit()

main(WIN, WIDTH)

