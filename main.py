#game premise: a game where u dodge obsticles

#THING TO FIX!!
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
coin_image = pygame.image.load("kenney_shape-characters/PNG/Default/tile_coin.png")
slow_Since = None
Fast = None
font = pygame.font.Font(None, 36)
player_x = 100
player_y = 100
velocity = [0,0]
speed = 0.2
goal_rect = pygame.Rect(600, 400, 60, 60)
show_tutorial = False
running = True
score = 0
coins = []
spawn_coin = 0
now = pygame.time.get_ticks()
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


def check_velocity(slow_Since, total_velocity):
    now = pygame.time.get_ticks()               
    if total_velocity < 15:
        if slow_Since is None:
            slow_Since = now                       
        text = font.render("You are going too slow!", True, (0, 0, 0))
        screen.blit(text, (400 - text.get_width() // 2, 10))
        elapsed_time = (now - slow_Since) / 1000   
        if elapsed_time > 3:
            return True, slow_Since
    else:
        slow_Since = None
    return False, slow_Since  


def update_coins(coin_image,now,player_rect,score,spawn_coin):
    
    if now >= spawn_coin:
        coin_x = random.randint(0,800- coin_image.get_width())
        coin_y = random.randint(0,600- coin_image.get_height())
        coins.append(coin_image.get_rect(topleft=(coin_x,coin_y)))
        spawn_coin = now + random.randint(1000,2000)
    for i in coins[:]:
        if player_rect.colliderect(i):
            coins.remove(i)
            score += 1
    return spawn_coin, score

def draw_coins(coins, score):
    for c in coins:
        screen.blit(coin_image, c)
    screen.blit(font.render(f'you have{score} coins!',True,(0,0,0)),(200,100))   #lowk idk why i did this couldve just done score_text then blit that but whatever


class projectile():
    def __init__(self,x,y,speed):
        self.image = pygame.image.load("kenney_shape-characters/PNG/Default/red_body_circle.png")
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = speed
    def update(self):
        self.image.x += speed
    def draw(self):
        screen.blit(self.image,self.rect)
   
running = title_screen()
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
   
    if step != 1 or not show_tutorial :
        game_over, slow_Since = check_velocity(slow_Since, total_velocity)
        if game_over == True:
            running = False
    player_rect = image.get_rect(topleft=(player_x, player_y))
   
    if show_tutorial:
        if step == 1:
            pygame.draw.rect(screen, (220, 50, 50), goal_rect)
            text = font.render(tutorial_steps[step - 1], True, (0, 0, 0))
            screen.blit(text, (400 - text.get_width() // 2, 40))
            if player_rect.colliderect(goal_rect):
                step = 2
        elif step == 2:
            text = font.render(tutorial_steps[step - 1], True, (0, 0, 0))
            screen.blit(text, (400 - text.get_width() // 2, 40))
            if total_velocity > 15:
                if Fast == None:
                    Fast = pygame.time.get_ticks()
                elapsed_time =  now - Fast
                if elapsed_time > 3000:
                    step = 3
            else:
                Fast = None

        elif step == 3:
            text = font.render(tutorial_steps[step-1],True,(0,0,0))
            screen.blit(text, (400 - text.get_width() // 2, 40))

    if not show_tutorial:
        spawn_coin,score = update_coins(coin_image,now,player_rect,score,spawn_coin)
        draw_coins(coins, score)

    pygame.display.flip()  
    clock.tick(60)
pygame.quit()

