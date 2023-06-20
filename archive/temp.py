
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pylsl import resolve_byprop, StreamInlet
import numpy as np
import math

# Initialization function
def init():
    ax.set_title('TEMP')
    ax.set_xlabel('Time 10s')
    ax.set_xlim(xlim[0],xlim[1]) # x軸固定
    ax.set_xticks([]) # 横軸の目盛りを削除
    axr.set_xticks([]) # 横軸の目盛りを削除
    ax.set_yticks([]) # 縦軸の目盛りを削除
    ax.set_ylabel('ch1')
    axr.set_yticks([]) # 縦軸の目盛りを削除
    return line1, 

def convert_data(y):
    converted = y * 0.005
    converted = math.floor(converted * 100) / 100
    return converted

# Stream data update function
def animate(i): 
    # Get the latest sample
    sample, timestamp = inlet.pull_sample()
    x = i
    y1 = math.floor(sample[0] * 100) / 100
    print(y1)
    if(len(xdata) > 10):
        xlim[0]  = x-10
        xlim[1]  = x
        ax.set_xlim(xlim[0], xlim[1])
        del xdata[0]
        del y1data[0]
    if x != 0:
        min = np.min(y1data)
        max = np.max(y1data)
        diff = max - min
        ax.set_ylim(min - diff * 0.1, max + diff * 0.1)
        ax.figure.canvas.draw()
        axr.set_ylabel(f"{np.mean(y1data):.2f}℃")
        axr.figure.canvas.draw()
    xdata.append(x) 
    y1data.append(y1) 
    # Update the 3 line
    line1.set_data(xdata, y1data)
    return line1,

def main():
    global xlim, xdata, y1data, inlet, ax, axr, line1
    xdata, y1data = [], []
    streams = resolve_byprop('type', 'TEMP', timeout=2)
    inlet = StreamInlet(streams[0])
    xlim = [0, 10]
    # Create a new figure for the plot
    fig,ax = plt.subplots()
    axr = ax.twinx()
    line1, = ax.plot([], [], color='red')
    # Create the animation
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=None, interval=1000, blit=True)

    # Show the plot
    plt.show()

if __name__ == '__main__':
    main()
