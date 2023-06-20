from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from subprocess import Popen
import pylsl
from kivy.clock import Clock

class DataProcessingApp(App):
    def build(self):
        # ルートとなるBoxLayout
        self.root_layout = BoxLayout(orientation='vertical')

        # テキストを配置するAnchorLayout
        self.text_layout = AnchorLayout(anchor_x='center', anchor_y='center')

        # ボタンを配置するBoxLayout
        self.button_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.acc_button = Button(text='ACC', size_hint=(0.2, 1))
        self.acc_button.bind(on_release=self.run_acc)
        self.button_layout.add_widget(self.acc_button)

        self.bioz_button = Button(text='BIOZ', size_hint=(0.2, 1))
        self.bioz_button.bind(on_release=self.run_bioz)
        self.button_layout.add_widget(self.bioz_button)

        self.eeg_button = Button(text='EEG', size_hint=(0.2, 1))
        self.eeg_button.bind(on_release=self.run_eeg)
        self.button_layout.add_widget(self.eeg_button)

        self.temp_button = Button(text='TEMP', size_hint=(0.2, 1))
        self.temp_button.bind(on_release=self.run_temp)
        self.button_layout.add_widget(self.temp_button)

        self.temp_button = Button(text='OPT', size_hint=(0.2, 1))
        self.temp_button.bind(on_release=self.run_opt)
        self.button_layout.add_widget(self.temp_button)

        self.root_layout.add_widget(self.text_layout)
        self.root_layout.add_widget(self.button_layout)

        # 初回のリロードを実行
        self.reload_streams()

        # タイマーを設定して定期的にリロードを実行
        Clock.schedule_interval(lambda dt: self.reload_streams(), 5)

        return self.root_layout

    def reload_streams(self):
        streams = pylsl.resolve_streams()
        if streams == []:
            self.text_layout.clear_widgets()
            label = Label(text='No stream found', font_size=50)
            self.text_layout.add_widget(label)
            self.button_layout.opacity = 0  # ボタンを非表示にする
        else:
            self.text_layout.clear_widgets()
            label = Label(text=streams[0].name(), font_size=50)
            self.text_layout.add_widget(label)
            self.button_layout.opacity = 1  # ボタンを表示する

    def run_acc(self, instance):
        Popen(['python', 'acc.py'])

    def run_eeg(self, instance):
        Popen(['python', 'eeg.py'])

    def run_bioz(self, instance):
        Popen(['python', 'bioz.py'])

    def run_temp(self, instance):
        Popen(['python', 'temp.py'])
        
    def run_opt(self, instance):
        Popen(['python', 'opt.py'])

if __name__ == '__main__':
    DataProcessingApp().run()
