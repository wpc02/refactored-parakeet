# -*- coding: utf-8 -*-
"""围棋入门学习网站"""

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

import go_content
import go_problems

app = Flask(__name__)
app.secret_key = "go-website-secret-2026"

LEVEL_SIZE = 5
TOTAL_LEVELS = go_problems.total_problems() // LEVEL_SIZE


def problem_level(n):
    return (n - 1) // LEVEL_SIZE + 1


def unlocked_level():
    return max(1, int(session.get("unlocked_level", 1)))


@app.route("/")
def index():
    return render_template("index.html", articles=go_content.ARTICLES, total=go_problems.total_problems())


@app.route("/learn/<slug>")
def article(slug):
    for item in go_content.ARTICLES:
        if item["slug"] == slug:
            return render_template("article.html", article=item)
    return redirect(url_for("index"))


@app.route("/problems")
def problems():
    levels = []
    for i in range(TOTAL_LEVELS):
        level = i + 1
        levels.append({
            "level": level,
            "start": (level - 1) * LEVEL_SIZE + 1,
            "end": min(level * LEVEL_SIZE, go_problems.total_problems()),
            "locked": level > unlocked_level(),
        })
    return render_template(
        "levels.html",
        levels=levels,
        unlocked=unlocked_level(),
        total_levels=TOTAL_LEVELS,
        help_html=go_content.SIHUO_HELP,
    )


@app.route("/levels")
def levels():
    return redirect(url_for("problems"))


@app.route("/problem/<int:n>")
def problem(n):
    p = go_problems.get_problem(n)
    if p is None:
        return redirect(url_for("problems"))

    if problem_level(n) > unlocked_level():
        return redirect(url_for("problems"))

    prev_n = n - 1 if n > 1 else None
    return render_template(
        "problem_v2.html",
        n=n,
        level=problem_level(n),
        p=p,
        board_text=go_problems.render_board(p["board"]),
        answer=go_problems.format_answer(n),
        prev_n=prev_n,
        total=go_problems.total_problems(),
    )


@app.route("/api/problem/<int:n>")
def api_problem(n):
    p = go_problems.get_problem(n)
    if p is None:
        return jsonify({"error": "not found"}), 404
    return jsonify({
        "id": n,
        "name": p["name"],
        "to_play": p["to_play"],
        "board": p["board"],
        "vital": p["vital"],
        "answer": p["answer"],
    })


@app.route("/api/problem/<int:n>/check", methods=["POST"])
def api_check(n):
    p = go_problems.get_problem(n)
    if p is None:
        return jsonify({"error": "not found"}), 404

    data = request.get_json(silent=True) or {}
    try:
        r = int(data.get("r", -1))
        c = int(data.get("c", -1))
    except (TypeError, ValueError):
        return jsonify({"error": "坐标无效"}), 400

    if not (0 <= r < go_problems.BOARD_SIZE and 0 <= c < go_problems.BOARD_SIZE):
        return jsonify({"error": "坐标无效"}), 400

    if p["board"][r][c] != ".":
        return jsonify({"error": "这个位置已经有棋子了"}), 400

    correct = any(r == vr and c == vc for vr, vc in p["vital"])

    level = problem_level(n)
    level_clear = False
    next_problem = None
    next_level = None

    if correct:
        if n < go_problems.total_problems():
            next_problem = n + 1
        if n % LEVEL_SIZE == 0 and level < TOTAL_LEVELS:
            level_clear = True
            next_level = level + 1
            session["unlocked_level"] = min(next_level, TOTAL_LEVELS)

    return jsonify({
        "correct": correct,
        "vital": p["vital"],
        "answer": p["answer"],
        "level": level,
        "level_clear": level_clear,
        "next_problem": next_problem,
        "next_level": next_level,
        "unlocked_level": unlocked_level(),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
