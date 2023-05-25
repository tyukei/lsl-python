import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pylsl import resolve_byprop, StreamInlet

# Initialization function
def init():
    ax.set_xlim(xlim[0],xlim[1]) # x軸固定
    ax.set_ylim(-1000, 20000) # y軸固定
    line1, = ax.plot([], [], label='acc X')
    line2, = ax.plot([], [], label='acc Y')
    line3, = ax.plot([], [], label='acc Z')
    ax.set_title("ACC") # タイトルを初期化
    ax.set_xticks([]) # 横軸の目盛りを削除
    ax.set_xlabel("Time 10sec")
    ax.legend() # 凡例を追加
    return line1, line2, line3, 


# Stream data update function
def animate(i): 
    # Get the latest sample
    sample, timestamp = inlet.pull_sample()
    x = i/25
    y1 = sample[0]
    y2 = sample[1]
    y3 = sample[2]
    print(y1, y2, y3)
    if(len(xdata) > 250):
        xlim[0]  = x-10
        xlim[1]  = x
        ax.set_xlim(xlim[0], xlim[1])
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
    global xlim, xdata, y1data, y2data, y3data, inlet, ax, line1, line2, line3
    xdata, y1data, y2data, y3data = [], [], [], []
    streams = resolve_byprop('type', 'ACC', timeout=2)
    inlet = StreamInlet(streams[0])
    xlim = [0, 10]
    # Create a new figure for the plot
    fig,ax = plt.subplots()
    line1, = ax.plot([], [])
    line2, = ax.plot([], [])
    line3, = ax.plot([], [])
    # Create the animation
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=None, interval=40, blit=True)

    # Show the plot
    plt.show()

if __name__ == '__main__':
    main()