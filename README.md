# XOShift

A strategic twist on Tic-Tac-Toe where players shift pieces along the board's rim to create winning lines. Built with Python and Pygame, XOShift features AI agent battles, replay analysis, and customizable board sizes.

![XOShift Game](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-Required-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎮 Game Overview

XOShift reimagines classic Tic-Tac-Toe with a unique shifting mechanic. Instead of simply placing pieces, players select cells from the board's rim and shift them to opposite edges, creating dynamic gameplay where the board state constantly evolves.

### Core Rules

- **Board Sizes**: 3×3, 4×4, or 5×5 grids
- **Win Condition**: Complete a full row, column, or diagonal (N-in-a-row for N×N board)
- **Movement**: Select a rim cell and shift it to an opposite edge
  - If empty rim cells exist, you **must** select an empty cell
  - If no empty rim cells exist, you **must** select your own piece
- **Shifting Mechanics**: When you shift a piece, all cells between the source and target slide in that direction
- **Turn Limit**: Games end in a draw after 250 turns

## 🚀 Features

- **Multiple Game Modes**
  - Human vs Human
  - Human vs AI Agent
  - AI Agent vs AI Agent
  - Replay Viewer
  
- **AI Agent System**
  - Load custom AI agents from Python files
  - Time-limited agent execution (2.2 seconds per move)
  - Multiprocessing support for safe agent execution
  - Sample random agent included

- **Replay System**
  - Automatic game recording in JSON format
  - Step-through replay viewer with forward/backward navigation
  - Metadata tracking (board size, players, winner)

- **Win Rate Simulator**
  - Test your AI agent against opponents
  - Automated batch game simulation
  - Statistical analysis of agent performance

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- Pygame library

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/XOShift.git
cd XOShift
```

2. Install dependencies:
```bash
pip install pygame
```

3. Run the game:
```bash
python main.py
```

## 🎯 How to Play

### Human vs Human Mode

1. Launch the game and select board size (3×3, 4×4, or 5×5)
2. Choose "Human vs Human" mode
3. Click on a valid rim cell to select it (highlighted in yellow)
4. Click on a valid target edge to complete your move
5. The game alternates between X and O players

### Playing Against AI

1. Select "Human vs Agent" or "Agent vs Human" mode
2. Place your agent file (e.g., `MyAgent.py`) in the XOShift directory
3. The AI will automatically make moves within the time limit

### Agent vs Agent Mode

Watch two AI agents battle it out! Perfect for testing and comparing agent strategies.

## 🤖 Creating Your Own AI Agent

Create a Python file with an `agent_move` function:

```python
from typing import List, Optional, Tuple
from agent_utils import get_all_valid_moves

def agent_move(board: List[List[Optional[str]]], player_symbol: str) -> Tuple[int, int, int, int]:
    """
    Your AI agent logic here.
    
    Args:
        board: 2D list representing the game board (None for empty cells)
        player_symbol: Your symbol ('X' or 'O')
    
    Returns:
        Tuple of (src_row, src_col, target_row, target_col)
    """
    # Get all valid moves
    valid_moves = get_all_valid_moves(board, player_symbol)
    
    # Implement your strategy here
    # ...
    
    return src_row, src_col, target_row, target_col
```

### Agent Utilities

The `agent_utils.py` module provides helper functions:

- `get_possible_selections(board, player_symbol)`: Returns valid source cells
- `get_all_valid_moves(board, player_symbol)`: Returns all legal moves as tuples

### Testing Your Agent

Use the win rate simulator to evaluate your agent:

```bash
python simulate_win_rate.py
```

Edit `simulate_win_rate.py` to specify:
- Your agent file path
- Number of games to simulate
- Board size
- Opponent agent

The simulator alternates starting positions and provides detailed statistics.

## 📁 Project Structure

```
XOShift/
├── main.py                  # Main game loop and orchestration
├── game.py                  # Core game logic and rules
├── ui.py                    # Pygame UI rendering and interaction
├── agent_loader.py          # Dynamic agent loading system
├── agent_utils.py           # Helper functions for AI agents
├── sample_agent.py          # Example random agent
├── simulate_win_rate.py     # Agent testing and evaluation
├── utils.py                 # General utilities
├── assets/
│   └── Alegreya-Regular.otf # Font file
└── replays/                 # Saved game replays (JSON)
```

## 🎬 Replay System

Games can be recorded and replayed:

1. Enable "Record Replay" when starting a game
2. Replays are saved to `replays/` directory with format:
   ```
   xo_{size}_{mode}_{timestamp}.json
   ```
3. Use "Replay" mode to load and view saved games
4. Navigate with on-screen controls or keyboard

### Replay File Format

```json
{
    "metadata": {
        "board_size": 5,
        "game_mode": "agent-agent",
        "player_x_type": "my_agent",
        "player_o_type": "sample_agent",
        "winner": "X"
    },
    "moves": [
        {
            "player": "X",
            "src_r": 0,
            "src_c": 2,
            "tgt_r": 4,
            "tgt_c": 2
        }
    ]
}
```

## 🧠 Strategy Tips

- **Control the Center**: Shifting pieces through the center creates more winning opportunities
- **Block Diagonals**: Diagonal wins are harder to defend against
- **Force Moves**: When the rim is full, your opponent must move their own pieces
- **Think Ahead**: Consider how shifts affect multiple rows/columns simultaneously
- **Empty Rim Priority**: Remember you must select empty rim cells when available

## 🛠️ Technical Details

### Agent Execution

- Agents run in separate processes for isolation
- 2.2-second time limit per move
- Invalid moves result in immediate loss
- Exceptions are caught and handled gracefully

### Performance

- Maximum 250 turns per game to prevent infinite loops
- Efficient move validation
- Optimized board state copying for agents

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Additional AI agent strategies
- Enhanced UI features
- Network multiplayer support
- Tournament mode
- Advanced replay analysis tools
- Performance optimizations

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Pygame](https://www.pygame.org/)
- Font: Alegreya by Juan Pablo del Peral
- Inspired by classic Tic-Tac-Toe with a strategic twist

## 📧 Contact

For questions, suggestions, or bug reports, please open an issue on GitHub.

---


