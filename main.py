from kivy.app import App
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import ScreenManager, Screen
from android.permissions import request_permissions, Permission
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.camera import Camera
from gradio_client import Client

request_permissions([Permission.CAMERA,Permission.WRITE_EXTERNAL_STORAGE,Permission.READ_EXTERNAL_STORAGE,Permission.INTERNET])
client = Client("https://sabari231024-vipsa.hf.space/--replicas/z9gkk/")

class ObjectRecognitionScreen(Screen):
    def __init__(self, **kwargs):
        super(ObjectRecognitionScreen, self).__init__(**kwargs)
        self.mode = 1  # 1 for object recognition, 2 for OCR
        layout = FloatLayout()
        self.camera = Camera(play=True, resolution=(640, 480))
        self.result_label = Label(text='', size_hint=(.8, .1), pos_hint={'center_x': .5, 'center_y': .9})
        mode_button = Button(text='Switch to OCR Mode', size_hint=(.2, .1), pos_hint={'center_x': .5, 'center_y': .2})
        mode_button.bind(on_press=self.switch_mode)
        btn = Button(text='Capture Image', size_hint=(.2, .1), pos_hint={'center_x': .5, 'center_y': .1})
        btn.bind(on_press=self.on_press_btn)
        layout.add_widget(self.camera)
        layout.add_widget(mode_button)
        layout.add_widget(btn)
        layout.add_widget(self.result_label)
        self.add_widget(layout)

    def switch_mode(self, instance):
        if self.mode == 1:
            self.mode = 2
            instance.text = 'Switch to Object Recognition Mode'
        else:
            self.mode = 1
            instance.text = 'Switch to OCR Mode'

    def on_press_btn(self, instance):
        # Capture image
        image_path = 'captured_image.jpg'
        self.camera.export_to_png(image_path)
        # Call the app function based on mode
        if self.mode == 1:
            result = client.predict(image_path, "1", "ta", api_name="/predict")
            self.result_label.text = "Object_recognition"
        else:
            result = client.predict(image_path, "2", "ta", api_name="/predict")
            self.result_label.text = "OCR_detection"
        # Play audio
        AudioPlayerApp.play_audio(result)  # Play the audio after capturing the image and getting the result

class AudioPlayerApp(App):
    @staticmethod
    def play_audio(audio_path):
        sound = SoundLoader.load(audio_path)
        if sound:
            sound.play()
        else:
            print("Error: Could not load audio file.")

    def build(self):
        play_button = Button(text='Play Audio', on_press=lambda instance: self.play_audio("path_to_your_audio_file.mp3"))
        return play_button

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        object_recognition_screen = ObjectRecognitionScreen(name='object_recognition')
        sm.add_widget(object_recognition_screen)
        return sm

if __name__ == '__main__':
    MyApp().run()
