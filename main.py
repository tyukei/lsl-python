import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pylsl import StreamInlet, resolve_byprop
import sys
import select
import tkinter as tk
import threading

# ストリームの情報を取得
streams = resolve_byprop('type', 'ACC', timeout=2)
if len(streams) == 0:
    print("ストリームが見つかりませんでした。")
    exit()
# ストリームを選択
inlet = StreamInlet(streams[0])

# データを取得し、グラフで表示する
fig = plt.figure()

x = []
y1 = []
y2 = []
y3 = []
running = True  # グラフの継続フラグ
pause = False

def stop_graph():
    global running
    running = False

def start_stop_button_click():
    global pause
    pause = not pause
    if not pause:
        start_stop_button.config(text='Stop')
        resume_thread()
    else:
        start_stop_button.config(text='Start')
        pause_thread()

def quit_button_click():
    stop_graph()
    root.quit()

def update_graph():
    while running:
        if not pause:
            # データを取得
            sample, timestamp = inlet.pull_sample()
            # データが欠損している場合はスキップ
            if sample is None:
                continue
            # データをプロット
            x.append(timestamp)
            y1.append(sample[0])
            y2.append(sample[1])
            y3.append(sample[2])
            # 横軸の範囲を制限する
            xmin = max(timestamp - 0.1, 0)  # 現在の時刻から0.1秒前までの範囲
            xmax = timestamp  # 現在の時刻
            ax1.set_xlim(xmin, xmax)
            ax2.set_xlim(xmin, xmax)
            ax3.set_xlim(xmin, xmax)
            ax1.clear()
            ax1.plot(x, y1)
            ax2.clear()
            ax2.plot(x, y2)
            ax3.clear()
            ax3.plot(x, y3)
            canvas.draw()


def pause_thread():
    global pause
    pause = True

def resume_thread():
    global pause
    pause = False

# GUIの設定
root = tk.Tk()
root.title("Real-time Graph")

# サブプロットを作成
ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)

# Figureを描画するためのキャンバスを作成
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# グラフの初期描画
ax1.plot(x, y1)
ax1.set_ylabel('Data 1')
ax2.plot(x, y2)
ax2.set_ylabel('Data 2')
ax3.plot(x, y3)
ax3.set_ylabel('Data 3')

# グラフ更新用スレッドの作成と開始
graph_thread = threading.Thread(target=update_graph)
graph_thread.start()

# ボタンを作成
start_stop_button = tk.Button(root, text='Stop', command=start_stop_button_click)
start_stop_button.pack()
quit_button = tk.Button(root, text='Quit', command=quit_button_click)
quit_button.pack()

# メインループ
root.mainloop()

# グラフが停止した後、スレッドを終了する
stop_graph()
graph_thread.join()