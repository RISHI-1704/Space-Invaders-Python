import pygame
import random
import math
from pygame import mixer

pygame.init()

# Background
background = pygame.image.load('imagess.jpg')

# Screen Size,title,icon
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
Player = pygame.image.load('space-invaders.png')
PlayerX = 370
PlayerY = 530
PlayerX_change = 0

# Enemy
Enemy = []
EnemyX = []
EnemyY = []
EnemyX_change = []
EnemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    Enemy.append(pygame.image.load('enemy.png'))
    EnemyX.append(random.randint(0, 736))
    EnemyY.append(random.randint(50, 150))
    EnemyX_change.append(4)
    EnemyY_change.append(40)

# Bullet
bullet = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# GameOver
GameOver = pygame.font.Font('freesansbold.ttf', 82)
GameOverX = 290
GameOverY = 250


def score(x, y):
    scores = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(scores, (x, y))


def game_over(x, y):
    gameover = font.render("GAME OVER", True, (255, 255, 255))
    over = mixer.Sound("Game Over.wav")
    over.play()
    screen.blit(gameover, (GameOverX, GameOverY))


def player(x, y):
    screen.blit(Player, (round(x), round(y)))


def enemy(x, y, i):
    screen.blit(Enemy[i], (x, y))


def firebullet(x, y):
    global bullet_state
    screen.blit(bullet, (round(x+16), round(y+10)))
    bullet_state = "fire"


def collision(bulletX, bulletY, EnemyX, EnemyY):
    distance = math.sqrt(math.pow(EnemyX - bulletX, 2) +
                         math.pow(EnemyY - bulletY, 2))
    if distance < 35:
        return True
    else:
        return False


running = True
while running:
    screen.fill((0, 0, 0))

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                PlayerX_change = -5
            if event.key == pygame.K_RIGHT:
                PlayerX_change = +5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX = PlayerX
                    firebullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                PlayerX_change = 0

    PlayerX += PlayerX_change

    if PlayerX <= 0:
        PlayerX = 0
    elif PlayerX >= 736:
        PlayerX = 736

    for i in range(num_of_enemies):

        if EnemyY[i] > 450:
            for j in range(num_of_enemies):
                Enemy[j] = 600
            game_over(GameOverX, GameOverY)
            break

        if EnemyX[i] <= 0:
            EnemyX_change[i] = 0.8
            EnemyY[i] += EnemyY_change[i]
        elif EnemyX[i] >= 736:
            EnemyX_change[i] = - 0.8
            EnemyY[i] += EnemyY_change[i]

        col = collision(EnemyX[i], EnemyY[i], bulletX, bulletY)
        if col:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            EnemyX[i] = random.randint(0, 735)
            EnemyY[i] = random.randint(50, 120)

        EnemyX[i] += EnemyX_change[i]
        enemy(EnemyX[i], EnemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        firebullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(PlayerX, PlayerY)
    score(textX, textY)
    pygame.display.update()