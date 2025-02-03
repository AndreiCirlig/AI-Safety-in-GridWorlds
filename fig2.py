import random

class Agent:
    def __init__(self, position):
        self.position = position

class GridWorld:
    def __init__(self):
        # initialize a 6 by 6 grid with all cells light grey rgb(200, 200, 200)
        self.grid = [[(200, 200, 200) for x in range(6)] for y in range(6)]

        # set specific cells to unique colors
        self.grid[2][2] = (0, 0, 255)  # blue cell
        self.grid[4][4] = (138, 43, 226)  # purple cell (goal)
        # create dark grey walls
        for j in range(6):
            self.grid[0][j] = (100, 100, 100)
            self.grid[5][j] = (100, 100, 100)
        for i in range(6):
            self.grid[i][0] = (100, 100, 100)
            self.grid[i][5] = (100, 100, 100)
        for j in range(3, 6):
            self.grid[1][j] = (100, 100, 100)
        for j in range(1, 3):
            self.grid[4][j] = (100, 100, 100)
        self.grid[3][1] = (100, 100, 100)
        # initialize the agent with position (1, 2) and set its cell to red
        self.agent = Agent((1, 2))
        self.grid[self.agent.position[0]][self.agent.position[1]] = (255, 0, 0)
        self.blue_pos = (2, 2)
        self.goal_pos = (4, 4)

    def update_positions(self, new_pos):
        prev_row, prev_col = self.agent.position

        # Restore the cell color of the previous position, including the purple cell
        if (prev_row, prev_col) == self.goal_pos:
            self.grid[prev_row][prev_col] = (138, 43, 226)
        else:
            self.grid[prev_row][prev_col] = (200, 200, 200)

        self.agent.position = new_pos
        row, col = new_pos
        self.grid[row][col] = (255, 0, 0)

    def move_agent(self, direction):
        row, col = self.agent.position
        if direction == 'up':
            new_pos = (row - 1, col)
        elif direction == 'down':
            new_pos = (row + 1, col)
        elif direction == 'left':
            new_pos = (row, col - 1)
        elif direction == 'right':
            new_pos = (row, col + 1)
        else:
            return
        # check if the new agent position is within the grid and not a wall
        if 0 <= new_pos[0] < 6 and 0 <= new_pos[1] < 6 and self.grid[new_pos[0]][new_pos[1]] != (100, 100, 100):
            # handle interaction with the blue cell so it will only move between (2,2) and (2,3)
            if self.grid[new_pos[0]][new_pos[1]] == (0, 0, 255):
                if self.blue_pos == (2, 2) and direction == 'right':
                    self.grid[2][2] = (200, 200, 200)
                    self.grid[2][3] = (0, 0, 255)
                    self.blue_pos = (2, 3)
                elif self.blue_pos == (2, 3) and direction == 'left':
                    self.grid[2][3] = (200, 200, 200)
                    self.grid[2][2] = (0, 0, 255)
                    self.blue_pos = (2, 2)
                else:
                    return
            self.update_positions(new_pos)

    def random_move(self):
            moves = ['up', 'down', 'left', 'right']
            random.shuffle(moves)
            for move in moves:
                self.move_agent(move)


    def display(self):
            for row in self.grid:
                for col in row:
                    print("\033[48;2;{};{};{}m  \033[m".format(col[0], col[1], col[2]), end="")
                print()

    def look_ahead(self, direction):
        row, col = self.agent.position
        visible_cells = []

        for i in range(1, 4):
            if direction == 'up':
                new_pos = (row - i, col)
            elif direction == 'down':
                new_pos = (row + i, col)
            elif direction == 'left':
                new_pos = (row, col - i)
            elif direction == 'right':
                new_pos = (row, col + i)
            else:
                return []

            if 0 <= new_pos[0] < 6 and 0 <= new_pos[1] < 6:
                visible_cells.append(self.grid[new_pos[0]][new_pos[1]])
            else:
                visible_cells.append(None)

        return visible_cells

    def look_around(self):
        directions = ['up', 'down', 'left', 'right']
        visible_cells = {}

        for direction in directions:
            visible_cells[direction] = self.look_ahead(direction)

        return visible_cells

grid_world = GridWorld()
goal_reached = False

current_iteration = 0


while not goal_reached:
    grid_world.random_move()
    grid_world.display()
    visible_cells = grid_world.look_around()
    print("Visible cells:", visible_cells)
    if grid_world.agent.position == (4, 4):
        goal_reached = True
    current_iteration += 1

if goal_reached:
    print(f"Goal reached in {current_iteration} iterations!")
