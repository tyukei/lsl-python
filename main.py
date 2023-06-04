import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

from kivy.app import App
from kivy.garden.matplotlib import FigureCanvasKivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from pylsl import resolve_byprop, StreamInlet


class MyApp(App):
    def start_animation(self):
        xdata, y1data, y2data, y3data, ymagdata = [], [], [], [], []
        streams = resolve_byprop('type', 'ACC', timeout=2)
        inlet = StreamInlet(streams[0])
        xlim = [0, 10]
        # Create a new figure for the plot
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, sharex=True)
        ax1r = ax1.twinx()
        ax2r = ax2.twinx()
        ax3r = ax3.twinx()
        ax4r = ax4.twinx()
        line1, = ax1.plot([], [], label='X', color='red')
        line2, = ax2.plot([], [], label='Y', color='blue')
        line3, = ax3.plot([], [], label='Z', color='green')
        linemag, = ax4.plot([], [], label='Magnitude', color='black')
        # Create the animation
        anim = animation.FuncAnimation(fig, self.run_animation, init_func=self.init,
                                       frames=10000000, interval=40, blit=True,
                                       fargs=(ax1, ax2, ax3, ax4, xdata, y1data, y2data, y3data,
                                              ymagdata, inlet, xlim, ax1r, ax2r, ax3r, ax4r,
                                              line1, line2, line3, linemag))

        plt.show()

    def init(self):
        return []

    def run_animation(self, i, ax1, ax2, ax3, ax4, xdata, y1data, y2data, y3data, ymagdata, inlet,
                      xlim, ax1r, ax2r, ax3r, ax4r, line1, line2, line3, linemag):
        sample, timestamp = inlet.pull_sample()
        x = i / 25
        y1 = sample[0]
        y2 = sample[1]
        y3 = sample[2]
        magnitude = (y1 ** 2 + y2 ** 2 + y3 ** 2) ** 0.5
        print(y1, y2, y3, magnitude)
        label1 = ax1r.set_ylabel(f"{np.mean(y1data):.0f}")
        ax2r.set_ylabel(f"{np.mean(y2data):.0f}")
        ax3r.set_ylabel(f"{np.mean(y3data):.0f}")
        ax4r.set_ylabel(f"{np.mean(ymagdata):.0f}")
        ax1r.figure.canvas.draw()
        ax2r.figure.canvas.draw()
        ax3r.figure.canvas.draw()
        ax4r.figure.canvas.draw()
        if len(xdata) > 250:
            xlim[0] = x - 10
            xlim[1] = x
            ax1.set_xlim(xlim[0], xlim[1])
            ax2.set_xlim(xlim[0], xlim[1])
            ax3.set_xlim(xlim[0], xlim[1])
            ax4.set_xlim(xlim[0], xlim[1])
        xdata.append(x)
        y1data.append(y1)
        y2data.append(y2)
        y3data.append(y3)
        ymagdata.append(magnitude)
        line1.set_data(xdata, y1data)
        line2.set_data(xdata, y2data)
        line3.set_data(xdata, y3data)
        linemag.set_data(xdata, ymagdata)
        ax1.relim()
        ax1.autoscale_view()
        ax2.relim()
        ax2.autoscale_view()
        ax3.relim()
        ax3.autoscale_view()
        ax4.relim()
        ax4.autoscale_view()

        return line1, line2, line3, linemag

    def build(self):
        canvas = FigureCanvasKivy(fig)
        anim = animation.FuncAnimation(fig, run_animation, init_func=init,
                                    frames=10000000, interval=40, blit=True)

        layout = AnchorLayout(anchor_x='left', anchor_y='top', padding=(10, 10))

        # Dropdown menu
        dropdown = DropDown()
        streams = resolve_byprop('type', 'ACC', timeout=2)
        if streams == []:
            btn = Button(text='No stream found', size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        else:
            for stream in streams:
                btn = Button(text=stream.name(), size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn: dropdown.select(btn.text))
                dropdown.add_widget(btn)

        # Main button
        main_button = Button(text='Select Stream', size_hint=(None, None), width=500, height=100)
        def on_dropdown_select(instance, text):
            main_button.text = text
            self.start_animation()

        # Bind dropdown to main button
        dropdown.bind(on_select=lambda instance, x: setattr(main_button, 'text', x))

        main_button.bind(on_release=dropdown.open)

        layout.add_widget(main_button)
        layout.add_widget(canvas)

        return layout


if __name__ == '__main__':
    MyApp().run()

