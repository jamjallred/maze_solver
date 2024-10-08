from geometry import *
from window import *
import time

class Maze():

    def __init__(self, 
                 x1, y1, 
                 num_rows, num_cols, 
                 cell_size_x, cell_size_y,
                 win=None):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win

        self._create_cells()

    def _create_cells(self):
        
        self._cells = [[Cell(self.__win) for m in range(self.__num_rows)] for n in range(self.__num_cols)]

        for i in range(self.__num_cols): # i picks column (along x-axis)
            for j in range(self.__num_rows): # j picks row (along y-axis)
                self._draw_cell(i, j)

        self._break_entrance_and_exit()

    def _draw_cell(self, i, j):

        cellx1 = self.__x1 + i*self.__cell_size_x
        cellx2 = cellx1 + self.__cell_size_x
        celly1 = self.__y1 + j*self.__cell_size_y
        celly2 = celly1 + self.__cell_size_y
        self._cells[i][j].draw(cellx1, celly1, cellx2, celly2)
        self._animate()

    def _animate(self):
        
        if self.__win is None:
            return
        
        self.__win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_left_wall = False
        self._draw_cell(0,0)
        self._cells[self.__num_cols-1][self.__num_rows-1].has_right_wall = False
        self._draw_cell(self.__num_cols-1, self.__num_rows-1)