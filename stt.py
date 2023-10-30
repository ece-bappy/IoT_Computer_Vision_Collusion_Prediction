# Python Program that helps translate Speech to Text
 
import speech_recognition as sr
 
# The Recognizer is initialized.
UserVoiceRecognizer = sr.Recognizer()
 
while True:
    try:
 
        with sr.Microphone() as UserVoiceInputSource:
 
            UserVoiceRecognizer.adjust_for_ambient_noise(UserVoiceInputSource, duration=0.5)
            
            # The Program listens to the user voice input.
            UserVoiceInput = UserVoiceRecognizer.listen(UserVoiceInputSource)
 
            Text_bn = UserVoiceRecognizer.recognize_google(UserVoiceInput, language = "bn-BD")
            Text_bn = Text_bn.lower()
            print(Text_bn)
            
            text_en = UserVoiceRecognizer.recognize_google(UserVoiceInput, language="en-IN")
            text_en = text_en.lower() 
            print(text_en)
    
    except KeyboardInterrupt:
        print('A KeyboardInterrupt encountered; Terminating the Program !!!')
        exit(0)
    
    except sr.UnknownValueError:
        print("No User Voice detected or recognized audio cannot be matched to text")
        
