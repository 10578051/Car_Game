import pygame
import math
import random
import time
from utils import scale_image, blit_rotate_center

pygame.init()

TRACK = pygame.image.load("GameAssets/NewSizeBackground.png")
TOP_TRACK = pygame.image.load("GameAssets/NewSizeBackgroundTop.png")
TOP_TRACK_MASK = pygame.mask.from_surface(TOP_TRACK)
BOTTOM_TRACK = pygame.image.load("GameAssets/NewSizeTrackBottom.png")
BOTTOM_TRACK_MASK = pygame.mask.from_surface(BOTTOM_TRACK)
OTHER_OBJECTS = pygame.image.load("GameAssets/CarObjects.png")
OTHER_OBJECTS_MASK = pygame.mask.from_surface(OTHER_OBJECTS)
GREEN_CAR = scale_image(pygame.image.load("GameAssets/car_green_3.png"), 0.45)
ORANGE_CAR = scale_image(pygame.image.load("GameAssets/orange-car-top-view.png"), 0.06)
PARKING_SPOT = pygame.image.load("GameAssets/ParkingSuccessful.png")
PARKING_SPOT_TOP = pygame.image.load("GameAssets/ParkingSuccessfulTop.png")
PARKING_SPOT_MASK = pygame.mask.from_surface(PARKING_SPOT_TOP)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car parking game")

FPS = 60

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

    def collide_top(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def collide_bottom(self, mask, x=0, y=135):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def collide_other(self, mask, x=0, y=168):
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

def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)

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
images = [(TRACK, (0, 0)), (TOP_TRACK, (0, 0)), (BOTTOM_TRACK, (0,135)), (OTHER_OBJECTS, (0,168)), (PARKING_SPOT, (340,225))]
player_car = PlayerCar(5, 1)

while run:
    clock.tick(FPS)

    draw(WIN, images, player_car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    move_player(player_car)
    if player_car.collide_top(TOP_TRACK_MASK) != None:
        player_car.bounce()

    elif player_car.collide_bottom(BOTTOM_TRACK_MASK) != None:
        player_car.bounce()

    elif player_car.collide_other(OTHER_OBJECTS_MASK) != None:
        player_car.bounce()

    if player_car.collide_top(PARKING_SPOT_MASK, 350, 225) != None:
        player_car.reset()
        print("finish")

pygame.quit()

#Source of the above code = https://www.youtube.com/watch?v=L3ktUWfAMPg&t=1267s&ab_channel=TechWithTim
#Source of the above code = https://www.youtube.com/watch?v=WfqXcyF0_b0&t=1028s&ab_channel=TechWithTim