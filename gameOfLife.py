#A Game of Life simulation using pygame

import pygame
import random
import time

WIDTH = HEIGHT = 800
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Game of life')
background_colour = (255,255,255)
screen.fill(background_colour)
pygame.display.flip()

def createGrid(sideLength):
    width = []
    for x in range(sideLength):
        height = []
        for y in range(sideLength):
            height.append(random.random() > 0.6)

        width.append(height)

    return width

def renderGrid(grid):
    cellWidth = WIDTH/len(grid)
    cellHeight= HEIGHT/len(grid[0])
    edgeWidth = 0.1

    for x in range (len(grid)):
        for y in range(len(grid[0])):
            color = grid[x][y]*255
            pygame.draw.rect(screen,(color,color,color),
                                        (x*cellWidth+edgeWidth,
                                        y*cellHeight+edgeWidth,
                                        cellWidth-edgeWidth*2,
                                        cellHeight-edgeWidth*2))
def iterate(cells):
    newCells = [[0] * len(cells) for _ in range(len(cells))]

    for x in range (len(cells)):
        for y in range(len(cells[0])):
            surroundingCount = 0

            if x == 0:
                if y == 0:
                    surroundingCount += cells[x+1][y]
                    surroundingCount += cells[x][y+1]
                    surroundingCount += cells[x+1][y+1]

                elif y == len(cells[0])-1:
                    surroundingCount += cells[x][y-1]
                    surroundingCount += cells[x+1][y-1]
                    surroundingCount += cells[x+1][y]

                else:
                    surroundingCount += cells[x][y-1]
                    surroundingCount += cells[x+1][y-1]
                    surroundingCount += cells[x+1][y]
                    surroundingCount += cells[x][y+1]
                    surroundingCount += cells[x+1][y+1]

            elif x == len(cells)-1:
                if y == 0:
                    surroundingCount += cells[x-1][y]
                    surroundingCount += cells[x-1][y+1]
                    surroundingCount += cells[x][y+1]

                elif y == len(cells[0])-1:
                    surroundingCount += cells[x-1][y-1]
                    surroundingCount += cells[x][y-1]
                    surroundingCount += cells[x-1][y]

                else:
                    surroundingCount += cells[x-1][y-1]
                    surroundingCount += cells[x][y-1]
                    surroundingCount += cells[x-1][y]
                    surroundingCount += cells[x-1][y+1]
                    surroundingCount += cells[x][y+1]

            else:
                if y == 0:
                    surroundingCount += cells[x-1][y]
                    surroundingCount += cells[x+1][y]
                    surroundingCount += cells[x-1][y+1]
                    surroundingCount += cells[x][y+1]
                    surroundingCount += cells[x+1][y+1]

                elif y == len(cells[0])-1:
                    surroundingCount += cells[x-1][y-1]
                    surroundingCount += cells[x][y-1]
                    surroundingCount += cells[x+1][y-1]
                    surroundingCount += cells[x-1][y]
                    surroundingCount += cells[x+1][y]

                else:
                    surroundingCount += cells[x-1][y-1]
                    surroundingCount += cells[x][y-1]
                    surroundingCount += cells[x+1][y-1]
                    surroundingCount += cells[x-1][y]
                    surroundingCount += cells[x+1][y]
                    surroundingCount += cells[x-1][y+1]
                    surroundingCount += cells[x][y+1]
                    surroundingCount += cells[x+1][y+1]

            if (surroundingCount == 2 or surroundingCount == 3) and cells[x][y] == 1:
                newCells[x][y] = 1

            elif surroundingCount == 3 and cells[x][y] == 0:
                newCells[x][y] = 1

            else:
                newCells[x][y] = 0

    return newCells

if __name__ == '__main__':
    running = True

    grid = createGrid(100)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              running = False

        renderGrid(grid)
        pygame.display.flip()

        grid = iterate(grid)

        time.sleep(0.01)
