import matplotlib
matplotlib.use('MacOSX')

import matplotlib.pyplot as plt
from pylsl import StreamInlet, resolve_byprop
import sys
import select

# ストリームの情報を取得
streams = resolve_byprop('type', 'ACC', timeout=2)
if len(streams) == 0:
    print("ストリームが見つかりませんでした。")
    exit()
# ストリームを選択
inlet = StreamInlet(streams[0])

# データを取得し、グラフで表示する
plt.ion()  # インタラクティブモードをオンにする
fig, ax = plt.subplots(1, 1)
x = []
y = []
running = True  # グラフの継続フラグ

def stop_graph():
    global running
    running = False

# キーボード入力を非同期で監視し、'q'が押されたらループを終了する
def keyboard_input():
    while running:
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            key = sys.stdin.readline().strip()
            if key == 'q':
                stop_graph()

# キーボード入力を非同期で監視するための設定
import threading
input_thread = threading.Thread(target=keyboard_input)
input_thread.daemon = True
input_thread.start()

while running:
    # データを取得
    sample, timestamp = inlet.pull_sample()
    # データが欠損している場合はスキップ
    if sample is None:
        continue
    # データをプロット
    x.append(timestamp)
    y.append(sample)
    ax.clear()
    ax.plot(x, y)
    plt.pause(0.001)

# グラフが停止した後、キーボード入力のスレッドを終了する
input_thread.join()
