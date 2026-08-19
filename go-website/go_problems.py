# -*- coding: utf-8 -*-
"""围棋入门死活题

优先加载 go_problems.json 中的 1000 道经典死活题（来源：GoGameGuru 分级题库 + OGS Puzzles，
已统一为用户执白、裁剪居中到 9 路棋盘）；
如果 JSON 缺失或损坏，则回退到自动生成器（经典眼位形状旋转/翻转变体）。
"""

import json
import os
import random

BOARD_SIZE = 9
TOTAL_PROBLEMS = 200

# 每个基础形状：
#   shape: 眼位空点（局部坐标）
#   name:  中文名称
#   vital: 要点（可多个）
#   answer_b / answer_w: 原色方向下，黑先/白先的结果说明
BASE_SHAPES = [
    {
        "name": "直三",
        "shape": [(1, 1), (1, 2), (1, 3)],
        "vital": [(1, 2)],
        "answer_b": "直三：黑先走中间可做活。",
        "answer_w": "直三：白先点中间可杀黑。",
    },
    {
        "name": "弯三",
        "shape": [(1, 1), (2, 1), (2, 2)],
        "vital": [(2, 1)],
        "answer_b": "弯三：黑先走拐角要点可做活。",
        "answer_w": "弯三：白先点拐角要点可杀黑。",
    },
    {
        "name": "直四",
        "shape": [(1, 1), (1, 2), (1, 3), (1, 4)],
        "vital": [],
        "answer_b": "直四：已经活棋，黑不用补。",
        "answer_w": "直四：白也无法杀，黑已活。",
    },
    {
        "name": "弯四",
        "shape": [(1, 1), (2, 1), (2, 2), (2, 3)],
        "vital": [],
        "answer_b": "弯四：已经活棋，黑不用补。",
        "answer_w": "弯四：白也无法杀，黑已活。",
    },
    {
        "name": "方四",
        "shape": [(1, 1), (1, 2), (2, 1), (2, 2)],
        "vital": [],
        "answer_b": "方四：死棋，黑先也无法做活。",
        "answer_w": "方四：白随时可杀。",
    },
    {
        "name": "刀把五",
        "shape": [(1, 1), (1, 2), (1, 3), (2, 2), (3, 2)],
        "vital": [(2, 2)],
        "answer_b": "刀把五：黑先走中心要点可做活。",
        "answer_w": "刀把五：白先点中心要点可杀黑。",
    },
    {
        "name": "梅花五",
        "shape": [(1, 2), (2, 1), (2, 2), (2, 3), (3, 2)],
        "vital": [(2, 2)],
        "answer_b": "梅花五：黑先走中心可做活。",
        "answer_w": "梅花五：白先点中心可杀黑。",
    },
    {
        "name": "花六",
        "shape": [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)],
        "vital": [],
        "answer_b": "花六：眼位较大，黑已活棋。",
        "answer_w": "花六：白也难以杀黑。",
    },
]


