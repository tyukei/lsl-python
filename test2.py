import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
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
    # グラフ表示領域を取得
    graph = st.empty()
    # メインループ
    frame = 0
    while True:
        update(frame, graph, inlet)
        frame += 1

# アニメーションのフレーム更新関数
def update(frame, graph, inlet):
    # データ生成
    # x = np.linspace(0, 10, 100)
    # y = np.sin(x + frame / 10.0)
    sample, timestamp = inlet.pull_sample()
    if sample is None:  # No more samples available, append a placeholder value
        x.append(frame)
        y.append(np.nan)
    else:
        x.append(frame)
        y.append(sample[0])

    # グラフ描画
    fig, ax = plt.subplots()
    ax.plot(x, y)

    # グラフを表示
    graph.pyplot(fig)
    
    # 一時停止
    time.sleep(0.1)



def main():
    setup_gui()
    setup_graph()

if __name__ == '__main__':
    main()