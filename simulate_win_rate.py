import importlib.util
import sys
import random
from game import XOShiftGame
from agent_utils import get_all_valid_moves
from sample_agent import agent_move as random_agent_move

def load_agent(path: str, func_name: str = "agent_move"):
    """
    Dynamically load a Python file at `path` which defines `agent_move`.
    Returns the function.
    """
    spec = importlib.util.spec_from_file_location("custom_agent", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["custom_agent"] = module
    spec.loader.exec_module(module)
    return getattr(module, func_name)

# Load your agent from your file
my_agent_move = load_agent("402243113.py")


def play_game(agent_X, agent_O, size=5, max_turns=250):
    """
    Plays one game on a size x size board.
    agent_X and agent_O are functions(board, symbol) -> (sr,sc,tr,tc).
    Returns winner symbol: 'X', 'O', or 'Draw'.
    """
    game = XOShiftGame(size=size)
    turns = 0
    while not game.winner and turns < max_turns:
        player = game.current_player
        board_copy = [row.copy() for row in game.board]
        if player == 'X':
            sr, sc, tr, tc = agent_X(board_copy, 'X')
        else:
            sr, sc, tr, tc = agent_O(board_copy, 'O')

        valid = game.apply_move(sr, sc, tr, tc, player)
        # if invalid move, immediate loss
        if not valid:
            return 'O' if player == 'X' else 'X'

        turns += 1
        if not game.winner:
            game.switch_player()

    return game.winner or 'Draw'


def simulate_games(num_games=100, board_size=5):
    results = {'X': 0, 'O': 0, 'Draw': 0}

    for i in range(num_games):
        # alternate who goes first
        if i % 2 == 0:
            winner = play_game(my_agent_move, random_agent_move, size=board_size)
        else:
            winner = play_game(random_agent_move, my_agent_move, size=board_size)
            # flip so your agent's wins always counted under 'X'
            if winner == 'O':
                winner = 'X'
            elif winner == 'X':
                winner = 'O'

        results[winner] += 1
        print(f"Game {i+1}: Winner = {winner}")

    total = num_games
    print("\n=== Results ===")
    print(f"Your agent wins:   {results['X']} / {total}  ({results['X']/total*100:.1f}%)")
    print(f"Random agent wins: {results['O']} / {total}  ({results['O']/total*100:.1f}%)")
    print(f"Draws:             {results['Draw']} / {total}  ({results['Draw']/total*100:.1f}%)")


if __name__ == "__main__":
    simulate_games(num_games=100, board_size=5)
