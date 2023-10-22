from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.utils import platform
from android.permissions import request_permissions, Permission
import time
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.audio import SoundLoader
from gradio_client import Client

# Request necessary permissions for Android
if platform == 'android':
    request_permissions([
        Permission.CAMERA,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE,
        Permission.INTERNET
    ])

client = Client("https://sabari231024-vipsa.hf.space/--replicas/z9gkk/")

class CameraClick(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def capture(self):
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        image_path = "IMG_{}.png".format(timestr)
        camera.export_to_png(image_path)
        print("Captured:", image_path)
        return image_path

class ObjectRecognitionScreen(Screen):
    def __init__(self, **kwargs):
        super(ObjectRecognitionScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        self.camera_layout = CameraClick()
        btn = Button(text='Capture Image', size_hint=(.2, .1), pos_hint={'center_x': .5, 'center_y': .1})
        btn.bind(on_press=self.on_press_btn)
        layout.add_widget(self.camera_layout)
        layout.add_widget(btn)
        self.result_label = Label(text='', size_hint=(.8, .1), pos_hint={'center_x': .5, 'center_y': .9})
        layout.add_widget(self.result_label)
        self.add_widget(layout)

    def on_press_btn(self, instance):
        image_path = self.camera_layout.capture()
        result = client.predict(image_path, "1", "ta", api_name="/predict")
        self.result_label.text = "Object Recognition"
        self.play_audio(result)

    def play_audio(self, audio_path):
        sound = SoundLoader.load(audio_path)
        if sound:
            sound.play()
        else:
            print("Error: Could not load audio file.")

class OCRDetectionScreen(Screen):
    def __init__(self, **kwargs):
        super(OCRDetectionScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        self.camera_layout = CameraClick()
        btn = Button(text='Capture Image', size_hint=(.2, .1), pos_hint={'center_x': .5, 'center_y': .1})
        btn.bind(on_press=self.on_press_btn)
        layout.add_widget(self.camera_layout)
        layout.add_widget(btn)
        self.result_label = Label(text='', size_hint=(.8, .1), pos_hint={'center_x': .5, 'center_y': .9})
        layout.add_widget(self.result_label)
        self.add_widget(layout)

    def on_press_btn(self, instance):
        image_path = self.camera_layout.capture()
        result = client.predict(image_path, "2", "ta", api_name="/predict")
        self.result_label.text = "OCR Detection"
        self.play_audio(result)

    def play_audio(self, audio_path):
        sound = SoundLoader.load(audio_path)
        if sound:
            sound.play()
        else:
            print("Error: Could not load audio file.")

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        object_recognition_screen = ObjectRecognitionScreen(name='object_recognition')
        ocr_detection_screen = OCRDetectionScreen(name='ocr_detection')
        sm.add_widget(object_recognition_screen)
        sm.add_widget(ocr_detection_screen)
        return sm

if __name__ == '__main__':
    MyApp().run()
