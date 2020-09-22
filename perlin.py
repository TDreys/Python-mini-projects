import random
import math
import pygame
import sys

def generateRandomGrid(gridSize):
    return [[getRandom2DVector() for _ in range(gridSize+1)]  for _ in range(gridSize+1)]

def cosInterp(x,lowy,highy):
    mu2 = (1-math.cos(x*math.pi))/2
    return (lowy*(1-mu2)+highy*mu2)

def getPerlinAtPoint(x,y,grid):
    #calculate which cell the pixel is located in
    cellx = math.floor(x)
    celly = math.floor(y)

    #get the vectors for the 4 nearest grid points
    topLeft = grid[cellx][celly]
    topRight = grid[cellx+1][celly]
    botLeft = grid[cellx][celly+1]
    botRight = grid[cellx+1][celly+1]

    #get the dot product for the random vector and distance vector for the pixel
    topLeftDot = dotProduct((x-cellx,y-celly),topLeft)
    topRightDot = dotProduct((x-(cellx+1),y-celly),topRight)
    botLeftDot = dotProduct((x-cellx,y-celly-1),botLeft)
    botRightDot = dotProduct((x-(cellx+1),y-(celly+1)),botRight)

    #interpolate the dot product values
    interpTop = cosInterp(x-cellx,topLeftDot,topRightDot)
    interpBot = cosInterp(x-cellx,botLeftDot,botRightDot)
    interpMiddle = cosInterp(y-celly,interpTop,interpBot)

    #THIS DATA IS NOT NORMALIZED
    return interpMiddle

def perlinNoise(pixelSize,gridSize):
    #create random grid of vectors
    grid = generateRandomGrid(gridSize)
    pixels = [[0] * pixelSize for _ in range(pixelSize)]

    #go through each pixel and calculate perlin value at the pixel
    for x in range(pixelSize):
        for y in range(pixelSize):
            #calculate the position of the pixel relative to the grid
            gridx = (x/pixelSize) * gridSize
            gridy = (y/pixelSize) * gridSize

            pixels[x][y] = getPerlinAtPoint(gridx,gridy,grid)

    return pixels

def dotProduct(vec1,vec2):
    return vec1[0]*vec2[0] + vec1[1]*vec2[1]

def getRandom2DVector():
    angle = random.random()*6.28
    x = math.cos(angle)
    y = math.sin(angle)
    return (x,y)

def renderGrid(grid,screen):
    cellWidth = int(300/len(grid))
    cellHeight= int(300/len(grid[0]))

    for x in range (len(grid)):
        for y in range(len(grid[0])):
            color = (grid[x][y] + 1)*100
            try:
                pygame.draw.rect(screen,(color,color,color),
                                        (x*cellWidth,y*cellHeight,
                                        cellWidth,cellHeight))
            except:
                print('not a color')

if __name__ == '__main__':
    frequency = 10
    if len(sys.argv) > 1 and str.isdigit(sys.argv[1]):
        frequency = int(sys.argv[1])
    else:
        print('use command line argument to change frequence, default=10')

    WIDTH = HEIGHT = 300
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('Perlin Noise')
    background_colour = (0,0,0)
    screen.fill(background_colour)

    grid = perlinNoise(300,frequency)

    renderGrid(grid,screen)

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              running = False
