import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
PORTAL_COLOR = (0, 0, 255)
OBSTACLE_COLOR = (128, 128, 128)
FONT_SIZE = 24
SCORE_COLOR = (255, 255, 255)
GAME_OVER_COLOR = (255, 0, 0)
GAME_OVER_FONT_SIZE = 48

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Portals, Scoring, Obstacles, and Restart")

# Initialize snake, food, portal, direction, score, game over status, and obstacles
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
portal1 = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
portal2 = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
dx, dy = 1, 0
score = 0
game_over = False
obstacles = [(3, 3), (4, 3), (5, 3), (6, 3)]  # Example obstacles

# Function to generate new food location
def generate_food():
    return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

# Function to generate new portal locations
def generate_portals():
    return (
        (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)),
        (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    )

# Function to display score on the screen
def display_score(score):
    font = pygame.font.Font(None, FONT_SIZE)
    score_text = font.render(f"Score: {score}", True, SCORE_COLOR)
    screen.blit(score_text, (10, 10))

# Function to display "Game Over" message on the screen
def display_game_over():
    font = pygame.font.Font(None, GAME_OVER_FONT_SIZE)
    game_over_text = font.render("Game Over", True, GAME_OVER_COLOR)
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 24))

# Function to draw obstacles on the screen
def draw_obstacles():
    for obstacle in obstacles:
        pygame.draw.rect(
            screen,
            OBSTACLE_COLOR,
            pygame.Rect(obstacle[0] * GRID_SIZE, obstacle[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        )

# Function to restart the game
def restart_game():
    global snake, food, portal1, portal2, dx, dy, score, game_over
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    food = generate_food()
    portal1, portal2 = generate_portals()
    dx, dy = 1, 0
    score = 0
    game_over = False

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -1
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, 1
                elif event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -1, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = 1, 0
            else:
                if event.key == pygame.K_r:  # Press "R" to restart the game
                    restart_game()
                elif event.key == pygame.K_q:  # Press "Q" to quit the game
                    pygame.quit()
                    sys.exit()

    if not game_over:
        # Move the snake
        new_head = (snake[0][0] + dx, snake[0][1] + dy)

        # Check for collisions with the snake's body
        if new_head in snake:
            game_over = True

        # Check for collisions with obstacles
        if new_head in obstacles:
            game_over = True

        snake.insert(0, new_head)

        # Check if snake ate food
        if snake[0] == food:
            food = generate_food()
            score += 1
        else:
            snake.pop()

        # Check for collisions with walls
        if (
            snake[0][0] < 0 or snake[0][0] >= GRID_WIDTH or
            snake[0][1] < 0 or snake[0][1] >= GRID_HEIGHT
        ):
            game_over = True

        # Check if snake goes through a portal
        if snake[0] == portal1:
            snake[0] = portal2
        elif snake[0] == portal2:
            snake[0] = portal1

    # Draw the screen
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(
        screen,
        FOOD_COLOR,
        pygame.Rect(food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    )
    pygame.draw.rect(
        screen,
        PORTAL_COLOR,
        pygame.Rect(portal1[0] * GRID_SIZE, portal1[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    )
    pygame.draw.rect(
        screen,
        PORTAL_COLOR,
        pygame.Rect(portal2[0] * GRID_SIZE, portal2[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    )
    draw_obstacles()  # Draw obstacles
    for segment in snake:
        pygame.draw.rect(
            screen,
            SNAKE_COLOR,
            pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        )
    
    display_score(score)  # Display the score on the screen

    if game_over:
        display_game_over()  # Display "Game Over" message

    pygame.display.flip()

    # Control game speed
    pygame.time.Clock().tick(10)
