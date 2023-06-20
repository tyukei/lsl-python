import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pylsl import resolve_byprop, StreamInlet
import numpy as np
import math

TYPE = 'ACC'
CHNEEL = 3
axs = []
ax2s = []
xlim = [0, 10]
xdata = []
ysdata = [[]]
grapphs = []

# Initialization function
def init():
    for ax in axs:
        ax.set_xlim(xlim[0],xlim[1]) # x軸固定
        ax.set_xticks([]) # 横軸の目盛りを削除
        ax.set_yticks([]) # 縦軸の目盛りを削除
        ax.spines['bottom'].set_visible(False) # 下の枠線を消す
        ax.spines['top'].set_visible(False) # 上の枠線を消す
    for ax in ax2s:
        ax.set_xlim(xlim[0],xlim[1])
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['bottom'].set_visible(False)
        ax.spines['top'].set_visible(False)
    plt.subplots_adjust(hspace=0)
    
def convert_data(y):
    # 少数第２
    converted = y * 6.1035 * 10**-2
    converted = math.floor(converted * 100) / 100
    return converted

def magnitude_data(y1, y2, y3):
    magnitude = (y1**2 + y2**2 + y3**2)**0.5
    magnitude = math.floor(magnitude * 100) / 100
    return magnitude

def animate(i, inlet):
    sample, timestamp = inlet.pull_sample()
    x = i/25
    y1 = convert_data(sample[0])
    y2 = convert_data(sample[1])
    y3 = convert_data(sample[2])
    y4 = magnitude_data(y1, y2, y3)
    ys = [y1, y2, y3, y4]
    print(x, y1, y2, y3, y4)
    if x >= xlim[1]:
        for ax in axs:
            ax.set_xlim(x-xlim[1], x)
        for ax in ax2s:
            ax.set_xlim(x-xlim[1], x)
    if x % 1 == 0 and x != 0: 
        for ax in ax2s:
            ax.set_ylabel(f"{np.mean(ys[ax2s.index(ax)])}mg")
        for ax in ax2s:
            ax.figure.canvas.draw()
        for ax in axs:
            ax.set_ylim(min(ysdata[axs.index(ax)])-0.1, max(ysdata[axs.index(ax)])+0.1)
            ax.figure.canvas.draw()
    xdata.append(x)
    for i, y in enumerate(ys):
        ysdata[i].append(y)
        grapphs[i].set_data(xdata, ysdata[i])
    return grapphs[1], grapphs[2], grapphs[3], grapphs[4]

    
def main():
    streams = resolve_byprop('type', TYPE, timeout=2)
    inlet = StreamInlet(streams[0])
    fig, axs = plt.subplots(CHNEEL+1, 1, figsize=(10, 10))
    for ax in axs:
        ax2s.append(ax.twinx())
        grapphs.append(ax.plot([], [], lw=2)[0])
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=40, blit=True, fargs=(inlet))
    plt.show()

if __name__ == "__main__":
    main()

    