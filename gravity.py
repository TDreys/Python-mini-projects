import pygame
import math
import time

WIDTH = HEIGHT = 800
screen = pygame.display.set_mode((WIDTH,HEIGHT))

def render(objects):
    for object in objects:
        pygame.draw.circle(screen,(255,255,255),(int(object.xpos),int(object.ypos)),object.radius)

def step(objects):
    steppedObjects = []
    for current in objects:
        forcex = 0
        forcey = 0
        stepped = Object(current.radius,current.xpos,current.ypos,current.xvel,current.yvel)

        for object in objects:
            if current == object:
                continue

            distancex = (object.xpos-current.xpos)
            distancey = (object.ypos-current.ypos)
            theta = math.atan2(distancey,distancex)

            distance = math.sqrt(distancex ** 2 + distancey ** 2)
            force = ((current.radius ** 2) * (object.radius ** 2))/distance ** 2

            if distance < current.radius+object.radius:
                len1 = distance - object.radius
                len2 = distance - current.radius
                toAdjust = (distance - len1 - len2)

                distance = current.radius+object.radius
                force = ((current.radius ** 2) * (object.radius ** 2))/distance ** 2
                force = -force * 20

                stepped.xpos -= toAdjust*math.cos(theta)
                stepped.ypos -= toAdjust*math.sin(theta)

            forcex += force * math.cos(theta)
            forcey += force * math.sin(theta)


        accelx = forcex/(current.radius ** 2)
        accely = forcey/(current.radius ** 2)

        stepped.xvel += accelx
        stepped.yvel += accely
        stepped.xpos += stepped.xvel
        stepped.ypos += stepped.yvel
        steppedObjects.append(stepped)

    return steppedObjects

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
