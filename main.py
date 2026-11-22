#game premise: a game where u dodge obsticles

#THING TO FIX!!
#the velocity check thing doesnt work, it closes after 10seconds instead of when u go slow
# finish the tutorial
#add a obstacle that shoots pasts the screen and if u touch it u die
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
tutorial_steps = ["Press w,a,s,d or arrow keys to move move in the red box!", "oh ya! you cant go slow", "dodge the obstacles good luck!"]
step = 1
assets = pygame.image.load("kenney_shape-characters/PNG/Default/yellow_body_square.png")
font = pygame.font.Font(None, 36)
player_x = 100
player_y = 100
velocity = [0,0]
speed = 0.2
goal_rect = pygame.Rect(600, 400, 60, 60)
show_tutorial = False
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

title_screen()
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

slow_Since = None

def check_velocity(slow_Since, total_velocity):
    now = pygame.time.get_ticks()               
    if total_velocity < 15:
        if slow_Since is None:
            slow_Since = now                       
        text = font.render("You are going too slow!", True, (0, 0, 0))
        screen.blit(text, (400 - text.get_width() // 2, 10))
        elapsed_time = (now - slow_Since) / 1000   
        if elapsed_time > 10:
            return True, slow_Since
    else:
        slow_Since = None
    return False, slow_Since                      
while running == True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    screen.fill((135, 206, 235))                                          # order was wrong it has to be fill blit then everything else in then flip thentick 
    player_x , player_y, velocity = movement(player_x, player_y, velocity)     
    screen.blit(image, (player_x, player_y))
    total_velocity = abs(velocity[0]) + abs(velocity[1])
    if step != 1 or show_tutorial == False:
        game_over, slow_Since = check_velocity(slow_Since, total_velocity)
        if game_over == True:
            pygame.quit()
    player_rect = image.get_rect(topleft=(player_x, player_y))
    
    if show_tutorial:
        if step == 1:
            pygame.draw.rect(screen, (220, 50, 50), goal_rect)
        text = font.render(tutorial_steps[step - 1], True, (0, 0, 0))
        screen.blit(text, (400 - text.get_width() // 2, 40))
        if player_rect.colliderect(goal_rect):
            step = 2
            if step == 2:
                Fast = False
                text = font.render(tutorial_steps[step - 1], True, (0, 0, 0))
                screen.blit(text, (400 - text.get_width() // 2, 40))
                timer_started = pygame.time.get_ticks()
                if (total_velocity < 100 and step == 2):                 
                    Fast = False
                    start_ticks = pygame.time.get_ticks()
                    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
                    text = font.render("You are going too slow!", True, (0, 0, 0))
                    screen.blit(text, (400 - text.get_width() // 2, 10))
                    if elapsed_time > 10:
                        pygame.quit()
                else:
                    Fast = True
                    while Fast == True:
                        elapsed_time = (pygame.time.get_ticks() - timer_started) / 1000
                    if elapsed_time > 5:
                        step = 3
                        Fast = False
    pygame.display.flip()  
    clock.tick(60)
pygame.quit()

