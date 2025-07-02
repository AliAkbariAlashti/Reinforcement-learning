import pygame
import random
import numpy as np
import platform

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 400
HEIGHT = 400
GRID_SIZE = 40
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 50

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Q-Learning parameters
ALPHA = 0.1  # Learning rate
GAMMA = 0.9  # Discount factor
EPSILON = 0.1  # Exploration rate
ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]

# Maze setup (1 = wall, 0 = empty)
MAZE = [
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0]
]

# Agent class
class Agent:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, action):
        new_x, new_y = self.x, self.y
        if action == "UP":
            new_y -= 1
        elif action == "DOWN":
            new_y += 1
        elif action == "LEFT":
            new_x -= 1
        elif action == "RIGHT":
            new_x += 1
        
        # Check if move is valid
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and MAZE[new_y][new_x] == 0:
            self.x, self.y = new_x, new_y
            return True
        return False

# Goal class
class Goal:
    def __init__(self):
        self.x = GRID_WIDTH - 1
        self.y = GRID_HEIGHT - 1

# Q-Learning Agent
class QLearningAgent:
    def __init__(self):
        self.q_table = {}
        self.actions = ACTIONS

    def get_state(self, agent):
        return (agent.x, agent.y)

    def get_action(self, state):
        if random.random() < EPSILON:
            return random.choice(self.actions)
        q_values = self.q_table.get(state, {a: 0 for a in self.actions})
        return max(q_values, key=q_values.get)

    def update_q_table(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = {a: 0 for a in self.actions}
        if next_state not in self.q_table:
            self.q_table[next_state] = {a: 0 for a in self.actions}
        
        current_q = self.q_table[state][action]
        next_max_q = max(self.q_table[next_state].values())
        self.q_table[state][action] = current_q + ALPHA * (reward + GAMMA * next_max_q - current_q)

# Game variables
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
agent = Agent()
goal = Goal()
ql_agent = QLearningAgent()
score = 0
steps = 0
episode = 0
game_over = False
font = pygame.font.Font(None, 36)

def setup():
    global agent, score, steps, game_over, episode
    pygame.display.set_caption("Maze Q-Learning")
    agent = Agent()
    score = 0
    steps = 0
    game_over = False
    episode += 1

def update_loop():
    global game_over, score, steps
    
    if game_over:
        setup()
        return

    # Get current state
    state = ql_agent.get_state(agent)
    
    # Choose action
    action = ql_agent.get_action(state)
    
    # Move agent
    valid_move = agent.move(action)
    
    # Calculate reward
    reward = -1  # Penalty for each move
    if not valid_move:
        reward = -10  # Penalty for hitting wall
    elif (agent.x, agent.y) == (goal.x, goal.y):
        reward = 100  # Reward for reaching goal
        score += 1
        game_over = True
    
    steps += 1
    
    # Update Q-table
    next_state = ql_agent.get_state(agent)
    ql_agent.update_q_table(state, action, reward, next_state)
    
    # Draw
    screen.fill(BLACK)
    
    # Draw maze
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if MAZE[y][x] == 1:
                pygame.draw.rect(screen, BLUE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    # Draw goal
    pygame.draw.rect(screen, RED, (goal.x * GRID_SIZE, goal.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    # Draw agent
    pygame.draw.rect(screen, GREEN, (agent.x * GRID_SIZE, agent.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    # Draw score, episode, and steps
    info_text = font.render(f"Score: {score} Episode: {episode} Steps: {steps}", True, WHITE)
    screen.blit(info_text, (10, 10))
    
    if game_over:
        game_over_text = font.render("Goal Reached! Restarting...", True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - 100, HEIGHT//2))
    
    pygame.display.flip()

def main():
    setup()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        update_loop()

if platform.system() == "Emscripten":
    main()
else:
    if __name__ == "__main__":
        main()