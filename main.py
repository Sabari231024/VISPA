import requests
import gtts as gt
import os
from googletrans import Translator
from playsound import playsound
import easyocr
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse
# Utility Functions



# Set background color to black
Window.clearcolor = (0, 0, 0, 1)

# ... (Utility functions and other code remain the same)
def object_recognition(image):
    API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
    headers = {"Authorization": "Bearer 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"}

    def query(filename):
        with open(filename, "rb") as f:
            data = f.read()
        response = requests.post(API_URL, headers=headers, data=data)
        return response.json()

    output = query(image)
    text = output[0]['generated_text']
    return text

def ocr_detection(image):
    lang_list=["hi", "mr", "ne", "en"]
    reader = easyocr.Reader(lang_list)
    translator = Translator()
    bounds = reader.readtext(image, add_margin=0.55, width_ths=0.7, link_threshold=0.8, decoder='beamsearch', blocklist='=.',detail=0)
    text_comb = ' '.join(bounds)
    lan1 = translator.detect(text_comb)
    l = lan1.lang
    text2 = []
    for i in bounds:
        lan = translator.detect(i)
        if lan.lang == l or lan.lang in lang_list:
            text1 = translator.translate(i, src=lan.lang)
            text2.append(text1.text)
    text = ' '.join(text2)
    if text:
        trans(text)
    else:
        None
    return text

def trans(text):
    translator = Translator()
    out = translator.translate(text, dest='ta')
    tts = gt.gTTS(text=out.text, lang='ta')
    tts.save('sample.mp3')
    playsound('sample.mp3')
    os.remove('sample.mp3')



class CustomDropDown(DropDown):
    def __init__(self, **kwargs):
        super(CustomDropDown, self).__init__(**kwargs)
        self.languages = {
            'English': 'en',
            'Hindi': 'hi',
            'Tamil': 'ta'
        }
        for lang, code in self.languages.items():
            btn = Button(text=lang, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.select_language(code))
            self.add_widget(btn)

    def select_language(self, code):
        print(f'Selected language code: {code}')

class ObjectRecognitionScreen(Screen):
    def __init__(self, **kwargs):
        super(ObjectRecognitionScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Mode: Object Recognition", size_hint_y=None, height=50)
        self.image = Image()
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.image)
        self.add_widget(self.layout)

class OCRDetectionScreen(Screen):
    def __init__(self, **kwargs):
        super(OCRDetectionScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Mode: OCR Detection", size_hint_y=None, height=50)
        self.image = Image()
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.image)

        # Create a button with a circular background for capturing images
        self.capture_button = Button(
            text='Capture Image',
            size_hint_y=None,
            height=100,
            background_color=(0, 0, 0, 0)  # Transparent background
        )
        self.capture_button.bind(on_press=self.capture_image)

        # Add the capture button to the layout
        self.layout.add_widget(self.capture_button)
        self.add_widget(self.layout)

    def on_lang_select(self, instance, lang):
        print(f'Selected language: {lang}')

    def capture_image(self, instance):
        # Logic for capturing images goes here
        pass

    def on_size(self, instance, value):
        # Update the button position and size to create a circle at the bottom
        with self.canvas:
            Color(0, 0, 0, 1)  # Black color for the border
            Ellipse(pos=(self.width/2 - 50, 0), size=(100, 100))  # Circle border
            Color(1, 1, 1, 1)  # White color for the circle
            Ellipse(pos=(self.width/2 - 45, 5), size=(90, 90))

class VIPSAApp(App):
    def build(self):
        sm = ScreenManager()
        object_recognition_screen = ObjectRecognitionScreen(name='object_recognition')
        ocr_detection_screen = OCRDetectionScreen(name='ocr')
        sm.add_widget(object_recognition_screen)
        sm.add_widget(ocr_detection_screen)
        sm.current = 'object_recognition'
        return sm

    def on_start(self):
        Window.clearcolor = (0, 0, 0, 1)  # Set window background color

# Set the app window size
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

if __name__ == '__main__':
    VIPSAApp().run()
