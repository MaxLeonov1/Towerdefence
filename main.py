import os
import sys
import random
import pygame



pygame.init()
concurrent_path = os.path.dirname(__file__)
os.chdir(concurrent_path)
WIDTH = 15*80
HEIGHT = 9*80
FPS = 60
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
from load import *

class Bush(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

class Path(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

class Towerhill(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

class Arrow(pygame.sprite.Sprite):
    def __init__(self, image, pos, dir):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.dir = dir

class Spider(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.dir = 'right'
        self.speedx = 2
        self.speedy = 0

    def update(self):
        if self.dir == 'right':
            self.speedx = 2
            self.speedy = 0
        if self.dir == 'top':
            self.speedx = 0
            self.speedy = 2
        if self.dir == 'bottom':
            self.speedx = 0
            self.speedy = -2

        if self.dir == 'left':
            self.speedx = -2
            self.speedy = 0




def drawMaps(nameFile):
    global pos
    maps = []
    source = str(nameFile)
    with open(source,"r") as file:
        for i in range(0,9):
            maps.append(file.readline().replace("\n","").split(",")[0:-1])

    pos = [0,0]
    for i in range(0,len(maps)):
        pos[1] = i*80
        for j in range(0,len(maps[0])):
            pos[0] = 80*j
            if maps[i][j] == '1':
                x = Bush(bush_image,pos)
                bush_group.add(x)
            if maps[i][j] == '2':
                x = Towerhill(towerhill_image,pos)
                towerhill_group.add(x)
            if maps[i][j] == '3':
                x = Path(path_image,pos)
                path_group.add(x)
            if maps[i][j] == '4':
                x = Arrow(top_arrow_image,pos,'top')
                arrow_group.add(x)
            if maps[i][j] == '5':
                x = Arrow(bottom_arrow_image,pos,'bottom')
                arrow_group.add(x)
            if maps[i][j] == '6':
                x = Arrow(left_arrow_image,pos,'left')
                arrow_group.add(x)
            if maps[i][j] == '7':
                x = Arrow(right_arrow_image,pos,'right')
                arrow_group.add(x)


def restart():
    global path_group,bush_group,towerhill_group,arrow_group,spider_group
    path_group = pygame.sprite.Group()
    bush_group = pygame.sprite.Group()
    towerhill_group = pygame.sprite.Group()
    arrow_group = pygame.sprite.Group()
    spider_group = pygame.sprite.Group()

def game_lvl():
    sc.fill('black')
    path_group.draw(sc)
    path_group.update()
    bush_group.draw(sc)
    bush_group.update()
    towerhill_group.draw(sc)
    towerhill_group.update()
    arrow_group.draw(sc)
    arrow_group.update()
    spider_group.draw(sc)
    spider_group.update()
    pygame.display.update()


restart()
drawMaps('map1.txt')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    game_lvl()
    clock.tick(FPS)
