import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
from pylsl import resolve_byprop, StreamInlet

WAIT_TIME_SECONDS = 0.04
x, y, y1 = [], [], []


def setup_gui():
    st.title('XHRO LSL Viewer')
    selected_type = st.sidebar.selectbox('Type', ('ACC', 'BIOZ', 'EEG', 'OPT', 'TEMP'))
    scale = st.sidebar.number_input('Scale', min_value=0, max_value=1000, step=1, value=150)
    selected_filter = st.sidebar.selectbox('Filter', ('BP1', 'BP2'))
    ave_ref = st.sidebar.checkbox('Ave Ref')
    norm = st.sidebar.checkbox('Norm.')
    ch1 = st.sidebar.checkbox('CH1')
    ch2 = st.sidebar.checkbox('CH2')
    ch3 = st.sidebar.checkbox('CH3')
    ch4 = st.sidebar.checkbox('CH4')

    streams = resolve_stream(selected_type)
    setup_graph(streams)

def resolve_stream(selected_type):
    type_mapping = {
        'ACC': 'ACC',
        'BIOZ': 'BIOZ',
        'EEG': 'EEG',
        'OPT': 'OPT',
        'TEMP': 'TEMP'
    }
    stream_type = type_mapping.get(selected_type, None)
    if stream_type:
        streams = resolve_byprop('type', stream_type, timeout=2)
        return streams
    else:
        return []
    
def setup_graph(streams):
    if len(streams) > 0:
        inlet = StreamInlet(streams[0])
        graph = st.empty()
        fig, (ax,ax1) = plt.subplots(nrows=2,sharex=True)
        i = 0
        while True:
            update(i, graph, inlet, fig, ax, ax1)
            i += 1


# アニメーションのフレーム更新関数
def update(i, graph, inlet, fig, ax, ax1):
    sample, timestamp = inlet.pull_sample()
    x.append(i*0.04)
    y.append(sample[0])
    y1.append(sample[1])

    if x[-1] > 10:
        del x[0]
        del y[0]
        del y1[0]

    if i % 25 == 0:
        ax.cla()
        ax.set_xlim(x[-1]-10, x[-1])
        ax.plot(x, y)
        ax1.cla()
        ax1.set_xlim(x[-1]-10, x[-1])
        ax1.plot(x, y1)
        graph.pyplot(fig)

    
    time.sleep(WAIT_TIME_SECONDS)



def main():
    setup_gui()

if __name__ == '__main__':
    main()