import pygame
from pygame.locals import *

# init
pygame.init()

clock = pygame.time.Clock()
fps = 60

# screen
screen_width = 562
screen_height = 610
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("flappy bird")


# game variables
ground_scroll = 0
scroll_speed = 1

# img
bg =pygame.image.load("img/bg.png")
ground = pygame.image.load("img/ground.png")
pygame_icon = pygame.image.load('img/bird1.png')

# program running game

class bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,4):
            img = pygame.image.load(f"img/bird{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.counter += 1
        flap_cooldown = 5

        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]

bird_group = pygame.sprite.Group()

flappy = bird(100, int(screen_height / 2))

bird_group.add(flappy)


ISRUN = True
while ISRUN:

    clock.tick(fps)


    # background game
    screen.blit(bg, (0,0))

    # object
    bird_group.draw(screen)
    bird_group.update()

    # scroll the ground
    screen.blit(ground, (ground_scroll,500))
    pygame.display.set_icon(pygame_icon)
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 20:
        ground_scroll = 0


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ISRUN = False
    pygame.display.update()

pygame.quit()