from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from subprocess import Popen
import pylsl

class DataProcessingApp(App):
    def build(self):
        # ルートとなるBoxLayout
        root_layout = BoxLayout(orientation='vertical')

        # テキストを配置するAnchorLayout
        text_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        streams = pylsl.resolve_streams()
        if streams == []:
            label = Label(text='No stream found', font_size=50)
            text_layout.add_widget(label)
            root_layout.add_widget(text_layout)

            reload_button = Button(text='Reload', size_hint=(0.2, 1))
            reload_button.bind(on_release=self.run_reload)
            root_layout.add_widget(reload_button)
        else:
            label = Label(text=streams[0].name(), font_size=50)
            text_layout.add_widget(label)
            root_layout.add_widget(text_layout)

            # ボタンを配置するBoxLayout
            button_layout = BoxLayout(orientation='horizontal', spacing=10)
            acc_button = Button(text='ACC', size_hint=(0.2, 1))
            acc_button.bind(on_release=self.run_acc)
            button_layout.add_widget(acc_button)

            bioz_button = Button(text='BIOZ', size_hint=(0.2, 1))
            bioz_button.bind(on_release=self.run_bioz)
            button_layout.add_widget(bioz_button)

            eeg_button = Button(text='EEG', size_hint=(0.2, 1))
            eeg_button.bind(on_release=self.run_eeg)
            button_layout.add_widget(eeg_button)

            temp_button = Button(text='TEMP', size_hint=(0.2, 1))
            temp_button.bind(on_release=self.run_temp)
            button_layout.add_widget(temp_button)

            root_layout.add_widget(button_layout)

        return root_layout

    def run_acc(self, instance):
        Popen(['python', 'acc.py'])

    def run_eeg(self, instance):
        Popen(['python', 'eeg.py'])

    def run_bioz(self, instance):
        Popen(['python', 'bioz.py'])

    def run_temp(self, instance):
        Popen(['python', 'temp.py'])

    def run_reload(self, instance):
        self.root.clear_widgets()
        self.build()
        DataProcessingApp().run()


if __name__ == '__main__':
    DataProcessingApp().run()
