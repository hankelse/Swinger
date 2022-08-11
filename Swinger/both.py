import pygame, sys, time, math, random
from pygame.constants import K_ESCAPE, K_SPACE, K_LSHIFT, K_a, K_d, K_w, K_s, K_q, K_l, K_UP, K_DOWN
pygame.init()

size = width, height =  800, 800
grid_size = 7
grid_unit_size = int(width/grid_size)
cycle_time = 0.025

screen = pygame.display.set_mode(size)

def are_touching(shape1, shape2): #shapes need .x .y and .size
    #ellipse
    kill_distance = (shape1.size+shape2.size)/2 #/4 ?
    if math.sqrt((shape1.x-shape2.x)**2 + (shape1.y-shape2.y)**2) <= kill_distance:
        return(True)
    return(False)

def clean_angle(angle):
    angle = angle %360
    if angle <0:
        angle = 360 - abs(angle)
    return(angle)

def sigmoid(x):
    if x<0: return(-1)
    if x>0: return(1)
    else: return(0)

# def circle_derivative(theta):
#     output = theta/(math.sqrt(1-theta**2))

def is_in_bounds(x, y):
    if x > width or x < 0 or y> height or y<0:
        return False
    return True

def line (angle, length, x, y, thickness):
    pygame.draw.line(screen, (0, 0, 0), (x,y), (x+length*math.cos(math.radians(angle)),y-length*math.sin(math.radians(angle))), thickness)

