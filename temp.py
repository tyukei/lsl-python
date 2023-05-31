
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pylsl import resolve_byprop, StreamInlet

# Initialization function
def init():
    ax.set_xlim(xlim[0],xlim[1]) # x軸固定
    line1, = ax.plot([], [], label='temp', color='red')
    ax.set_xticks([]) # 横軸の目盛りを削除
    ax.set_yticks([]) # 縦軸の目盛りを削除
    ax.set_xlabel("Time 10sec") # x軸ラベル
    ax.set_title("TEMP 1Hz") # タイトルを追加
    ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0, fontsize=8)
    return line1, 


# Stream data update function
def animate(i): 
    # Get the latest sample
    sample, timestamp = inlet.pull_sample()
    x = i
    y1 = sample[0]
    print(y1)
    if(len(xdata) > 10):
        xlim[0]  = x-10
        xlim[1]  = x
        ax.set_xlim(xlim[0], xlim[1])
    xdata.append(x) 
    y1data.append(y1) 
    # Update the 3 line
    line1.set_data(xdata, y1data)
    ax.relim()
    ax.autoscale_view()
    return line1,

def main():
    global xlim, xdata, y1data, inlet, ax, line1
    xdata, y1data = [], []
    streams = resolve_byprop('type', 'TEMP', timeout=2)
    inlet = StreamInlet(streams[0])
    xlim = [0, 10]
    # Create a new figure for the plot
    fig,ax = plt.subplots()
    line1, = ax.plot([], [], color='red')
    # Create the animation
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=None, interval=1000, blit=True)

    # Show the plot
    plt.show()

if __name__ == '__main__':
    main()
