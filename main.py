import random
from math import sqrt, log

# UCB1 Formula


def ucb1(node, exploration_constant=0.5):
    if node.visits == 0:
        return float('inf')
    return (node.wins / node.visits) + exploration_constant * sqrt(log(node.parent.visits) / node.visits)

# Node Class for MCTS Tree


class Node:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.move = move

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_legal_moves())

    def best_child(self, exploration_constant=0.5):
        return max(self.children, key=lambda child: ucb1(child, exploration_constant))

    def expand(self):
        untried_moves = [move for move in self.state.get_legal_moves() if move not in [
            child.move for child in self.children]]
        move = random.choice(untried_moves)
        next_state = self.state.make_move(move)
        child_node = Node(next_state, parent=self, move=move)
        self.children.append(child_node)
        return child_node

    def update(self, result):
        self.visits += 1
        self.wins += result

# Simple Tic-Tac-Toe Game Logic


class TicTacToe:
    def __init__(self, board=None, player=1):
        self.board = board if board else [0] * 9
        self.player = player

    def get_legal_moves(self):
        return [i for i in range(9) if self.board[i] == 0]

    def is_legal_move(self, move):
        return move in self.get_legal_moves()

    def make_move(self, move):
        new_board = self.board[:]
        new_board[move] = self.player
        return TicTacToe(new_board, -self.player)

    def is_terminal(self):
        return self.get_winner() is not None or not self.get_legal_moves()

    def get_winner(self):
        winning_positions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for positions in winning_positions:
            values = [self.board[i] for i in positions]
            if abs(sum(values)) == 3:
                return values[0]
        if not self.get_legal_moves():
            return 0  # Draw
        return None

# MCTS Algorithm


def mcts(root, iterations=1000):
    for _ in range(iterations):
        node = root

        # 1. Selection
        while node.is_fully_expanded() and not node.state.is_terminal():
            node = node.best_child()

        # 2. Expansion
        if not node.is_fully_expanded():
            node = node.expand()

        # 3. Simulation (Improved)
        simulation_state = node.state
        while not simulation_state.is_terminal():
            legal_moves = simulation_state.get_legal_moves()

            # Simple Heuristic: Block the opponent or win if possible
            if 4 in legal_moves:  # Prefer the center if available
                move = 4
            else:
                move = random.choice(legal_moves)

            simulation_state = simulation_state.make_move(move)

        # 4. Backpropagation
        winner = simulation_state.get_winner()
        while node:
            if winner == 0:  # Draw
                result = 0.5
            elif winner == node.parent.state.player if node.parent else 1:
                result = 1
            else:
                result = 0

            node.update(result)
            node = node.parent

    return root.best_child(exploration_constant=0).move

# Example Game Loop


def play_game():
    game = TicTacToe(player=-1)
    while not game.is_terminal():
        print_board(game.board)
        if game.player == 1:
            print("AI's Turn:")
            root = Node(game)
            move = mcts(root, iterations=1000)
        else:
            print("Your Turn:")
            move = int(input())

            while not game.is_legal_move(move):
                print("Illegal Move! Try Again:")
                print_board(game.board)
                move = int(input("Your Turn : "))

        game = game.make_move(move)

    winner = game.get_winner()
    if winner == 1:
        print("AI Wins!")
    elif winner == -1:
        print("Random Player Wins!")
    else:
        print("Draw!")

# Helper function to print the board


def print_board(board):
    symbols = {1: "X", -1: "O", 0: " "}

    cur = 0
    for i in range(3):
        for j in range(3):
          print(symbols[board[cur]], end="")
          if j < 2:
              print(" | ", end="")
          else:
              print()
          cur += 1
        if i < 2:
            print("-" * 9)


# Start the game
play_game()
