import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pylsl import resolve_byprop, StreamInlet
import numpy as np
import math

# Initialization function
def init():
    ax1.set_title('ACC')
    ax4.set_xlabel('Time 10s')
    ax1.set_xlim(xlim[0],xlim[1]) # x軸固定
    ax2.set_xlim(xlim[0],xlim[1]) # x軸固定
    ax3.set_xlim(xlim[0],xlim[1]) # x軸固定
    ax4.set_xlim(xlim[0],xlim[1]) # x軸固定
    # delete x axis 
    ax1.set_xticks([]) # 横軸の目盛りを削除
    ax2.set_xticks([]) # 横軸の目盛りを削除
    ax3.set_xticks([]) # 横軸の目盛りを削除
    ax4.set_xticks([]) # 横軸の目盛りを削除
    # delete y axis
    ax1.set_yticks([]) # 横軸の目盛りを削除
    ax2.set_yticks([]) # 横軸の目盛りを削除
    ax3.set_yticks([]) # 横軸の目盛りを削除
    ax4.set_yticks([]) # 横軸の目盛りを削除
    ax1.set_ylabel('ch1')
    ax2.set_ylabel('ch2')
    ax3.set_ylabel('ch3')
    ax4.set_ylabel('Magnitude')
    ax1r.set_yticks([])
    ax2r.set_yticks([])
    ax3r.set_yticks([])
    ax4r.set_yticks([])
    # 上と下の枠線を消す
    ax1.spines['bottom'].set_visible(False)
    ax1r.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2r.spines['top'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2r.spines['bottom'].set_visible(False)
    ax3.spines['top'].set_visible(False)
    ax3r.spines['top'].set_visible(False)
    ax3.spines['bottom'].set_visible(False)
    ax3r.spines['bottom'].set_visible(False)
    ax4.spines['top'].set_visible(False)
    ax4r.spines['top'].set_visible(False)
    # axの上下の間を詰める
    plt.subplots_adjust(hspace=0)


    return line1, line2, line3, linemag,

def convert_data(y):
    # 少数第２
    converted = y * 6.1035 * 10**-2
    converted = math.floor(converted * 100) / 100
    return converted

def magnitude_data(y1, y2, y3):
    magnitude = (y1**2 + y2**2 + y3**2)**0.5
    magnitude = math.floor(magnitude * 100) / 100
    return magnitude

# Stream data update function
def animate(i, ax1, ax2, ax3, ax4): 
    # Get the latest sample

    sample, timestamp = inlet.pull_sample()
    x = i/25
    y1 = convert_data(sample[0])
    y2 = convert_data(sample[1])
    y3 = convert_data(sample[2])
    magnitude = magnitude_data(y1, y2, y3)

    print(y1, y2, y3, magnitude)
    if(len(xdata) > 250):
        xlim[0]  = x-10
        xlim[1]  = x
        ax1.set_xlim(xlim[0], xlim[1])
        ax2.set_xlim(xlim[0], xlim[1])
        ax3.set_xlim(xlim[0], xlim[1])
        ax4.set_xlim(xlim[0], xlim[1])
        del xdata[0]
        del y1data[0]
        del y2data[0]
        del y3data[0]
        del ymagdata[0]
    if(i % 25 == 0) and (i != 0):
        ax1r.set_ylabel(f"{np.mean(y1data):.0f}mg")
        ax2r.set_ylabel(f"{np.mean(y2data):.0f}mg")
        ax3r.set_ylabel(f"{np.mean(y3data):.0f}mg")
        ax4r.set_ylabel(f"{np.mean(ymagdata):.0f}mg")
        ax1r.figure.canvas.draw()
        ax2r.figure.canvas.draw()
        ax3r.figure.canvas.draw()
        ax4r.figure.canvas.draw()
        ax1.set_ylim(np.min(y1data), np.max(y1data))
        ax2.set_ylim(np.min(y2data), np.max(y2data))
        ax3.set_ylim(np.min(y3data), np.max(y3data))
        ax4.set_ylim(np.min(ymagdata), np.max(ymagdata))
    xdata.append(x) 
    y1data.append(y1) 
    y2data.append(y2)
    y3data.append(y3)
    ymagdata.append(magnitude)
    line1.set_data(xdata, y1data)
    line2.set_data(xdata, y2data)
    line3.set_data(xdata, y3data)
    linemag.set_data(xdata, ymagdata)
    
    return line1, line2, line3, linemag,

def main():
    global xlim, xdata, y1data, y2data, y3data, ymagdata, inlet, ax1, ax1r, ax2r, ax2, ax3r, ax3, ax4r, ax4, line1, line2, line3, linemag
    xdata, y1data, y2data, y3data, ymagdata = [], [], [], [], []
    streams = resolve_byprop('type', 'ACC', timeout=2)
    inlet = StreamInlet(streams[0])
    xlim = [0, 10]
    # Create a new figure for the plot
    fig,(ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, sharex=True)
    ax1r = ax1.twinx()
    ax2r = ax2.twinx()
    ax3r = ax3.twinx()
    ax4r = ax4.twinx()
    line1, = ax1.plot([], [], label='X', color='red')
    line2, = ax2.plot([], [], label='Y', color='blue')
    line3, = ax3.plot([], [], label='Z', color='green')
    linemag, = ax4.plot([], [], label='Magnitude', color='black')
    # Create the animation
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=10000000, interval=40, blit=True, fargs=(ax1, ax2, ax3, ax4))


    # Show the plot
    # plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
