import pygame, sys, time, math
from pygame.constants import K_ESCAPE, K_SPACE, K_LSHIFT
pygame.init()

size = width, height =  800, 800
grid_size = 7
grid_unit_size = int(width/grid_size)
cycle_time = 0.025

screen = pygame.display.set_mode(size)

def is_in_bounds(x, y):
    if x > width or x < 0 or y> height or y<0:
        return False
    return True

def line (angle, length, x, y, thickness):
    pygame.draw.line(screen, (0, 0, 0), (x,y), (x+length*math.cos(math.radians(angle)),y-length*math.sin(math.radians(angle))), thickness)

#rigid - Only can have 1 leg
class Rigid_Player:
    def __init__ (self, starting_x, starting_y, length):
        self.starting_x, self.starting_y = starting_x, starting_y
        self.length = length
        self.static = self.b1 = Block(self.starting_x, self.starting_y)
        self.moving = self.b2 = Block(self.starting_x, self.starting_y)
        self.connecter = Line(self.starting_x, self.starting_y, starting_theta, thickness, self.length)
        self.direction = 1
        self.move_delay = 0.25
        self.last_pivot = 0
        self.rotate_speed = starting_rotate_speed
    def rotate (self):
        keys = pygame.key.get_pressed()
        now = time.time()
        if keys[K_LSHIFT]: sprint_factor = 2
        else: sprint_factor = 1
        if keys[K_SPACE] and now- self.last_pivot > self.move_delay:
            self.last_pivot = self.pivot()
                
        else:
            self.rotate_speed += rotate_acceleration
            move_valid = self.connecter.rotate(self.rotate_speed, self.direction, sprint_factor)
            if move_valid == False: self.direction *= -1
            self.moving.move(self.connecter.x2, self.connecter.y2)
            self.static.move(self.connecter.x1, self.connecter.y1)
    def pivot(self):
        print("pivot")
        self.rotate_speed = starting_rotate_speed
        self.direction *= -1
        new_static = self.moving
        self.moving = self.static
        self.static = new_static
        new_x1, new_y1 = self.connecter.x2, self.connecter.y2
        self.connecter.x2, self.connecter.y2 = self.connecter.x1, self.connecter.y1
        self.connecter.x1, self.connecter.y1 = new_x1, new_y1

        
        self.connecter.angle -=180
        return(time.time())

    def draw(self):
        self.connecter.draw()
        self.static.draw(True)
        self.moving.draw(False)
        


#flexible - can have as many legs as possible
class Flexible_Player:
    pass


class Line:
    def __init__(self, x, y, angle, thickness, length):
        self.x1, self.y1, self.angle, self.thickness, self.length = x, y, angle, thickness, length
        self.x2, self.y2 = self.x1, self.y1
    def rotate(self, rotate_speed, direction, sprint_factor):
        self.angle += rotate_speed*direction*sprint_factor
        self.new_x2, self.new_y2 = self.x1+self.length*math.cos(math.radians(self.angle)),self.y1-self.length*math.sin(math.radians(self.angle))
        if is_in_bounds(self.new_x2, self.new_y2):
            self.x2, self.y2 = self.new_x2, self.new_y2
            return True #move is valid
        else: return False #must pivot!
    def draw(self):
        pygame.draw.line(screen, (0, 0, 0), (self.x1, self.y1), (self.x2, self.y2), thickness)

class Block:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.thickness = thickness
        self.static = False
    def move(self, x, y):
        self.x, self.y = x, y
    def draw(self, is_static):
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.x-self.thickness, self.y-self.thickness, self.thickness*2, self.thickness*2))
        if is_static == True:
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.x-self.thickness/2, self.y-self.thickness/2, self.thickness, self.thickness))


starting_theta = 360
starting_rotate_speed = 4
rotate_acceleration = 0.1
thickness = 10

player1 = Rigid_Player(400, 400, 100)

player2 = Flexible_Player()

# destination = Block(400, 400)
# start = Block(400, 400)
# line_ = Line(400, 400, starting_theta, thickness, 100)

starting_rotate_speed
theta = starting_theta
while 1:
    now = time.time()
    screen.fill((255, 255, 255))
    keys=pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        quit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    # line_.rotate(rotate_speed)
    # start.move(line_.x2, line_.y2)
    # destination.move(line_.x1, line_.x1)

    player1.rotate()
    player1.draw()

    # line_.draw()
    # start.draw()
    # destination.draw()
    #line(theta, 100, 400, 400, thickness)
  
    
    pygame.display.flip()
    elapsed = time.time()-now
    if elapsed < cycle_time:
        time.sleep(cycle_time-elapsed)
