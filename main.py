import pygame
import math
import random
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Lord")

favicon = pygame.image.load("images/astronaut.png")
pygame.display.set_icon(favicon)

spaceshipImg = pygame.image.load("images/spaceship.png")
shipX_coordinate = 368
shipY_coordinate = 480
X_change = 0
Y_change = 0
speed = 0.55  # speed of spaceship along X and Y

monsterImg = []
monsterX_coordinate = []
monsterY_coordinate = []
monsterX_change = []  # change this and monster_speedX to change speed of monster
monsterY_change = []  # monster speed on Y axis
monster_speedX = []
no_of_monsters = 5

for i in range(no_of_monsters):
    monsterImg.append(pygame.image.load("images/monster2.png"))
    monsterX_coordinate.append(random.randint(0, 736))
    monsterY_coordinate.append(random.randint(0, 150))
    monsterX_change.append(0.45)  # change this and monster_speedX to change speed of monster
    monsterY_change.append(0.04)  # monster speed on Y axis
    monster_speedX.append(0.45)

bulletImg = pygame.image.load("images/bullet.png")
bulletX_coordinate = 0
bulletY_coordinate = 480
bulletX_change = 0  # change this and monster_speedX to change speed of monster
bulletY_change = 0.9  # monster speed on Y axis
bullet_speedX = 0
bullet_state = "ready"

score = 0
score_font = pygame.font.Font("fonts/gi_incognito.ttf", 42)
textX, textY = 10, 10

gameover = False
gameover_font = pygame.font.Font("fonts/gi_incognito.ttf", 82)


def spaceship(x, y):
    screen.blit(spaceshipImg, (x, y))


def monster(x, y, i):
    screen.blit(monsterImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def collided(monsterX, monsterY, bulletX, bulletY):
    x1_x2 = math.pow(monsterX - bulletX, 2)
    y1_y2 = math.pow(monsterY - bulletY, 2)
    distance = math.sqrt(x1_x2 + y1_y2)
    return True if distance < 31 else False


def show_score(x, y):
    score_on_scr = score_font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score_on_scr, (x, y))


def game_over():
    go_on_scr = gameover_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(go_on_scr, (250, 250))


# game loop
running = True
while running:
    screen.fill((4, 0, 26))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                X_change = -speed
            if event.key == pygame.K_RIGHT:
                X_change = speed
            if event.key == pygame.K_UP:
                Y_change = -speed
            if event.key == pygame.K_DOWN:
                Y_change = speed
            if event.key == pygame.K_SPACE and bullet_state is "ready":
                # adding sound
                bullet_sound = mixer.Sound("music/fire.wav")
                bullet_sound.play()
                bulletX_coordinate = shipX_coordinate
                fire_bullet(bulletX_coordinate, bulletY_coordinate)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                X_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                Y_change = 0

    shipX_coordinate += X_change
    shipY_coordinate += Y_change
    # boundaries for X-Axis
    if shipX_coordinate <= 0:
        shipX_coordinate = 0
    elif shipX_coordinate >= 736:
        shipX_coordinate = 736
    # boundaries for Y-axis
    if shipY_coordinate <= 0:
        shipY_coordinate = 0
    elif shipY_coordinate >= 600:
        shipY_coordinate = 600

    for x in range(no_of_monsters):

        if monsterY_coordinate[x] > 480:
            for j in range(no_of_monsters):
                monsterY_coordinate[j] = 2000
            game_over()

            if not gameover:
                gameover_sound = mixer.Sound("music/game_over.wav")
                gameover_sound.play()
                gameover = True
            break

        monsterX_coordinate[x] += monsterX_change[x]
        monsterY_coordinate[x] += monsterY_change[x]
        # boundaries for X-Axis for monsters
        if monsterX_coordinate[x] <= 0:
            monsterX_coordinate[x] = 0
            monsterX_change[x] = monster_speedX[x]
        elif monsterX_coordinate[x] >= 736:
            monsterX_coordinate[x] = 736
            monsterX_change[x] = -monster_speedX[x]

        is_collided = collided(monsterX_coordinate[x], monsterY_coordinate[x], bulletX_coordinate, bulletY_coordinate)
        if is_collided:
            collision_sound = mixer.Sound("music/collision.wav")
            collision_sound.play()
            bulletY_coordinate = 480
            bullet_state = "ready"
            score += 1
            # print(score)
            monsterX_coordinate[x] = random.randint(0, 736)  # respan
            monsterY_coordinate[x] = random.randint(0, 100)
        monster(monsterX_coordinate[x], monsterY_coordinate[x], x)

    if bulletY_coordinate <= 0:
        bulletY_coordinate = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX_coordinate, bulletY_coordinate)
        bulletY_coordinate -= bulletY_change

    spaceship(shipX_coordinate, shipY_coordinate)
    show_score(textX, textY)
    pygame.display.update()
