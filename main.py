import pygame
import time

pygame.init()
WIDTH = 500
HEIGHT = 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Square Jumper Beta")
run = True

# COLOURS
PINK = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
image = pygame.image.load("background.png")

# SOUND EFFECTS
jump_SFX = pygame.mixer.Sound("jumpSFX.wav")
game_over_SFX = pygame.mixer.Sound("gameOverSFX.wav")

# Music
pygame.mixer.music.load("backGroundMusic.mp3")
pygame.mixer.music.play(-1)


class Player:
    def __init__(self, x, y, width, height, colour, jump_count=10, velocity=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = float(velocity)
        self.colour = colour
        self.jump_count = jump_count
        self.is_jump = False
        self.green = True
        self.added = False
        self.rect = None
        self.game_over = False
        self.points = 0
        self.blue_turn = True
        self.green_turn = False

    def update_points(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(f"Points: {self.points}", True, PINK, BLUE)
        window.blit(text, (0, 0))

    def display_game_over(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Game Over!', True, RED, YELLOW)
        window.blit(text, (160, 250))
        self.game_over = True

    def check_collision(self):
        bottom_left = [self.x, (self.y + self.height) + self.width]
        bottom_right = [self.x + self.width, (self.y + self.height) + self.width]

        # Puts square on top of green platform
        if self.green is True and self.added is False:
            self.added = True
            self.y -= green_platform.height

        # Checks to see if falls

        falls = (bottom_right[0] < green_platform.x and bottom_right[1] > green_platform.y) or (
                bottom_left[0] > (blue_platform.x + blue_platform.width) and bottom_left[1] > blue_platform.y)
        if falls:
            self.y += self.velocity
            if player.y > green_platform.y + 20:
                player.display_game_over()
                game_over_SFX.play()

        # checks if on blue
        landed_on_blue = blue_platform.x <= bottom_left[0] <= blue_platform.x + blue_platform.width
        landed_on_green = green_platform.x <= bottom_right[0] <= green_platform.x + green_platform.width

        if landed_on_blue and self.blue_turn:
            self.points += 1
            self.blue_turn = False
            self.green_turn = True
        elif landed_on_green and self.green_turn:
            self.points += 1
            self.green_turn = False
            self.blue_turn = True

        # Check if square collide with red obstacle
        collide_with_obstacle = pygame.Rect.colliderect(self.rect, obstacle.obstacle)
        if collide_with_obstacle:
            self.display_game_over()
            game_over_SFX.play()

    def drawCharacter(self, win):
        self.rect = pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))


class Obstacle:
    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.obstacle = None

    def drawObstacle(self, win):
        self.obstacle = pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))


class Platform(Obstacle):
    def __init__(self, x, y, width, height, colour):
        super().__init__(x, y, width, height, colour)
        self.rect = None

    def drawPlatform(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))


player = Player(100, 420, 80, 80, PINK, velocity=9.8)
obstacle = Obstacle((WIDTH / 2) - (50 / 2), 400, 50, 100, RED)
green_platform = Platform(100, 480, 100, 20, GREEN)
blue_platform = Platform(300, 480, 100, 20, BLUE)

while run:
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player.velocity
    if keys[pygame.K_RIGHT] and player.x < 400:
        player.x += player.velocity
    if not player.is_jump:
        if keys[pygame.K_SPACE]:
            player.is_jump = True
            jump_SFX.play()
    else:
        if player.jump_count >= -10:

            neg = 1
            if player.jump_count < 0:
                neg = -1
            player.y -= ((player.jump_count ** 2) * 0.7) * neg
            player.jump_count -= 1
        else:
            player.is_jump = False
            player.jump_count = 10

    if player.game_over:
        run = False
        time.sleep(5)
    window.fill((0, 0, 0))
    window.blit(image, (0, 0))
    player.drawCharacter(window)
    obstacle.drawObstacle(window)
    green_platform.drawPlatform(window)
    blue_platform.drawPlatform(window)
    player.update_points()
    player.check_collision()
    pygame.display.update()

pygame.quit()
