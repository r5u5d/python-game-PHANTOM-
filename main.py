print("hello, world")
from ast import While

import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock
image = pygame.image.load("kenny_shape-characters/")
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


    

