import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pylsl import resolve_byprop, StreamInlet
import numpy as np

# Initialization function
def init():
    ax1.set_xlim(xlim[0],xlim[1]) # x軸固定
    ax2.set_xlim(xlim[0],xlim[1]) # x軸固定
    ax3.set_xlim(xlim[0],xlim[1]) # x軸固定
    ax4.set_xlim(xlim[0],xlim[1]) # x軸固定
    # delte frame botton and top in graph
    ax1.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax3.spines['top'].set_visible(False)
    ax3.spines['bottom'].set_visible(False)
    ax4.spines['top'].set_visible(False)
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
    ax1.set_ylabel('1')
    ax2.set_ylabel('2')
    ax3.set_ylabel('3')
    ax4.set_ylabel('Magnitude')
    return line1, line2, line3, linemag,


# Stream data update function
def animate(i, ax1, ax2, ax3, ax4): 
    # Get the latest sample
    plt.cla()
    sample, timestamp = inlet.pull_sample()
    x = i/25
    y1 = sample[0]
    y2 = sample[1]
    y3 = sample[2]
    magnitude = (y1**2 + y2**2 + y3**2)**0.5
    print(y1, y2, y3, magnitude)

    if(len(xdata) > 250):
        xlim[0]  = x-10
        xlim[1]  = x
        ax1.set_xlim(xlim[0], xlim[1])
        ax2.set_xlim(xlim[0], xlim[1])
        ax3.set_xlim(xlim[0], xlim[1])
        ax4.set_xlim(xlim[0], xlim[1])
    xdata.append(x) 
    y1data.append(y1) 
    y2data.append(y2)
    y3data.append(y3)
    ymagdata.append(magnitude)
    line1.set_data(xdata, y1data)
    line2.set_data(xdata, y2data)
    line3.set_data(xdata, y3data)
    linemag.set_data(xdata, ymagdata)
    ax1.relim()
    ax1.autoscale_view()
    ax2.relim()
    ax2.autoscale_view()
    ax3.relim()
    ax3.autoscale_view()
    ax4.relim()
    ax4.autoscale_view()
    return line1, line2, line3, linemag,

def main():
    global xlim, xdata, y1data, y2data, y3data, ymagdata, inlet, ax1, ax2,ax3,ax4, line1, line2, line3, linemag
    xdata, y1data, y2data, y3data, ymagdata = [], [], [], [], []
    streams = resolve_byprop('type', 'ACC', timeout=2)
    inlet = StreamInlet(streams[0])
    xlim = [0, 10]
    # Create a new figure for the plot
    fig,(ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, sharex=True)
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