class Player:
    def __init__ (self, starting_x, starting_y, length):
        self.starting_x, self.starting_y = starting_x, starting_y
        self.length = length
        self.static = self.b1 = Block(self.starting_x, self.starting_y)
        self.moving = self.b2 = Block(self.starting_x, self.starting_y)
        self.connecter = Line(self.starting_x, self.starting_y, starting_theta, thickness, self.length)
        self.direction = 1
        self.move_delay = 0.25
        self.last_action = 0
        self.rotate_speed = starting_rotate_speed
        self.rotate_acceleration = rotate_acceleration
        self.x_velocity, self.y_velocity = 0, 0
        self.jump_x, self.jump_y = 0, 0
        self.state = "swing"
        self.swing_direction = "change"
    def move (self):
        keys = pygame.key.get_pressed()
        now = time.time()

        if keys[decelerate]:
            self.rotate_acceleration = abs(self.rotate_acceleration)*-1
        elif keys[accelerate]:
            self.rotate_acceleration = abs(self.rotate_acceleration)


        if self.state == "swing":
            if keys[sprint]: self.sprint_factor = 2
            else: self.sprint_factor = 1
            if keys[release] and now- self.last_action > self.move_delay:
                self.state = "fly"
                self.jump_x, self.jump_y = self.moving.x, self.moving.y #used to find the change in distance over jump and move the rest that amount
                self.x_velocity, self.y_velocity = self.get_velocities()
                self.last_action = self.shoot()
                self.flying = self.static
                self.bounces = 0 #keep track to determine rotation direction when landed
            elif keys[pivot]and now- self.last_action > self.move_delay:
                self.last_action = self.pivot()
            else:
                if self.rotate_acceleration > 0 or (self.rotate_acceleration <0 and self.rotate_speed + self.rotate_acceleration >=0):
                    self.rotate_speed += self.rotate_acceleration
                
                move_valid = self.connecter.rotate(self.rotate_speed, self.direction, self.sprint_factor)
                if move_valid == False: self.direction *= -1
                self.moving.move(self.connecter.x2, self.connecter.y2)
                self.static.move(self.connecter.x1, self.connecter.y1)
        elif self.state == "fly":
            if (keys[left] or keys[right] or keys[up] or keys[down]) and now - self.last_action > self.move_delay:
                self.state = "swing"
                self.swing_direction = self.get_swing_change(keys)
                #self.x_velocity, self.y_velocity = 0,0
                self.last_action = self.land()
                self.move()
            else:
                
                new_flying_x = self.flying.x + self.x_velocity *self.direction*-1
                new_flying_y = self.flying.y + self.y_velocity*self.direction*-1
                if is_in_bounds(new_flying_x, new_flying_y) == False:
                    self.bounces += 1
                    if new_flying_x >= width or new_flying_x <= 0: 
                        print("bounce x")
                        self.x_velocity = self.x_velocity*-1
                    if new_flying_y >= height or new_flying_y <= 0: 
                        print("bounce y")
                        self.y_velocity=self.y_velocity*-1 
                    new_flying_x = self.flying.x + self.x_velocity *self.direction*-1
                    new_flying_y = self.flying.y + self.y_velocity*self.direction*-1

                self.flying.x = new_flying_x
                self.flying.y = new_flying_y

    def get_velocities(self):
        angle = self.connecter.angle%360 #simplify angle for simplicities sake
        change_x = self.length*(math.cos(math.radians(angle+self.rotate_speed))-math.cos(math.radians(angle))) #find the x distance being traveled between current value and next based on speed
        change_y = self.length*(math.sin(math.radians(angle+self.rotate_speed))-math.sin(math.radians(angle))) #find the y distance being traveled between current value and next based on speed
        net_distance = math.sqrt(change_x**2+change_y**2) #pythag to find net distace
        net_velocity = net_distance*self.sprint_factor #velocity = distance/frames but frames = 1
        self.x_v, self.y_v = -1*math.cos(math.radians(self.connecter.angle+90))*net_velocity, math.sin(math.radians(self.connecter.angle+90))*net_velocity
        
        return self.x_v, self.y_v

    def get_swing_change(self, keys):
        #direction = ""
        if self.direction == 1: current_direction = "CC" ##counter clockwise
        elif self.direction == -1: current_direction = "C" #clockwise

        print(self.x_velocity, self.y_velocity,current_direction, self.direction)
        if keys[left]: 
    
            if self.y_velocity*self.direction < 0:
                desired_direction = "C"
                print("down", desired_direction)
            else: 
                desired_direction = "CC"
                print("up", desired_direction)

        elif keys[up]: 
            if self.x_velocity*self.direction < 0: #if x_velocity is positive
                desired_direction = "CC"
            else: desired_direction = "C"


        elif keys[down]: 
            if self.x_velocity*self.direction < 0:
                desired_direction = "C"
            else: desired_direction = "CC"


        elif keys[right]: 
            if self.y_velocity*self.direction < 0:
                desired_direction = "CC"
            else: desired_direction = "C"
        print(desired_direction, current_direction)
        if desired_direction != current_direction: return("change")
        else: return("same")
            


    def shoot(self):

        #self.connecter.x2, self.connecter.y2 = self.connecter.x1 - math.tan(self.connecter.angle), self.connecter.y1 + 1
        #self.rotate_speed = starting_rotate_speed
        
        new_static = self.moving
        self.moving = self.static
        self.static = new_static
        new_x1, new_y1 = self.connecter.x2, self.connecter.y2
        self.connecter.x2, self.connecter.y2 = self.connecter.x1, self.connecter.y1
        self.connecter.x1, self.connecter.y1 = new_x1, new_y1

        
        #self.connecter.angle -=180
        return(time.time())

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

    def land(self):
        #print(self.x_velocity, self.y_velocity)
        new_moving_x, new_moving_y = self.static.x, self.static.y
        self.static.x, self.static.y = self.moving.x, self.moving.y
        self.moving.x, self.moving.y = new_moving_x, new_moving_y

        change_x, change_y = self.moving.x - self.jump_x, self.moving.y - self.jump_y

        self.connecter.x1, self.connecter.y1 = self.static.x + change_x, self.static.y + change_y

        #if self.bounces % 2 != 0:
            #self.direction *= -1
        
        ## need to find the angle at which the block is moving and then use the angle whose tangent is perpendicular to that
        #self.connecter.angle = math.degrees(math.atan(self.y_velocity/self.x_velocity))
        if self.y_velocity > 0:
            self.connecter.angle = math.degrees(math.atan(self.x_velocity/self.y_velocity))
        elif self.y_velocity < 0:
            self.connecter.angle = math.degrees(math.atan(self.x_velocity/self.y_velocity))-180
        else:
            pass
        #self.connecter.angle = self.connecter.angle %90
        
        #print(self.length*math.acos(math.radians(self.connecter.angle)))
        #print(math.cos(math.radians(self.connecter.angle)), math.sin(math.radians(self.connecter.angle)))
        #self.connecter.x1, self.connecter.y1 = self.moving.x+self.length*math.cos(math.radians(180-self.connecter.angle)), self.moving.y+self.length*math.sin(math.radians(180-self.connecter.angle))
        #if self.swing_direction == "change_direction": self.swing_direction = "same"
        #if self.swing_direction == "swing": self.swing_direction = "change_direction"
        # swing = "change_direction"
        # swing = "same"

        if self.swing_direction == "change":
            print("changed")
            self.connecter.x1, self.connecter.y1 = self.moving.x-self.length*math.cos(math.radians(180-self.connecter.angle)), self.moving.y-self.length*math.sin(math.radians(180-self.connecter.angle))
            self.connecter.angle+=180
            self.direction *= -1
            #self.swing_direction = "same"
        elif self.swing_direction == "same":
            print("same")
            self.connecter.x1, self.connecter.y1 = self.moving.x+self.length*math.cos(math.radians(180-self.connecter.angle)), self.moving.y+self.length*math.sin(math.radians(180-self.connecter.angle))
            #self.swing_direction = "change"
        #self.connecter.angle += 180
        return(time.time())


    def draw(self):
        if self.state == "swing":
            self.connecter.draw()
            self.moving.draw(False)
        self.static.draw(True)
        

