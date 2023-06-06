import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pylsl import resolve_byprop, StreamInlet
import numpy as np


def run_app():
    fig, ax = plt.subplots()
    x = []
    y = []
    line, = ax.plot([], [], label='sin', color='red')

    def init():
        ax.set_xlim(0, 2*np.pi)
        ax.set_ylim(-1, 1)
        line.set_data([], [])
        return line,

    def animate(i):
        x.append(i)
        y.append(np.sin(i))
        line.set_data(x, y)
        return line,
    ani = animation.FuncAnimation(fig, animate,init_func=init, frames=10000000, interval=40, blit=True)
    components.html(ani.to_jshtml(), height=1000)


def main():
    st.title('XHRO LSL Viewer')
    selected_type = st.selectbox('Type', ('ACC', 'BIOZ', 'EEG', 'OPT', 'TEMP'))
    scale = st.number_input('Scale', min_value=0, max_value=1000, step=1, value=150)
    selected_filter = st.selectbox('Filter', ('BP1', 'BP2'))
    ave_ref = st.checkbox('Ave Ref')
    norm = st.checkbox('Norm.')
    zero_mean = st.checkbox('Zero mean')
    run_app()

if __name__ == '__main__':
    main()
