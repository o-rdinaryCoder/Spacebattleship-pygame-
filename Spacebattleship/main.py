import pygame
import random
import math
import os
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((1280, 720))
screen_running = True

pygame.display.set_caption("Space Battleship")

icon = pygame.image.load(os.path.join('Data', 'spaceship.png'))
pygame.display.set_icon(icon)

background = pygame.image.load(os.path.join('Data', 'background.png'))

player_icon = pygame.image.load(os.path.join('Data', 'character_icon.png'))
character_position_X = 608
character_position_Y = 640
change_X = 0
change_Y = 0
speed = 5

enemy_icon = []
enemy_position_X1 = []
enemy_position_Y1 = []
change_X1 = []
change_Y1 = []
num_of_enemies = 6

add_enemies = 0

for i in range(num_of_enemies):
    enemy_icon.append(pygame.image.load(os.path.join('Data', 'enemy.png')))
    enemy_position_X1.append(random.randint(0, 1215))
    enemy_position_Y1.append(random.randint(75, 300))
    change_X1.append(3)
    change_Y1.append(40)

bullet_icon = pygame.image.load(os.path.join('Data', 'bullet.png'))
bullet_position_X1 = 608
bullet_position_Y1 = 640
bullet_X1 = 0
bullet_Y1 = 20
bullet_state = "ready"

score_value = 0
font = pygame.font.SysFont('calibri', 20)
font2 = pygame.font.SysFont('calibri', 15)
font3 = pygame.font.SysFont('calibri', 30)
score_position_X = 0
score_position_Y = 0


def score_display(x, y):
    score = font.render("SCORE: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
    name = font2.render("CREATED BY AYUSH KHAREL", True, (255, 255, 255))
    screen.blit(name, (0, 705))
    comment = font3.render("USE THE ARROW KEYS TO CONTROL THE SPACESHIP AND 'SPACE' KEY TO SHOOT", True, (255,255,255))
    screen.blit(comment, (240, 0))
    comment2 = font3.render("Don't let the alien touch you, or the bottom", True, (255,255,255))
    screen.blit(comment2, (440,30))
    comment3 = font.render("Score 40 to win", True, (255,255,255))
    screen.blit(comment3, (0,20))


def player(x, y):
    screen.blit(player_icon, (x, y))


def enemy(x1, y1):
    screen.blit(enemy_icon[a], (x1, y1))


def bullet(x2, y2):
    screen.blit(bullet_icon, (x2 + 16, y2 + 16))
    global bullet_state
    bullet_state = "fire"


def is_collision(enemyx, enemyY, bulletx, bullety):
    distance = math.sqrt((bulletx - enemyx) ** 2 + (bullety - enemyY) ** 2)
    return distance

def game_end(x, y):
    text1 = pygame.font.SysFont('calibri', 200, True)
    game_over = text1.render("GAME OVER!!", True, (255, 0, 0))
    screen.blit(game_over, (x, y))

while screen_running:
    screen.fill((58.2, 58.2, 58.2))
    screen.blit(background, (0, 0))

    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            screen_running = False
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_RIGHT:
                change_X += speed
            if events.key == pygame.K_LEFT:
                change_X -= speed
            if events.key == pygame.K_UP:
                change_Y -= speed
            if events.key == pygame.K_DOWN:
                change_Y += speed
            if events.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    laser_sound = mixer.Sound(os.path.join('Data', 'laser.wav'))
                    laser_sound.play()
                    bullet_position_X1 = character_position_X
                    bullet_position_Y1 = character_position_Y
                    bullet(bullet_position_X1, bullet_position_Y1)
        if events.type == pygame.KEYUP:
            if events.key == pygame.K_RIGHT or events.key == pygame.K_LEFT:
                change_X = 0
            if events.key == pygame.K_UP or events.key == pygame.K_DOWN:
                change_Y = 0

    character_position_Y += change_Y
    character_position_X += change_X

    if character_position_X > 1216:
        character_position_X = 1216
    elif character_position_X < 0:
        character_position_X = 0
    elif character_position_Y > 656:
        character_position_Y = 656
    elif character_position_Y < 0:
        character_position_Y = 0

    for a in range(num_of_enemies):
        enemy_position_X1[a] += change_X1[a]
        if enemy_position_X1[a] >= 1216:
            change_X1[a] = -3
            enemy_position_Y1[a] += change_Y1[a]
        elif enemy_position_X1[a] <= 0:
            change_X1[a] = 3
            enemy_position_Y1[a] += change_Y1[a]
        elif enemy_position_Y1[a] > 656:
            enemy_position_Y1[a] = 656
        elif enemy_position_Y1[a] < 0:
            enemy_position_Y1[a] = 0

        distance_between = is_collision(enemy_position_X1[a], enemy_position_Y1[a], bullet_position_X1,
                                        bullet_position_Y1)
        if distance_between < 27:
            explosion_sound = mixer.Sound(os.path.join('Data', 'explosion.wav'))
            explosion_sound.play()
            bullet_position_Y1 = 640
            bullet_state = "ready"
            score_value += 1
            enemy_position_X1[a] = random.randint(0, 1215)
            enemy_position_Y1[a] = random.randint(75, 100)

        enemy(enemy_position_X1[a], enemy_position_Y1[a])

        distance = math.sqrt(math.pow(enemy_position_X1[a] - character_position_X, 2) + math.pow(
            enemy_position_Y1[a] - character_position_Y, 2))

        if distance < 27:
            game_end(25, 300)
            screen_running = False
    if bullet_position_Y1 <= 0:
        bullet_state = "ready"
        bullet_position_Y1 = 640

    if bullet_state == "fire":
        bullet(bullet_position_X1, bullet_position_Y1)
        bullet_position_Y1 -= bullet_Y1

    if score_value == 40:
        text1 = pygame.font.SysFont('calibri', 200, True)
        win = text1.render("YOU WIN!", True, (0, 255, 0))
        screen.blit(win, (200, 200))
        screen_running = False

    player(character_position_X, character_position_Y)
    score_display(score_position_X, score_position_Y)
    pygame.display.update()
