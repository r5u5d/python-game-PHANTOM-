#game premise: a game where u dodge obsticles
print("hello, world")


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
tutorial_steps = ["Press w,a,s,d or arrow keys to move move in the red box!", "stop! you cant go slow", "dodge the obstacles good luck!"]
step = 0
assets = pygame.image.load("kenney_shape-characters/PNG/Default/yellow_body_square.png")
font = pygame.font.Font(None, 36)
player_x = 100
player_y = 100
velocity = [0,0]
speed = 0.2
goal_rect = pygame.Rect(600, 400, 60, 60)
show_tutorial = True
running = True
def movement(player_x, player_y, velocity):
    key = pygame.key.get_pressed()
    if key[pygame.K_UP] or key[pygame.K_w]:
        velocity[1] += -1
    if key[pygame.K_DOWN] or key[pygame.K_s]:
        velocity[1] += 1
    if key[pygame.K_LEFT] or key[pygame.K_a]:
        velocity[0] += -1
    if key[pygame.K_RIGHT] or key[pygame.K_d]:
        velocity[0] += 1
    player_x += velocity[0] * speed
    player_y += velocity[1] * speed
            
    if velocity[0] > 0:
        velocity[0] -= velocity[0] * 0.01
    if velocity[0] < 0:
        velocity[0] += velocity[0] * -0.01
    if velocity[1] > 0:
        velocity[1] -= velocity[1] * 0.01
    if velocity[1] < 0:
        velocity[1] += velocity[1] * -0.01
    if player_x < 0 or player_x > 800 - image.get_width():
        player_x -= velocity[0] * speed
    if player_y < 0 or player_y > 600 - image.get_height():
        player_y -= velocity[1] * speed
    return player_x, player_y , velocity
def title_screen():
    global running
    running = True
    while running == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return running
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return running
                elif event.key == pygame.K_RETURN:
                    running = True
                    return running
                elif event.key == pygame.K_KP_ENTER:
                    running = True
                    return running
        screen.fill((135, 206, 235))
        text = font.render("Press Enter to Start", True, (0, 0, 0))
        screen.blit(text, (400 - text.get_width() // 2, 300 - text.get_height() // 2))
        pygame.display.flip()

running = title_screen()
def draw_tutorial():
    show_tutorial = True
    while show_tutorial == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif event.key == pygame.K_RETURN:
                    pygame.quit()
                elif event.key == pygame.K_KP_ENTER:
                    pygame.quit()
        screen.fill((135, 206, 235))
        text = font.render("Press w,a,s,d or arrow keys to move", True, (0, 0, 0))
        screen.blit(text, (400 - text.get_width() // 2, 300 - text.get_height() // 2))
        pygame.display.flip()



while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    player_x , player_y, velocity = movement(player_x, player_y, velocity)     
    screen.blit(image, (player_x, player_y))
    pygame.display.flip()  
    screen.fill((135, 206, 235))
    clock.tick(60)
    player_rect = image.get_rect(topleft=(player_x, player_y))
    if velocity[0] + velocity[1] < 20:
        pass
    
    if show_tutorial:
        if step == 1:
            pygame.draw.rect(screen, (220, 50, 50), goal_rect)
        text = font.render(tutorial_steps[step], True, (0, 0, 0))
        screen.blit(text, (400 - text.get_width() // 2, 40))
        if player_rect.colliderect(goal_rect):
                step += 1
        

            
    screen.fill((135, 206, 235))
    clock.tick(60)
pygame.quit()

