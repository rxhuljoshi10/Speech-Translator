from customtkinter import *
from SpeechToText import listen
from PIL import Image,ImageTk
from googletrans import Translator,LANGCODES
import clipboard
from gtts import gTTS
import pygame

all_Languages = LANGCODES

def speak(text,lang = None):
    def playSound(path):
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        pygame.quit()

    langCode = LANGCODES.get(lang)
    tts = gTTS(text=text, lang=langCode)
    voicePath = "output.mp3"
    tts.save(voicePath)
    playSound(voicePath)


def translateText(text,lang="en"):
    translator = Translator()
    text = translator.translate(text,dest=lang)
    clipboard.copy(text.text)
    return text

def loadImage(image_path, size = (25,25)):
    image_pil = Image.open(image_path)
    image_pil = image_pil.resize(size, Image.ANTIALIAS)
    return ImageTk.PhotoImage(image_pil)

def displayText(obj,text):
    obj.delete("1.0", END)
    obj.insert(END,text)
    root.update_idletasks()

def drawLine(root,obj):
    obj = CTkCanvas(root,width=630,height=1)
    obj.grid(pady=20)

def main(root):
    def convertSpeech(text):
        if text:
            destinLang = toLangInput.get()
            newText = translateText(text,destinLang).text
            displayText(output,newText)
            if not mute:
                speak(newText,destinLang)

    def notice(func):
        def wrapper():
            noticeLable.configure(text="Speak Out Text...")
            root.update_idletasks()
            func()
            noticeLable.configure(text="")
            root.update()
        return wrapper

    @notice
    def speech():
        sourceLang = fromLangInput.get()
        text = listen(sourceLang)
        if text:
            displayText(textInput,text)
            convertSpeech(text)
        
    def translate():
        text = textInput.get("1.0", END)
        convertSpeech(text)

    def on_click(event):
        CurrInput = textInput.get("1.0", END)
        if placeholderText in CurrInput:
            textInput.delete("1.0", END)

    def on_leave(event):
        if textInput.get("1.0", END) == "\n":
            textInput.insert(END, placeholderText)

    def speaker():
        global mute
        if not mute:
            speakerbtn.configure(image=muteImg)
            mute=True
        else:
            speakerbtn.configure(image=unmuteImg)
            mute=False
    

    frameLang = CTkFrame(root)
    frameLang.grid(padx=5, pady=(10,0), sticky=W)

    
    fromLangLabel = CTkLabel(frameLang, text="From Language : ",font=CTkFont("bold",15))
    fromLangLabel.grid(padx=5, pady=5, sticky=W)
    
    fromLangInput = CTkComboBox(frameLang, values=list(all_Languages.keys()))
    fromLangInput.grid(row=0, column=1, padx=5, pady=5, sticky=W)
    fromLangInput.set("english")

    
    toLangLabel = CTkLabel(frameLang, text="To Language : ",font=CTkFont("bold",15))
    toLangLabel.grid(padx=5, pady=5, sticky=W)

    toLangInput = CTkComboBox(frameLang, values=list(all_Languages.keys()))
    toLangInput.grid(row=1, column=1, padx=5, pady=5, sticky=W)
    toLangInput.set("english")


    speechbtn = CTkButton(frameLang, text="SPEAK", command=speech, height=40, width=80, bg_color="green")
    speechbtn.grid(row=0, column=2, padx=(60,10), pady=5)

    drawLine(root,"line1")

    originalLable = CTkLabel(root, text="Original : ",font=CTkFont("bold",15))
    originalLable.grid(padx=5, pady=5, sticky=W)

    placeholderText = "Enter Text here..."
    textInput = CTkTextbox(root, height=50, width=410)
    textInput.insert(END, placeholderText)
    textInput.bind('<FocusIn>', on_click)
    textInput.bind('<FocusOut>', on_leave)
    textInput.grid(row=4, padx=10)


    translatebtn = CTkButton(root, text="Translate", command=translate)
    translatebtn.grid(padx=10, pady=(5,20), sticky=E)

    translatedText = CTkLabel(root, text="Translated Text : ",font=CTkFont("bold",15))
    translatedText.grid(padx=5, pady=5, sticky=W)    

    unmuteImg = loadImage("unmute.png")
    muteImg = loadImage("mute.png")

    speakerbtn = CTkButton(root, text="", height=0, width=0, image=unmuteImg, command=speaker)
    speakerbtn.grid(row=6, sticky=E, padx=10)

    output = CTkTextbox(root, height=80, width=410)
    output.grid(column=0, padx=5)

    drawLine(root,"line2")

    noticeLable = CTkLabel(root, text="", font=CTkFont("Courier",15))
    noticeLable.grid(padx=10, sticky=W)


if __name__ == "__main__":
    mute = False
    set_appearance_mode("dark")
    set_default_color_theme("green")
    root = CTk()
    root.geometry("433x455")
    root.title("Speech Translator")
    iconPath = "microphone.ico"
    root.iconbitmap(iconPath)
    root.resizable(False,False)
    main(root)
    root.mainloop()