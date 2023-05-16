import matplotlib
matplotlib.use('MacOSX')

import matplotlib.pyplot as plt
from pylsl import StreamInlet, resolve_byprop

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
while True:
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
