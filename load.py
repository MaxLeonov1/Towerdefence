import os
import pygame
def load_image(directory):
    image_list = []
    files = os.listdir(directory)
    for i in files:
        image = pygame.image.load(f'{directory}/{i}').convert_alpha()
        image_list.append(image)
    return image_list

bush_image = pygame.image.load('image/tile map/bush_tile 1.png').convert_alpha()
path_image = pygame.image.load('image/tile map/grass_tile_1.png').convert_alpha()
towerhill_image = pygame.image.load('image/tile map/bush_tile_tower.png').convert_alpha()
top_arrow_image = pygame.image.load('image/tile map/top.png').convert_alpha()
bottom_arrow_image = pygame.image.load('image/tile map/bottom.png').convert_alpha()
left_arrow_image = pygame.image.load('image/tile map/left.png').convert_alpha()
right_arrow_image = pygame.image.load('image/tile map/right.png').convert_alpha()
enemy1_image = pygame.image.load('image/enemy/right.png').convert_alpha()
panel_image = pygame.image.load('image/panel.jpg').convert_alpha()
tower_1_on_image = pygame.image.load('image/tower 1/1_on.png').convert_alpha()
tower_1_off_image = pygame.image.load('image/tower 1/1_of.png').convert_alpha()
update_sing_image = pygame.image.load('image/upgrade.png').convert_alpha()
tower_1_2_image = pygame.image.load('image/tower 1_1/tower/1.png').convert_alpha()
bullet_image_1_1 = pygame.image.load('image/tower 1/bullet 1.png').convert_alpha()
tower_1_1_animage = load_image('image/tower 1/tower')
tower_1_2_animage = load_image('image/tower 1_1/tower')
bullet_1_1_animage = load_image('image/tower 1/bullet_blow')
tower_2_1_off = pygame.image.load('image/tower 2/1 off.png').convert_alpha()
tower_2_1_animage = load_image('image/tower 2/tower')
tower_2_2_animage = load_image('image/tower 2/tower2')
boom_animage = load_image('image/tower 2/bullet')
bullet_image_2 = pygame.image.load('image/tower 2/bullet 2.png').convert_alpha()