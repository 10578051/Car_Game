import pygame
import math
import random
import time
from utils import scale_image, blit_rotate_center

pygame.init()

TRACK = pygame.image.load("GameAssets/AltBackground2.png")
GREEN_CAR = scale_image(pygame.image.load("GameAssets/car_green_3.png"), 0.45)
ORANGE_CAR = scale_image(pygame.image.load("GameAssets/orange-car-top-view.png"), 0.07)

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

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self,win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

class PlayerCar(AbstractCar):
    IMG = ORANGE_CAR
    START_POS = (180, 200)

def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    pygame.display.update()

run = True
clock = pygame.time.Clock()
#Higher the number below the faster it will go
images = [(TRACK, (0, 0))]
player_car = PlayerCar(4, 4)

while run:
    clock.tick(FPS)

    draw(WIN, images, player_car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_car.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        player_car.rotate(right=True)

pygame.quit()


