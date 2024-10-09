from window import *
from geometry import *
from maze import *
import cmd

def testing_out():
    neighbors = []

def main():

    win = Window(800, 600)

    maze = Maze(30,10,30,40,18,18,win)
    maze.solve()

    win.wait_for_close()


main()