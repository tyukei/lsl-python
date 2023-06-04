#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from kivy.garden.matplotlib.backend_kivy import FigureCanvas

class GraphApp(App):
    """Matplotlib のグラフを表示するアプリケーション"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'Matplotlib graph on Kivy'

    def build(self):
        # メインの画面
        main_screen = BoxLayout()
        main_screen.orientation = 'vertical'

        # 上部にラベルを追加しておく
        label_text = 'The following is a graph of Matplotlib'
        label = Label(text=label_text)
        label.size_hint_y = 0.2
        main_screen.add_widget(label)

        # サイン波のデータを用意する
        x = np.linspace(-np.pi, np.pi, 100)
        y = np.sin(x)
        # 描画する領域を用意する
        fig, ax = plt.subplots()
        # プロットする
        ax.plot(x, y)
        # Figure#canvas をウィジェットとして追加する
        main_screen.add_widget(fig.canvas)

        return main_screen


def main():
    # アプリケーションを開始する
    app = GraphApp()
    app.run()


if __name__ == '__main__':
    main()