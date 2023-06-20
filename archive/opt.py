import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pylsl import resolve_byprop, StreamInlet
import numpy as np
import math

# Initialization function
def init():
    ax1.set_title('OPT 50Hz')
    ax5.set_xlabel('Time 10s')
    ax1.set_xlim(xlim[0],xlim[1]) # x軸固定
    ax2.set_xlim(xlim[0],xlim[1]) # x軸固定
    ax3.set_xlim(xlim[0],xlim[1]) # x軸固定
    ax4.set_xlim(xlim[0],xlim[1]) # x軸固定
    ax5.set_xlim(xlim[0],xlim[1]) # x軸固定
    # delete x axis
    ax1.set_xticks([]) # 横軸の目盛りを削除
    ax2.set_xticks([]) # 横軸の目盛りを削除
    ax3.set_xticks([]) # 横軸の目盛りを削除
    ax4.set_xticks([]) # 横軸の目盛りを削除
    ax5.set_xticks([]) # 横軸の目盛りを削除
    # delete y axis
    ax1.set_yticks([]) # 横軸の目盛りを削除
    ax2.set_yticks([]) # 横軸の目盛りを削除
    ax3.set_yticks([]) # 横軸の目盛りを削除
    ax4.set_yticks([]) # 横軸の目盛りを削除
    ax5.set_yticks([]) # 横軸の目盛りを削除
    ax1.set_ylabel('ch1')
    ax2.set_ylabel('ch2')
    ax3.set_ylabel('ch3')
    ax4.set_ylabel('ch4')
    ax5.set_ylabel('magnitude')
    ax1r.set_yticks([]) # 縦軸の目盛りを削除
    ax2r.set_yticks([]) # 縦軸の目盛りを削除
    ax3r.set_yticks([]) # 縦軸の目盛りを削除
    ax4r.set_yticks([]) # 縦軸の目盛りを削除
    ax5r.set_yticks([]) # 縦軸の目盛りを削除
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
    ax4.spines['bottom'].set_visible(False)
    ax4r.spines['bottom'].set_visible(False)
    ax5.spines['top'].set_visible(False)
    ax5r.spines['top'].set_visible(False)
    plt.subplots_adjust(hspace=0)
    return line1, line2, line3, line4, line5

def convert_data(y):
    y = math.floor(y * 100) / 100
    return y
def magnitude_data(y1, y2, y3, y4):
    magnitude = (y1**2 + y2**2 + y3**2 + y4**2)**0.5
    magnitude = math.floor(magnitude * 100) / 100
    return magnitude

# Stream data update function
def animate(i): 
    # Get the latest sample
    sample, timestamp = inlet.pull_sample()
    x = i/20
    y1 = convert_data(sample[0])
    y2 = convert_data(sample[1])
    y3 = convert_data(sample[2])
    y4 = convert_data(sample[3])
    y5 = magnitude_data(y1, y2, y3, y4)
    print(y1, y2, y3, y4, y5)
    if(len(xdata) > 200):
        xlim[0]  = x-10
        xlim[1]  = x
        ax1.set_xlim(xlim[0], xlim[1])
        ax2.set_xlim(xlim[0], xlim[1])
        ax3.set_xlim(xlim[0], xlim[1])
        ax4.set_xlim(xlim[0], xlim[1])
        ax5.set_xlim(xlim[0], xlim[1])
        del xdata[0]
        del y1data[0]
        del y2data[0]
        del y3data[0]
        del y4data[0]
        del y5data[0]
    if i % 20 == 0 and i != 0:
        ax1r.set_ylabel(f"{np.mean(y1data):.0f}")
        ax2r.set_ylabel(f"{np.mean(y2data):.0f}")
        ax3r.set_ylabel(f"{np.mean(y3data):.0f}")
        ax4r.set_ylabel(f"{np.mean(y4data):.0f}")
        ax5r.set_ylabel(f"{np.mean(y5data):.0f}")
        ax1r.figure.canvas.draw()
        ax2r.figure.canvas.draw()
        ax3r.figure.canvas.draw()
        ax4r.figure.canvas.draw()
        ax5r.figure.canvas.draw()
        ax1.set_ylim(np.min(y1data), np.max(y1data))
        ax2.set_ylim(np.min(y2data), np.max(y2data))
        ax3.set_ylim(np.min(y3data), np.max(y3data))
        ax4.set_ylim(np.min(y4data), np.max(y4data))
        ax5.set_ylim(np.min(y5data), np.max(y5data))
    xdata.append(x) 
    y1data.append(y1) 
    y2data.append(y2)
    y3data.append(y3)
    y4data.append(y4)
    y5data.append(y5)
    # Update the 3 line
    line1.set_data(xdata, y1data)
    line2.set_data(xdata, y2data)
    line3.set_data(xdata, y3data)
    line4.set_data(xdata, y4data)
    line5.set_data(xdata, y5data)
    return line1, line2, line3, line4, line5

def main():
    global xlim, xdata, y1data, y2data, y3data, y4data, y5data, inlet, ax1, ax2, ax3, ax4, ax5, ax1r, ax2r, ax3r, ax4r, ax5r, line1, line2, line3, line4, line5
    xdata, y1data, y2data, y3data, y4data, y5data = [], [], [], [], [], []
    streams = resolve_byprop('type', 'OPT', timeout=2)
    inlet = StreamInlet(streams[0])
    xlim = [0, 10]
    # Create a new figure for the plot
    fig,(ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, figsize=(10, 6))
    ax1r = ax1.twinx()
    ax2r = ax2.twinx()
    ax3r = ax3.twinx()
    ax4r = ax4.twinx()
    ax5r = ax5.twinx()
    line1, = ax1.plot([], [], color='over red')
    line2, = ax2.plot([], [], color='red')
    line3, = ax3.plot([], [], color='green')
    line4, = ax4.plot([], [], color='brew')
    line5, = ax5.plot([], [], color='black')
    # Create the animation
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=None, interval=20, blit=True)

    # Show the plot
    plt.show()

if __name__ == '__main__':
    main()
