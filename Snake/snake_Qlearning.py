# import pygame
# import random
# import numpy as np

# # Initialize Pygame
# pygame.init()

# # Constants
# WIDTH = 400
# HEIGHT = 400
# GRID_SIZE = 20
# GRID_WIDTH = WIDTH // GRID_SIZE
# GRID_HEIGHT = HEIGHT // GRID_SIZE
# FPS = 100

# # Colors
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# RED = (255, 0, 0)
# GREEN = (0, 255, 0)
# BLUE = (0, 0, 255)

# # Q-Learning parameters
# ALPHA = 0.1
# GAMMA = 0.9
# EPSILON = 0.1
# ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]

# # Snake class
# class Snake:
#     def __init__(self):
#         self.x = GRID_WIDTH // 2
#         self.y = GRID_HEIGHT // 2
#         self.direction = "RIGHT"
#         self.body = [(self.x, self.y)]
#         self.length = 1

#     def move(self, direction):
#         if direction == "UP":
#             self.y -= 1
#         elif direction == "DOWN":
#             self.y += 1
#         elif direction == "LEFT":
#             self.x -= 1
#         elif direction == "RIGHT":
#             self.x += 1

#         self.x %= GRID_WIDTH
#         self.y %= GRID_HEIGHT

#         self.body.insert(0, (self.x, self.y))
#         if len(self.body) > self.length:
#             self.body.pop()

#     def check_collision(self, obstacles):
#         return (self.x, self.y) in self.body[1:] or (self.x, self.y) in obstacles

#     def grow(self):
#         self.length += 1

# # Food class
# class Food:
#     def __init__(self, obstacles, snake_body):
#         self.position = self.random_pos(obstacles, snake_body)

#     def random_pos(self, obstacles, snake_body):
#         while True:
#             pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
#             if pos not in obstacles and pos not in snake_body:
#                 return pos

# # Q-Learning Agent
# class QLearningAgent:
#     def __init__(self):
#         self.q_table = {}
#         self.actions = ACTIONS

#     def get_state(self, snake, food, obstacles):
#         head = (snake.x, snake.y)
#         food_dir = (
#             1 if food.position[0] > head[0] else -1 if food.position[0] < head[0] else 0,
#             1 if food.position[1] > head[1] else -1 if food.position[1] < head[1] else 0,
#         )

#         danger = [0, 0, 0, 0]  # UP, DOWN, LEFT, RIGHT
#         for i, (dx, dy) in enumerate([(0, -1), (0, 1), (-1, 0), (1, 0)]):
#             nx = (head[0] + dx) % GRID_WIDTH
#             ny = (head[1] + dy) % GRID_HEIGHT
#             if (nx, ny) in snake.body[1:] or (nx, ny) in obstacles:
#                 danger[i] = 1

#         return (food_dir[0], food_dir[1], tuple(danger))

#     def get_action(self, state):
#         if random.random() < EPSILON:
#             return random.choice(self.actions)
#         q_values = self.q_table.get(state, {a: 0 for a in self.actions})
#         return max(q_values, key=q_values.get)

#     def update_q_table(self, state, action, reward, next_state):
#         if state not in self.q_table:
#             self.q_table[state] = {a: 0 for a in self.actions}
#         if next_state not in self.q_table:
#             self.q_table[next_state] = {a: 0 for a in self.actions}

#         current_q = self.q_table[state][action]
#         next_max_q = max(self.q_table[next_state].values())
#         self.q_table[state][action] = current_q + ALPHA * (reward + GAMMA * next_max_q - current_q)

# # Game setup
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Snake Q-Learning")
# clock = pygame.time.Clock()
# font = pygame.font.Font(None, 36)

# # Fixed obstacles
# obstacles = [(5, 5), (5, 6), (5, 7), (10, 10), (10, 11)]

# # Initialize game variables
# snake = Snake()
# food = Food(obstacles, snake.body)
# agent = QLearningAgent()
# score = 0
# episode = 0
# game_over = False

# def reset_game():
#     global snake, food, score, game_over, episode
#     snake = Snake()
#     food = Food(obstacles, snake.body)
#     score = 0
#     game_over = False
#     episode += 1

