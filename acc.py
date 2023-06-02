import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pylsl import resolve_byprop, StreamInlet
import numpy as np

# Initialization function
def init():
    ax.set_xlim(xlim[0],xlim[1]) # x軸固定
    line1, = ax.plot([], [], label='X', color='red')
    line2, = ax.plot([], [], label='Y', color='blue')
    line3, = ax.plot([], [], label='Z', color='green')
    linemag, = ax.plot([], [], label='Magnitude', color='black')
    ax.set_title("ACC") # タイトルを初期化
    ax.set_xticks([]) # 横軸の目盛りを削除
    ax.set_yticks([]) # 縦軸の目盛りを削除
    ax.set_xlabel("Time 10sec")
    ax.set_ylabel("Acceleration")
    ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0, fontsize=8)
    return line1, line2, line3, linemag,


# Stream data update function
def animate(i): 
    # Get the latest sample
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
        ax.set_xlim(xlim[0], xlim[1])
    xdata.append(x) 
    y1data.append(y1) 
    y2data.append(y2)
    y3data.append(y3)
    mean1 = np.mean(y1)
    mean2 = np.mean(y2)
    mean3 = np.mean(y3)
    ymagdata.append(magnitude)
    # Update the 3 line
    line1.set_data(xdata, y1data)
    line2.set_data(xdata, y2data)
    line3.set_data(xdata, y3data)
    linemag.set_data(xdata, ymagdata)
    ax.axhline(mean1, color='r', linestyle='--', label='Mean 1')
    ax.axhline(mean2, color='g', linestyle='--', label='Mean 2')
    ax.axhline(mean3, color='b', linestyle='--', label='Mean 3')
    ax.relim()
    ax.autoscale_view()
    return line1, line2, line3, linemag,

def main():
    global xlim, xdata, y1data, y2data, y3data, ymagdata, inlet, ax, line1, line2, line3, linemag
    xdata, y1data, y2data, y3data, ymagdata = [], [], [], [], []
    streams = resolve_byprop('type', 'ACC', timeout=2)
    inlet = StreamInlet(streams[0])
    xlim = [0, 10]
    # Create a new figure for the plot
    fig,ax = plt.subplots()
    line1, = ax.plot([], [], color='red')
    line2, = ax.plot([], [], color='blue')
    line3, = ax.plot([], [], color='green')
    linemag, = ax.plot([], [], color='black')
    # Create the animation
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=None, interval=40, blit=True)

    # Show the plot
    plt.show()

if __name__ == '__main__':
    main()
