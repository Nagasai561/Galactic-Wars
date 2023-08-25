import pygame
import math
import sys
import random

#constants
screen_size = 5
screen_width, screen_height = 250*screen_size, 150*screen_size
spaceship_width, spaceship_height = screen_width//9, screen_height//9
spaceship_velocity = screen_width//50
monster_width, monster_height = screen_width//12, screen_height//9
monster_velocity = screen_width//120
bullet_width, bullet_height = screen_width//15, screen_height//100
bullet_velocity = screen_width//15


#init
pygame.init()
pygame.display.set_caption("Galactic wars")


#screen 
screen = pygame.display.set_mode((screen_width, screen_height))

#other essentials
clock = pygame.time.Clock()
run = True
score = 0
is_gameover = False
is_start_menu = True
level = "none"
reason = "none"
monster_level = ["Assets/space_monster_blue.png", "Assets/space_monster_green.png", "Assets/space_monster_red.png"]
monster_health = [1,2,3]



#assets and objects
space = pygame.transform.scale(pygame.image.load("Assets/space.png"), (screen_width, screen_height))
start_menu_bg = pygame.Surface((screen_width, screen_height))
start_menu_bg.fill((0,0,0))
hurt_sound = pygame.mixer.Sound("Assets/hurt_sound.wav")
bullet_sound = pygame.mixer.Sound("Assets/bullet_sound.wav")

