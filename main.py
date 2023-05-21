import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pylsl import StreamInlet, resolve_byprop
import pylsl as lsl
import sys
import select
import tkinter as tk
from tkinter import ttk
import threading


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
            if len(x) > 250:
                xlim[0] += 1
                xlim[1] += 1
            # データをプロット
            x.append(len(y1) * 0.04)  # 時間を0.04秒ごとに増加
            y1.append(sample[0])
            y2.append(sample[1])
            y3.append(sample[2])
            last_x = y1[-1]
            last_y = y2[-1]
            last_z = y3[-1]
            magnitude = (last_x**2 + last_y**2 + last_z**2) ** 0.5
            y4.append(magnitude)

            print(str(y1[-1]) + "\t" + str(y2[-1]) + "\t" + str(y3[-1])+ "\t" + str(y4[-1]))

            ax1.clear()
            ax1.set_xlim(xlim[0] * 0.04, xlim[1] * 0.04)
            ax1.set_ylabel('ACC X')
            ax1.plot(x, y1,color='red')
            ax2.clear()
            ax2.set_xlim(xlim[0] * 0.04, xlim[1] * 0.04)
            ax2.set_ylabel('ACC Y')
            ax2.plot(x, y2,color='green')
            ax3.clear()
            ax3.set_xlim(xlim[0] * 0.04, xlim[1] * 0.04)
            ax3.set_ylabel('ACC Z')
            ax3.plot(x, y3,color='blue')
            canvas.draw()
            ax4.clear()
            ax4.set_xlim(xlim[0] * 0.04, xlim[1] * 0.04)
            ax4.set_ylabel('ACC Magnitude')
            ax4.plot(x, y4,color="black")


def pause_thread():
    global pause
    pause = True


def resume_thread():
    global pause
    pause = False


    
def main():
    global streams, inlet, fig, xlim, x, y1, y2, y3, y4, running, pause, root, start_stop_button, quit_button, ax1, ax2, ax3, ax4, canvas

    # ストリームの解決
    streams = lsl.resolve_streams()
    # ストリームの種類の配列を生成
    stream_types = [stream.type() for stream in streams]


    # ストリームの情報を取得
    streams = resolve_byprop('type', 'EEG', timeout=2)
    if len(streams) == 0:
        print("ストリームが見つかりませんでした。")
        exit()
    # ストリームを選択
    inlet = StreamInlet(streams[0])

    # データを取得し、グラフで表示する
    fig = plt.figure()
    xlim = [0, 250]  # 横軸の範囲
    x = []
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    running = True  # グラフの継続フラグ
    pause = False

    # GUIの設定
    root = tk.Tk()
    root.geometry("1800x1000")  # 初期のウィンドウサイズ
    root.title("Real-time Graph")

# ドロップダウンメニュー
    stream_type_combobox = ttk.Combobox(root, values=stream_types, state="readonly")
    stream_type_combobox.pack(pady=10)
    stream_type_combobox.current(0)  # デフォルトの選択肢を設定
    start_stop_button = tk.Button(root, text='Stop', command=start_stop_button_click, bg='blue', fg='white',
                                  padx=10, pady=5, font=('Helvetica', 12, 'bold'))
    start_stop_button.pack(pady=10)

    quit_button = tk.Button(root, text='Quit', command=quit_button_click, bg='blue', fg='white',
                            padx=10, pady=5, font=('Helvetica', 12, 'bold'))
    quit_button.pack(pady=10)

    # サブプロットを作成
    ax1 = fig.add_subplot(411)
    ax2 = fig.add_subplot(412)
    ax3 = fig.add_subplot(413)
    ax4 = fig.add_subplot(414)

    # キャンバスを作成
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()
    canvas.get_tk_widget().configure(width=1500, height=800)
    fig.set_size_inches(15, 8)  # インチ単位で幅8インチ、高さ6インチに設定

    # 上下の枠を非表示にする
    ax1.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax3.spines['top'].set_visible(False)
    ax3.spines['bottom'].set_visible(False)
    ax4.spines['top'].set_visible(False)

    # サブプロット間の余白を調整
    plt.subplots_adjust(hspace=0)

    graph_thread = threading.Thread(target=update_graph)
    graph_thread.start()

    root.mainloop()

    stop_graph()
    graph_thread.join()


if __name__ == '__main__':
    main()
