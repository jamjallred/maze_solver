from geometry import *
from window import *
import time
import random

class Maze():

    def __init__(self, 
                 x1, y1, 
                 num_rows, num_cols, 
                 cell_size_x, cell_size_y,
                 win=None, seed=None):

        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__seed = seed

        self._create_cells()
        self.entr_y, self.exit_y = self._break_entrance_and_exit()
        self._break_walls_r(int(self.__num_cols*random.random()), 
                            int(self.__num_rows*random.random()))
        self._reset_cells_visited()

    def _create_cells(self):
        
        self._cells = [[Cell(self.__win) for m in range(self.__num_rows)] for n in range(self.__num_cols)]

        for i in range(self.__num_cols): # i picks column (along x-axis)
            for j in range(self.__num_rows): # j picks row (along y-axis)
                self._draw_cell(i, j)
            self._animate(50)

    def _draw_cell(self, i, j):

        cellx1 = self.__x1 + i*self.__cell_size_x
        cellx2 = cellx1 + self.__cell_size_x
        celly1 = self.__y1 + j*self.__cell_size_y
        celly2 = celly1 + self.__cell_size_y
        self._cells[i][j].draw(cellx1, celly1, cellx2, celly2)
        #self._animate()

    def _animate(self, delay):
        
        if self.__win is None:
            return
        
        self.__win.redraw()
        time.sleep(delay/1000)

    def _break_entrance_and_exit(self):
        entr_x, entr_y = 0, int(self.__num_rows*random.random())
        exit_x, exit_y = self.__num_cols-1, int(self.__num_rows*random.random())
        enter = self._cells[entr_x][entr_y]
        enter.has_left_wall = False
        self._draw_cell(entr_x, entr_y)
        leave = self._cells[exit_x][exit_y]
        leave.has_right_wall = False
        self._draw_cell(exit_x, exit_y)
        return entr_y, exit_y

    def _break_walls_r(self, i, j):
        # depth-first traversal through the cells, breaking down walls
        if self.__seed is not None:
            random.seed(self.__seed)
        
        current_cell = self._cells[i][j]
        current_cell.visited = True

        neighbors = [] # populate this with all neighbors, visited or not, tuple coordinates
        # find neighbors
        if i > 0: # if not on left wall, left neighbor exists
            neighbors.append((i-1, j, "left"))
        if i < self.__num_cols-1: # if not on right wall, right neighbor exists
            neighbors.append((i+1, j, "right"))
        if j > 0: # if not on top wall, top neighbor exists
            neighbors.append((i, j-1, "top"))
        if j < self.__num_rows-1: # if not on bottom wall, bottom neighbor exists
            neighbors.append((i, j+1, "bottom"))

        visit_order = list(range(len(neighbors)))
        random.shuffle(visit_order) # randomize order we look at neighbors

        for k in visit_order:
            m = neighbors[k][0]
            n = neighbors[k][1]
            next_cell = self._cells[m][n]
            if not next_cell.visited:
                # handle walls
                match neighbors[k][2]:
                    case "left":
                        current_cell.has_left_wall = False
                        next_cell.has_right_wall = False
                    case "right":
                        current_cell.has_right_wall = False
                        next_cell.has_left_wall = False
                    case "top":
                        current_cell.has_top_wall = False
                        next_cell.has_bottom_wall = False
                    case "bottom":
                        current_cell.has_bottom_wall = False
                        next_cell.has_top_wall = False
                self._break_walls_r(m,n)
            
        self._draw_cell(i,j)
        self._animate(5)

    def _reset_cells_visited(self):
        for col in self._cells:
            for c in col:
                c.visited = False
        

    def solve(self):
        self._draw_entering()
        return self._solve_r(0, self.entr_y)
        
    def _solve_r(self, i, j):
        
        self._animate(30)
        cur = self._cells[i][j]
        cur.visited = True

        if i == self.__num_cols-1 and j == self.exit_y:
            self._draw_leaving()
            return True
        
        adj = ["left", "right", "top", "bottom"]
        if i == 0 and j == self.entr_y:
            adj.remove("left")
        random.shuffle(adj)
        # randomize checking order
        # check for cells in set order and go down that branch if it exists
        for a in adj:
            match a:
                case "right":
                    if not cur.has_right_wall:
                        next = self._cells[i+1][j]
                        if not next.visited:
                            cur.draw_move(next)
                            if self._solve_r(i+1, j):
                                return True
                            else:
                                cur.draw_move(next, undo=True)
                case "bottom":
                    if not cur.has_bottom_wall:
                        next = self._cells[i][j+1]
                        if not next.visited:
                            cur.draw_move(next)
                            if self._solve_r(i, j+1):
                                return True
                            else:
                                cur.draw_move(next, undo=True)
                case "top":
                    if not cur.has_top_wall:
                        next = self._cells[i][j-1]
                        if not next.visited:
                            cur.draw_move(next)
                            if self._solve_r(i, j-1):
                                return True
                            else:
                                cur.draw_move(next, undo=True)
                case "left":
                    if not cur.has_left_wall:
                        next = self._cells[i-1][j]
                        if not next.visited:
                            cur.draw_move(next)
                            if self._solve_r(i-1, j):
                                return True
                            else:
                                cur.draw_move(next, undo=True)
        
        return False
    
    def _draw_entering(self):
        entrance_y = self.__y1 + int((self.entr_y + 0.5)*self.__cell_size_y)
        l = Line(Point(self.__x1 - self.__cell_size_x, entrance_y), 
                 Point(self.__x1 + self.__cell_size_x, entrance_y))
        self.__win.draw_line(l, "red")


    def _draw_leaving(self):
        exit_y = self.__y1 + int((self.exit_y + 0.5)*self.__cell_size_y)
        exit_x = self.__x1 + int((self.__num_cols-1 + 0.5)*self.__cell_size_x)
        l = Line(Point(exit_x, exit_y),
                 Point(exit_x + self.__cell_size_x, exit_y))
        self.__win.draw_line(l, "red")