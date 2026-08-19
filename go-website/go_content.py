# -*- coding: utf-8 -*-
"""围棋入门知识文章内容（网站版）"""


def _svg_go_board(size=7, cell=38, stones=None, labels=None, marks=None):
    """生成小型棋盘 SVG 示意图（用于文章中图文并茂）。

    stones: {(r, c): 'B' | 'W'} 棋子
    labels: {(r, c): '1'}       气点/数字标记（画在交叉点上方的小圆里）
    marks:  {(r, c): '×' | '★'} 红色重点标记
    """
    stones = stones or {}
    labels = labels or {}
    marks = marks or {}
    pad = 30
    W = pad * 2 + cell * (size - 1)
    parts = [
        f'<svg class="mini-board" viewBox="0 0 {W} {W}" role="img" aria-label="棋盘示意图">',
        f'<rect x="0" y="0" width="{W}" height="{W}" rx="12" fill="#eebf6f"/>',
    ]
    for i in range(size):
        y = pad + i * cell
        x = pad + i * cell
        parts.append(
            f'<line x1="{pad}" y1="{y}" x2="{pad + cell * (size - 1)}" y2="{y}" '
            f'stroke="#7a5a2e" stroke-width="1.2"/>'
        )
        parts.append(
            f'<line x1="{x}" y1="{pad}" x2="{x}" y2="{pad + cell * (size - 1)}" '
            f'stroke="#7a5a2e" stroke-width="1.2"/>'
        )
    for (r, c), text in labels.items():
        x = pad + c * cell
        y = pad + r * cell
        parts.append(
            f'<circle cx="{x}" cy="{y - cell * 0.34}" r="11" fill="#ffe9a8" '
            f'stroke="#8a5a2b" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{x}" y="{y - cell * 0.34}" text-anchor="middle" '
            f'dominant-baseline="central" font-size="13" font-weight="bold" '
            f'fill="#6b421d">{text}</text>'
        )
    for (r, c), color in stones.items():
        x = pad + c * cell
        y = pad + r * cell
        rpx = cell * 0.42
        parts.append(f'<circle cx="{x}" cy="{y + 2}" r="{rpx}" fill="rgba(0,0,0,0.25)"/>')
        if color == "B":
            parts.append(f'<circle cx="{x}" cy="{y}" r="{rpx}" fill="#262626"/>')
            parts.append(
                f'<circle cx="{x - rpx * 0.3}" cy="{y - rpx * 0.3}" r="{rpx * 0.22}" '
                f'fill="rgba(255,255,255,0.35)"/>'
            )
        else:
            parts.append(
                f'<circle cx="{x}" cy="{y}" r="{rpx}" fill="#fbfbfb" '
                f'stroke="#444" stroke-width="1"/>'
            )
            parts.append(
                f'<circle cx="{x - rpx * 0.3}" cy="{y - rpx * 0.3}" r="{rpx * 0.2}" '
                f'fill="#ffffff"/>'
            )
    for (r, c), text in marks.items():
        x = pad + c * cell
        y = pad + r * cell
        parts.append(
            f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="central" '
            f'font-size="{cell * 0.55}" fill="#c0392b" font-weight="bold">{text}</text>'
        )
    parts.append("</svg>")
    return "".join(parts)


# ---------------- 示意图素材 ----------------
_SVG_QI_CENTER = _svg_go_board(
    stones={(3, 3): "B"},
    labels={(2, 3): "1", (4, 3): "2", (3, 2): "3", (3, 4): "4"},
)
_SVG_QI_EDGE = _svg_go_board(
    stones={(0, 3): "B"},
    labels={(1, 3): "1", (0, 2): "2", (0, 4): "3"},
)
_SVG_QI_CORNER = _svg_go_board(
    stones={(0, 0): "B"},
    labels={(0, 1): "1", (1, 0): "2"},
)
_SVG_QI_TWO = _svg_go_board(
    stones={(3, 3): "B", (3, 4): "B"},
    labels={(2, 3): "1", (4, 3): "2", (2, 4): "3", (4, 4): "4", (3, 2): "5", (3, 5): "6"},
)
_SVG_TIZI_BEFORE = _svg_go_board(
    stones={(3, 3): "W", (2, 3): "B", (4, 3): "B", (3, 2): "B"},
    labels={(3, 4): "1"},
)
_SVG_TIZI_AFTER = _svg_go_board(
    stones={(2, 3): "B", (4, 3): "B", (3, 2): "B", (3, 4): "B"},
    marks={(3, 3): "×"},
)
_SVG_SIHUO = _svg_go_board(
    stones={
        (1, 2): "B", (1, 3): "B", (1, 4): "B",
        (3, 2): "B", (3, 3): "B", (3, 4): "B",
        (2, 1): "B", (2, 5): "B",
    },
    marks={(2, 3): "★"},
)

