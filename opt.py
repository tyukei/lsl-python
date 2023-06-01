import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pylsl import resolve_byprop, StreamInlet

# Initialization function
def init():
    ax.set_xlim(xlim[0],xlim[1]) # x軸固定
    line1, = ax.plot([], [], label='1', color='red')
    line2, = ax.plot([], [], label='2', color='blue')
    line3, = ax.plot([], [], label='3', color='green')
    line4, = ax.plot([], [], label='4', color='yellow')
    ax.set_xticks([]) # 横軸の目盛りを削除
    ax.set_yticks([]) # 横軸の目盛りを削除
    ax.set_xlabel("Time 10sec") # x軸ラベル
    ax.set_title("OPT 50Hz") # タイトルを追加
    ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0, fontsize=8)
    return line1, line2,


# Stream data update function
def animate(i): 
    # Get the latest sample
    sample, timestamp = inlet.pull_sample()
    x = i/20
    y1 = sample[0]
    y2 = sample[1]
    y3 = sample[2]
    y4 = sample[3]
    print(y1, y2)
    if(len(xdata) > 200):
        xlim[0]  = x-10
        xlim[1]  = x
        ax.set_xlim(xlim[0], xlim[1])
    xdata.append(x) 
    y1data.append(y1) 
    y2data.append(y2)
    y3data.append(y3)
    y4data.append(y4)
    # Update the 3 line
    line1.set_data(xdata, y1data)
    line2.set_data(xdata, y2data)
    line3.set_data(xdata, y3data)
    line4.set_data(xdata, y4data)
    ax.relim()
    ax.autoscale_view()
    return line1, line2, line3, line4

def main():
    global xlim, xdata, y1data, y2data, y3data, y4data, inlet, ax, line1, line2, line3, line4
    xdata, y1data, y2data, y3data, y4data = [], [], [], [], []
    streams = resolve_byprop('type', 'OPT', timeout=2)
    inlet = StreamInlet(streams[0])
    xlim = [0, 10]
    # Create a new figure for the plot
    fig,ax = plt.subplots()
    line1, = ax.plot([], [], color='red')
    line2, = ax.plot([], [], color='blue')
    line3, = ax.plot([], [], color='green')
    line4, = ax.plot([], [], color='yellow')
    # Create the animation
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=None, interval=20, blit=True)

    # Show the plot
    plt.show()

if __name__ == '__main__':
    main()
