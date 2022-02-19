# V2 of Falling dodger Game in Python By Steven Weinstein on 2-19-2022
# Import and initialize required modules and functions
import pygame
import random
import time
import os
pygame.init()
pygame.font.init()
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    K_p,
    KEYDOWN,
    QUIT,
)
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
highscore = 0
score = 0
pause = False
highscoredoc = open(os.path.expanduser(
    "~/Desktop/DodgerGameV2dev/highest_score_local.txt"), "r")
highscore = highscoredoc.read()
highscoredoc.close()
highscoredoc = open(os.path.expanduser(
    "~/Desktop/DodgerGameV2dev/highest_score_local.txt"), "w")
try:
    highscore = int(highscore)
except ValueError:
    print("Error, high score is not an integer. Please fix this in order to save your high score.")
    highscore = 0

# Setting up game window
running = True
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dodger Game v2.0 EXPERIMENTAL')
screen.fill((0,0,0))
banner = f"Score : {score}  High Score : {highscore}"
font = pygame.font.Font(pygame.font.get_default_font(), 36)
myfont = pygame.font.SysFont('helvetica', 22)
# textsurface = myfont.render(banner, False, (255, 255, 255))
# screen.blit(textsurface,(150,0))
screen.fill((0,0,0))
# Setting up player classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((24, 24))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.xpos = 300
        self.ypos = 576
        self.direction = "stop"
    def update(self, pressed_keys, pause = False):
        if pressed_keys[K_LEFT]:
            self.direction = "left"
        if pressed_keys[K_RIGHT]:
            self.direction = "right"
        if pressed_keys[K_SPACE]:
            self.direction = "stop"
        if not pause:
            if self.direction == "left":
                self.xpos -= 3
            elif self.direction == "right":
                self.xpos += 3
# Faller class for falling objects
class Faller(pygame.sprite.Sprite):
    def __init__(self):
        super(Faller, self).__init__()
        self.surf = pygame.Surface((24,24))
        self.surf.fill((48, 196, 22))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(2, 4)
        self.xpos = random.randint(0,600)
        self.ypos = 0

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self, score):
        newscore = score
        self.ypos += self.speed
        if self.ypos >= SCREEN_HEIGHT-24:
            if abs(self.xpos - player.xpos) >= 32:
                newscore = score + 1
            self.reset_location()
        return newscore
    def reset_location(self):
        self.xpos = random.randint(0,600)
        self.ypos = 0

def showtext(highscore, score):
    banner = f"Score : {score}  High Score : {highscore}"
    myfont = pygame.font.SysFont('helvetica', 30)
    textsurface = myfont.render(banner, False, (255, 255, 255))
    # screen.blit(textsurface,(150,0))
    return textsurface
player = Player()
faller1 = Faller()
faller2 = Faller()
faller3 = Faller()

# Main loop for gameplay
while running:
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_p]:
        if pause:
            pause = False
        if not pause:
            pause = True
    while pause:
        player.update(pressed_keys)
        time.sleep(0.5)
        if pressed_keys[K_p]:
            if pause:
                pause = False
            if not pause:
                pause = True
    if score > int(highscore):
        highscore = score
        highscoredoc.seek(0)
        highscoredoc.write(str(highscore))
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
                break
        elif event.type == QUIT:
            running = False
            break
    player.update(pressed_keys)
    score = faller1.update(score)
    score = faller2.update(score)
    score = faller3.update(score)
    # Keeps player on the screen
    if player.rect.left < 0:
        player.rect.left = 0
    if player.rect.right > SCREEN_WIDTH:
        player.rect.right = SCREEN_WIDTH
    if player.rect.top <= 0:
        player.rect.top = 0
    if player.rect.bottom >= SCREEN_HEIGHT:
        player.rect.bottom = SCREEN_HEIGHT
    screen.blit(player.surf, (player.xpos, player.ypos))
    screen.blit(faller1.surf, (faller1.xpos, faller1.ypos))
    screen.blit(faller2.surf, (faller2.xpos, faller2.ypos))
    screen.blit(faller3.surf, (faller3.xpos, faller3.ypos))
    textsurface = showtext(highscore, score)
    screen.blit(textsurface,(150,0))
    pygame.display.flip()
    screen.fill((0, 0, 0))