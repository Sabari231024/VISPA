**Project Overview**
This project aims to develop an application to assist visually impaired individuals in their daily activities using machine learning techniques. The application performs object recognition and optical character recognition (OCR) on images captured through the app, translates the results into multiple languages, and converts them into speech for better understanding by visually impaired users.

**Objectives**
1)Perform object recognition on captured images.
2)Conduct OCR detection on images.
3)Translate results into multiple languages.
4)Convert translated results into speech.
**Methodology**
1)Object recognition and OCR detection are interfaced using the Gradio API, which requires an image input and is called based on the mode.
2)Processed results are translated using Google Translator.
3)Translated results are converted to audio using GTTS.
4)The models are deployed on Hugging Face Spaces and utilized via API.
5)A Kivy frontend application is created with two modes: object recognition and OCR detection, utilizing a single API by specifying the mode.
**Project Components**
Frontend Files: Uploaded to GitHub for launching the application.
Images: Required for the frontend.
Buildozer.spec: Configuration file for building the application.
Hugging Face Model: Deployed at Hugging Face Space.
**Instructions**
Clone the repository.
Install necessary dependencies.
Launch the application using the provided frontend files.
Ensure images required for frontend are accessible.
Use the specified Hugging Face API for model utilization.
**Technologies Used**
Python
Gradio
Google Translator
GTTS
Hugging Face Spaces
Kivy
**API RELATED SPACE:**
the model is deployed in hugging face in an space whose api is been used inorder improve the portability of the app.
link for the space: https://huggingface.co/spaces/Sabari231024/VIPSA
