import time
import tkinter as tk
import turtle

# ウィンドウを作成
root = tk.Tk()
root.title("Real-time Graph")
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack()

# Turtleを作成
t = turtle.RawTurtle(canvas)

# グラフの描画設定
t.pensize(2)
t.speed(0)
t.up()
t.goto(-380, -280)
t.down()

# グラフを描画
for i in range(1000):
    # データを取得
    sample, timestamp = inlet.pull_sample()
    # データが欠損している場合はスキップ
    if sample is None:
        continue
    x, y, z = sample
    
    # データをプロット
    t.goto(i - 380, x * 100)
    t.goto(i - 380, y * 100)
    t.goto(i - 380, z * 100)

    time.sleep(0.01)  # グラフ更新のための待機時間

root.mainloop()
