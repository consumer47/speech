import json
import os
import speech_recognition as sr
from gtts import gTTS
import pyttsx3


class SpeechAssistant:

    def __init__(self, command_file):
        self.commands = self.load_commands(command_file)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()

    def load_commands(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)["commands"]

    def listen(self):
        with self.microphone as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            return audio

    def recognize_speech(self, audio):
        try:
            text = self.recognizer.recognize_google(audio).lower()
            print(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return ""

    def respond(self, message):
        tts = gTTS(text=message, lang='en')
        tts.save("response.mp3")
        os.system("mpg123 response.mp3")

        # Alternative using pyttsx3
        # self.tts_engine.say(message)
        # self.tts_engine.runAndWait()

    def execute_command(self, command):
        if command == "add_todo":
            self.add_todo()
        elif command == "add_card_to_anki":
            self.add_card_to_anki()
        elif command == "start_anki_training":
            self.start_anki_training()
        else:
            self.respond("Command not recognized")

    def add_todo(self):
        self.respond("What is the todo item?")
        audio = self.listen()
        item = self.recognize_speech(audio)
        if item:
            self.respond(f"Todo item '{item}' added")

    def add_card_to_anki(self):
        self.respond("What is the card question?")
        audio = self.listen()
        question = self.recognize_speech(audio)
        if question:
            self.respond("What is the card answer?")
            audio = self.listen()
            answer = self.recognize_speech(audio)
            if answer:
                self.respond(f"Card with question '{
                             question}' and answer '{answer}' added")

    def start_anki_training(self):
        self.respond("Starting Anki training")

    def run(self):
        while True:
            audio = self.listen()
            command = self.recognize_speech(audio)
            if command in self.commands:
                self.execute_command(self.commands[command])
            else:
                self.respond("I didnt understand brudi")


if __name__ == "__main__":
    assistant = SpeechAssistant("commands.json")
    assistant.run()
