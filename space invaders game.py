import math
import random
import pygame
from pygame import mixer


pygame.init()

# create the screen
screen = pygame.display.set_mode((1000, 700))

# load the background image
try:
    background = pygame.image.load('background.png')
except pygame.error as e:
    print(f"Unable to load background image: {e}")
    pygame.quit()
    exit()

screen_width, screen_height = screen.get_size()

background = pygame.transform.scale(background, (screen_width, screen_height))

# Caption and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 100
playerY = 600
playerX_change = 0

player_width, player_height = 120, 120  # Set the desired size here
playerImg = pygame.transform.scale(playerImg, (player_width, player_height))

# Enemy Setup
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

enemy_width, enemy_height = 120, 120

# Set the same speed for all enemies
horizontal_speed = 2
vertical_speed = 20

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyImg[i] = pygame.transform.scale(enemyImg[i], (enemy_width, enemy_height))
    enemyX.append(random.randint(0, 736))  # Random starting X position
    enemyY.append(random.randint(50, 150))  # Random starting Y position
    enemyX_change.append(horizontal_speed)  # Same speed for all enemies
    enemyY_change.append(vertical_speed)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 380
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

bullet_width, bullet_height = 10, 30
bulletImg = pygame.transform.scale(bulletImg, (bullet_width, bullet_height))

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    return distance < 27

# Handle events function
def handle_events():
    global playerX_change, bulletX, bulletY, bullet_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False  # Exit game loop

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    return True

# Clock object to control frame rate
clock = pygame.time.Clock()
FPS = 120

# Game Loop
running = True
while running:
    # Control the frame rate
    clock.tick(FPS)
    running = handle_events()

    # Player Movement
    playerX += playerX_change
    if playerX < 0:  # Prevents going beyond the left edge
        playerX = 0
    elif playerX > screen_width - player_width:  # Prevents going beyond the right edge
        playerX = screen_width - player_width

    # Draw background and player
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    player(playerX, playerY)

    # Enemy Movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 340:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = horizontal_speed
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -horizontal_speed
            enemyY[i] += enemyY_change[i]

        # Collision detection
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 380
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 380
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Display score and update screen
    show_score(textX, textY)
    pygame.display.update()