spaceships = pygame.sprite.Group()
class spaceship(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Assets/spaceship.png"), (spaceship_width, spaceship_height)), 270)
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        global is_gameover, reason
        keys_pressed = pygame.key.get_pressed()
        if(keys_pressed[pygame.K_UP]):
            self.rect.y -= spaceship_velocity
            if(self.rect.bottom < 0):
                self.rect.top = screen_height
        if(keys_pressed[pygame.K_DOWN]):
            self.rect.y += spaceship_velocity
            if(self.rect.top > screen_height):
                self.rect.bottom = 0
        if(keys_pressed[pygame.K_LEFT]):
            self.rect.left -= spaceship_velocity
            if(self.rect.right < 0):
                self.rect.left = screen_width
        if(keys_pressed[pygame.K_RIGHT]):
            self.rect.right += spaceship_velocity
            if(self.rect.left > screen_width):
                self.rect.right = 0 

        for bullet in bullets:
            if(self.rect.colliderect(bullet)):
                if(pygame.sprite.spritecollide(bullet, spaceships, False, pygame.sprite.collide_mask)):
                    if(bullet.rect.center[0] <= self.rect.center[0]):
                        is_gameover = True
                        reason = "You have been hit by bullet"
            
        

monsters = pygame.sprite.Group()
class monster(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        if(level == "easy"):
           self.monster_type = 0
        elif(level == "medium"):
            self.monster_type = random.randint(0,1)
        else:
            self.monster_type = random.randint(0,2)

        self.image = pygame.transform.scale(pygame.image.load(monster_level[self.monster_type]), (monster_width, monster_height))
        self.health = monster_health[self.monster_type]

        

        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        global score

        if(level == "easy"):
            self.rect.x -= monster_velocity
        elif(level == "normal"):
            self.rect.x -= monster_velocity*1.2
        else:
            self.rect.x -= monster_velocity*1.2

        for bullet in bullets:
            if(self.rect.colliderect(bullet.rect)):
                self.health -= 1
                if(self.health <= 0):
                    score += self.monster_type+1          
                    self.kill()
                    hurt_sound.play()
                  

                bullet.kill()
        
        global is_gameover, current_time, reason

        if pygame.sprite.spritecollide(self, spaceships, False, pygame.sprite.collide_mask):
            is_gameover = True
            reason = "Monster has caught you"
        if(self.rect.right < 0):
            is_gameover = True
            reason = "Monster has reached the end"
        if(is_gameover):
            current_time = pygame.time.get_ticks()
        
        if level == "easy":
            if not monsters:
                new_monster = monster((random.randint((screen_width*3)//4, screen_width-monster_width//2), random.randint(monster_height//2, screen_height - monster_height//2)))
                monsters.add(new_monster)
        elif level == "medium":
            if len(monsters) < 2:
                new_monster = monster((random.randint((screen_width*3)//4, screen_width-monster_width//2), random.randint(monster_height//2, screen_height - monster_height//2)))   
                monsters.add(new_monster)
        else:
            if len(monsters) < 3:
                new_monster = monster((random.randint((screen_width*3)//4, screen_width-monster_width//2), random.randint(monster_height//2, screen_height - monster_height//2)))   
                monsters.add(new_monster)


    

bullets = pygame.sprite.Group()
class bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((bullet_width, bullet_height))
        self.rect = self.image.get_rect(center = pos)
        self.image.fill("Red")
        self.wrap_count = 0
    
    def update(self):
        if(level == "easy"):
            if(self.rect.left > screen_width):
                self.kill()
            else:
                self.rect.x += bullet_velocity
        elif(level == "medium"):
            self.rect.x += bullet_velocity
            if((self.rect.left > screen_width)):
                self.rect.right = 0
                self.wrap_count += 1
            if(self.wrap_count > 1):
                self.kill()
        else:
            self.rect.x += bullet_velocity
            if(self.rect.left > screen_width):
                self.rect.right = 0
                self.wrap_count += 1
            if(self.wrap_count > 2):
                self.kill()

            

    

class text: #(string, center_pos, color_bg, color_in, font)
    def __init__(self, string, center_pos, color_text, font):
        self.text_surf = font.render(string, False, color_text)
        self.rect = self.text_surf.get_rect(center=center_pos)
        self.bg_surf = pygame.Surface(self.text_surf.get_size())
    def draw_text(self):
        screen.blit(self.bg_surf, self.rect)
        screen.blit(self.text_surf, self.rect)


#textual part
font_big = pygame.font.SysFont("Comic Sans MS", math.floor(screen_height/7))
font_small = pygame.font.SysFont("Comic Sans MS", math.floor(screen_height/11))
easy_text = text("Easy", (screen_width*(3/16), screen_height*(3/4)), (0, 255, 42), font_small)
medium_text = text("Medium", (screen_width*(8/16), screen_height*(3/4)),  (0, 255, 42), font_small)
hard_text = text("Hard", (screen_width*(13/16), screen_height*(3/4)),  (0, 255, 42), font_small)
galactic_war_text = text("Galactic Wars", (screen_width/2,screen_height/3),  (0,255,42), font_big)
gameover_text = text("Game Over", (screen_width/2, screen_height*(3/22)),  (255,0,0), font_big)
reset_text = text("Reset", (screen_width*(1/2), screen_height*(39/44)), (0,255,0), font_small)


#--------------------functions--------------------------

def draw_stuff():
    screen.blit(space, (0, 0))
    score_while_running = text(f"Score: {score}", (screen_width*(17/20), screen_height/15), (255,255,255), font_small)
    score_while_running.draw_text()
    spaceships.draw(screen)
    monsters.draw(screen)
    bullets.draw(screen)
    pygame.display.update()

def update_stuff():
    spaceships.update()
    monsters.update()
    bullets.update()



def shoot_bullet():
    new_bullet = bullet(player_ship.rect.midright)
    bullets.add(new_bullet)
    bullet_sound.play()

def gameover():
    global score
    screen.blit(start_menu_bg, (0,0))
    gameover_text.draw_text()
    reason_text = text(reason, (screen_width/2, screen_height*(15/44)), (255,0,0), font_small)
    reason_text.draw_text()
    level_text = text(f"Level: {level}", (screen_width/2, screen_height*(23/44)), (255,255,0), font_small)
    level_text.draw_text()
    score_text = text(f"Score is: {score}", (screen_width/2, screen_height*(31/44)), (0,255,255), font_big)
    score_text.draw_text()
    reset_text.draw_text()
    pygame.display.update()

def start_menu():
    global is_start_menu, score
    score = 0

    screen.blit(start_menu_bg, (0,0))
    galactic_war_text.draw_text()
    easy_text.draw_text()
    medium_text.draw_text()
    hard_text.draw_text()
    pygame.display.update()

    if(level != "none"):
        is_start_menu = False

#while loop
while run:
    clock.tick(30)
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.quit()
            sys.exit()

        if(is_start_menu):
            if(event.type == pygame.MOUSEBUTTONUP):
                if(easy_text.rect.collidepoint(pygame.mouse.get_pos())):
                    level = "easy"
                elif(medium_text.rect.collidepoint(pygame.mouse.get_pos())):
                    level = "medium"
                elif(hard_text.rect.collidepoint(pygame.mouse.get_pos())):
                    level = "hard"

                player_ship = spaceship((spaceship_width//2, screen_height//2))
                spaceships.add(player_ship)

                new_monster = monster((random.randint(screen_width//2, screen_width-monster_width//2), random.randint(monster_height//2, screen_height - monster_height//2)))
                monsters.add(new_monster) 

        if(is_gameover):
            if(event.type == pygame.MOUSEBUTTONUP):
                if(reset_text.rect.collidepoint(pygame.mouse.get_pos())):
                    is_gameover = False
                    is_start_menu = True
                    level = "none"
                    monsters.empty()
                    bullets.empty()
                    spaceships.empty()

        if((not is_start_menu) and (not is_gameover)):
            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_SPACE):
                    shoot_bullet()
    
    if is_start_menu:
        start_menu()
    elif is_gameover:
        gameover()
    else:
        update_stuff()
        draw_stuff()


    




