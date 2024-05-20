import pygame
from random import randint
import time
 
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Coin Hunt")
 
#Images
monster_png = pygame.image.load("hirvio.png")
robo_png = pygame.image.load("robo.png")
coin_png = pygame.image.load("kolikko.png")
 
#Texts
game_font = pygame.font.SysFont(None, 26)
points = 0
score_text = game_font.render(f"Points: {points}", True, (0, 0, 0))
lives = 3
lives_text = game_font.render(f"Lives: {lives}", True, (0, 0, 0))
boost = game_font.render(f"[1]10 Speed-boost(20s)", True, (0, 0, 0))
invincibility = game_font.render(f"[2]15 Invincibility(15s)", True, (0, 0, 0))
extra_life = game_font.render(f"[3]25 1+Life", True, (0, 0, 0))
 
#Variables
robo_x = (640 / 2) - robo_png.get_width()
robo_y = (480 - robo_png.get_width()) / 2  
coin_x = 640 / 2
coin_y = 480 / 2
total_coins = 0
player_speed = 2.3
 
is_invincible = False
right = False
left = False
up = False
down = False
game_started = False
timer_activated = False
timer_time = None
 
enemies = []
game_started_time = pygame.time.get_ticks()
 
clock = pygame.time.Clock()
 
class Monster:
    def __init__(self, side: int):
        self.x = 0
        self.y = 0
        self.side = side
    
    #Randomly chooses which corner the enemy starts from 
    def initialize(self): 
        if self.side == 0:
            self.x = randint(0, 640 - monster_png.get_width())
            self.y = 0 - monster_png.get_height()
        elif self.side == 1:
            self.x = 640  
            self.y = randint(0, 480 - monster_png.get_height())
        elif self.side == 2:
            self.x = randint(0, 640)
            self.y = 480  
        elif self.side == 3:
            self.x = 0 - monster_png.get_width() 
            self.y = randint(0, 480 - monster_png.get_height())
                    
    def move(self):
        if self.side == 0:
            self.y += 2  
        elif self.side == 1:
            self.x += -2
        elif self.side == 2:
            self.y += -2  
        elif self.side == 3:
            self.x += 2
        screen.blit(monster_png, (self.x, self.y))
        
#Timer to reset the upgrades   
def timer(time_to_wait: int):
    start_time = time.time()
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= time_to_wait:
            return True  
        yield 
 
#Start loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game_started = True
                break
 
    screen.fill((204, 255, 229))
    start_font = pygame.font.SysFont(None, 36)
    title = start_font.render("Coin Hunt", True, (0, 0, 0))
    start_text = start_font.render("Press ENTER to start", True, (0, 0, 0))
    screen.blit(title, (250, 100))
    screen.blit(start_text, (200, 200))
 
    pygame.display.flip()
 
    clock = pygame.time.Clock()
    clock.tick(60)
 
    if game_started:
        break
            