# ---------------- 文章 ----------------
ARTICLES = [
    {
        "slug": "tizi",
        "title": "围棋入门：什么是提子",
        "summary": "把对方棋子的气全部堵住，就能把棋子从棋盘上提掉。",
        "content": f"""<p class="lead">“提子”就是<strong>吃掉对方棋子</strong>：把对方棋子所有的“气”都堵住，就能把它从棋盘上拿掉。</p>

<h2>第一步：认识“气”</h2>
<p>一颗棋子的“气”，是它<strong>上下左右</strong>紧挨着的<strong>空交叉点</strong>。气就像棋子的“生命值”，气没了，棋子就要被提走。</p>
<figure class="go-figure">
  {_SVG_QI_CENTER}
  <figcaption>中央一颗黑子有 4 口气：上面 1、下面 2、左面 3、右面 4。</figcaption>
</figure>

<h2>第二步：把气全部堵住 = 提子</h2>
<p>用你的棋子把对方的气<strong>一格一格占住</strong>。当最后一口气也被占住时，对方这颗棋子就“没气了”，必须立刻从棋盘上拿走——这就是<strong>提子</strong>。</p>
<div class="fig-row">
  <figure class="go-figure">
    {_SVG_TIZI_BEFORE}
    <figcaption>白子被围住，只剩 1 口气（数字 1）。</figcaption>
  </figure>
  <figure class="go-figure">
    {_SVG_TIZI_AFTER}
    <figcaption>最后 1 口气被黑子占住，白子被提掉（×）。</figcaption>
  </figure>
</div>

<h2>三个要点</h2>
<ol class="num-steps">
  <li><strong>气 = 上下左右</strong>相邻的空点，<em>斜对角不算气</em>。</li>
  <li>几颗连在一起的棋子要<strong>当成一整块</strong>，数整块外围的气。</li>
  <li>落子后如果对方没气了，<strong>必须先提掉对方棋子</strong>。</li>
</ol>

<div class="tip-box">💡 小知识：对方只剩一口气时叫做<strong>“叫吃”</strong>。这时对方通常会逃跑或补棋，你可以选择继续追击。</div>

<h2>自己动手试试</h2>
<p>在棋盘上摆一颗白子，用黑子把它的上下左右都围住，然后亲手把它拿掉——这就是提子！</p>""",
    },
    {
        "slug": "qi",
        "title": "围棋的“气”怎么看",
        "summary": "一颗棋子的气，就是它上下左右相邻的交叉点。",
        "content": f"""<p class="lead">“气”是围棋里衡量棋子的“生命值”。学会数气，才能看懂提子、死活和整盘棋。</p>

<h2>一颗棋子的气</h2>
<p>一颗棋子的气 = 它<strong>上下左右</strong>紧挨着的<strong>空交叉点</strong>。棋子放的位置不同，气也不一样：</p>
<div class="fig-row">
  <figure class="go-figure">
    {_SVG_QI_CENTER}
    <figcaption>棋盘中央：4 口气</figcaption>
  </figure>
  <figure class="go-figure">
    {_SVG_QI_EDGE}
    <figcaption>棋盘边上：3 口气</figcaption>
  </figure>
  <figure class="go-figure">
    {_SVG_QI_CORNER}
    <figcaption>棋盘角上：2 口气</figcaption>
  </figure>
</div>

<h2>数气的步骤</h2>
<ol class="num-steps">
  <li>先找到目标棋子（或一整块棋）。</li>
  <li>看它<strong>上、下、左、右</strong>四个方向。</li>
  <li>数一数还有多少个<strong>空交叉点</strong>。</li>
  <li>连在一起的棋子当成<strong>一整块</strong>，数整块外围的气。</li>
</ol>

<h2>连在一起的棋子，气要合起来数</h2>
<p>两颗棋子“手拉手”连在一起时，要当成一整块来看，数这一整块外围的气：</p>
<figure class="go-figure">
  {_SVG_QI_TWO}
  <figcaption>两颗连子一共有 6 口气（1~6），比单独两颗棋子加起来少 2 口气。</figcaption>
</figure>

<div class="tip-box">💡 记住：<strong>斜对角不是气</strong>。只有上下左右紧挨着的空点才算气。</div>

<h2>自己动手试试</h2>
<p>先摆一颗子数它的气；再在旁边连一颗，数整块的气；最后用对方棋子把气堵光，看看“提子”是怎么发生的。</p>""",
    },
]

# ---------------- 死活题说明（闯关页问号弹窗用） ----------------
SIHUO_HELP = f"""<p class="help-lead">死活题就是“局部小战斗”：判断一块棋能不能活、能不能杀死对方，并找出<strong>最关键的一手</strong>。</p>
<figure class="go-figure">
  {_SVG_SIHUO}
  <figcaption>直三：要点在中间（★）。点中要点，棋就能活（或被杀）。</figcaption>
</figure>
<ul class="help-list">
  <li><strong>你执白棋</strong>，每题由你先落一子；</li>
  <li><strong>单击</strong>落子预览，<strong>双击</strong>落子并直接提交；</li>
  <li>落在“要点”上即答对，弹窗会显示正解要点与参考手顺；</li>
  <li>每关 5 题，答对最后一题自动解锁下一关。</li>
</ul>""";
