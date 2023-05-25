from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from subprocess import Popen

class DataProcessingApp(App):
    def build(self):
        anchor_layout = AnchorLayout()

        box_layout = BoxLayout(orientation='horizontal', spacing=50 ,padding=100)
        anchor_layout.add_widget(box_layout)

        acc_button = Button(text='ACC', size_hint=(0.2, 1))
        acc_button.bind(on_release=self.run_acc)
        box_layout.add_widget(acc_button)

        bioz_button = Button(text='BIOZ', size_hint=(0.2, 1))
        bioz_button.bind(on_release=self.run_bioz)
        box_layout.add_widget(bioz_button)

        eeg_button = Button(text='EEG', size_hint=(0.2, 1))
        eeg_button.bind(on_release=self.run_eeg)
        box_layout.add_widget(eeg_button)

        temp_button = Button(text='TEMP', size_hint=(0.2, 1))
        temp_button.bind(on_release=self.run_temp)
        box_layout.add_widget(temp_button)

        return anchor_layout

    def run_acc(self, instance):
        Popen(['python', 'acc.py'])

    def run_eeg(self, instance):
        Popen(['python', 'eeg.py'])
    
    def run_bioz(self, instance):
        Popen(['python', 'bioz.py'])

    def run_temp(self, instance):
        Popen(['python', 'temp.py'])

if __name__ == '__main__':
    DataProcessingApp().run()
