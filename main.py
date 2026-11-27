#game premise: a game where u dodge obsticles
#THING TO FIX!!#
#it changes bg?  
#work on read me 
# make it load on a browser

count_down = 0
print("hello, world")
import sys
import pygame
from pygame.transform import flip
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
import random
number = random.randint(0, 4)
different_blocks = ["yellow_body_square.png", "blue_body_square.png", "green_body_square.png", "red_body_square.png", 
                    "purple_body_square.png"]
face_number = random.randint(0,10)
different_faces = ["a","b","c","d","e","f","g","h","i","k","l"]
faces = pygame.image.load(f"kenney_shape-characters/PNG/Default/face_{different_faces[face_number]}.png")
image = pygame.image.load(f"kenney_shape-characters/PNG/Default/{different_blocks[number]}")
tutorial_steps = ["Press w,a,s,d or arrow keys to move move in the red box!", "oh ya! you cant go slow, Stay fast for {} seconds", "dodge the obstacles good luck!"]
step = 1
coin_image = pygame.image.load("kenney_shape-characters/PNG/Default/tile_coin.png")
countdown_sound = pygame.mixer.Sound("lesiakower-countdown-sound-effect-8-bit-151797.mp3")
projectile_image = pygame.image.load("kenney_shape-characters/PNG/Default/red_body_circle.png")
bomb_image = pygame.image.load("floating_mine.png")
coin_pickup_sound = pygame.mixer.Sound("coin.wav")
og_bomb_image = pygame.image.load("floating_mine.png")
bomb_image = pygame.transform.scale(og_bomb_image,(100,100))
pygame.mixer.music.load("freesound_community-8-bit-heaven-26287.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)
death_sound = pygame.mixer.Sound("lesiakower-8-bit-game-over-sound-effect-331435.mp3")
game_start_sound = pygame.mixer.Sound("freesound_community-game-start-6104.mp3")
tutorial_timer =0
og_warning_image = pygame.image.load("Arrow 0.png")
warning_image = pygame.transform.scale(og_warning_image,(40,40))
font = pygame.font.Font(None, 36)
goal_rect = pygame.Rect(600, 400, 60, 60)
og_bg = pygame.image.load("sky.jpg")
bg = pygame.transform.scale(og_bg,(800,600))
projectiles = []
coins = []
bombs = []
slow_Since = None
Fast = None


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
def title_screen(bg):
    global running
    
    running = True
    start_button = pygame.image.load("start_button.JPEG") 
    start_rect = start_button.get_rect(center=(400,450))
    while running == True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return running
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return running
                elif event.key == pygame.K_KP_ENTER:
                    running = True
                    game_start_sound.play()
                    return running
                elif event.key == pygame.K_RETURN:
                    running = True
                    game_start_sound.play()
                    return running
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(mouse_pos):
                    running = True
                    game_start_sound.play()
                    return running
        
        screen.fill((135, 206, 235))
        screen.blit(bg,(0,0)) 
        font = pygame.font.Font("PressStart2P-Regular.ttf", 17)
        text = font.render("Press Enter or click to start!", True, (0, 0, 0))
        screen.blit(text, (400 - text.get_width() // 2, 300 - text.get_height() // 2))
        font = pygame.font.Font("PressStart2P-Regular.ttf", 67)
        text = font.render("DODGE BALLS", True, (0, 0, 0))
        screen.blit(text, (400 - text.get_width() // 2, 100 - text.get_height() // 2))
        screen.blit(start_button,start_rect)
        font = pygame.font.Font(None, 36)
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

def survival_timer():
    text = font.render(f"You have survived for {time_survived//60} seconds", True, (0, 0, 0))
    screen.blit(text, (400 - text.get_width() // 2, 500))

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
    def __init__(self,p_speed):
        self.image = pygame.image.load("kenney_shape-characters/PNG/Default/red_body_circle.png")
        p_speed = level_loader(time_survived,p_speed,random_x)
       
        self.speed_x = 0
        self.speed_y = 0
        sides = ["right","left","top","down"]
        side_number = random.randint(0,3)
        self.sides = sides[side_number]
        if self.sides == "right":
            self.speed_x = -p_speed
            self.rect = self.image.get_rect(center=(1000,random.randint(30,570)))
        elif self.sides == "left":
            self.speed_x = p_speed
            self.rect = self.image.get_rect(center=(-200,random.randint(30,570)))
        elif self.sides == "top":
            self.speed_y = -p_speed
            self.rect = self.image.get_rect(center=(random.randint(30,770),800))
        elif self.sides == "down":
            self.speed_y = p_speed
            self.rect = self.image.get_rect(center=(random.randint(30,770),-200))
        



    def update(self,random_x):
        random_speed = random.randint(0,random_x)
        if self.speed_x != 0:
            if self.speed_x < 0:
                self.rect.x += self.speed_x - random_speed
            else:
                self.rect.x += self.speed_x + random_speed
     
        if self.speed_y != 0:
            if self.speed_y  <0:
                self.rect.y += self.speed_y - random_speed
            else:
                self.rect.y +=self.speed_y + random_speed
          
    def draw(self,warning_image):
       
        if self.rect.x >800 and self.sides == "right":
            warn_rect = warning_image.get_rect(center=(750,self.rect.centery))
            flip_warning_image = flip(warning_image,True,False)
            screen.blit(flip_warning_image,warn_rect)
        elif self.rect.x <0 and self.sides == "left":
            warn_rect = warning_image.get_rect(center=(50,self.rect.centery))
            screen.blit(warning_image,warn_rect)
        elif self.rect.y > 600 and self.sides == "top":
            warn_rect = warning_image.get_rect(center=(self.rect.centerx,550))
            flip_warning_image = pygame.transform.rotate(warning_image,90)  
            screen.blit(flip_warning_image,warn_rect)
        elif self.rect.y < 0 and self.sides == "down":
            warn_rect = warning_image.get_rect(center=(self.rect.centerx,20))
            flip_warning_image = pygame.transform.rotate(warning_image,270)  
            screen.blit(flip_warning_image,warn_rect) 
        else:
            screen.blit(self.image,self.rect)
    def collision(self,player_rect,show_tutorial):
        if self.rect.colliderect(player_rect):
            show_tutorial = death_screen(show_tutorial,death_slow,score)
    def off_screen(self):
        if self.rect.x < -250 or self.rect.x > 1050 or self.rect.y < -250 or self.rect.y > 850:
            return True
        else:
            return False

def bomb_spawner(now,spawn_bomb,bombs):
    if not show_tutorial:
        if now >= spawn_bomb + random.randint(3000,5000):
            bomb_x = random.randint(0,800)
            bomb_y = random.randint(0,600)
            bomb_rect = bomb_image.get_rect(center=(bomb_x,bomb_y))
            bombs.append({
                "rect" : bomb_rect,
                "explode_time" : now + 3000
                })
            spawn_bomb = now
    return spawn_bomb
  
       
def bomb_explode(now,bombs,projectiles):
    directions = [(5,0,"left"), (-5,0,"right"),(0,5,"down"),(0,-5,"top")]
    for b in bombs[:]:

        if now > b["explode_time"]:
            for velocity_x , velocity_y, side_dir in directions:
                p = projectile(p_speed)
                p.rect.center = b["rect"].center
                p.speed_x = velocity_x
                p.speed_y = velocity_y
                projectiles.append(p)
                p.sides = side_dir
            bombs.remove(b)
      
        
def draw_bomb_explosion(bombs):
    for bomb in bombs:
        screen.blit(bomb_image , bomb["rect"])
        
    
def survival_timer():
    text = font.render(f"You have survived for {time_survived//60} seconds", True, (0, 0, 0))
    screen.blit(text, (400 - text.get_width() // 2, 500))

    
def reset_stuff():
    global player_x,player_y,bomb_x,random_x,bomb_y,game_start_time,death_slow,slow_Since,count_down,tutorial_timer,explode_bomb,spawn_bomb,velocity,speed,show_tutorial,running,score,p_speed,spawn_projectile,p_x,p_y,spawn_coin,level,time_survived
    player_x = 400
    player_y = 300
    velocity = [0,0]
    speed = 0.2
    show_tutorial = True
    running = True
    score = 0
    game_start_time = pygame.time.get_ticks()
    p_speed = 3
    spawn_bomb = 0
    explode_bomb = 0
    spawn_projectile = 0
    bomb_x = 0 
    bomb_y = 0
    slow_Since = None
    count_down = 0
    tutorial_timer = 0
    p_x = 400
    random_x = 3
    p_y = 350
    spawn_coin = 0
    death_slow = False
    time_survived = 0
    level = 1
    bombs.clear()
    projectiles.clear()
    coins.clear()
def level_loader(time_survived,p_speed,random_x):
    p_speed = p_speed + time_survived //300
    random_x = 3 + time_survived// 600
    return p_speed
    return random_x
  
def death_animations(velocity,image,faces):
    projectiles.clear()
    coins.clear()
    fall_speed = 18
  
    for i in range (160):
        
        screen.fill((135,206,235))
        player_y = player_rect.y
        spinning_sprite = pygame.transform.rotate(image,i *4)
        spinning_face = pygame.transform.rotate(faces,i*4)  
        
        if i >= 28 and i < 100:
            fall_speed = 0
            faces = pygame.image.load(f"kenney_shape-characters/PNG/Default/face_j.png")
            spinning_sprite = pygame.transform.rotate(image, i*3)
            spinning_face = pygame.transform.rotate(faces,i*3)  
        if i == 34:
            fall_speed = -2
        screen.blit(spinning_sprite,player_rect)
        screen.blit(spinning_face, (player_x+13, player_y+20))
        fall_speed -= 0.9
        player_y -= fall_speed
        player_rect.y -= fall_speed


        pygame.display.flip()
        clock.tick(60)
       
        
        

def death_screen(show_tutorial,death_slow,score):
    run = True
   
    death_sound.play()
    death_animations(velocity,image,faces)
    while run == True:
        screen.fill((0,0,0))
        font = pygame.font.Font(None,36)
        text = font.render(f"you collected {score} coins", True, (255,255,255))
        screen.blit(text, (400 - text.get_width() // 2, 550))

    
        font = pygame.font.Font("PressStart2P-Regular.ttf",54) 
        text = font.render(f"YOU DIED", True, (255,0,0))
        screen.blit(text, (400 - text.get_width() // 2, 100))
        
        font = pygame.font.Font(None, 30)
        text = font.render("would u like to try again? Press space to" 
        " try again press esc to quit...",True, (255,255,255))
        screen.blit(text, (400 - text.get_width() // 2, 300))

        font = pygame.font.Font(None, 36)
        text = font.render(f"You have survived for {time_survived//60} seconds", True, (255,255,255))
        screen.blit(text, (400 - text.get_width() // 2, 500))
        
        if death_slow == True:
            text = font.render(f"you were moving too slow...", True, (255,255,255))
            screen.blit(text, (400 - text.get_width() // 2, 400))
         
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
              
                elif event.key == pygame.K_SPACE:
                    show_tutorial = False
                    reset_stuff()
                    run = False

        pygame.display.flip()

reset_stuff()
running = title_screen(bg)
while running == True:
    
    now = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    screen.fill((136,205,235))                                        # order was wrong it has to be fill blit then everything else in then flip thentick 
    player_x , player_y, velocity = movement(player_x, player_y, velocity)     
    screen.blit(image, (player_x, player_y))
    screen.blit(faces, (player_x+15, player_y+15))
    total_velocity = abs(velocity[0]) + abs(velocity[1])
    

    if step != 1 and step != 3:
        game_over, slow_Since = check_velocity(slow_Since, total_velocity)
        if game_over == True:
            death_slow = True
            death_screen(show_tutorial,death_slow,score)
            continue
      
           
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
            screen.blit(faces, (player_x+15, player_y+15))
            slow_Since = None
     
            velocity = [0,0]
                    
            if now >= tutorial_timer:
                projectiles.append(projectile(p_speed))
                tutorial_timer = now + 1000
                step = 4
                game_start_time = now
            
        elif step == 4:
            slow_Since = None
            show_tutorial = False
        

    if not show_tutorial:
        time_survived += 1
       
        spawn_coin,score = update_coins(coin_image,now,player_rect,score,spawn_coin)
        draw_coins(coins, score)
        survival_timer()
        if now >= spawn_projectile: 
            projectiles.append(projectile(p_speed))
            spawn_projectile = now + random.randint(1000,3000)
    for i in projectiles[:]:        
        i.update(random_x)
        i.draw(warning_image)
        i.collision(player_rect,show_tutorial)
        if i.off_screen():
            projectiles.remove(i)
    if now - game_start_time >= 10000:
        spawn_bomb = bomb_spawner(now,spawn_bomb,bombs)
        bomb_explode(now,bombs,projectiles)
        draw_bomb_explosion(bombs)
    elif not show_tutorial:
        text = font.render("bombs will spawn after 10 seconds..",True,(0,0,0))
        screen.blit(text, (400 - text.get_width() // 2, 40))

    pygame.display.flip()  
    clock.tick(60)
pygame.quit()

