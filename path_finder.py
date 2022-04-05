import curses
from curses import wrapper
import queue
import time

testcase = [
    ["#", "#", "O", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", " ", " ", "#"],
    ["#", "#", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", " ", " ", "#", " ", "#", " ", "#"],
    ["#", "#", " ", " #", " ", " ", " ", "X", "#"]

]


def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j
    return None


def find_free_ways(maze, row, col):
    freeways = []
    if row > 0:  # нижняя граница
        freeways.append((row - 1, col))
    if row + 1 < len(maze):  # верхняя граница
        freeways.append((row + 1, col))
    if col > 0:  # левая граница
        freeways.append((row, col - 1))
    if col + 1 < len(maze[0]):  # правая граница
        freeways.append((row, col + 1))
    return freeways


def print_maze(maze, stdscr, path=[]):
    cyan = curses.color_pair(1)
    red = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j * 3, "*", red)
            else:
                stdscr.addstr(i, j * 3, value, cyan)


def find_path(maze, stdscr):
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)
    visited = set()

    q = queue.Queue()
    q.put((start_pos, [start_pos]))

    while not q.empty():
        current_pos, path = q.get()  # Первый элемент в очереди
        row, col = current_pos

        stdscr.clear()
        # stdscr.addstr(10, 0, "Path = " + str(path))
        # stdscr.addstr(11, 7, str(visited))
        print_maze(maze, stdscr, path)
        time.sleep(0.1)
        stdscr.refresh()

        if maze[row][col] == end:
            return path

        freeways = find_free_ways(maze, row, col)
        for way in freeways:
            if way in visited:
                continue
            r, c = way
            if maze[r][c] == "#":
                continue

            new_path = path + [way]
            q.put((way, new_path))
            visited.add(way)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    # print_maze(testcase, stdscr)
    find_path(testcase, stdscr)
    stdscr.getch()


wrapper(main)
