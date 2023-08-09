import speech_recognition as sr

def listen(Lang = None):
    if not Lang:
        Lang = 'en'
    listener=sr.Recognizer()
    try:
        with sr.Microphone() as source:
            #listener.energy_threshold=10000
            print("Listening...")
            audio_text=listener.listen(source,0,10)
            text=listener.recognize_google(audio_text,language=Lang)
            return text
    except:
        return None

if __name__ == "__main__":
    lang = input("Which language will you be speaking? : ")
    while 1:
        text = listen(lang)
        if text:
            print(text)