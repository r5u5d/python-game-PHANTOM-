print("hello, world")
from ast import While

import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
import random
number = random.randint(0, 5)
different_blocks = ["yellow_body_square.png", "blue_body_square.png", "green_body_square.png", "red_body_square.png", 
                    "purple_body_square.png", "orange_body_square.png"]
image = pygame.image.load(f"kenney_shape-characters/PNG/Default/{different_blocks[0]}")
image.blit(image, (100, 100))




running = True
while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    screen.fill((0, 0, 0))
    clock.tick(60)

    
    screen.blit(image, (100, 100))



pygame.quit()


    

