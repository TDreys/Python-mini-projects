import pygame
import math
import time

WIDTH = HEIGHT = 800
screen = pygame.display.set_mode((WIDTH,HEIGHT))

def render(objects):
    for object in objects:
        pygame.draw.circle(screen,(255,255,255),(int(object.xpos),int(object.ypos)),object.radius)

def step(objects):
    stepped = []
    for current in objects:
        forcex = 0
        forcey = 0
        for object in objects:
            if current == object:
                continue

            distancex = (current.xpos-object.xpos)
            distancey = (current.ypos-object.ypos)
            theta = math.atan2(distancey,distancex)

            distance = math.sqrt(distancex ** 2 + distancey ** 2)
            if distance < max(current.radius,object.radius):
                distance = max(current.radius,object.radius)
            force = ((current.radius ** 2) * (object.radius ** 2))/distance ** 2

            forcex -= force * math.cos(theta)
            forcey -= force * math.sin(theta)


        accelx = forcex/(current.radius ** 2)
        accely = forcey/(current.radius ** 2)
        current.xvel += accelx
        current.yvel += accely
        current.xpos += current.xvel
        current.ypos += current.yvel
        stepped.append(current)

    return stepped

class Object:
    def __init__(self,radius,xpos,ypos,xvel,yvel):
        self.radius = radius
        self.xpos = xpos
        self.ypos = ypos
        self.xvel = xvel
        self.yvel = yvel


if __name__ == '__main__':
    running = True

    pygame.display.set_caption('Gravity Sim')
    background_colour = (0,0,0)
    screen.fill(background_colour)
    pygame.display.flip()
    radius = 50
    objects = []
    clicked = False

    while running:
        screen.fill((0,0,0))
        (mousex,mousey) = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    radius += 3
                elif event.button == 5:
                    radius -= 3

        if pygame.mouse.get_pressed() == (0,0,0) and clicked:
            clicked = False
            (x,y) = pygame.mouse.get_rel()
            objects.append(Object(radius,mousex,mousey,-x/50,-y/50))

        elif pygame.mouse.get_pressed() == (1,0,0) and not clicked:
            clicked = True
            pygame.mouse.get_rel()


        pygame.draw.circle(screen,(255,255,255),(mousex,mousey),radius)

        render(objects)
        objects = step(objects)

        pygame.display.flip()

        time.sleep(0.01)
