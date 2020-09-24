import pygame
import math
import heapq
import time

def createGrid(size):
    print('finish createGrid')

def gridToGraph(grid):
    graph = {}
    for x in range (len(grid)):
        for y in range(len(grid[0])):
            graph[(x,y)] = []
            try:
                if x == 0 or y == 0: raise IndexError
                if not grid[x-1][y-1]:
                    graph[(x,y)].append((x-1,y-1))
            except:
                pass

            try:
                if y == 0: raise IndexError
                if not grid[x][y-1]:
                    graph[(x,y)].append((x,y-1))
            except:
                pass

            try:
                if y == 0: raise IndexError
                if not grid[x+1][y-1]:
                    graph[(x,y)].append((x+1,y-1))
            except:
                pass

            try:
                if x == 0: raise IndexError
                if not grid[x-1][y]:
                    graph[(x,y)].append((x-1,y))
            except:
                pass

            try:
                if not grid[x+1][y]:
                    graph[(x,y)].append((x+1,y))
            except:
                pass

            try:
                if x == 0: raise IndexError
                if not grid[x-1][y+1]:
                    graph[(x,y)].append((x-1,y+1))
            except:
                pass

            try:
                if not grid[x][y+1]:
                    graph[(x,y)].append((x,y+1))
            except:
                pass

            try:
                if not grid[x+1][y+1]:
                    graph[(x,y)].append((x+1,y+1))
            except:
                pass

    return graph

def aStar(graph,start,goal):
    frontier = [(0,start)]
    cameFrom = {}
    shortestPathCost = {x:math.inf for x in graph.keys()}
    shortestPathCost[start] = 0

    while not len(frontier) == 0:
        #print(frontier)
        current = heapq.heappop(frontier)[1]

        if current == goal:
            path = []
            while not current == start:
                path.append(cameFrom[current])
                current = cameFrom[current]
            return path

        for neighbour in graph[current]:
            heuristic = math.sqrt((goal[0]-neighbour[0])**2+(goal[1]-neighbour[1])**2)*2
            linearDistance = math.sqrt((current[0]-neighbour[0])**2+(current[1]-neighbour[1])**2)

            score = linearDistance + shortestPathCost[current]

            if score < shortestPathCost[neighbour]:
                cameFrom[neighbour] = current
                shortestPathCost[neighbour] = score

                if neighbour not in frontier:
                    heapq.heappush(frontier,(score+heuristic,neighbour))

        for cell in cameFrom:
            renderCell(cell[0],cell[1],(255,0,255),50)

        for cell in frontier:
            renderCell(cell[1][0],cell[1][1],(255,255,0),50)

        pygame.display.flip()

        time.sleep(0.001)

    return []


def renderCell(x,y,color,gridSize):
    cellWidth = WIDTH/gridSize
    cellHeight= HEIGHT/gridSize
    edgeWidth = 0.3
    pygame.draw.rect(screen,(color[0],color[1],color[2]),
                                (x*cellWidth+edgeWidth,
                                y*cellHeight+edgeWidth,
                                cellWidth-edgeWidth*2,
                                cellHeight-edgeWidth*2))

def renderGrid(grid):
    cellWidth = WIDTH/len(grid)
    cellHeight= HEIGHT/len(grid[0])
    edgeWidth = 0.3

    for x in range (len(grid)):
        for y in range(len(grid[0])):
            color = grid[x][y]*255
            pygame.draw.rect(screen,(color,color,color),
                                        (x*cellWidth+edgeWidth,
                                        y*cellHeight+edgeWidth,
                                        cellWidth-edgeWidth*2,
                                        cellHeight-edgeWidth*2))


if __name__ == '__main__':
    WIDTH = HEIGHT = 500
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('A Star')
    background_colour = (255,255,255)
    screen.fill(background_colour)

    running = True

    gridSize = 50
    grid = [[False for _ in range(gridSize)] for _ in range(gridSize)]
    start = (-1,-1)
    end = (-1,-1)
    path = []
    selecting = False
    started = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    started = True

        if not started:
            if pygame.mouse.get_pressed() == (1,0,0):
                (x,y) = pygame.mouse.get_pos()
                cellx = math.floor(x/(WIDTH/gridSize))
                celly = math.floor(y/(HEIGHT/gridSize))
                grid[cellx][celly] = True

            elif pygame.mouse.get_pressed() == (0,0,1):
                (x,y) = pygame.mouse.get_pos()
                cellx = math.floor(x/(WIDTH/gridSize))
                celly = math.floor(y/(WIDTH/gridSize))
                grid[cellx][celly] = False

            elif pygame.mouse.get_pressed() == (0,1,0) and selecting == False:
                selecting = True
                (x,y) = pygame.mouse.get_pos()
                cellx = math.floor(x/(WIDTH/gridSize))
                celly = math.floor(y/(WIDTH/gridSize))

                if start == (-1,-1) and not end == (cellx,celly):
                    start = (cellx,celly)

                elif end == (-1,-1) and not start == (cellx,celly):
                    end = (cellx,celly)

                elif start == (cellx,celly):
                    start = (-1,-1)

                elif end == (cellx,celly):
                    end = (-1,-1)

            elif pygame.mouse.get_pressed() == (0,0,0):
                selecting = False

        renderGrid(grid)
        for cell in path:
            renderCell(cell[0],cell[1],(0,255,255),gridSize)
        renderCell(start[0],start[1],(0,255,0),gridSize)
        renderCell(end[0],end[1],(255,0,0),gridSize)

        if started:
            graph = gridToGraph(grid)
            path = aStar(graph,start,end)
            started = False

        pygame.display.flip()
