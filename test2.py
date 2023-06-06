import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
from pylsl import resolve_byprop, StreamInlet

WAIT_TIME_SECONDS = 0.04
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
    graph = st.empty()
    i = 0
    while True:
        update(i, graph, inlet)
        i += 1

# アニメーションのフレーム更新関数
def update(i, graph, inlet):
    sample, timestamp = inlet.pull_sample()
    x.append(i*0.04)
    y.append(sample[0])

    if x[-1] > 10:
        del x[0]
        del y[0]
    # グラフ描画
    fig, ax = plt.subplots()
    ax.set_xlim(x[-1]-10, x[-1])
    ax.plot(x, y)

    # グラフを表示
    graph.pyplot(fig)
    
    # 一時停止
    time.sleep(WAIT_TIME_SECONDS)



def main():
    setup_gui()
    setup_graph()

if __name__ == '__main__':
    main()