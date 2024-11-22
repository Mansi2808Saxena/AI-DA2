import numpy as np
import copy

class PuzzleState:
    def __init__(self, board, goal, heuristic="manhattan"):
        self.board = board
        self.goal = goal
        self.heuristic = heuristic
        self.empty_tile = self.find_empty_tile()

    def find_empty_tile(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    return i, j

    def calculate_heuristic(self):
        if self.heuristic == "manhattan":
            return self.manhattan_distance()

    def manhattan_distance(self):
        distance = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] != 0:
                    goal_position = np.where(self.goal == self.board[i][j])
                    distance += abs(goal_position[0][0] - i) + abs(goal_position[1][0] - j)
        return distance

    def generate_neighbors(self):
        i, j = self.empty_tile
        neighbors = []
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]  

        for move in moves:
            ni, nj = i + move[0], j + move[1]
            if 0 <= ni < len(self.board) and 0 <= nj < len(self.board[0]):
                new_board = copy.deepcopy(self.board)
                new_board[i][j], new_board[ni][nj] = new_board[ni][nj], new_board[i][j]
                neighbors.append(PuzzleState(new_board, self.goal, self.heuristic))

        return neighbors

    def is_goal(self):
        return np.array_equal(self.board, self.goal)

def hill_climbing(start_state):
    current_state = start_state
    steps = 0

    while not current_state.is_goal():
        neighbors = current_state.generate_neighbors()
        neighbors.sort(key=lambda x: x.calculate_heuristic())

        best_neighbor = neighbors[0]

        if best_neighbor.calculate_heuristic() >= current_state.calculate_heuristic():
            
            break

        current_state = best_neighbor
        steps += 1

    return current_state, steps


initial_board = np.array([
    [1, 2, 3],
    [4, 0, 5],
    [7, 8, 6]
])

goal_board = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
])

start_state = PuzzleState(initial_board, goal_board, heuristic="manhattan")

final_state, steps = hill_climbing(start_state)


print("PASS CASE")
print("Initial Board:")
print(initial_board)
print("Final Board:")
print(final_state.board)
print(f"Steps Taken: {steps}")
print(f"Final Heuristic Value: {final_state.calculate_heuristic()}")
