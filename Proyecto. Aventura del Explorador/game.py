import pgzrun
from random import randint
from math import sqrt
from pygame import Rect

# Configuración de pantalla
WIDTH = 800
HEIGHT = 600
TITLE = "Pixel Adventurer"

# Clases
class Hero:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT - 150
        self.speed = 5
        self.jump_power = 15
        self.is_jumping = False
        self.direction = "right"
        self.animation_frames = {
            "idle": [Actor("hero/idle_1"), Actor("hero/idle_2")],
            "run": [Actor("hero/run_1"), Actor("hero/run_2")]
        }
        self.current_animation = "idle"
        self.frame_index = 0
        self.rect = Rect(self.x, self.y, 50, 80)
    
    def update(self):
        # Movimiento
        if keyboard.left:
            self.x -= self.speed
            self.direction = "left"
            self.current_animation = "run"
        elif keyboard.right:
            self.x += self.speed
            self.direction = "right"
            self.current_animation = "run"
        else:
            self.current_animation = "idle"
        
        # Salto
        if keyboard.space and not self.is_jumping:
            self.is_jumping = True
            sounds.jump.play()
        
        if self.is_jumping:
            self.y -= self.jump_power
            self.jump_power -= 1
            if self.y >= HEIGHT - 150:
                self.y = HEIGHT - 150
                self.is_jumping = False
                self.jump_power = 15
        
        # Actualizar rectángulo de colisión
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self):
        frame = self.animation_frames[self.current_animation][self.frame_index // 10]
        frame.x = self.x
        frame.y = self.y
        if self.direction == "left":
            frame.flip_x = True
        else:
            frame.flip_x = False
        frame.draw()
        self.frame_index = (self.frame_index + 1) % 20

class Enemy:
    def __init__(self):
        self.x = randint(WIDTH, WIDTH + 300)
        self.y = HEIGHT - 130
        self.speed = randint(1, 3)
        self.animation = [Actor("enemy/slime_1"), Actor("enemy/slime_2")]
        self.frame_index = 0
        self.rect = Rect(self.x, self.y, 60, 60)
    
    def update(self):
        self.x -= self.speed
        if self.x < -100:
            self.x = randint(WIDTH, WIDTH + 300)
        self.rect.x = self.x
        self.frame_index = (self.frame_index + 1) % 20
    
    def draw(self):
        frame = self.animation[self.frame_index // 10]
        frame.x = self.x
        frame.y = self.y
        frame.draw()

# Inicialización
hero = Hero()
enemies = [Enemy() for _ in range(3)]
game_state = "menu"  # menu/playing
music.play("background")

# Funciones PGZero
def update():
    if game_state == "playing":
        hero.update()
        for enemy in enemies:
            enemy.update()
            if hero.rect.colliderect(enemy.rect):
                game_state = "menu"

def draw():
    if game_state == "menu":
        screen.blit("background", (0, 0))
        if button("Start Game", WIDTH//2 - 100, HEIGHT//2):
            game_state = "playing"
    else:
        screen.blit("background", (0, 0))
        hero.draw()
        for enemy in enemies:
            enemy.draw()

def button(text, x, y):
    btn = Rect(x, y, 200, 50)
    if btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        return True
    screen.draw.filled_rect(btn, (0, 100, 200))
    screen.draw.text(text, center=(x + 100, y + 25))
    return False

pgzrun.go()