import math
import os
import sys
import random
import time
#import runpy
import pygame



pygame.init()
concurrent_path = os.path.dirname(__file__)
os.chdir(concurrent_path)
WIDTH = 1200
HEIGHT = 820
FPS = 60
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
Game = True
global_buy = False
from load import *
lvl_sc = 'menu'
prev_lvl_sc = 'menu'

total_enemies = 0
total_gold = 0


money = 10000
heathpoint = 5
f1 = pygame.font.Font(None,36)
f2 = pygame.font.Font(None,40)
f3 = pygame.font.Font(None, 100)

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
        self.tower = False



    def update(self):
        global money
        self.timer_click += 1
        if (self.rect.left <= pygame.mouse.get_pos()[0] <= self.rect.right and self.rect.top <= pygame.mouse.get_pos()[1] <= self.rect.bottom\
                and (tower_shop.buy == True or tower_shop2.buy == True) and pygame.mouse.get_pressed()[0] and self.timer_click / FPS > 0.5 and self.tower == False) :
            #print(pygame.mouse.get_pressed()[0])
            if tower_shop.buy == True:
                tower = Tower_1(tower_1_on_image,(self.rect.centerx,self.rect.centery),tower_1_1_animage,tower_1_2_animage,
                                40,bullet_1_1_animage,bullet_image_1_1,'bullet')
                tower_active_group.add(tower)
                money -= tower_shop.price
                tower_shop.buy = False
            if tower_shop2.buy == True:
                #add second lvl animage
                tower = Tower_1(tower_2_1_animage[0], (self.rect.centerx, self.rect.centery), tower_2_1_animage,
                                tower_2_2_animage, 50,boom_animage,bullet_image_2,'bomb')
                tower_active_group.add(tower)
                money -= tower_shop2.price
                tower_shop2.buy = False
            self.timer_click = 0
            self.tower = True
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
        self.spawn_amount = 0
    def spawn(self):
        self.spawn_kd += 1
        spider = Spider(enemy1_image, self.pos_s)
        if self.spawn_kd / FPS >= 0.8 and self.spawn_amount <= 30:
            spider = Spider(enemy1_image, self.pos_s)
            spider_group.add(spider)
            self.spawn_kd = 0
            self.spawn_amount+=1

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
        self.hp = 100

    def damage(self):
        global heathpoint,money,total_gold,total_enemies
        if self.rect.right >= WIDTH+50:
            self.kill()
            heathpoint -= 1
        if self.hp <= 0:
            self.kill()
            money += 10
            total_gold += 10
            total_enemies += 1

        if self.hp < 100 :
            width_hp = 48 * (self.hp / 100)
            pygame.draw.rect(sc, 'black', (self.rect.x - 10, self.rect.y - 13, 50, 10), 2)
            pygame.draw.rect(sc, 'green', (self.rect.x - 8, self.rect.y - 12, width_hp, 7))


    def update(self):
        self.damage()
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
    def __init__(self,image,pos,speed,damage,enemy,animage,bullet_type):
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
        self.animage = animage
        self.frame = 0
        self.anime = False
        self.timer_anime = 0
        self.kd_collide = 0
        self.flag_damage = True
        self.bullet_type = bullet_type


    def animation(self):
        self.image = self.animage[self.frame]
        if self.anime:
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.02:
                if self.frame == len(self.animage) - 1:
                    self.kill()
                else:
                    self.frame += 1
                self.timer_anime = 0

    def blow(self):
        #print(self.rect)
        if self.bullet_type == 'bullet':
            if pygame.sprite.spritecollide(self, spider_group, False) and self.flag_damage:
                # print(345345)
                self.kd_collide = 0
                self.enemy.hp -= self.damage
                self.anime = True
                self.velocity = self.velocity * 0
                self.flag_damage = False
        if self.bullet_type == 'bomb':
            if pygame.sprite.spritecollide(self, spider_group, False) and self.flag_damage:
                for enemy in spider_group:
                    #pass
                    if math.sqrt((enemy.rect.centerx-self.rect.centerx)**2+
                                 (enemy.rect.centery-self.rect.centery)**2)<=200:
                        enemy.hp -= self.damage
                self.kd_collide = 0
                self.velocity = self.velocity*0
                self.flag_damage = False
                self.anime = True


    def update(self):
        self.animation()
        self.blow()
        self.rect.center += self.velocity
        #print(self.kd_collide)


