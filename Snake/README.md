# 🐍 Snake Game with Q-Learning

This project implements a classic Snake game powered by a simple **Q-Learning** algorithm. The snake learns to reach food while avoiding obstacles and its own body using basic reinforcement learning techniques. The game is built with **Python** and **Pygame**.

---

## 🎯 Features

- 🧱 **Environment:**  
  20x20 grid-based world with static obstacles, food, and the moving snake.

- 🧠 **Q-Learning Logic:**
  - **State:**  
    Relative position of food (x, y) and danger indicators (up, down, left, right).
  - **Actions:**  
    `Up`, `Down`, `Left`, `Right`.
  - **Rewards:**  
    +10 for eating food, -10 for collisions, -0.1 for each movement step.
  - **Hyperparameters:**  
    - Learning Rate `α = 0.1`  
    - Discount Factor `γ = 0.9`  
    - Exploration Rate `ε = 0.1`

- 🎨 **Graphics:**
  - Snake: 🟩 Green  
  - Food: 🟥 Red  
  - Obstacles: 🟦 Blue  
  - Score & Episode counter displayed on screen

- 🕹️ **Execution:**  
  Runs with a standard `pygame` loop. No external reinforcement learning libraries required.

---

## 🧰 Requirements

- ✅ Python 3.8+
- ✅ [Pygame](https://www.pygame.org/) library

🚀 How to Run
Download the maze_qlearning.py file.

Run the script locally with:
python maze_qlearning.py
📈 Observing the Learning Process
🔄 Early Episodes:
-The agent explores randomly and often hits walls.

🧠 Later Episodes:
The agent gradually learns to find shorter and safer paths to the goal.

📊 On-Screen Info:
  - The score, current episode, and number of steps are displayed in the top-left corner.

💡 Possible Improvements
  - 📉 Gradually decrease ε over time to shift from exploration to exploitation.

  - 🧱 Introduce dynamic/moving walls for a more challenging environment.

  - 🤖 Implement Deep Q-Learning (DQN) for scaling to larger maze sizes.

-🧭 Store and visualize the optimal path after training is complete.
