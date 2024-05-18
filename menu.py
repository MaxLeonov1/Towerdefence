# import os
# import runpy
# import sys
# import pygame
# pygame.init()

# f1 = pygame.font.Font(None,80)
# f2 = pygame.font.Font(None,40)




# concurrent_path = os.path.dirname(__file__)
# os.chdir(concurrent_path)
# WIDTH = 1200
# HEIGHT = 820
# FPS = 60
# sc = pygame.display.set_mode((WIDTH, HEIGHT))
# clock = pygame.time.Clock()

# def sings():
#     sc.fill('grey')
#     name_text = f1.render('TOWERDEFENCE',1,(100,100,100))
#     game_text = f2.render('Game',1,(100,100,100))
#     exit_text = f2.render('Exit',1,(100,100,100))
#     sc.blit(name_text,(365,200))
#     pygame.draw.rect(sc,(200,200,200),(400,350,400,100))
#     sc.blit(game_text, (420, 370))
#     pygame.draw.rect(sc, (200, 200, 200), (400, 500, 400, 100))
#     sc.blit(exit_text,(420,520))
#     pygame.display.update()

# def buttons():
#     if (400 <= pygame.mouse.get_pos()[0] <= 800 and 500 <= pygame.mouse.get_pos()[1] <= 600 \
#     and pygame.mouse.get_pressed()[0]):
#         sys.exit()
#     if (400 <= pygame.mouse.get_pos()[0] <= 800 and 350 <= pygame.mouse.get_pos()[1] <= 450 \
#             and pygame.mouse.get_pressed()[0]):
#         runpy.run_path(f'{os.getcwd()}/main.py')

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()
#     sings()
#     buttons()
#     clock.tick(FPS)