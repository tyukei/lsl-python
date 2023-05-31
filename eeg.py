import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pylsl import resolve_byprop, StreamInlet

# Initialization function
def init():
    ax.set_xlim(xlim[0],xlim[1]) # x軸固定
    ax.set_ylim(0, 1000000) # y軸固定
    line1, = ax.plot([], [], label='eeg 1')
    line2, = ax.plot([], [], label='eeg 2')
    ax.set_xticks([]) # 横軸の目盛りを削除
    ax.set_xlabel("Time 10sec") # x軸ラベル
    ax.set_title("EEG 250Hz", fontsize=15) # タイトルを追加
    ax.legend() # 凡例を追加
    return line1, line2,


# Stream data update function
def animate(i): 
    # Get the latest sample
    sample, timestamp = inlet.pull_sample()
    x = i/250
    y1 = sample[0]
    y2 = sample[1]
    print(y1, y2)
    if(len(xdata) > 2500):
        xlim[0]  = x-10
        xlim[1]  = x
        ax.set_xlim(xlim[0], xlim[1])
    xdata.append(x) 
    y1data.append(y1) 
    y2data.append(y2)
    # Update the 3 line
    line1.set_data(xdata, y1data)
    line2.set_data(xdata, y2data)
    return line1, line2, 

def main():
    global xlim, xdata, y1data, y2data, y3data, inlet, ax, line1, line2
    xdata, y1data, y2data, y3data = [], [], [], []
    streams = resolve_byprop('type', 'EEG', timeout=2)
    inlet = StreamInlet(streams[0])
    xlim = [0, 10]
    # Create a new figure for the plot
    fig,ax = plt.subplots()
    line1, = ax.plot([], [])
    line2, = ax.plot([], [])
    # Create the animation
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=None, interval=4, blit=True)

    # Show the plot
    plt.show()

if __name__ == '__main__':
    main()