# # Main loop
# running = True
# while running:
#     clock.tick(FPS)
#     screen.fill(BLACK)

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     if game_over:
#         reset_game()
#         continue

#     # Get state
#     state = agent.get_state(snake, food, obstacles)
#     action = agent.get_action(state)
#     snake.move(action)

#     # Calculate reward
#     reward = -0.1
#     if snake.check_collision(obstacles):
#         reward = -10
#         game_over = True
#     elif (snake.x, snake.y) == food.position:
#         reward = 10
#         snake.grow()
#         score += 1
#         food.position = food.random_pos(obstacles, snake.body)

#     # Update Q-table
#     next_state = agent.get_state(snake, food, obstacles)
#     agent.update_q_table(state, action, reward, next_state)

#     # Draw obstacles
#     for obs in obstacles:
#         pygame.draw.rect(screen, BLUE, (obs[0]*GRID_SIZE, obs[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))

#     # Draw food
#     pygame.draw.rect(screen, RED, (food.position[0]*GRID_SIZE, food.position[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))

#     # Draw snake
#     for segment in snake.body:
#         pygame.draw.rect(screen, GREEN, (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))

#     # Draw score
#     text = font.render(f"Score: {score}  Episode: {episode}", True, WHITE)
#     screen.blit(text, (10, 10))

#     pygame.display.flip()

# pygame.quit()
# # End of the game
# # Save the Q-table to a file
# import pickle
# with open("q_table.pkl", "wb") as f:
#     pickle.dump(agent.q_table, f)
# # Load the Q-table from a file
# with open("q_table.pkl", "rb") as f:
#     agent.q_table = pickle.load(f)
# # Print the Q-table
# print("Q-Table:")
# for state, actions in agent.q_table.items():
#     print(f"{state}: {actions}")
# # End of the code
# # This code implements a simple Snake game using Q-learning for the snake's movement strategy.

import pickle
import pandas as pd

# Define the output file names
output_csv_file = 'q_table_dataframe.csv'
output_parquet_file = 'q_table_dataframe.parquet'

try:
    # 1. Load (unpickle) the object from the .pkl file
    with open('q_table.pkl', 'rb') as file:
        loaded_object = pickle.load(file)
    print("Object loaded successfully!")
    print(f"Type of loaded object: {type(loaded_object)}")

    # 2. Attempt to convert to DataFrame based on common types
    df = None
    if isinstance(loaded_object, dict):
        df = pd.DataFrame(loaded_object)
        print("Converted dictionary to DataFrame.")
    elif isinstance(loaded_object, list):
        try:
            df = pd.DataFrame(loaded_object)
            print("Converted list (assumed list of lists/records) to DataFrame.")
        except ValueError:
            df = pd.DataFrame.from_records(loaded_object)
            print("Converted list (assumed list of records) to DataFrame.")
    elif isinstance(loaded_object, (pd.DataFrame, pd.Series)):
        if isinstance(loaded_object, pd.Series):
            df = loaded_object.to_frame()
            print("Converted Series to DataFrame.")
        else:
            df = loaded_object
            print("Object is already a DataFrame.")
    else:
        print("The loaded object is of an unexpected type for direct DataFrame conversion.")
        print("You might need to manually transform it before creating a DataFrame.")

    # 3. Save the DataFrame if conversion was successful
    if df is not None:
        print("\nFirst 5 rows of the DataFrame:")
        print(df.head())
        print("\nDataFrame Info:")
        df.info()

        # Save to CSV
        df.to_csv(output_csv_file, index=False) # index=False prevents writing DataFrame index as a column
        print(f"\nDataFrame saved successfully to {output_csv_file}")

        # Save to Parquet (more efficient for larger datasets)
        df.to_parquet(output_parquet_file, index=False) # index=False prevents writing DataFrame index as a column
        print(f"DataFrame saved successfully to {output_parquet_file}")

except FileNotFoundError:
    print("Error: The specified .pkl file was not found.")
except Exception as e:
    print(f"An error occurred during loading, conversion, or saving: {e}")