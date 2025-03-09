import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

FPS = 60

DINO_WIDTH = 75
DINO_HEIGHT = 75
GRAVITY = 0.8
JUMP_VELOCITY = -16

CACTUS_WIDTH = 30
CACTUS_HEIGHT = 60
BASE_CACTUS_SPEED = 7

class Dino:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.width = DINO_WIDTH
        self.height = DINO_HEIGHT
        self.image = image
        self.velocity_y = 0
        self.is_jumping = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = JUMP_VELOCITY
            self.is_jumping = True

    def update(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
        if self.y >= HEIGHT - self.height:
            self.y = HEIGHT - self.height
            self.velocity_y = 0
            self.is_jumping = False
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        surface.blit((255, 255, 255), (self.x, self.y))

class Obstacle:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.width = CACTUS_WIDTH
        self.height = CACTUS_HEIGHT
        self.image = image
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, speed):
        self.x -= speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        surface.blit((0, 200, 0), (self.x, self.y))

def game_over_screen(score):
    font_big = pygame.font.SysFont("Arial", 48)
    font_small = pygame.font.SysFont("Arial", 24)
    text = font_big.render("Game Over", True, (0, 0, 0))
    score_text = font_small.render(f"Score: {score}", True, (0, 0, 0))
    WIN.fill((255, 255, 255))
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height()))
    WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 10))
    pygame.display.update()
    pygame.time.delay(2000)

def main():
    clock = pygame.time.Clock()
    score = 0
    spawn_timer = 0
    obstacles = []
    dino = Dino(50, HEIGHT, dino_img)
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump()
        dino.update()
        spawn_timer += 1
        if spawn_timer > random.randint(60, 150):
            obstacles.append(Obstacle(WIDTH, HEIGHT - CACTUS_HEIGHT, cactus_img))
            spawn_timer = 0
        current_speed = BASE_CACTUS_SPEED + score // 5
        for obstacle in obstacles[:]:
            obstacle.update(current_speed)
            if obstacle.x + obstacle.width < 0:
                obstacles.remove(obstacle)
                score += 1
            if dino.rect.colliderect(obstacle.rect):
                game_over_screen(score)
                main()
        WIN.blit((0, 0, 200), (0, 0))
        dino.draw(WIN)
        for obstacle in obstacles:
            obstacle.draw(WIN)
        font = pygame.font.SysFont("Arial", 24)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        WIN.blit(score_text, (10, 10))
        pygame.display.update()

if __name__ == "__main__":
    main()