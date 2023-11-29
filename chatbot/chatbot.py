# chatbot/chatbot.py
import speech_recognition as sr
from gtts import gTTS
import os
import pygame


def speak(text):
    # Save the text as an audio file
    tts = gTTS(text)
    tts.save("chatbot_response.mp3")

    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load("chatbot_response.mp3")

    # Play the audio
    pygame.mixer.music.play()

    clock = pygame.time.Clock()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        clock.tick(30)  # Adjust the frame rate as needed

    # Stop and quit the pygame mixer
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    # Remove the audio file after it's no longer in use
    if os.path.exists("chatbot_response.mp3"):
        os.remove("chatbot_response.mp3")


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("You can speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            user_input = recognizer.recognize_google(audio, language='en-US')
            print("You (Voice):", user_input)
            return user_input
        except sr.UnknownValueError:
            return None
