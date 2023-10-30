import speech_recognition as sr
import datetime

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

            # Get the current timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Save the speech and timestamp to a text file with UTF-8 encoding
            with open("speech_transcript.txt", "a", encoding="utf-8") as file:
                file.write(f"[{timestamp}] Bengali: {Text_bn}\n")
                file.write(f"[{timestamp}] English: {text_en}\n")

    except KeyboardInterrupt:
        print("A KeyboardInterrupt encountered; Terminating the Program !!!")
        break

    except sr.UnknownValueError:
        print("No User Voice detected or recognized audio cannot be matched to text")
