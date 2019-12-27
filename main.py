import pygame
from random import randint
import math
from pygame import mixer

# init pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# name & icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('planet.png')
pygame.display.set_icon(icon)

# background pic
background = pygame.image.load('SpaceRockBackground.png')

# background sound
mixer.music.load('witcher.mp3')
mixer.music.play(-1)

# Player
playerIMG = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerMove = 0

# Monster
monsterIMG = list()
monsterX = list()
monsterY = list()
monsterMoveX = list()
monsterMoveY = list()
num_monsters = 6

for i in range(num_monsters):
    monsterIMG.append(pygame.image.load('monster2.png'))
    monsterX.append(randint(1, 735))
    monsterY.append(randint(25, 125))
    monsterMoveX.append(4)
    monsterMoveY.append(40)

# bullet
bulleyIMG = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletMoveX = 0
bulletMoveY = -15
bullet_state = 'ready'

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 28)
textX = 10
textY = 10

# game over
GameOverFont = pygame.font.Font('freesansbold.ttf', 64)

def game_over():
    GameOver = GameOverFont.render('GAME OVER', True, (255, 0, 0))
    screen.blit(GameOver, (200, 250))

def show_score(x, y):
    score = font.render('Score : ' + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerIMG, (x, y))


def monster(x, y, i):
    screen.blit(monsterIMG[i], (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulleyIMG, (x + 16, y + 10))


def isCollision(monsterX, monsterY, bulletX, bulletY):
    distance = math.sqrt((math.pow(monsterX - bulletX, 2)) + (math.pow(monsterY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# start game
running = True
while running:

    # RGB - Red, Green, Blue
    screen.fill((5, 130, 15))
    # background icon
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check if its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerMove = 5.5
            if event.key == pygame.K_LEFT:
                playerMove = -5.5
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    # get the current x cordinate of spaceship
                    bulletX = playerX
                    bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerMove = 0

    # 5 = 5 + -0.5 -> 5 = 5 - 0.5
    # 5 = 5 + 0.5

    # spaceship boundaries so that it doesnt go out of screen
    playerX += playerMove

    if playerX <= 0:
        playerMove = 0
    if playerX >= 736:
        playerX = 736

    # monster movement
    for i in range(num_monsters):
        if monsterY[i] > 440:
            for j in range(num_monsters):
                monsterY[j] = 2000
            game_over()
            break

        monsterX[i] += monsterMoveX[i]
        if monsterX[i] <= 0:
            monsterMoveX[i] = 4
            monsterY[i] += monsterMoveY[i]
        elif monsterX[i] >= 736:
            monsterMoveX[i] = -4
            monsterY[i] += monsterMoveY[i]

        # collision
        collision = isCollision(monsterX[i], monsterY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            monsterX[i] = randint(1, 735)
            monsterY[i] = randint(25, 125)

        monster(monsterX[i], monsterY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state is 'fire':
        bullet(bulletX, bulletY)
        bulletY += bulletMoveY

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
