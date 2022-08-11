import re
import pygame, sys, time, math
from pygame.constants import K_SPACE, K_w, K_a, K_s, K_d
pygame.init()

size = width, height =  800, 800
cycle_time = 0.025

screen = pygame.display.set_mode(size)

def are_touching(shape1, shape2): #shapes need .x .y and .size
    #ellipse
    kill_distance = (shape1.size+shape2.size)/2 #/4 ?
    if math.sqrt((shape1.x-shape2.x)**2 + (shape1.y-shape2.y)**2) <= kill_distance:
        return(True)
    return(False)

class Rect:
    def __init__(self, x, y, size, speed):
        self.x, self.y, self.size = x, y, size
        self.x_v, self.y_v = 1, 1
        self.speed = speed
    def move(self):
        if self.x <= 0: self.x_v = 1
        elif self.x >= width: self.x_v = -1
        if self.y <= 0: self.y_v = 1
        elif self.y >= height: self.y_v = -1
        self.x += self.x_v * self.speed
        self.y += self.y_v * self.speed
    def draw(self):
        pygame.draw.ellipse(screen, (0, 0, 0), pygame.Rect(self.x-self.size/2, self.y-self.size/2, self.size, self.size))

class Circle:
    def __init__(self, x, y, size, speed):
        self.x, self.y, self.size = x, y, size
        self.x_v, self.y_v = 1, 1
        self.speed = speed
    def move(self):
        if self.x <= 0: self.x_v = 1
        elif self.x >= width: self.x_v = -1
        if self.y <= 0: self.y_v = 1
        elif self.y >= height: self.y_v = -1
        self.x += self.x_v * self.speed
        self.y += self.y_v * self.speed
    def draw(self):
        pygame.draw.ellipse(screen, (0, 0, 0), pygame.Rect(self.x-self.size/2, self.y-self.size/2, self.size, self.size))

rect = Rect(300, 310, 40, 3)
ellipse  = Circle(120, 200, 100, 10)

while 1:
    now = time.time()
    screen.fill((160, 160, 160))
    keys=pygame.key.get_pressed()
    if keys[K_SPACE]:
        quit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    rect.move()
    ellipse.move()
    rect.draw()
    ellipse.draw()

   
    
    pygame.display.flip()
    elapsed = time.time()-now
    if elapsed < cycle_time:
        time.sleep(cycle_time-elapsed)
    if are_touching(rect, ellipse) == True: time.sleep(2)