def _empty_board():
    return [["." for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def _clone_board(board):
    return [row[:] for row in board]


def _rotate(board):
    n = len(board)
    return [[board[n - 1 - c][r] for c in range(n)] for r in range(n)]


def _flip_h(board):
    return [row[::-1] for row in board]


def _symmetries(board):
    """返回 8 个旋转/翻转变体。"""
    result = []
    current = _clone_board(board)
    for _ in range(4):
        result.append(_clone_board(current))
        result.append(_flip_h(current))
        current = _rotate(current)
    return result


def _shape_to_board(shape, offset_r=2, offset_c=2):
    """把局部眼位空点放到 9 路棋盘指定位置，四周用黑棋围住。"""
    points = [(r + offset_r, c + offset_c) for (r, c) in shape]
    board = _empty_board()

    min_r = min(r for r, _ in points) - 1
    max_r = max(r for r, _ in points) + 1
    min_c = min(c for _, c in points) - 1
    max_c = max(c for _, c in points) + 1

    for r in range(max(0, min_r), min(BOARD_SIZE, max_r + 1)):
        for c in range(max(0, min_c), min(BOARD_SIZE, max_c + 1)):
            if (r, c) not in points:
                board[r][c] = "B"
    return board


def _swap_colors(board):
    result = _clone_board(board)
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if result[r][c] == "B":
                result[r][c] = "W"
            elif result[r][c] == "W":
                result[r][c] = "B"
    return result


def _make_vital_map(vital, offset_r=2, offset_c=2):
    """生成要点标记棋盘，后续用和棋盘相同的变换保持坐标一致。"""
    board = _empty_board()
    for (r, c) in vital:
        rr = r + offset_r
        cc = c + offset_c
        if 0 <= rr < BOARD_SIZE and 0 <= cc < BOARD_SIZE:
            board[rr][cc] = "V"
    return board


def _extract_vital(vital_board):
    points = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if vital_board[r][c] == "V":
                points.append((r, c))
    return points


def _decorate_board(board, vital, seed):
    """在远离题目关键区域的位置添加背景棋子，增加题目外观差异。

    关键区域（已有棋子、要点及其附近）不会被改动，因此不影响题目答案。
    """
    rng = random.Random(seed)
    result = _clone_board(board)

    protected = set()
    anchors = list(vital)
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] != ".":
                anchors.append((r, c))

    for (ar, ac) in anchors:
        for dr in (-2, -1, 0, 1, 2):
            for dc in (-2, -1, 0, 1, 2):
                rr, cc = ar + dr, ac + dc
                if 0 <= rr < BOARD_SIZE and 0 <= cc < BOARD_SIZE:
                    protected.add((rr, cc))

    candidates = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if (r, c) not in protected and result[r][c] == ".":
                candidates.append((r, c))

    rng.shuffle(candidates)
    count = min(len(candidates), 3 + seed % 5)
    for i in range(count):
        r, c = candidates[i]
        result[r][c] = "W" if i % 2 == 0 else "B"
    return result


def render_board(board):
    lines = ["    A B C D E F G H I"]
    for r in range(BOARD_SIZE):
        row = f"{BOARD_SIZE - r:2d} "
        for c in range(BOARD_SIZE):
            ch = board[r][c]
            if ch == "B":
                ch = "●"
            elif ch == "W":
                ch = "○"
            else:
                ch = "·"
            row += ch + " "
        lines.append(row.rstrip())
    return "\n".join(lines)


def _answer_for(base, to_play, color_swapped):
    # 黑白互换后，轮到黑棋相当于原来轮到白棋，反之亦然
    role = to_play
    if color_swapped:
        role = "W" if to_play == "B" else "B"
    return base["answer_b"] if role == "B" else base["answer_w"]


def _build_problem_list():
    problems = []
    placements = [
        (2, 2), (0, 0), (0, 4), (4, 0), (4, 4),
        (0, 2), (4, 2), (2, 0), (2, 4), (1, 1), (3, 3),
    ]
    # 只使用有明确“要点”的形状，保证题目可以互动判断对错。
    # 题目统一为黑棋目标，用户执白棋进攻/点杀。
    interactive_shapes = [b for b in BASE_SHAPES if b["vital"]]
    for base in interactive_shapes:
        for offset_r, offset_c in placements:
            board = _shape_to_board(base["shape"], offset_r, offset_c)
            vital_map = _make_vital_map(base["vital"], offset_r, offset_c)
            board_syms = _symmetries(board)
            vital_syms = _symmetries(vital_map)
            for sym_board, sym_vital in zip(board_syms, vital_syms):
                vital_points = _extract_vital(sym_vital)
                if not vital_points:
                    continue
                decorated = _decorate_board(sym_board, vital_points, len(problems))
                problems.append({
                    "name": base["name"],
                    "to_play": "W",
                    "board": decorated,
                    "vital": vital_points,
                    "answer": base["answer_w"],
                })
                if len(problems) >= TOTAL_PROBLEMS:
                    return problems
    # 如果不足 200，循环补充
    while len(problems) < TOTAL_PROBLEMS:
        src = problems[len(problems) % len(problems)] if problems else None
        if src is None:
            break
        problems.append(dict(src))
    return problems


_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "go_problems.json")


def _load_json_problems():
    """优先加载外部 JSON 题库（经典死活题）；失败时回退到自动生成。"""
    try:
        with open(_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        problems = data if isinstance(data, list) else data.get("problems", [])
        if problems and all(
            "board" in p and "vital" in p and "to_play" in p for p in problems
        ):
            # JSON 中 vital 是 [r, c] 列表；转成 (r, c) 元组，
            # 否则 (r, c) in vital 中 元组 != 列表，永远判错。
            for p in problems:
                p["vital"] = [tuple(v) for v in p["vital"]]
            return problems
    except (OSError, ValueError):
        pass
    return None


PROBLEMS = _load_json_problems() or _build_problem_list()


def get_problem(n):
    if n < 1 or n > len(PROBLEMS):
        return None
    return PROBLEMS[n - 1]


def format_problem(n):
    p = get_problem(n)
    if p is None:
        return f"没有第 {n} 题，目前共有 {len(PROBLEMS)} 题。"

    player = "黑" if p["to_play"] == "B" else "白"
    board_text = render_board(p["board"])
    return (
        f"【死活题 {n}/{len(PROBLEMS)}】{p['name']}，{player}先\n\n"
        f"{board_text}\n\n"
        f"● 黑棋　○ 白棋　· 空点\n"
        f"请点击棋盘上的空点落子。"
    )


def format_answer(n):
    p = get_problem(n)
    if p is None:
        return "题目不存在。"
    return f"【第 {n} 题答案】\n{p['answer']}"


def total_problems():
    return len(PROBLEMS)
