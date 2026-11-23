#game premise: a game where u dodge obsticles
#THING TO FIX!!#
#music for title screen and game start sound effects
#better title screen
#make faces on blocks
#give a death screen 
#make game harder over time 
#make a indicator warning on side on
# it changes bg?
count_down = 0

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
tutorial_steps = ["Press w,a,s,d or arrow keys to move move in the red box!", "oh ya! you cant go slow, Stay fast for {} seconds", "dodge the obstacles good luck!"]
step = 1
coin_image = pygame.image.load("kenney_shape-characters/PNG/Default/tile_coin.png")
countdown_sound = pygame.mixer.Sound("lesiakower-countdown-sound-effect-8-bit-151797.mp3")
projectile_image = pygame.image.load("kenney_shape-characters/PNG/Default/red_body_circle.png")
coin_pickup_sound = pygame.mixer.Sound("coin.wav")
bg_sound = pygame.mixer.Sound("freesound_community-8-bit-heaven-26287.mp3")
bg_sound.play(-1)
slow_Since = None
Fast = None
font = pygame.font.Font(None, 36)
player_x = 100
player_y = 100
velocity = [0,0]
speed = 0.2
goal_rect = pygame.Rect(600, 400, 60, 60)
show_tutorial = True
running = True
score = 0
p_speed = 5
spawn_projectile = 0
p_x = 100
p_y = 100
projectiles = []
coins = []
spawn_coin = 0
tutorial_timer =0
time_survived = 0

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
        spawn_coin = now + random.randint(3000,10000)
    for i in coins[:]:
        if player_rect.colliderect(i):
            coins.remove(i)
            score += 1
            coin_pickup_sound.play()
    return spawn_coin, score

def draw_coins(coins, score):
    for c in coins:
        screen.blit(coin_image, c)
    screen.blit(coin_image,(750,555))
    screen.blit(font.render(f'you have {score}x         coins!',True,(0,0,0)),(650,530))   #lowk idk why i did this couldve just done score_text then blit that but whatever

class projectile():
    def __init__(self,p_x,p_y,p_speed):
        self.image = pygame.image.load("kenney_shape-characters/PNG/Default/red_body_circle.png")
        p_y = random.randint(0,600)
        p_x = 0
        self.rect = self.image.get_rect(center=(p_x,p_y))
        self.speed = p_speed 
    def update(self):
        self.rect.x += p_speed + random.randint(0,4)
    def draw(self):
        screen.blit(self.image,self.rect)
    def collision(self,player_rect):
        if self.rect.colliderect(player_rect):
            pygame.quit()
def survival_timer():
    text = font.render(f"You have survived for {time_survived//60} seconds", True, (0, 0, 0))
    screen.blit(text, (400 - text.get_width() // 2, 500))
    
running = title_screen()
while running == True:
    
    now = pygame.time.get_ticks()
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
    

    if step != 1 and step != 3:
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
            remaining = max(0, 3 - count_down)
            message = tutorial_steps[1].format(f"{remaining:.1f}")
            text = font.render(message, True, (0, 0, 0))
            screen.blit(text, (400 - text.get_width() // 2, 40))
            if slow_Since == None:
                count_down += 1/60
                if round(count_down) == 3:
                    step = 3
            else:
                count_down = 0
                

        elif step == 3:
            if tutorial_timer == 0:
                countdown_sound.play()
                text = font.render(tutorial_steps[step-1],True,(0,0,0))
                screen.blit(text, (400 - text.get_width() // 2, 40))
                player_x = 400
                player_y = 300
                tutorial_timer = now + 3100
            text = font.render("okay watch out better dodge! the game is starting!",True,(0,0,0))
            screen.blit(text, (400 - text.get_width() // 2, 40))
            screen.blit(image, (player_x, player_y))
            slow_Since = None
     
            velocity = [0,0]
                    
            if now >= tutorial_timer:
                projectiles.append(projectile(p_x,p_y,p_speed))
                tutorial_timer = now + 1000
                step = 4
        elif step == 4:
            slow_Since = None
            show_tutorial = False

    if not show_tutorial:
        time_survived += 1
        spawn_coin,score = update_coins(coin_image,now,player_rect,score,spawn_coin)
        draw_coins(coins, score)
        survival_timer()
        if now >= spawn_projectile:
                
            projectiles.append(projectile(p_y, p_x ,p_speed))
            spawn_projectile = now + random.randint(1000,3000)
    for i in projectiles:        
        i.update()
        i.draw()
        i.collision(player_rect)
    pygame.display.flip()  
    clock.tick(60)
pygame.quit()

