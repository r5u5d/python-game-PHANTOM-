#game premise: create a game where you can jump more than a certain amount of times
print("hello, world")
from ast import While
from math import floor
from math import floor

import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
import random
number = random.randint(0, 4)
different_blocks = ["yellow_body_square.png", "blue_body_square.png", "green_body_square.png", "red_body_square.png", 
                    "purple_body_square.png"]
image = pygame.image.load(f"kenney_shape-characters/PNG/Default/{different_blocks[number]}")
player_x = 100
player_y = 100


running = True
while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    key = pygame.key.get_pressed()

    player_y += 5
    if key[pygame.K_UP] or key[pygame.K_w]:
        player_y -= 5
    elif key[pygame.K_DOWN] or key[pygame.K_s]:
        player_y += 5
    elif key[pygame.K_LEFT] or key[pygame.K_a]:
        player_x -= 5
    elif key[pygame.K_RIGHT] or key[pygame.K_d]:
        player_x += 5
    
    if player_y < ground:
        player_y = ground      
    
    screen.fill((0, 0, 0))
    clock.tick(60)

    screen.blit(image, (player_x, player_y))
    pygame.display.flip()



pygame.quit()


    