class Enemy:
    def __init__(self, starting_x, starting_y, speed):
        self.x, self.y = starting_x, starting_y
        self.speed = speed
        self.x_v, self.y_v = self.speed, self.speed
        self.x_direction, self.y_direction = random.choice((-1, 1)), random.choice((-1, 1))
        self.size = random.randint(20, 75)
    def move(self): 
        # self.x += self.x_v
        # self.y += self.y_v
        new_x = self.x + self.x_v * self.x_direction*-1
        new_y = self.y + self.y_v*self.y_direction*-1
        if is_in_bounds(new_x, new_y) == False:
            if new_x >= width or new_x <= 0: 
                print("bounce x")
                self.x_v = self.x_v*-1
            if new_y >= height or new_y <= 0: 
                print("bounce y")
                self.y_v = self.y_v*-1 
            new_x = self.x + self.x_v*self.x_direction*-1
            new_y = self.y + self.y_v*self.y_direction*-1

        self.x = new_x
        self.y = new_y
    def destroy(self, player):
        self.x_v, self.y_v = player.get_velocities()
    def draw(self):
        pygame.draw.ellipse(screen, (255, 100, 80), pygame.Rect(self.x-self.size/2, self.y-self.size/2, self.size, self.size))

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
        self.size = thickness*2
        self.static = False
    def move(self, x, y):
        self.x, self.y = x, y
    def draw(self, is_static):
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.x-self.size/2, self.y-self.size/2, self.size, self.size))
        if is_static == True:
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.x-self.size/4, self.y-self.size/4, self.size/2, self.size/2))


starting_theta = 360
starting_rotate_speed = 4
rotate_acceleration = 0.001
thickness = 10
fly_delay = 0.2

player = Player(400, 400, 100)

enemy_number = 10
enemies = []
for i in range(enemy_number):enemies.append(Enemy(random.randint(0, width), random.randint(0, height), random.randint(2, 6)))
#enemy = Enemy(100, 100, 5)

release = K_SPACE
sprint = K_l
up = K_w
left = K_a
right = K_d
down = K_s
pivot = K_LSHIFT
accelerate = K_UP
decelerate = K_DOWN

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
 

    player.move()
    player.draw()

    for enemy in enemies:
        enemy.move()
        if player.state == "swing":
            if are_touching(enemy, player.static) == True: 
                pass
                #player dies
            if are_touching(enemy, player.moving) == True: 
                #enemy dies
                enemy.destroy(player)
                #enemies.remove(enemy)
                pass
        else: 
            if are_touching(enemy, player.static) == True:
                #player dies
                pass
        enemy.draw()
    

    # line_.draw()
    # start.draw()
    # destination.draw()
    #line(theta, 100, 400, 400, thickness)
  
    
    pygame.display.flip()
    elapsed = time.time()-now
    if elapsed < cycle_time:
        time.sleep(cycle_time-elapsed)
