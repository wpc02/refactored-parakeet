# 围棋入门学习网站

## 功能

- 围棋入门知识：
  - 什么是提子
  - 围棋的“气”怎么看
  - 死活题练习说明
- 1000 道经典死活题，200 关闯关
  - 题库来源：GoGameGuru 分级死活题（入门 130 题 + 中级 70 题）+ OGS Puzzles（800 题，https://online-go.com/puzzles），
    经 https://github.com/akitaonrails/frank_go 转存，许可证 CC BY-NC-SA 4.0（非商业用途）
  - 原题均为黑先，已统一黑白互换为用户执白；棋盘裁剪居中到 9 路
  - 题目数据保存在 `go_problems.json`（缺失时回退为程序自动生成题）
  - 每关 5 题，未解锁关卡显示加锁，不能点击
  - 可互动：点击棋盘落子
  - 双击落子并直接提交
  - 答对/答错都弹窗提示
  - 答对弹窗内提供“下一题”按钮
  - 写实风格棋子
  - 答错可重来

## 公网部署

快速测试：运行 `公网穿透-cloudflared.bat`，可获得临时公网地址。
长期部署：参考 `部署到公网.md`。

## 启动

```bat
cd /d "C:\deepseek  harness\weiqi\go-website"
C:\Python\python.exe -m pip install -r requirements.txt
C:\Python\python.exe app.py
```

或双击 `start-go-website.bat`。

打开浏览器访问：

```text
http://127.0.0.1:8080
```

## 目录

```text
go-website
├─ app.py
├─ go_content.py
├─ go_problems.py
├─ go_problems.json   ← 1000 道经典死活题题库
├─ templates
│  ├─ base.html
│  ├─ index.html
│  ├─ article.html
│  ├─ problems.html
│  └─ problem.html
├─ static
│  └─ style.css
├─ requirements.txt
├─ start-go-website.bat
└─ README.md
```
