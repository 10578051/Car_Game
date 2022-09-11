import pygame
import math
import random
import time
from utils import scale_image, blit_rotate_center, blit_text_center

#The following initialises the font module in pygame
pygame.font.init()

pygame.init()

#The following are the images I will be using in the game
#This includes the track, the track overlay which will be used for collision
#The cars, and any objects which the car should 'collide' with

TRACK = pygame.image.load("GameAssets/Revised/Background.png")
TOP_TRACK = pygame.image.load("GameAssets/Revised/TrackCutOut.png")
TOP_TRACK_MASK = pygame.mask.from_surface(TOP_TRACK)
OTHER_OBJECTS = pygame.image.load("GameAssets/Revised/Object1.png")
OTHER_OBJECTS_MASK = pygame.mask.from_surface(OTHER_OBJECTS)
OTHER_OBJECTS_2 = pygame.image.load("GameAssets/Revised/Object2.png")
OTHER_OBJECTS_2_MASK = pygame.mask.from_surface(OTHER_OBJECTS)
GREEN_CAR = scale_image(pygame.image.load("GameAssets/car_green_3.png"), 0.45)
ORANGE_CAR = scale_image(pygame.image.load("GameAssets/orange-car-top-view.png"), 0.06)
FINISH1 = pygame.image.load("GameAssets/win1.png")
SPACE1 = pygame.image.load("GameAssets/Space1.png")
PARKING_SPOT_MASK = pygame.mask.from_surface(FINISH1)

#PARKING_SPOT = pygame.image.load("GameAssets/ParkingSuccessful.png")
#PARKING_SPOT_TOP = pygame.image.load("GameAssets/ParkingSuccessfulTop.png")
#PARKING_SPOT_MASK = pygame.mask.from_surface(PARKING_SPOT_TOP)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car parking game")

FPS = 60

#Defining a font which will be used on screen
MAIN_FONT = pygame.font.SysFont("aerial", 30)

#The following class will hold information on the game
#We will start on level 1 and define how many levels there are

class GameInformation:
    LEVELS = 3

    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.level_start_time = 0

    def next_level(self):
        self.level += 1
        self.started = False

    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0

    #If the level we get to is greater than the amount of levels
    #in the game then the game will be finished

    def game_finished(self):
        return self.level > self.LEVELS

    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def get_level_time(self):
        if not self.started:
            return 0
        return self.level_start_time - time.time()

class AbstractCar:

    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self,win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backwards(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def collide_other(self, mask, x=343, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def collide_other_2(self, mask, x=502, y=431):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def collide_finish1(self, mask, x=546, y=185):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def collide_finish2(self, mask, x=546, y=222):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def collide_finish3(self, mask, x=546, y=256):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def collide_finish4(self, mask, x=546, y=290):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def collide_finish5(self, mask, x=546, y=323):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

class PlayerCar(AbstractCar):
    IMG = ORANGE_CAR
    START_POS = (64, 500)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration/2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()

def draw(win, images, player_car, game_information):
    for img, pos in images:
        win.blit(img, pos)

    level_text = MAIN_FONT.render(f"Level {game_information.level}", 1, (0, 0, 0))
    win.blit(level_text, (10, HEIGHT - level_text.get_height() - 5))

    player_car.draw(win)
    pygame.display.update()

def move_player(player_car):

    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_LEFT]:
        player_car.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        player_car.rotate(right=True)
    if keys[pygame.K_UP]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_DOWN]:
        moved = True
        player_car.move_backwards()

    if not moved:
        player_car.reduce_speed()

run = True
clock = pygame.time.Clock()
#Higher the number below the faster it will go
images = [(TRACK, (0, 0)), (TOP_TRACK, (0, 0)), (OTHER_OBJECTS, (343,0)), (OTHER_OBJECTS_2, (502,431)), (FINISH1, (546,185)), (SPACE1, (500,185)), (FINISH1, (546,222)), (SPACE1, (500,222)), (FINISH1, (546,256)), (SPACE1, (500,256)), (FINISH1, (546,290)), (SPACE1, (500,290)), (FINISH1, (546,323)),
          (SPACE1, (500, 323))]

#Where the car will start
player_car = PlayerCar(5, 1)

game_information = GameInformation()

while run:
    clock.tick(FPS)

    draw(WIN, images, player_car, game_information)

    #The following will show information on the screen before the game begins

    while not game_information.started:
        blit_text_center(WIN, MAIN_FONT, f"Press any key to begin the game. You are on level {game_information.level}!")
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

            if event.type == pygame.KEYDOWN:
                game_information.start_level()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    move_player(player_car)
    if player_car.collide(TOP_TRACK_MASK) != None:
        player_car.bounce()

    elif player_car.collide_other(OTHER_OBJECTS_MASK) != None:
        player_car.bounce()

    elif player_car.collide_other_2(OTHER_OBJECTS_2_MASK) != None:
        player_car.bounce()

    if player_car.collide_finish1(PARKING_SPOT_MASK, 546, 185) != None:
        player_car.reset()
        print("finish")

    if player_car.collide_finish2(PARKING_SPOT_MASK, 546, 222) != None:
        player_car.reset()
        print("finish")

    if player_car.collide_finish3(PARKING_SPOT_MASK, 546, 256) != None:
        player_car.reset()
        print("finish")

    if player_car.collide_finish4(PARKING_SPOT_MASK, 546, 290) != None:
        player_car.reset()
        print("finish")

    if player_car.collide_finish5(PARKING_SPOT_MASK, 546, 323) != None:
        player_car.reset()
        print("finish")

pygame.quit()

#Source of the above code = https://www.youtube.com/watch?v=L3ktUWfAMPg&t=1267s&ab_channel=TechWithTim
#Source of the above code = https://www.youtube.com/watch?v=WfqXcyF0_b0&t=1028s&ab_channel=TechWithTim