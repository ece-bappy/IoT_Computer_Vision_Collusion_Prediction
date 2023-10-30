import speech_recognition as sr
import datetime
from pushbullet import Pushbullet

# Set your Pushbullet API key
api_key = "o.q8q17365BvNqIlUAhdeuwcwkR3Jzn8nH"

# Initialize the Pushbullet client
pb = Pushbullet(api_key)

# The Recognizer is initialized.
UserVoiceRecognizer = sr.Recognizer()

while True:
    try:
        with sr.Microphone() as UserVoiceInputSource:
            UserVoiceRecognizer.adjust_for_ambient_noise(
                UserVoiceInputSource, duration=0.5
            )
            # The Program listens to the user voice input.
            UserVoiceInput = UserVoiceRecognizer.listen(UserVoiceInputSource)

            Text_bn = UserVoiceRecognizer.recognize_google(
                UserVoiceInput, language="bn-BD"
            )
            Text_bn = Text_bn.lower()
            print("Bengali:", Text_bn)

            text_en = UserVoiceRecognizer.recognize_google(
                UserVoiceInput, language="en-IN"
            )
            text_en = text_en.lower()
            print("English:", text_en)

            # Check if the specific word is detected
            if text_en == "bangladesh":
                # Get the current timestamp
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                push_title = "People Detected"
                push_message = f"Number of people detected: {num_people}"
                push = pb.push_note(push_title, push_message)

    except KeyboardInterrupt:
        print("A KeyboardInterrupt encountered; Terminating the Program !!!")
        break

    except sr.UnknownValueError:
        print("No User Voice detected or recognized audio cannot be matched to text")
