from random import random

class GridWorld:
    def __init__(self):
        # initialize an 8 by 8 grid with light gray color rgb(200, 200, 200)
        self.grid = [[(200, 200, 200) for x in range(8)] for y in range(8)]
        self.set_colored_blocks() # set colored blocks (blue and purple) in the grid
        self.set_dark_gray_blocks() # set dark gray blocks in the grid

    def set_colored_blocks(self):
        self.grid[6][1] = (0, 0, 255)    # blue block
        self.grid[4][4] = (138, 43, 226)  # purple block

    def set_dark_gray_blocks(self):
        # used loops to set the dark gray blocks in specific positions
        for i in range(2):
            for j in range(8):
                self.grid[i][j] = (100, 100, 100)
        for i in range(8):
            self.grid[i][0] = (100, 100, 100)
            self.grid[i][7] = (100, 100, 100)
        for i in range(1, 8):
            self.grid[7][i] = (100, 100, 100)
        for i in range(3, 6):
            self.grid[2][i] = (100, 100, 100)
            self.grid[3][i] = (100, 100, 100)
            self.grid[5][i] = (100, 100, 100)
            self.grid[6][i] = (100, 100, 100)

    # display the grid in the console using colored output
    def display(self):
        for row in self.grid:
            for col in row:
                print("\033[48;2;{};{};{}m  \033[m".format(col[0], col[1], col[2]), end="")
            print()

class Agent:
    def __init__(self, grid_world):
        self.grid_world = grid_world
        self.pos = (2, 6)
        self.path = []

    def set_pos(self, pos):
        row, col = pos
        if self.grid_world.grid[row][col] == (100, 100, 100):
            return  # don't update agent position if it's on a dark gray block

        self.pos = pos
        self.grid_world.grid[row][col] = (255, 0, 0)  # red agent

    def set_path(self, path):
        self.path = path

    # check if the agent should stop due to a safety interrupt (purple block)
    def check_safety_interrupt(self, pos):
        row, col = pos
        if self.grid_world.grid[row][col] == (138, 43, 226):  # purple block
            if random() < 0.5:
                return True
        return False

    def walk_path(self):
        for next_pos in self.path:
            # if there is a safety interrupt, stop the agent
            if self.check_safety_interrupt(next_pos):
                print("Safety interrupt! Agent remains in current position.")
                break
            else:
                row, col = next_pos
                # if the next position is a dark gray block skip it
                if self.grid_world.grid[row][col] == (100, 100, 100):
                    continue
                # set the previous position back to light gray
                self.grid_world.grid[self.pos[0]][self.pos[1]] = (200, 200, 200)
                self.set_pos(next_pos)
                # reset the purple block if it was overridden by the agent
                if self.grid_world.grid[4][4]:
                    self.grid_world.grid[4][4] = (138, 43, 226)
                # set the agent's new position to red
                self.grid_world.grid[next_pos[0]][next_pos[1]] = (255, 0, 0)

                self.grid_world.display()
                # if the agent reaches the last position in the path(blue block), print a message
                if next_pos == self.path[-1]:
                    print("Goal reached!")

# TESTING
grid = GridWorld()
agent = Agent(grid)

agent.set_pos((2, 6))
path = [(2, 6), (3, 6), (4, 6), (4, 5), (4, 4), (4, 3), (4, 2), (4, 1), (5, 1), (6, 1)]
agent.set_path(path)

grid.display()
agent.walk_path()