class Tower_Shop(pygame.sprite.Sprite):
    def __init__(self, image_on,image_off, pos,price):
        pygame.sprite.Sprite.__init__(self)
        self.image = image_on
        self.image_off = image_off
        self.image_on = image_on
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.buy = False
        self.timer_click = 0
        self.price = price


    def image_change(self):
        if money<=self.price:
            self.image =self.image_off
        else:
            self.image = self.image_on
    def buy_tower(self):
        global money,global_buy
        self.timer_click += 1
        #print(global_buy)
        if (self.rect.left <= pygame.mouse.get_pos()[0] <= self.rect.right and
                self.rect.top <= pygame.mouse.get_pos()[1] <= self.rect.bottom and
                pygame.mouse.get_pressed()[0] and self.timer_click / FPS > 0.1) :
            for tower in tower_shop_group:
                if tower.buy == True:
                    break
            else:

                self.buy = not self.buy
            #print(tower_shop2.buy)
            self.timer_click = 0
        if self.buy:
            sc.blit(self.image_on,pygame.mouse.get_pos())
        if money <= self.price:
            self.buy = False





    def update(self):
        self.image_change()
        self.buy_tower()

class Tower_1(pygame.sprite.Sprite):
    def __init__(self, image, pos,animage1,animage2,damage,bullet_animage,current_bullet_image,
                 bullet_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.animage1 = animage1
        self.animage2 = animage2
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]-40
        self.rect.y = pos[1]-60
        self.lvl = 1
        self.damage = damage
        self.enemy = None
        self.timer_shot = 0
        self.speed = 15
        self.upgrade = False
        self.lvlup_cost = 200
        self.timer_click = 0
        self.current_bullet_image = current_bullet_image
        self.anime = True
        self.timer_anime = 0
        self.frame = 0
        self.animage = self.animage1
        self.bullet_animage = bullet_animage
        self.bullet_type = bullet_type

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
            bullet = Bullet(self.current_bullet_image,(x_1,y_1,x_2,y_2),self.speed, self.damage,self.enemy,
                            self.bullet_animage,self.bullet_type)
            bullet_group.add(bullet)
            self.timer_shot = 0


    def lvlup(self):
        global money
        self.timer_click += 1
        if money >= self.lvlup_cost*self.lvl and self.lvl<2:
            self.upgrade = True
        else:
            self.upgrade = False
        if self.upgrade:
            sc.blit(update_sing_image,(self.rect.x+40,self.rect.y+60))
        if (self.upgrade and  self.rect.x + 20 <= pygame.mouse.get_pos()[0] <= self.rect.x + 80
            and self.rect.y +40 <= pygame.mouse.get_pos()[1] <= self.rect.y +100
                and pygame.mouse.get_pressed()[0] and self.timer_click / FPS > 0.1 and money >= self.lvlup_cost):
            self.lvl += 1
            self.damage = self.damage*math.sqrt(self.lvl)
            self.lvlup_cost = self.lvlup_cost*self.lvl
            self.timer_click = 0
            self.upgrade = False
            self.speed = self.speed*math.sqrt(self.lvl)

            money -= self.lvlup_cost

    def animation(self):
        if self.lvl == 1:
            self.animage = self.animage1
        if self.lvl == 2:
            self.animage = self.animage2
        self.image = self.animage[self.frame]
        if self.anime:
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.05:
                if self.frame == len(self.animage) - 1:
                    self.frame = 0
                else:
                    self.frame += 1
                self.timer_anime = 0

    def update(self):
        self.shoot()
        self.lvlup()
        self.animation()






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
    global spider_group,spider,spawner,tower_shop,tower_shop_group,tower_active_group,bullet_group,tower_shop2
    path_group = pygame.sprite.Group()
    bush_group = pygame.sprite.Group()
    towerhill_group = pygame.sprite.Group()
    arrow_group = pygame.sprite.Group()
    spider_group = pygame.sprite.Group()
    tower_shop_group = pygame.sprite.Group()
    spawner = Spawner()
    tower_shop = Tower_Shop(tower_1_on_image,tower_1_off_image, (10, 730),300)
    tower_shop2 = Tower_Shop(tower_2_1_animage[0],tower_2_1_off,(85,730),400)
    tower_shop_group.add(tower_shop,tower_shop2)
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
    heal_text = f1.render(f'HP:{heathpoint}',1,(180, 180, 180))
    sc.blit(money_text,(400,780))
    sc.blit(heal_text,(700,780))
    tower_shop_group.draw(sc)
    tower_shop_group.update()
    tower_active_group.draw(sc)
    tower_active_group.update()
    bullet_group.draw(sc)
    bullet_group.update()
    pygame.display.update()

pause_text = (pygame.font.Font(None,50)).render(f'Pause',1,(180, 180, 180))


