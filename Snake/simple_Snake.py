import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Snake class
class Snake:
    def __init__(self):
        self.x = GRID_WIDTH // 2
        self.y = GRID_HEIGHT // 2
        self.direction = "RIGHT"
        self.body = [(self.x, self.y)]
        self.length = 1

    def move(self):
        if self.direction == "UP":
            self.y -= 1
        elif self.direction == "DOWN":
            self.y += 1
        elif self.direction == "LEFT":
            self.x -= 1
        elif self.direction == "RIGHT":
            self.x += 1

        self.x %= GRID_WIDTH
        self.y %= GRID_HEIGHT

        self.body.insert(0, (self.x, self.y))
        if len(self.body) > self.length:
            self.body.pop()

    def check_collision(self):
        return (self.x, self.y) in self.body[1:]

    def grow(self):
        self.length += 1

# Food class
class Food:
    def __init__(self):
        self.position = self.random_pos()

    def random_pos(self):
        return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

# Game setup
def setup():
    pygame.display.set_caption("Snake Game")
    return Snake(), Food(), 0, False

# Game variables
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

snake, food, score, game_over = setup()

# Game loop
running = True
while running:
    clock.tick(FPS)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != "DOWN":
                snake.direction = "UP"
            elif event.key == pygame.K_DOWN and snake.direction != "UP":
                snake.direction = "DOWN"
            elif event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                snake.direction = "LEFT"
            elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                snake.direction = "RIGHT"
            elif game_over and event.key == pygame.K_r:
                snake, food, score, game_over = setup()

    if not game_over:
        snake.move()

        if (snake.x, snake.y) == food.position:
            snake.grow()
            score += 1
            food.position = food.random_pos()

        if snake.check_collision():
            game_over = True

    # Draw everything
    screen.fill(BLACK)

    # Draw food
    pygame.draw.rect(screen, RED, (food.position[0] * GRID_SIZE, food.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw snake
    for segment in snake.body:
        pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Draw game over
    if game_over:
        game_over_text = font.render("Game Over! Press R to restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - 170, HEIGHT // 2 - 20))

    pygame.display.flip()

pygame.quit()
