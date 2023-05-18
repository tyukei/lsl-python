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
xlim = [0,25] # 横軸の範囲
x = []
y1 = []
y2 = []
y3 = []
running = True  # グラフの継続フラグ
pause = False
start_time = None  # 最初のデータのタイムスタンプ

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
    global start_time
    while running:
        if not pause:
            # データを取得
            sample, timestamp = inlet.pull_sample()
            if start_time is None:
                start_time = timestamp
            # データが欠損している場合はスキップ
            if sample is None:
                continue
            if len(x) > 25:
                xlim[0] += 1
                xlim[1] += 1
            # データをプロット
            x.append(len(y1) * 0.04)  # 時間を0.04秒ごとに増加
            y1.append(sample[0])
            y2.append(sample[1])
            y3.append(sample[2])
            
            # xminとxmaxをprintする
            print("xmin:" + str(xlim[0] * 0.04) + "\txmax:" + str(xlim[1] * 0.04))
            # y1,y2,y3の最後の値をprintする
            print("y1:" + str(y1[-1]) + "\ty2:" + str(y2[-1]) + "\ty3:" + str(y3[-1]))
            
            ax1.clear()
            ax1.set_xlim(xlim[0] * 0.04, xlim[1] * 0.04)    
            ax1.plot(x, y1)
            ax2.clear()
            ax2.set_xlim(xlim[0] * 0.04, xlim[1] * 0.04)
            ax2.plot(x, y2)
            ax3.clear()
            ax3.set_xlim(xlim[0] * 0.04, xlim[1] * 0.04)
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

graph_thread = threading.Thread(target=update_graph)
graph_thread.start()

start_stop_button = tk.Button(root, text='Stop', command=start_stop_button_click)
start_stop_button.pack()
quit_button = tk.Button(root, text='Quit', command=quit_button_click)
quit_button.pack()

root.mainloop()

stop_graph()
graph_thread.join()
