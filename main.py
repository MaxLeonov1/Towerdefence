import math
import os
import sys
import random
import pygame



pygame.init()
concurrent_path = os.path.dirname(__file__)
os.chdir(concurrent_path)
WIDTH = 1200
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
        self.timer_click = 0

    def update(self):
        global money
        self.timer_click += 1
        if self.rect.left <= pygame.mouse.get_pos()[0] <= self.rect.right and self.rect.top <= pygame.mouse.get_pos()[1] <= self.rect.bottom and tower_shop.buy == True and pygame.mouse.get_pressed()[0] and self.timer_click / FPS > 0.5 :
            tower = Tower_1(tower_1_on_image,(self.rect.centerx,self.rect.centery))
            tower_active_group.add(tower)
            money -= 300
            self.timer_click = 0
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
class Bullet(pygame.sprite.Sprite):
    def __init__(self,image,pos,speed,damage,enemy):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.damage = damage
        self.enemy = enemy
        self.rect = self.image.get_rect()
        self.speed = speed
        self.start_pos = pygame.math.Vector2(pos[0],pos[1])
        self.end_pos = pygame.math.Vector2(pos[2], pos[3])
        self.velocity = (self.end_pos - self.start_pos).normalize()*self.speed
        self.rect.center = self.start_pos

    def update(self):
        self.rect.center += self.velocity
        if self.rect.center == self.end_pos:
            self.kill()
            self.enemy.kill()


class Tower_Shop(pygame.sprite.Sprite):

    def __init__(self, image_on,image_off, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image_on
        self.image_off = image_off
        self.image_on = image_on
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.buy = False
        self.timer_click = 0

    def image_change(self):
        if money<300:
            self.image =self.image_off
        else:
            self.image = self.image_on
    def buy_tower(self):

        global money
        self.timer_click += 1
        if (tower_shop.rect.left <= pygame.mouse.get_pos()[0] <= tower_shop.rect.right and
                tower_shop.rect.top <= pygame.mouse.get_pos()[1] <= tower_shop.rect.bottom and
                pygame.mouse.get_pressed()[0] and self.timer_click / FPS > 0.1) :
            self.buy = not self.buy
            self.timer_click = 0
            #print(self.buy)
        if self.buy:
            sc.blit(tower_1_on_image,pygame.mouse.get_pos())
        if money <= 300:
            self.buy = False
    def update(self):
        self.image_change()
        self.buy_tower()

class Tower_1(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]-40
        self.rect.y = pos[1]-60
        self.lvl = 1
        self.damage = 30
        self.enemy = None
        self.timer_shot = 0
        self.speed = 15
        self.upgrade = False
        self.lvlup_cost = 200
        self.timer_click = 0
        self.current_bullet_image = bullet_image_1_1

    def shoot(self):
        self.timer_shot += 1
        if self.enemy is None:
            for enemy in spider_group:
                if ((self.rect.centerx - enemy.rect.centerx)**2+
                        (self.rect.centery - enemy.rect.centery)**2)**0.5 < 200:
                    self.enemy = enemy
                    break
        if self.enemy is not None:
            if ((self.rect.centerx - self.enemy.rect.centerx) ** 2 +
                (self.rect.centery - self.enemy.rect.centery) ** 2) ** 0.5 > 200:
                self.enemy = None
        if self.enemy not in spider_group:
            self.enemy = None
        if (self.enemy != None and self.timer_shot/FPS > 1):
            x_1 = self.rect.centerx
            y_1 = self.rect.top
            x_2 = self.enemy.rect.centerx
            y_2 = self.enemy.rect.centery
            bullet = Bullet(self.current_bullet_image,(x_1,y_1,x_2,y_2),self.speed, self.damage,self.enemy)
            bullet_group.add(bullet)
            self.timer_shot = 0


    def lvlup(self):
        global money
        #print(self.lvl)
        self.timer_click += 1
        if money >= self.lvlup_cost*self.lvl and self.lvl<2:
            self.upgrade = True
        if self.upgrade:
            sc.blit(update_sing_image,(self.rect.x+40,self.rect.y+60))
        if (self.upgrade and  self.rect.x + 20 <= pygame.mouse.get_pos()[0] <= self.rect.x + 80
            and self.rect.y +40 <= pygame.mouse.get_pos()[1] <= self.rect.y +100
                and pygame.mouse.get_pressed()[0] and self.timer_click / FPS > 0.1 and money >= self.lvlup_cost) :
            self.damage = self.damage*self.lvl
            self.image = tower_1_2_image
            self.lvlup_cost = self.lvlup_cost*self.lvl
            self.timer_click = 0
            self.lvl += 1
            self.upgrade = False
            self.speed = self.speed*math.sqrt(self.lvl)

            money -= self.lvlup_cost


    def update(self):
        self.shoot()
        self.lvlup()






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
    global path_group,bush_group,towerhill_group,arrow_group
    global spider_group,spider,spawner,tower_shop,tower_shop_group,tower_active_group,bullet_group
    path_group = pygame.sprite.Group()
    bush_group = pygame.sprite.Group()
    towerhill_group = pygame.sprite.Group()
    arrow_group = pygame.sprite.Group()
    spider_group = pygame.sprite.Group()
    tower_shop_group = pygame.sprite.Group()
    spawner = Spawner()
    tower_shop = Tower_Shop(tower_1_on_image,tower_1_off_image, (10, 730))
    tower_shop_group.add(tower_shop)
    tower_active_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()



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
    tower_active_group.draw(sc)
    tower_active_group.update()
    bullet_group.draw(sc)
    bullet_group.update()
    pygame.display.update()







restart()
drawMaps('map1.txt')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    game_lvl()
    clock.tick(FPS)
