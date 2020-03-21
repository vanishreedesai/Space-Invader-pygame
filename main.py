import pygame
from pygame import mixer
import random
import math

# initialize pygam
pygame.init()
# creating screen
screen = pygame.display.set_mode((800, 600))
# after adding bg pic players move very slow bcoz while loop has to execute very heavy i.e bg pic
BBackground = pygame.image.load('C:/Program Files/JetBrains/PyCharm Community Edition 2019.3.4/space_background.png')

#background sound
mixer.music.load('C:/Users/hp/Downloads/music_zapsplat_tense_quiz_bed_106.mp3')
mixer.music.play(-1 )   #to play music continuously

# title and icon

pygame.display.set_caption("Space Invader")
icon = pygame.image.load("C:/Users/hp/Downloads/ufo.png")
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('C:/Program Files/JetBrains/PyCharm Community Edition 2019.3.4/rocketa.png')
playerX = 370
playerX_change = 0
playerY = 480

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6
for i in range(num_enemies):  # creating multiple enmies
    enemyImg.append(pygame.image.load('C:/Users/hp/Downloads/space-ship.png'))
    enemyX.append(random.randint(0, 735))  # enemy must appear at random places
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# bullet
bulletImg = pygame.image.load('C:/Users/hp/Downloads/bullet.png')
bulletX = 0  # enemy must appear at random places
bulletY = 480  # playerY at 480 and bullet starting point should be same as spaceship
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"  # ready means bullet cant be seen onscreen and fire the bullet is moving

# score
score_val = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#game over
over_font= pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200,250))
def show_score(x, y):
    score = font.render("Score:" + str(score_val), True, (255, 255, 255))
    screen.blit(score,(x,y))


def player(x, y):
    screen.blit(playerImg, (x, y))  # to draw image on the screen


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # to draw image on the screen


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))  # bullet has to appear at the center of spaceship


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:
    screen.blit(BBackground, (0, 0))
    for event in pygame.event.get():  # any key you press is an event and every event is logged into enent.get()
        if event.type == pygame.QUIT:
            running = False
        # if a key is pressed check whether its left or right
        if event.type == pygame.KEYDOWN:  # checkes whether a key is pressed

            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound=mixer.Sound('C:/Users/hp/Downloads/gun_44mag_11.wav')
                    bullet_sound.play() #no -1 bcoz no need to play continously
                    bulletX = playerX  # only start point....bullet wont follow the spaceship
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:  # key is released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # checking for boundaries
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # bcoz size of image is 64 and width is 800 so 800-64
        playerX = 736

    # enemy movemnt
    for i in range(num_enemies):
        #game over
        if enemyY[i]>440:
            over = mixer.Sound('C:/Users/hp/Downloads/buzzer_x.wav')
            over.play()
            for j in range(num_enemies):
                enemyY[j]=2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bullet_explosion = mixer.Sound('C:/Users/hp/Downloads/explosion_x.wav')
            bullet_explosion.play()
            bulletY = 480
            bullet_state = "ready"
            score_val += 1

            enemyX[i] = random.randint(0, 735)  # enemy must appear at random places
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # collision

    player(playerX, playerY)  # always after screen fill
    show_score(textX,textY)
    # to update continuously
    pygame.display.update()
