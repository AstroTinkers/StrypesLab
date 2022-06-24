import sys
import collections


def printMaze(maze_to_print):
    for row in maze_to_print:
        print("".join(row))


def solveMaze(maze_to_walk, x, y):
    x, y = int(x), int(y)
    start = x, y
    wall, clear, goal = '#', ' ', 'g'
    queue = collections.deque()
    queue.append(start)
    seen = {start}
    while queue:
        path = queue.popleft()
        x, y = path
        if maze_to_walk[y][x] == goal:
            return maze_to_walk
        for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= x2 < len(maze_to_walk)-1 and 0 <= y2 < len(maze_to_walk[0])-1 and maze_to_walk[y2][x2] != wall:
                if (x2, y2) not in seen:
                    queue.append((x2, y2))
                    if maze_to_walk[x2][y2] != 'g':
                        maze_to_walk[x2][y2] = '.'
                    seen.add((x2, y2))
                else:
                    maze_to_walk[x2][y2] = 'x'
                    queue.append((x2, y2))
                    seen.add((x2, y2))
    return maze_to_walk



maze = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        ['#', ' ', '#', '#', '#', '#', '#', '#', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', '#', ' ', '#'],
        ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#', ' ', '#', ' ', '#', '#', ' ', '#', ' ', '#'],
        ['#', ' ', '#', '#', '#', '#', '#', '#', '#', ' ', '#', ' ', '#', ' ', '#', '#', ' ', '#', ' ', '#'],
        ['#', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#', '#', ' ', '#', ' ', '#'],
        ['#', ' ', '#', 'g', '#', '#', '#', ' ', '#', '#', '#', '#', '#', ' ', '#', '#', ' ', '#', ' ', '#'],
        ['#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', '#', ' ', '#', ' ', '#'],
        ['#', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]


solveMaze(maze, sys.argv[1], sys.argv[2])
printMaze(maze)