#Game loop    
while game_started:
    for event in pygame.event.get():
        #Allow movement with arrow keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and robo_x > 0:
                left = True
            if event.key == pygame.K_RIGHT and robo_x+robo_png.get_width() < 640:
                right = True
 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left = False
            if event.key == pygame.K_RIGHT:
                right = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and robo_y > 0:
                up = True
            if event.key == pygame.K_DOWN and robo_y+robo_png.get_height() < 480:
                down = True
 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                up = False
            if event.key == pygame.K_DOWN:
                down = False
        
        #Allow movement with WASD          
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and robo_x > 0:
                left = True
            if event.key == pygame.K_d and robo_x+robo_png.get_width() < 640:
                right = True
 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_d:
                right = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and robo_y > 0:
                up = True
            if event.key == pygame.K_s and robo_y+robo_png.get_height() < 480:
                down = True
 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                up = False
            if event.key == pygame.K_s:
                down = False
 
        #Manages the upgrades
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 and points >= 10:
                timer_time = timer(15)
                timer_activated = True
                points -= 10
                boost = game_font.render(f"[1]10 speed-boost(20s)", True, (0, 255, 0))
                player_speed = 5
            if event.key == pygame.K_2 and points >=15:
                timer_time = timer(15)
                timer_activated = True
                points -= 15
                is_invincible = True
                invincibility = game_font.render(f"[2]15 Invincibility(15s)", True, (0, 255, 0))       
            if event.key == pygame.K_3 and points >= 25 and lives < 3: 
                timer_time = timer(1)
                timer_activated = True
                points -= 25
                lives += 1
                lives_text = game_font.render(f"Lives: {lives}", True, (0, 0, 0))
                extra_life = game_font.render(f"[3]25 1+Life", True, (0, 255, 0))
                
 
        if event.type == pygame.QUIT:
            exit()
    
    #Activates the upgrades for a limited time        
    if timer_activated:
        try:
            next(timer_time)  
        except StopIteration:
            player_speed = 2.3
            is_invincible = False
            timer_activated = False
            score_text = game_font.render(f"Points: {points}", True, (0, 0, 0))
            boost = game_font.render(f"[1]10 Speed-boost(20s)", True, (0, 0, 0))
            invincibility = game_font.render(f"[2]15 Invincibility(15s)", True, (0, 0, 0))
            extra_life = game_font.render(f"[3]25 1+Life", True, (0, 0, 0))
            lives_text = game_font.render(f"Lives: {lives}", True, (0, 0, 0))
                      
    #Moves the player
    if right:
        robo_x += player_speed
    if left:
        robo_x -= player_speed
    if up:
        robo_y -= player_speed
    if down:
        robo_y += player_speed
    
    #Keep player within bounds  
    if robo_y+robo_png.get_height() >= 480:
       down = False
    if robo_y <= 0:
       up = False
    if robo_x+robo_png.get_width() >= 640:
        right = False
    if robo_x <= 0:
        left = False
    
    #Instantiating new enemies
    if randint(0, 100) < 1:
        side = randint(0, 3)
        hirvio_testi = Monster(side)
        hirvio_testi.initialize()
        enemies.append(hirvio_testi)
            
   #Checks if player is touching the coin
    robo_rect = pygame.Rect(robo_x, robo_y, robo_png.get_width(), robo_png.get_height())
    coin_rect = pygame.Rect(coin_x, coin_y, coin_png.get_width(), coin_png.get_height())
    if robo_rect.colliderect(coin_rect):
        coin_x = randint(0, 640 - coin_png.get_width())
        coin_y = randint(0, 480 - coin_png.get_height())
        points += 1
        total_coins += 1
        score_text = game_font.render(f"Points: {points}", True, (0, 0, 0))
      
    #Draw on screen
    screen.fill((204, 255, 229))
    screen.blit(robo_png, (robo_x, robo_y))
    screen.blit(coin_png, (coin_x, coin_y))
    screen.blit(score_text, (550, 10))
    screen.blit(lives_text, (0, 10))
    screen.blit(boost, (0, 440))
    screen.blit(invincibility, (640 // 2 - invincibility.get_width() // 2, 440))
    screen.blit(extra_life, (640 - extra_life.get_width(), 440)) 
    
    #Counts played time in seconds
    game_time = (pygame.time.get_ticks() - game_started_time) / 1000
    
    #Moves monsters and checks if they hit the player or if the player is in an invincible state
    for enemy in enemies:
        enemy.move()
        hirvio_rect = pygame.Rect(enemy.x, enemy.y, monster_png.get_width(), monster_png.get_height())
        if robo_rect.colliderect(hirvio_rect):
            if not is_invincible:
                lives -= 1
                timer_time = timer(3)
                timer_activated = True
                lives_text = game_font.render(f"Lives: {lives}", True, (255, 0, 0))
                
            enemies.remove(enemy)
            break
    
    #Game ends if lives go below 1      
    if lives <= 0:
        game_ended = True
        game_started = False
        
   #Updates the list to remove monsters that are off the screen
    enemies = [enemy for enemy in enemies if 0 - monster_png.get_width() <= enemy.x <= 640 and 0 - monster_png.get_height() <= enemy.y <= 480]
 
    pygame.display.flip()
 
    clock.tick(60)
    
#End screen loop
while game_ended:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                break
    
    screen.fill((204, 255, 229))
    end_font = pygame.font.SysFont(None, 36)
    title = end_font.render("Game Over", True, (0, 0, 0))
    total_score = end_font.render(f"Coins collected {total_coins}", True, (0, 0, 0))
    text = end_font.render(f"Time survived {round(game_time, 1)} s", True, (0, 0, 0))
    screen.blit(title, (250, 100))
    screen.blit(total_score, (220, 200))
    screen.blit(text, (210, 300))
 
    pygame.display.flip()
 
    clock = pygame.time.Clock()
    clock.tick(60)
 
   
pygame.quit()
    