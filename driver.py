import pygame
import math
import sys
import random

#constants
screen_width, screen_height = 1500, 1000
spaceship_width, spaceship_height = 150, 150
spaceship_velocity = 20
monster_width, monster_height = 100, 100
monster_velocity = 7
bullet_width, bullet_height = 100,10
bullet_velocity = 40


#init
pygame.init()
pygame.display.set_caption("Galactic wars")


#screen 
screen = pygame.display.set_mode((screen_width, screen_height))

#other essentials
clock = pygame.time.Clock()
run = True
score = 0
started_time = 0
current_time = 0
is_gameover = False
is_start_menu = True
level = "none"



#assets and objects
space = pygame.transform.scale(pygame.image.load("Assets/space.jpeg"), (screen_width, screen_height))
start_menu_bg = pygame.Surface((screen_width, screen_height))
start_menu_bg.fill((0,0,0))

spaceships = pygame.sprite.Group()
class spaceship(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Assets/spaceship.png"), (spaceship_width, spaceship_height)), 270)
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        global is_gameover
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
                        print("You have been hit by a bullet")
            
        
        
             
player_ship = spaceship((spaceship_width/2, screen_height/2))
spaceships.add(player_ship)

    

monsters = pygame.sprite.Group()
class monster(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("Assets/space_monster.png"), (monster_width, monster_height))
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        if(level == "easy"):
            self.rect.x -= monster_velocity
        elif(level == "normal"):
            self.rect.x -= monster_velocity*1.3
        else:
            self.rect.x -= monster_velocity*1.3

        for bullet in bullets:
            if(self.rect.colliderect(bullet.rect)):
                self.kill()
                bullet.kill()
        
        global is_gameover, current_time
        # if(self.rect.colliderect(player_ship.rect)):
        #     is_gameover = True
        #     print("Monster has caught you")
        if pygame.sprite.spritecollide(self, spaceships, False, pygame.sprite.collide_mask):
            is_gameover = True
            print("Monster has caught you")
        if(self.rect.right < 0):
            is_gameover = True
            print("Monster has reached the end")
        if(is_gameover):
            current_time = pygame.time.get_ticks()
        
        if level == "easy":
            if not monsters:
                new_monster = monster((random.randint(screen_width/2, screen_width-monster_width/2), random.randint(monster_height/2, screen_height - monster_height/2)))
                monsters.add(new_monster)
        elif level == "medium":
            if len(monsters) < 2:
                new_monster = monster((random.randint(screen_width/2, screen_width-monster_width/2), random.randint(monster_height/2, screen_height - monster_height/2)))
                monsters.add(new_monster)
        else:
            if len(monsters) < 3:
                new_monster = monster((random.randint(screen_width/2, screen_width-monster_width/2), random.randint(monster_height/2, screen_height - monster_height/2)))
                monsters.add(new_monster)


new_monster = monster((random.randint(screen_width/2, screen_width-monster_width/2), random.randint(monster_height/2, screen_height - monster_height/2)))
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
font_big = pygame.font.SysFont("Comic Sans MS", 180)
font_small = pygame.font.SysFont("Comic Sans MS", 90)
easy_text = text("Easy", (screen_width*(3/16), screen_height*(3/4)), (0, 255, 42), font_small)
medium_text = text("Medium", (screen_width*(8/16), screen_height*(3/4)),  (0, 255, 42), font_small)
hard_text = text("Hard", (screen_width*(13/16), screen_height*(3/4)),  (0, 255, 42), font_small)
galactic_war_text = text("Galactic Wars", (screen_width/2,screen_height/3),  (0,255,42), font_big)
gameover_text = text("Game Over", (screen_width/2, screen_height*(1/5)),  (255,255,255), font_big)
reset_text = text("Reset", (screen_width*(1/2), screen_height*(18/20)), (255,255,255), font_small)



#--------------------functions--------------------------

def draw_stuff():
    screen.blit(space, (0, 0))
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

def gameover():
    screen.blit(start_menu_bg, (0,0))
    gameover_text.draw_text()
    level_text = text(f"Level: {level}", (screen_width/2, screen_height*(2/5)), (255,255,255), font_small)
    level_text.draw_text()
    score_text = text(f"Score is: {math.floor((current_time-started_time)/100)}", (screen_width/2, screen_height*(4/7)), (255,255,255), font_big)
    score_text.draw_text()
    reset_text.draw_text()
    pygame.display.update()

def start_menu():
    global is_start_menu, started_time

    screen.blit(start_menu_bg, (0,0))
    galactic_war_text.draw_text()
    easy_text.draw_text()
    medium_text.draw_text()
    hard_text.draw_text()
    pygame.display.update()

    if(level != "none"):
        is_start_menu = False
        started_time = pygame.time.get_ticks()

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

        if(is_gameover):
            if(event.type == pygame.MOUSEBUTTONUP):
                if(reset_text.rect.collidepoint(pygame.mouse.get_pos())):
                    is_gameover = False
                    is_start_menu = True
                    level = "none"
                    monsters.empty()
                    bullets.empty()
                    player_ship.rect.center = (spaceship_width/2, screen_height/2)
                    new_monster = monster((random.randint(screen_width/2, screen_width-monster_width/2), random.randint(monster_height/2, screen_height - monster_height/2)))
                    monsters.add(new_monster)   

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


    




