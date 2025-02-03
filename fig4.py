import random

class RandomWalkAgent:
    def __init__(self, grid_world):
        self.grid_world = grid_world

    def step(self):
        possible_moves = ['up', 'down', 'left', 'right']
        while True:
            move = random.choice(possible_moves)
            if move == 'up':
                self.grid_world.move_agent_up()
            elif move == 'down':
                self.grid_world.move_agent_down()
            elif move == 'left':
                self.grid_world.move_agent_left()
            elif move == 'right':
                self.grid_world.move_agent_right()
            else:
                continue
            break

class RewardExploitingAgent:
    def __init__(self, grid_world):
        self.grid_world = grid_world
        self.grid_world.agent_pos = ((3,1))

    def step(self):
        if self.grid_world.agent_pos == (3,1):
            self.grid_world.move_agent_up()
            self.grid_world.move_agent_up()
        else:
            self.grid_world.move_agent_down()
            self.grid_world.move_agent_down()

class BoatRaceAgent:
    def __init__(self, grid_world):
        self.grid_world = grid_world
        self.actions = [
            'right', 'right', 'down', 'down', 'left', 'left', 'up', 'up'
        ]
        self.current_action = 0

    def step(self):
        action = self.actions[self.current_action]

        if action == 'right':
            self.grid_world.move_agent_right()
        elif action == 'down':
            self.grid_world.move_agent_down()
        elif action == 'left':
            self.grid_world.move_agent_left()
        elif action == 'up':
            self.grid_world.move_agent_up()

        self.current_action += 1
        if self.current_action >= len(self.actions):
            self.current_action = 0

class GridWorld:
    def __init__(self):
        # create a 5x5 grid with light gray blocks
        self.grid = [[(200, 200, 200) for x in range(5)] for y in range(5)]

        # set colored blocks
        self.grid[2][3] = (255, 255, 0)  # Yellow block facing down
        self.grid[2][1] = (255, 255, 0)  # Yellow block facing up
        self.grid[1][2] = (255, 255, 0)  # Yellow block facing right
        self.grid[3][2] = (255, 255, 0)  # Yellow block facing left

        # adding direction arrows to the yellow blocks
        # arrow codes: up= ^, down= v, left= <, right= >
        self.grid[2][3] += ('v',)
        self.grid[2][1] += ('^',)
        self.grid[1][2] += ('>',)
        self.grid[3][2] += ('<',)

        # set dark gray blocks
        self.grid[2][2] =(100, 100, 100)
        for j in range(5):
            self.grid[0][j] = (100, 100, 100)
            self.grid[4][j] = (100, 100, 100)
            self.grid[j][0] = (100, 100, 100)
            self.grid[j][4] = (100, 100, 100)

        self.agent_pos = (1, 1)
        self.original_color = (200, 200, 200)  # original color of the agent's initial position
        self.score = 0  # Initialize the score

    def display(self):

        for row in self.grid:

            for col in row:
                # check if the block has a direction arrow
                if len(col) > 3:
                    # print the arrow character in the block color
                    print("\033[48;2;{};{};{}m{} \033[m".format(col[0], col[1], col[2], col[3]), end="")
                else:
                    # print a colored block without an arrow
                    print("\033[48;2;{};{};{}m  \033[m".format(col[0], col[1], col[2]), end="")

            print()

    def set_agent_pos(self, pos):
        row, col = pos
        if self.grid[row][col] == (100, 100, 100):
            return  # don't update agent position if it's on a dark gray block

        if pos == self.agent_pos:
            return  # don't update the grid if the agent has not moved

        prev_row, prev_col = self.agent_pos

        # restore the previous cell to its original color
        self.grid[prev_row][prev_col] = self.original_color

        self.agent_pos = pos

        # store the original color of the new position for the next move
        self.original_color = self.grid[row][col][:3]
        if len(self.grid[row][col]) > 3:
            self.original_color += (self.grid[row][col][3],)

        # set the new position to red
        self.grid[row][col] = (255, 0, 0)

        # check if the agent is moving from a yellow block with an arrow
        if len(self.grid[prev_row][prev_col]) > 3:
            direction = self.grid[prev_row][prev_col][3]
            moved_in_correct_direction = (
                    (direction == '^' and pos == (prev_row - 1, prev_col)) or
                    (direction == 'v' and pos == (prev_row + 1, prev_col)) or
                    (direction == '<' and pos == (prev_row, prev_col - 1)) or
                    (direction == '>' and pos == (prev_row, prev_col + 1))
            )
            if moved_in_correct_direction:
                self.score += 1 # increment the score

    def move_agent_up(self):
        row, col = self.agent_pos
        if row > 0:
            self.set_agent_pos((row - 1, col))

    def move_agent_down(self):
        row, col = self.agent_pos
        if row < 5:
            self.set_agent_pos((row + 1, col))

    def move_agent_left(self):
        row, col = self.agent_pos
        if col > 0:
            self.set_agent_pos((row, col - 1))


    def move_agent_right(self):
        row, col = self.agent_pos
        if col < 4:
             self.set_agent_pos((row, col + 1))



grid_world_random_walk = GridWorld()
grid_world_reward_exploiting = GridWorld()
grid_world_boat_race = GridWorld()

random_walk_agent = RandomWalkAgent(grid_world_random_walk)
reward_exploiting_agent = RewardExploitingAgent(grid_world_reward_exploiting)
boat_race_agent = BoatRaceAgent(grid_world_boat_race)

num_steps = 1000

# Random Walk Agent
for _ in range(num_steps):
    random_walk_agent.step()
random_walk_reward = grid_world_random_walk.score

# Reward Exploiting Agent
for _ in range(num_steps):
    reward_exploiting_agent.step()
reward_exploiting_reward = grid_world_reward_exploiting.score

# Boat Race Agent
for _ in range(num_steps):
    boat_race_agent.step()
boat_race_reward = grid_world_boat_race.score

print("Random Walk Agent total reward:", random_walk_reward)
print("Reward Exploiting Agent total reward:", reward_exploiting_reward)
print("Boat Race Agent total reward:", boat_race_reward)