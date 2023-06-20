import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import streamlit as st
import streamlit.components.v1 as components
from pylsl import resolve_byprop, StreamInlet

x, y = [], []

def setup_gui():
    st.title('XHRO LSL Viewer')
    selected_type = st.sidebar.selectbox('Type', ('ACC', 'BIOZ', 'EEG', 'OPT', 'TEMP'))
    scale = st.sidebar.number_input('Scale', min_value=0, max_value=1000, step=1, value=150)
    selected_filter = st.sidebar.selectbox('Filter', ('BP1', 'BP2'))
    ave_ref = st.sidebar.checkbox('Ave Ref')
    norm = st.sidebar.checkbox('Norm.')

def setup_graph():
    streams = resolve_byprop('type', 'ACC', timeout=2)
    inlet = StreamInlet(streams[0])
    fig = plt.figure()

    data = np.random.rand(2, 25)
    l, = plt.plot([], [], 'r-')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.xlabel('x')
    plt.title('test')
    line_ani = animation.FuncAnimation(fig, update_line, fargs=(inlet, l), interval=50, blit=True)
    components.html(line_ani.to_jshtml(), height=1000)

def update_line(num, inlet, line):
    sample, timestamp = inlet.pull_sample()
    if sample is None:  # No more samples available, append a placeholder value
        x.append(num)
        y.append(np.nan)
    else:
        x.append(num)
        y.append(sample[0])
    line.set_data(x, y)
    return line,


def main():
    setup_gui()
    setup_graph()

if __name__ == '__main__':
    main()
