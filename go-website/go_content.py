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
            f'<circle cx="{x}" cy="{y}" r="11" fill="#ffe9a8" '
            f'stroke="#8a5a2b" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{x}" y="{y}" text-anchor="middle" '
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


def _svg_board19():
    """19 路棋盘示意图：标注 8 个星位（金点）与天元（红点）。"""
    size = 19
    cell = 15
    pad = 24
    W = pad * 2 + cell * (size - 1)
    parts = [
        f'<svg class="mini-board" viewBox="0 0 {W} {W}" role="img" aria-label="19路棋盘示意图">',
        f'<rect x="0" y="0" width="{W}" height="{W}" rx="12" fill="#eebf6f"/>',
    ]
    for i in range(size):
        y = pad + i * cell
        x = pad + i * cell
        parts.append(
            f'<line x1="{pad}" y1="{y}" x2="{pad + cell * (size - 1)}" y2="{y}" '
            f'stroke="#7a5a2e" stroke-width="1.1"/>'
        )
        parts.append(
            f'<line x1="{x}" y1="{pad}" x2="{x}" y2="{pad + cell * (size - 1)}" '
            f'stroke="#7a5a2e" stroke-width="1.1"/>'
        )
    # 8 个星位：四角星 + 四边星（都在三路线交叉点上）
    stars = [(3, 3), (3, 15), (15, 3), (15, 15), (3, 9), (9, 3), (9, 15), (15, 9)]
    for r, c in stars:
        x = pad + c * cell
        y = pad + r * cell
        parts.append(
            f'<circle cx="{x}" cy="{y}" r="4" fill="#c98f2e" '
            f'stroke="#8a5a2b" stroke-width="1"/>'
        )
    # 天元：棋盘正中央
    x = pad + 9 * cell
    y = pad + 9 * cell
    parts.append(f'<circle cx="{x}" cy="{y}" r="5.5" fill="#c0392b"/>')
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
_SVG_BOARD19 = _svg_board19()
# 禁着点：角上白棋大龙围住 × 点，黑下 × 无气且提不掉白棋（白棋外气仍在）
_SVG_FORBIDDEN = _svg_go_board(
    stones={
        (0, 1): "W", (1, 0): "W", (1, 1): "W", (1, 2): "W", (2, 1): "W",
        (0, 2): "B", (2, 0): "B",
    },
    marks={(0, 0): "×"},
)
# 劫争：黑子 (2,2) 只剩 1 口气 (3,2)；白 1 提黑后，黑不能马上在 ★ 位提回
_SVG_KO = _svg_go_board(
    stones={
        (2, 2): "B",
        (1, 2): "W", (2, 1): "W", (2, 3): "W",
        (3, 1): "B", (3, 3): "B", (4, 2): "B",
    },
    labels={(3, 2): "1"},
    marks={(2, 2): "★"},
)

# ---------------- 文章 ----------------
ARTICLES = [
    {
        "slug": "rules",
        "title": "围棋规则",
        "summary": "认识棋盘、了解基本规则和禁手，学会围棋的玩法。",
        "content": f"""<p class="lead">围棋是两人轮流在棋盘上落子的策略游戏：最后谁围住的“地盘”多，谁就赢。规则很简单，变化却无穷无尽。</p>

<h2>棋盘与棋子</h2>
<p>标准棋盘是 <strong>19 路 × 19 路</strong>，共有 <strong>361 个交叉点</strong>。棋子下在交叉点上（不是格子里）。黑棋先手，双方各执一色。</p>
<figure class="go-figure">
  {_SVG_BOARD19}
  <figcaption>19 路棋盘：四角、四边共 8 个<strong>星位</strong>（金点），正中央是<strong>天元</strong>（红点）。</figcaption>
</figure>
<p>棋盘位置有讲究：<strong>角</strong>（两条边交汇处）、<strong>边</strong>（一条边附近）、<strong>中央</strong>。角最“省钱”，所以高手布局总是先占角、再占边、最后才向中央发展。<strong>星位</strong>是占角时常用的起点（三路线交叉点），<strong>天元</strong>是棋盘正中心，也是最中央的位置。</p>

<h2>基本规则</h2>
<ol class="num-steps">
  <li><strong>轮流落子</strong>：黑先白后，一人一手，落子后不能移动。</li>
  <li><strong>下在空交叉点</strong>：不能下在已经有棋子的点上。</li>
  <li><strong>气尽提子</strong>：棋子的“气”被全部堵住时，必须立刻从棋盘上提掉（详见<a href="/learn/tizi">提子</a>）。</li>
  <li><strong>落子无悔</strong>：拿起来就生效，不能反悔重下。</li>
</ol>

<h2>禁手：有些棋不能下</h2>
<p>有几种落子是被<strong>禁止</strong>的，下了就是“禁着”（犯规）：</p>
<h3>① 禁着点：不能“自杀”</h3>
<p>如果落子之后，<strong>自己这颗棋子没有任何气</strong>，而且<strong>不能提掉对方任何棋子</strong>，这个点就是<strong>禁着点</strong>（也叫禁入点），不能下。</p>
<figure class="go-figure">
  {_SVG_FORBIDDEN}
  <figcaption>角上 × 处：黑棋下在这里自己没气，又提不掉白棋（白棋外面还有气），所以是禁着点。</figcaption>
</figure>
<h3>② 打劫：不能马上提回</h3>
<p>“打劫”是围棋最著名的特殊规则。如下图：黑子只剩 1 口气，白棋下 1 位可以提掉它；但黑棋<strong>不能立刻</strong>在 ★ 位把白子提回来，否则双方会无限循环。黑棋必须先在<strong>别处走一手</strong>（找劫材），等白棋应了之后，才能再提回。</p>
<figure class="go-figure">
  {_SVG_KO}
  <figcaption>劫争：白 1 提黑后，黑不能马上在 ★ 提回，须先在别处走一手。</figcaption>
</figure>
<p>初学者只要记住<strong>“不能马上提回”</strong>这一条就够了。</p>

<h2>终局与胜负</h2>
<p>双方都认为没有棋可下时对局结束（也可以认输）。最后<strong>围住交叉点（目）多的一方获胜</strong>。</p>
<ul class="num-steps">
  <li><strong>中国规则（数子法）</strong>：黑棋贴 3¾ 子，数棋盘上双方的子与空，黑 185 子以上胜。</li>
  <li><strong>日韩规则（数目法）</strong>：数双方围住的空，黑贴 6 目半或 7 目半。</li>
</ul>
<p>初学者不必纠结贴目细节，记住“<strong>谁的地盘大谁赢</strong>”就够了。</p>

<div class="tip-box">💡 下一步：先读懂<a href="/learn/qi">气</a>和<a href="/learn/tizi">提子</a>，然后去<a href="/problems">死活题闯关</a>练手吧！</div>""",
    },
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
        "title": "气",
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
