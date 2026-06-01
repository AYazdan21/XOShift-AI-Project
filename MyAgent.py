from typing import List, Optional, Tuple
import time
import math
import copy
from agent_utils import get_all_valid_moves

TIME_LIMIT = 1.6          # set this depending on the device
WIN_SCORE = 1_000_000
LOSS_SCORE = -1_000_000

NEAR_WIN_MY  = 65_000 #50_000     # my n-1 on an open line
NEAR_WIN_OPP = 50_000 #65_000     # opponent n-1 on an open line 


def agent_move(board: List[List[Optional[str]]], player_symbol: str) -> Tuple[int, int, int, int]:
    start_time = time.time()
    n = len(board)
    ME = player_symbol
    OP = 'O' if ME == 'X' else 'X'

    def apply_move_sim(bd: List[List[Optional[str]]],
                       mv: Tuple[int, int, int, int],
                       sym: str) -> List[List[Optional[str]]]:
        nb = copy.deepcopy(bd)
        sr, sc, tr, tc = mv
        if sr == tr:  # horizontal shift
            if tc < sc:
                for col_idx in range(sc, tc, -1):
                    nb[sr][col_idx] = nb[sr][col_idx - 1]
            else:
                for col_idx in range(sc, tc):
                    nb[sr][col_idx] = nb[sr][col_idx + 1]
        else:  # vertical shift
            if tr < sr:
                for row_idx in range(sr, tr, -1):
                    nb[row_idx][sc] = nb[row_idx - 1][sc]
            else:
                for row_idx in range(sr, tr):
                    nb[row_idx][sc] = nb[row_idx + 1][sc]
        nb[tr][tc] = sym
        return nb

    def check_winner_sim(bd: List[List[Optional[str]]]) -> Optional[str]:
        # rows
        for r in range(n):
            first = bd[r][0]
            if first is not None and all(bd[r][c] == first for c in range(n)):
                return first
        # cols
        for c in range(n):
            first = bd[0][c]
            if first is not None and all(bd[r][c] == first for r in range(n)):
                return first
        # main diag
        d0 = bd[0][0]
        if d0 is not None and all(bd[i][i] == d0 for i in range(n)):
            return d0
        # anti diag
        d1 = bd[0][n - 1]
        if d1 is not None and all(bd[i][n - 1 - i] == d1 for i in range(n)):
            return d1
        return None

    def _evaluate_line(line_vals: List[Optional[str]], me: str) -> int:
        opp = OP if me == ME else ME
        m = line_vals.count(me)
        o = line_vals.count(opp)
        nloc = len(line_vals)

        if m > 0 and o > 0:
            return 0
        
        if m == nloc:
            return WIN_SCORE
        if o == nloc:
            return LOSS_SCORE

        if m == nloc - 1 and o == 0:
            return NEAR_WIN_MY
        if o == nloc - 1 and m == 0:
            return -NEAR_WIN_OPP

        if o == 0 and m > 0:
            return 6 * (m * m)
        if m == 0 and o > 0:
            return -7 * (o * o)

        return 0

    def evaluate(bd: List[List[Optional[str]]], me: str) -> int:
        total = 0
        # rows & cols 
        for r in range(n):
            total += _evaluate_line(bd[r], me)
        for c in range(n):
            col = [bd[r][c] for r in range(n)]
            total += _evaluate_line(col, me)
        # diagonals
        main_d = [bd[i][i] for i in range(n)]
        anti_d = [bd[i][n - 1 - i] for i in range(n)]
        total += _evaluate_line(main_d, me)
        total += _evaluate_line(anti_d, me)

        # center bias 
        c = n // 2
        opp = OP if me == ME else ME
        if n % 2 == 1:
            if bd[c][c] == me: total += 10
            elif bd[c][c] == opp: total -= 10
        else:
            for r in (c - 1, c):
                for cc in (c - 1, c):
                    if bd[r][cc] == me: total += 5
                    elif bd[r][cc] == opp: total -= 5

        return total

    # alpha beta
    def next_sym(symbol: str) -> str:
        return OP if symbol == ME else ME

    def minimax(bd: List[List[Optional[str]]],
                depth: int,
                alpha: int,
                beta: int,
                is_maximizing: bool,
                cur_sym: str,
                root_sym: str) -> int:
        
        # time management
        if time.time() - start_time >= TIME_LIMIT:
            raise TimeoutError()

        # terminal check
        winner = check_winner_sim(bd)
        if winner == root_sym:
            return WIN_SCORE + depth  # prefer faster wins
        if winner is not None:
            return LOSS_SCORE - depth  # avoid slower losses

        if depth == 0:
            return evaluate(bd, root_sym)

        moves = get_all_valid_moves(bd, cur_sym)
        if not moves:
            return evaluate(bd, root_sym)

        # order by 1 ply eval (simulate once for score)
        ordered: List[Tuple[int, Tuple[int, int, int, int]]] = []
        for mv in moves:
            child_board_for_order = apply_move_sim(bd, mv, cur_sym)
            score = evaluate(child_board_for_order, root_sym)
            ordered.append((score, mv))
        ordered.sort(key=lambda x: x[0], reverse=is_maximizing)

        if is_maximizing:
            value = -math.inf
            for _, mv in ordered:
                if time.time() - start_time >= TIME_LIMIT:
                    raise TimeoutError()
                # Recompute child 
                child_board = apply_move_sim(bd, mv, cur_sym)
                child_val = minimax(child_board, depth - 1, alpha, beta, False,
                                    next_sym(cur_sym), root_sym)
                if child_val > value:
                    value = child_val
                if value > alpha:
                    alpha = value
                if beta <= alpha:
                    break
            return int(value)
        else:
            value = math.inf
            for _, mv in ordered:
                if time.time() - start_time >= TIME_LIMIT:
                    raise TimeoutError()
                # Recompute child 
                child_board = apply_move_sim(bd, mv, cur_sym)
                child_val = minimax(child_board, depth - 1, alpha, beta, True,
                                    next_sym(cur_sym), root_sym)
                if child_val < value:
                    value = child_val
                if value < beta:
                    beta = value
                if beta <= alpha:
                    break
            return int(value)

    valid_moves = get_all_valid_moves(board, ME)
    if not valid_moves:
        return (0, 0, 0, 0)
    if len(valid_moves) == 1:
        return valid_moves[0]

    # instant win check
    for mv in valid_moves:
        if check_winner_sim(apply_move_sim(board, mv, ME)) == ME:
            return mv

    # iterative deepening
    max_depth_caps = {3: 7, 4: 6, 5: 5}
    MAX_DEPTH = max_depth_caps.get(n, 5)
    depth = 3

    best_move = valid_moves[0]
    best_val = -math.inf
    prev_iter_time = 0.0

    while depth <= MAX_DEPTH:
        if (time.time() - start_time) + prev_iter_time >= TIME_LIMIT * 0.98:
            break
        try:
            alpha, beta = -math.inf, math.inf
            cur_best_mv = None
            cur_best_val = -math.inf

            # root ordering (simulate for score)
            root_scored: List[Tuple[int, Tuple[int, int, int, int]]] = []
            for mv in valid_moves:
                nb_for_order = apply_move_sim(board, mv, ME)
                root_scored.append((evaluate(nb_for_order, ME), mv))
            root_scored.sort(key=lambda x: x[0], reverse=True)

            iter_start = time.time()
            for _, mv in root_scored:
                if time.time() - start_time >= TIME_LIMIT:
                    raise TimeoutError()
                # Recompute child 
                nb = apply_move_sim(board, mv, ME)
                val = minimax(nb, depth - 1, alpha, beta, False, OP, ME)
                if val > cur_best_val:
                    cur_best_val = val
                    cur_best_mv = mv
                if cur_best_val > alpha:
                    alpha = cur_best_val
                if beta <= alpha:
                    break

            if cur_best_mv is not None:
                best_move = cur_best_mv
                best_val = cur_best_val

            prev_iter_time = time.time() - iter_start
            depth += 1

        except TimeoutError:
            break

    return best_move
