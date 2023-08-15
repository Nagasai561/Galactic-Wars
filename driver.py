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
bullet_velocity = 50


#init
pygame.init()
pygame.display.set_caption("Galactic wars")


#screen 
screen = pygame.display.set_mode((screen_width, screen_height))


#assets and objects
space = pygame.transform.scale(pygame.image.load("Assets/space.jpeg"), (screen_width, screen_height))

spaceships = pygame.sprite.Group()
class spaceship(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Assets/spaceship.png"), (spaceship_width, spaceship_height)), 270)
        self.rect = self.image.get_rect(center=pos)

    def update(self):
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
             
player_ship = spaceship((screen_width/3, screen_height/3))
spaceships.add(player_ship)

    

monsters = pygame.sprite.Group()
class monster(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("Assets/space_monster.png"), (monster_width, monster_height))
        self.rect = self.image.get_rect(center = pos)
    
    def update(self):
        self.rect.x -= monster_velocity
        for bullet in bullets:
            if(self.rect.colliderect(bullet.rect)):
                self.kill()
        
        global is_gameover
        if(self.rect.colliderect(player_ship.rect)):
            is_gameover = True
        if(self.rect.right < 0):
            is_gameover = True
        
        if not monsters:
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
    
    def update(self):
        if(self.rect.x > screen_width):
            self.kill()
        else:
            self.rect.x += bullet_velocity
    


#other essentials
clock = pygame.time.Clock()
run = True
font = pygame.font.SysFont("Comic Sans MS", 180)
gameover_text = font.render("Gameover", False, (255,255,255))
is_gameover = False
level = "None"

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
    screen.blit(space, (0,0))
    screen.blit(gameover_text, (screen_width/3.5, screen_height/3))
    pygame.display.update()

#while loop
def game():

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_SPACE):
                    shoot_bullet()
        
        if not is_gameover:
            update_stuff()
            draw_stuff()
        else:
            gameover()



def start_screen():
    pass

game()
