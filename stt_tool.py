import speech_recognition as sr


def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Please say something: ")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    print("Recognizing...")

    try:
        # Using the default Google Web Speech API
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
    except sr.UnknownValueError:
        print("Google Web Speech API could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")


if __name__ == "__main__":
    main()
