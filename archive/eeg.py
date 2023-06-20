import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pylsl import resolve_byprop, StreamInlet
import numpy as np
import math

# Initialization function
def init():
    # title
    ax1.set_title('EEG 250Hz')
    ax3.set_xlabel('Time 10s')
    ax1.set_xlim(xlim[0],xlim[1]) # x軸固定
    ax2.set_xlim(xlim[0],xlim[1]) # x軸固定
    ax3.set_xlim(xlim[0],xlim[1]) # x軸固定
    ax1.set_xticks([]) # 横軸の目盛りを削除
    ax2.set_xticks([]) # 横軸の目盛りを削除
    ax3.set_xticks([]) # 横軸の目盛りを削除
    ax1.set_yticks([]) # 横軸の目盛りを削除
    ax2.set_yticks([]) # 横軸の目盛りを削除
    ax3.set_yticks([]) # 横軸の目盛りを削除
    ax1.set_ylabel('ch1')
    ax2.set_ylabel('ch2')
    ax3.set_ylabel('ch1 - ch2')
    ax1r.set_yticks([])
    ax2r.set_yticks([])
    ax3r.set_yticks([])
    # 上と下の枠線を消す
    ax1.spines['bottom'].set_visible(False)
    ax1r.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2r.spines['top'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2r.spines['bottom'].set_visible(False)
    ax3.spines['top'].set_visible(False)
    ax3r.spines['top'].set_visible(False)
    plt.subplots_adjust(hspace=0)
    return line1, line2, line3,

def convert_data(y):
    converted = y * ((2*4.5 // 24) // 0x1000000) * 1000 * 1000
    converted = math.floor(converted * 100) / 100
    return converted

def magnitude_data(y1, y2):
    magnitude = y1 - y2
    return magnitude

# Stream data update function
def animate(i): 
    # Get the latest sample
    sample, timestamp = inlet.pull_sample()
    x = i/250
    y1 = convert_data(sample[0])
    y2 = convert_data(sample[1])
    y3 = magnitude_data(y1, y2)
    print(y1, y2, y3)
    if(len(xdata) > 2500):
        xlim[0]  = x-10
        xlim[1]  = x
        ax1.set_xlim(xlim[0], xlim[1])
        ax2.set_xlim(xlim[0], xlim[1])
        ax3.set_xlim(xlim[0], xlim[1])
        del xdata[0]
        del y1data[0]
        del y2data[0]
        del y3data[0]
    if i % 250 == 0:
        ax1r.set_ylabel(f"{np.mean(y1data):.0f}μV")
        ax2r.set_ylabel(f"{np.mean(y2data):.0f}μV")
        ax3r.set_ylabel(f"{np.mean(y3data):.0f}μV")
        ax1r.figure.canvas.draw()
        ax2r.figure.canvas.draw()
        ax3r.figure.canvas.draw()
        ax1.set_ylim(np.min(y1data), np.max(y1data))
        ax2.set_ylim(np.min(y2data), np.max(y2data))
        ax3.set_ylim(np.min(y3data), np.max(y3data))
    xdata.append(x) 
    y1data.append(y1) 
    y2data.append(y2)
    y3data.append(y3)
    # Update the 3 line
    line1.set_data(xdata, y1data)
    line2.set_data(xdata, y2data)
    line3.set_data(xdata, y3data)
    return line1, line2, line3,

def main():
    global xlim, xdata, y1data, y2data, y3data, inlet, ax1, ax1r, ax2, ax2r, ax3, ax3r, line1, line2, line3
    xdata, y1data, y2data, y3data = [], [], [], []
    streams = resolve_byprop('type', 'EEG', timeout=2)
    inlet = StreamInlet(streams[0])
    xlim = [0, 10]
    # Create a new figure for the plot
    fig,(ax1, ax2, ax3) = plt.subplots(nrows=3, sharex=True)
    ax1r = ax1.twinx()
    ax2r = ax2.twinx()
    ax3r = ax3.twinx()
    line1, = ax1.plot([], [], color='red')
    line2, = ax2.plot([], [], color='blue')
    line3, = ax3.plot([], [], color='green')
    # Create the animation
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=None, interval=4, blit=True)

    # Show the plot
    plt.show()

if __name__ == '__main__':
    main()