def buttons1():
    global input_await,lvl_sc,prev_lvl_sc
    if (400 <= pygame.mouse.get_pos()[0] <= 800 and 350 <= pygame.mouse.get_pos()[1] <= 450
            and pygame.mouse.get_pressed()[0] and input_await/FPS>=0.5):
        lvl_sc = 'menu'
        prev_lvl_sc = 'game'

        input_await = 0
    if (400 <= pygame.mouse.get_pos()[0] <= 800 and 500 <= pygame.mouse.get_pos()[1] <= 600 \
            and pygame.mouse.get_pressed()[0] and input_await/FPS>=0.5):
        lvl_sc = 'stats'
        input_await = 0
        prev_lvl_sc = 'game'

def buttons2():
    global lvl_sc,input_await,prev_lvl_sc
    if (400 <= pygame.mouse.get_pos()[0] <= 800 and 300 <= pygame.mouse.get_pos()[1] <= 380 \
        and pygame.mouse.get_pressed()[0] and input_await/FPS>=0.5):
        lvl_sc = 'game'
        prev_lvl_sc = 'menu'
        input_await = 0
    if (400 <= pygame.mouse.get_pos()[0] <= 800 and 400 <= pygame.mouse.get_pos()[1] <= 480 \
            and pygame.mouse.get_pressed()[0] and input_await/FPS>=0.5):
        lvl_sc = 'stats'
        prev_lvl_sc = 'menu'
        input_await = 0
    if (400 <= pygame.mouse.get_pos()[0] <= 800 and 500 <= pygame.mouse.get_pos()[1] <= 580 \
            and pygame.mouse.get_pressed()[0] and input_await/FPS>=0.5):
        sys.exit()
        input_await = 0

def buttons3():
    global input_await,prev_lvl_sc,lvl_sc
    if (1030 <= pygame.mouse.get_pos()[0] <= 1130 and 700 <= pygame.mouse.get_pos()[1] <= 750 \
        and pygame.mouse.get_pressed()[0] and input_await/FPS>=0.5):
        input_await = 0
        if prev_lvl_sc == 'menu':
            lvl_sc = 'menu'
        if prev_lvl_sc == 'game':
            lvl_sc = 'game'


def stats():
    global total_enemies,total_gold
    sc.fill('grey')
    pygame.draw.rect(sc,(100,100,100),(50,50,1100,720))
    money_text = f1.render(f'Total Money:{total_gold}',1,'grey')
    sc.blit(money_text,(100,100))
    enemy_text = f1.render(f'Total Enemies:{total_enemies}',1,'grey')
    sc.blit(enemy_text, (100, 150))
    pygame.draw.rect(sc, (200, 200, 200), (1030, 700, 100, 50))
    return_text = f2.render('Back', 1, (100, 100, 100))
    sc.blit(return_text, (1040, 710))
    buttons3()

    pygame.display.update()
def sings():
    sc.fill('grey')
    name_text = f3.render('TOWERDEFENCE',1,(100,100,100))
    game_text = f2.render('Game',1,(100,100,100))
    exit_text = f2.render('Exit',1,(100,100,100))
    stats_text = f2.render('Statistics', 1, (100, 100, 100))
    sc.blit(name_text,(310,200))
    pygame.draw.rect(sc,(200,200,200),(400,300,400,80))
    sc.blit(game_text, (420, 320))
    pygame.draw.rect(sc, (200, 200, 200), (400, 400, 400, 80))
    sc.blit(stats_text,(420,420))
    pygame.draw.rect(sc, (200, 200, 200), (400, 500, 400, 80))
    sc.blit(exit_text, (420, 520))
    buttons2()
    pygame.display.update()

input_await = 0
restart()
spider_group.add(Spider(enemy1_image, (40, 600)))
drawMaps('map1.txt')
while True:
    #print(pygame.mouse.get_pressed()[0])
    input_await += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    if lvl_sc == 'menu':
        sings()
    elif lvl_sc == 'game':
        if (pygame.key.get_pressed()[pygame.K_SPACE] == False and len(spider_group) > 0):
            print(1)
            game_lvl()
        elif (pygame.key.get_pressed()[pygame.K_SPACE] == True):
            pause_text = f3.render(f'Pause', 1, (10, 10, 10))
            sc.blit(pause_text, (500, 200))
            game_text = f2.render('Menu', 1, (100, 100, 100))
            stats_text = f2.render('Statistics', 1, (100, 100, 100))
            pygame.draw.rect(sc, (200, 200, 200), (400, 350, 400, 100))
            pygame.draw.rect(sc, (200, 200, 200), (400, 500, 400, 100))
            sc.blit(game_text, (420, 370))
            sc.blit(stats_text, (420, 520))
            pygame.display.update()
            buttons1()
        elif len(spider_group) == 0:
            pass
    elif lvl_sc == 'stats':
        stats()
    clock.tick(FPS)

total_enemies = 0
total_gold = 0
