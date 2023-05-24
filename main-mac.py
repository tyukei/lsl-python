import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pylsl import resolve_byprop, StreamInlet

# Create a new figure for the plot
fig,ax = plt.subplots()
line, = ax.plot([], [])
title = ax.set_title(None, fontsize=15) # タイトルを追加

# Initialization function
def init():
    ax.set_xlim(xlim[0],xlim[1]) # x軸固定
    ax.set_ylim(16000, 17000) # y軸固定
    line.set_data([], [])
    title.set_text("ACC") # タイトルを初期化
    ax.set_xticks([]) # 横軸の目盛りを削除
    ax.set_xlabel("Time 10sec")
    return line,


# Stream data update function
def animate(i): 
    # Get the latest sample
    sample, timestamp = inlet.pull_sample()
    x = i/25
    y = sample[0]
    if(len(xdata) > 250):
        xlim[0]  = x-10
        xlim[1]  = x
        ax.set_xlim(xlim[0], xlim[1])
    xdata.append(x) 
    ydata.append(y) 
    line.set_data(xdata, ydata)
    return line,

def main():
    global xlim, xdata, ydata, inlet
    xdata, ydata = [], []
    streams = resolve_byprop('type', 'ACC', timeout=2)
    inlet = StreamInlet(streams[0])
    xlim = [0, 10]

    # Create the animation
    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=None, interval=40, blit=True)

    # Show the plot
    plt.show()

if __name__ == '__main__':
    main()
