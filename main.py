import os
import sys
import random
import pygame



pygame.init()
concurrent_path = os.path.dirname(__file__)
os.chdir(concurrent_path)
WIDTH = 15*80
HEIGHT = 820
FPS = 60
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
from load import *


money = 1000
f1 = pygame.font.Font(None,36)

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



class Spawner():
    def __init__(self):
        self.spawn_kd = 0
        self.pos_s = (40, 600)
    def spawn(self):
        self.spawn_kd += 1
        if self.spawn_kd / FPS >= 1:
            spider = Spider(enemy1_image, self.pos_s)
            spider.add(spider_group)
            self.spawn_kd = 0

class Tower_Shop(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.buy = True
        self.timer_click = 0

    def image_change(self):
        if money<300:
            self.image = tower_1_of_image
        else:
            self.image = tower_1_on_image
    def buy_tower(self):
        if self.timer_click > 0:
            self.timer_click -= 1/FPS
        if tower_shop.rect.left <= pygame.mouse.get_pos()[0] <= tower_shop.rect.right and tower_shop.rect.top <= pygame.mouse.get_pos()[1] <= tower_shop.rect.bottom and pygame.mouse. and self.timer_click == 0:
            self.buy = True
            print(self.buy)




    def update(self):
        self.image_change()
        self.buy_tower()

class Tower(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]



class Spider(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.dir = 'right'
        self.speedx = 2
        self.speedy = 0

    def update(self):
        if self.dir == 'right':
            self.speedx = 2
            self.speedy = 0
        elif self.dir == 'top':
            self.speedx = 0
            self.speedy = -2
        elif self.dir == 'bottom':
            self.speedx = 0
            self.speedy = 2
        elif self.dir == 'left':
            self.speedx = -2
            self.speedy = 0
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if pygame.sprite.spritecollide(self,arrow_group,False):
            tile = pygame.sprite.spritecollide(self, arrow_group,False)[0]
            if abs(self.rect.centerx - tile.rect.centerx) <= 5 and abs(self.rect.centery - tile.rect.centery) <= 5:

                self.dir = tile.dir






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
    global path_group,bush_group,towerhill_group,arrow_group,spider_group,spider,spawner,tower_shop,tower_shop_group
    path_group = pygame.sprite.Group()
    bush_group = pygame.sprite.Group()
    towerhill_group = pygame.sprite.Group()
    arrow_group = pygame.sprite.Group()
    spider_group = pygame.sprite.Group()
    tower_shop_group = pygame.sprite.Group()
    spawner = Spawner()
    tower_shop = Tower_Shop(tower_1_on_image, (10, 730))
    tower_shop_group.add(tower_shop)



def game_lvl():
    spawner.spawn()
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
    sc.blit(panel_image, (0, 720))
    money_text = f1.render(f'money:{money}', 1, (180, 180, 180))
    sc.blit(money_text,(600,780))
    tower_shop_group.draw(sc)
    tower_shop_group.update()
    pygame.display.update()






restart()
drawMaps('map1.txt')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    game_lvl()
    clock.tick(FPS)
