import copy
import random

# --- Helper ---
def ops_color(color):
    return "b" if color == "w" else "w"


def evaluate_fast(game_map):
    black = 0
    white = 0
    for color in game_map.vertices_colors:
        if color == "b":
            black += 1
        elif color == "w":
            white += 1
    return black - white

# --- Territory-based evaluation ---
def evaluate(game_map,fast=False):
    if fast:
        return evaluate_fast(game_map)
    temp_map = game_map.copy_graph()

    count_list = [0 for _ in range(len(temp_map.vertices))]

    for i in range(len(count_list)):
        if count_list[i] != 0:
            continue

        if temp_map.vertices_colors[i] == "e":
            comp = temp_map.find_componnent(i)
            neighbors = temp_map.find_negihbors_of_list(comp)

            if neighbors == []:
                comp_color = "e"
            else:
                comp_color = temp_map.vertices_colors[neighbors[0]]

            for v in neighbors:
                if temp_map.vertices_colors[v] != comp_color:
                    comp_color = "e"

            for v in comp:
                count_list[v] = comp_color

        else:
            count_list[i] = temp_map.vertices_colors[i]

    black = 0
    white = 0

    for val in count_list:
        if val == "b":
            black += 1
        elif val == "w":
            white += 1

    return black - white


# --- Legal moves (includes PASS) ---
def get_legal_moves(game_map, turn, enable_pass=False):
    moves = []

    for i in range(len(game_map.vertices)):
        if game_map.vertices_colors[i] != "e":
            continue

        temp_map = game_map.copy_graph()

        temp_map.vertices_colors[i] = turn
        temp_map.kill(ops_color(turn))

        before = temp_map.vertices_colors[:]
        temp_map.kill(turn)

        # suicide
        if before != temp_map.vertices_colors:
            continue

        # ko
        if temp_map.vertices_colors in game_map.history:
            continue

        moves.append(i)

    if enable_pass:
        score = evaluate(game_map)
        pass_conditions = False

        # Pass if not losing
        if (turn == "b" and score >= 0) or (turn == "w" and score <= 0):
            pass_conditions = True

        # Pass if winning and previous player passed

        if pass_conditions:
            moves.append(None)
    else:
        # When smart_pass is False, always consider pass as a possible move
        moves.append(None)

    return moves


# --- Apply move ---
def apply_move(game_map, move, turn):
    new_map = game_map.copy_graph()

    if move is None:
        # PASS
        new_map.history.append(new_map.vertices_colors[:])
        return new_map

    new_map.vertices_colors[move] = turn
    new_map.kill(ops_color(turn))
    new_map.history.append(new_map.vertices_colors[:])

    return new_map


# --- Alpha-Beta ---

def alphabeta(game_map, depth, alpha, beta, turn, maximizing_player, fast_eval, enable_pass=False):
    #random.seed(42)  # Seed for reproducible random choices
    if depth == 0:
        return evaluate(game_map, fast_eval), None
    if ((enable_pass) and (len(game_map.history) > 1)) and game_map.history[-1] == game_map.history[-2]:
        if (turn == "b" and evaluate(game_map) > 0) or (turn == "w" and evaluate(game_map) < 0):
            return evaluate(game_map, fast_eval), None

    moves = get_legal_moves(game_map, turn, enable_pass)
    random.shuffle(moves)

    if not moves:
        return evaluate(game_map, fast_eval), None

    best_moves = []

    if maximizing_player:
        max_eval = -float("inf")

        for move in moves:
            new_map = apply_move(game_map, move, turn)

            eval_score, _ = alphabeta(
                new_map,
                depth - 1,
                alpha,
                beta,
                ops_color(turn),
                False,
                fast_eval,
                enable_pass
            )

            if eval_score > max_eval:
                max_eval = eval_score
                best_moves = [move]
            #elif eval_score == max_eval:
                #best_moves.append(move)

            alpha = max(alpha, eval_score)

            if beta <= alpha:
                break

        return max_eval, random.choice(best_moves)

    else:
        min_eval = float("inf")

        for move in moves:
            new_map = apply_move(game_map, move, turn)

            eval_score, _ = alphabeta(
                new_map,
                depth - 1,
                alpha,
                beta,
                ops_color(turn),
                True,
                fast_eval,
                enable_pass
            )

            if eval_score < min_eval:
                min_eval = eval_score
                best_moves = [move]
            #elif eval_score == min_eval:
                #best_moves.append(move)

            beta = min(beta, eval_score)

            if beta <= alpha:
                break

        return min_eval, random.choice(best_moves)

# --- Bot interface ---
def bot_move(game_map, turn, depth=3, fast_eval=False, smart_pass=False):
    _, move = alphabeta(
        game_map,
        depth,
        -float("inf"),
        float("inf"),
        turn,
        maximizing_player=(turn == "b"),
        fast_eval=fast_eval,
        enable_pass=smart_pass
    )
    return move