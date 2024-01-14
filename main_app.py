from typing import Any
import pygame
from pygame.locals import *
from pygame.sprite import Group
import random
import sys

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
vel = 0
scroll_speed = 2
flying = False
game_over = False
game_start = False
pipe_gap = 150
pipe_appear = 2000
last_pipe = pygame.time.get_ticks() - pipe_appear
score = 0
pass_pipe = False


# asset
bg = pygame.image.load("img/bg.png")
ground = pygame.image.load("img/ground.png")
pygame_icon = pygame.image.load('img/bird1.png')
restart_img = pygame.image.load('img/restart.png')
start_img = pygame.image.load('img/start.png')


# text
font = pygame.font.SysFont("pixel", 40)
color = (255,255,255)

def text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


def sys_reset():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score



class bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
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
        self.velocity = vel
        self.clicked = False


    def update(self): 
        # gravitasi
        if flying == True or game_over == True:
            self.velocity += 0.5
            if self.velocity > 8:
                self.velocity = 8
            if self.rect.bottom < 500:    
                self.rect.y += int(self.velocity)
            if self.rect.top < 0:
                self.rect.y -= int(self.velocity)
            
            
        # jump
        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.velocity = -7
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            
        # animation
        if game_over == False and flying == True:
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1            
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
            # rotate bird
            self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -3)
        
        if game_over == True:
            self.image = pygame.transform.rotate(self.images[self.index], -30)
            pygame.time.delay(2)
            self.image = pygame.transform.rotate(self.images[self.index], -60)
            pygame.time.delay(2)
                
        if game_over == False and pygame.mouse.get_pressed()[0] == 1:
            self.image = pygame.transform.rotate(self.images[self.index], 0)

class pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x,y + int(pipe_gap / 2)]
    
    def update(self):
        if flying == True:
            self.rect.x -= scroll_speed
            if self.rect.right < 0:
                self.kill()

class start_button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
    def draw(self):
        press = False
    
        # get mouse position
        MosPos = pygame.mouse.get_pos()
        if self.rect.collidepoint(MosPos):
            if pygame.mouse.get_pressed()[0] == 1:
                press = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return press

class restart_button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def draw(self):
        press = False
    
        # get mouse position
        MosPos = pygame.mouse.get_pos()
        if self.rect.collidepoint(MosPos):
            if pygame.mouse.get_pressed()[0] == 1:
                press = True
    
        # make button 
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return press

    def draw(self):
        press = False
    
        # get mouse position
        MosPos = pygame.mouse.get_pos()
        if self.rect.collidepoint(MosPos):
            if pygame.mouse.get_pressed()[0] == 1:
                press = True
    
        # make button 
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return press


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = bird(100, int(screen_height / 2))
bird_group.add(flappy)

# button start restart
button_start = start_button((screen_width - 120) / 2, ((screen_height - 180) // 2 ), start_img)
button_res = restart_button((screen_width - 120) / 2, ((screen_height - 100) // 2 ), restart_img)

ISRUN = True
while ISRUN:

    clock.tick(fps)


    # background game
    screen.blit(bg, (0,0))

    # object bird and pipe
    pipe_group.draw(screen)
    bird_group.draw(screen)
    bird_group.update()

    # draw ground
    screen.blit(ground, (ground_scroll,500))
    pygame.display.set_icon(pygame_icon)
    
    # check score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
    # text in screen
        # score in screen
    text(str(score), font, color, int(screen_width / 2), 10)

    # check collission
    if pygame.sprite.groupcollide(bird_group,pipe_group, False, False):
        game_over = True

    if game_over == False and flying == True:
        # generate pipe
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_appear:
            pipe_height = random.randint(-100, 100)
            top_pipe = pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            btm_pipe = pipe(screen_width, int(screen_height / 2) + pipe_height, 1) 
            pipe_group.add(btm_pipe,top_pipe)
            last_pipe = time_now
                

        # scroll the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 21:
            ground_scroll = 0
        pipe_group.update()


    # check if bird hit the ground
    if flappy.rect.bottom >= 500:
        game_over = True
        flying = False

    if game_over == False and game_start == False:
        if button_start.draw() == True:
            game_start = True

    if game_over == True:
        if button_res.draw() == True:
            game_over = False
            game_start = False
            score = sys_reset()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ISRUN = False
        if game_over == False and pygame.MOUSEBUTTONDOWN and game_start == True:
            flying = True
        if game_over ==True:
            flying = False
        
    
    pygame.display.update()
pygame.quit()