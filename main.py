from window import *
from geometry import *
from maze import *

def main():

    win = Window(800, 600)

    # points = []
    # for i in range(100,601,100):
    #     points.append(Point(i,i))

    # lines = []
    # for i in range(0,6,2):
    #     lines.append(Line(points[i], points[i+1]))

    # for line in lines:
    #     win.draw_line(line, "black")

    # c = Cell(win)
    # d = Cell(win)
    # c.draw(100,100,200,200)
    # d.draw(200,200,300,300)
    # c.draw_move(d, undo=True)

    maze = Maze(50,50,4,5,100,100,win)

    win.wait_for_close()


main()