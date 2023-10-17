from kivy.app import App
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.camera import Camera
from gradio_client import Client

client = Client("https://sabari231024-vipsa.hf.space/--replicas/9z975/")

class ObjectRecognitionScreen(Screen):
    def __init__(self, **kwargs):
        super(ObjectRecognitionScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        self.camera = Camera(play=True, resolution=(640, 480))
        btn = Button(text='Capture Image', size_hint=(.2, .1), pos_hint={'center_x': .5, 'center_y': .1})
        btn.bind(on_press=self.on_press_btn)
        layout.add_widget(self.camera)
        layout.add_widget(btn)
        self.result_label = Label(text='', size_hint=(.8, .1), pos_hint={'center_x': .5, 'center_y': .9})
        layout.add_widget(self.result_label)
        self.add_widget(layout)

    def on_press_btn(self, instance):
        # Capture image
        image_path = 'captured_image.jpg'
        self.camera.export_to_png(image_path)
        # Call the app function
        result = client.predict(image_path, "1", "ta", api_name="/predict")
        # Show the result on the screen
        self.result_label.text = "Object_recognition"
        # Play audio
        AudioPlayerApp.play_audio(result)  # Play the audio after capturing the image and getting the result

class OCRDetectionScreen(Screen):
    def __init__(self, **kwargs):
        super(OCRDetectionScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        self.camera = Camera(play=True, resolution=(640, 480))
        btn = Button(text='Capture Image', size_hint=(.2, .1), pos_hint={'center_x': .5, 'center_y': .1})
        btn.bind(on_press=self.on_press_btn)
        layout.add_widget(self.camera)
        layout.add_widget(btn)
        self.result_label = Label(text='', size_hint=(.8, .1), pos_hint={'center_x': .5, 'center_y': .9})
        layout.add_widget(self.result_label)
        self.add_widget(layout)

    def on_press_btn(self, instance):
        # Capture image
        image_path = 'captured_image.jpg'
        self.camera.export_to_png(image_path)
        # Call the app function
        result = client.predict(image_path, "2", "ta", api_name="/predict")
        # Show the result on the screen
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
        ocr_detection_screen = OCRDetectionScreen(name='ocr_detection')
        sm.add_widget(object_recognition_screen)
        sm.add_widget(ocr_detection_screen)
        return sm

if __name__ == '__main__':
    MyApp().run()
