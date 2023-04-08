import openai
import pyttsx3
import speech_recognition as sr
import os
import json
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

# Text-to-Speech-Funktion
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Speech-to-Text-Funktion
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Sprechen Sie Ihren Text:")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="de-DE")
            return text
        except:
            return "Entschuldigung, ich konnte Sie nicht verstehen."

# API-Authentifizierung und API-Key-Speicherung
def authenticate_api_key(api_key):
    openai.api_key = api_key
    with open("api_key.json", "w") as f:
        json.dump({"api_key": api_key}, f)

# API-Key abrufen
def get_api_key():
    if os.path.exists("api_key.json"):
        with open("api_key.json", "r") as f:
            api_key = json.load(f)["api_key"]
            return api_key
    else:
        api_key = input("Bitte geben Sie Ihren OpenAI API-Key ein: ")
        authenticate_api_key(api_key)
        return api_key

# OpenAI ChatGPT API Anfrage
def chat_gpt_request(api_key, messages,max_tokens, n):
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=max_tokens,
        n=n,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].message['content'].strip()

class ChatApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ChatGPT App")
        self.geometry("400x600")
        self.configure(bg="#ECE5DD")

        self.create_widgets()
        self.messages = [{'role': 'system', 'content': 'Sie sind jetzt mit ChatGPT verbunden.'}]

    def create_widgets(self):
        self.message_frame = tk.Frame(self, bg="#ECE5DD")
        self.message_frame.place(relwidth=1, relheight=0.7)

        self.scrollbar = ttk.Scrollbar(self.message_frame, orient="vertical")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.message_area = tk.Text(self.message_frame, wrap=tk.WORD, yscrollcommand=self.scrollbar.set, bg="#ECE5DD", state=tk.DISABLED, font=("Helvetica", 12))
        self.message_area.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.message_area.yview)

        self.entry_var = tk.StringVar()
        self.entry_box = ttk.Entry(self, textvariable=self.entry_var, width=30)
        self.entry_box.place(relx=0.05, rely=0.75)

        self.send_button = ttk.Button(self, text="Senden", command=self.send_message)
        self.send_button.place(relx=0.7, rely=0.75)

        self.record_button = ttk.Button(self, text="Spracheingabe", command=self.speech_input)
        self.record_button.place(relx=0.8, rely=0.75)

        self.max_tokens_label = ttk.Label(self, text="Max. Tokens:")
        self.max_tokens_label.place(relx=0.05, rely=0.85)
        self.max_tokens_var = tk.IntVar(value=100)
        self.max_tokens_scale = tk.Scale(self, from_=0, to=4000, variable=self.max_tokens_var, orient=tk.HORIZONTAL, length=200, resolution=10)
        self.max_tokens_scale.place(relx=0.25, rely=0.85)

        self.n_label = ttk.Label(self, text="n:")
        self.n_label.place(relx=0.05, rely=0.95)
        self.n_var = tk.IntVar(value=1)
        self.n_scale = tk.Scale(self, from_=1, to=10, variable=self.n_var, orient=tk.HORIZONTAL, length=200, resolution=1)
        self.n_scale.place(relx=0.25, rely=0.95)


    def insert_message(self, text, user, side):
        self.message_area.configure(state='normal')
        color = "#34B7F1" if user == "Sie" else "#DCF8C6"
        wrap_length = 250 if side == tk.LEFT else 150
        self.message_area.tag_config(side, justify=side, background=color, lmargin1=10, lmargin2=10, spacing3=5)
        self.message_area.tag_config("code", font=("Courier", 12), background="#F0F0F0")

        self.message_area.insert(tk.END, f"{user}: ", side)
    
        # Code-Snippet-Erkennung und präformatierte Anzeige
        start = 0
        in_code_block = False
        for part in text.split("`"):
            if in_code_block:
                self.message_area.insert(tk.END, part, ("code", side))
            else:
                self.message_area.insert(tk.END, part, side)
            in_code_block = not in_code_block

        self.message_area.insert(tk.END, "\n", side)
        self.message_area.window_create(tk.END, window=self.create_play_button(text))
        self.message_area.insert(tk.END, "\n", side)
        self.message_area.configure(state='disabled')


    def create_play_button(self, text):
        button = ttk.Button(self.message_area, text="▶", command=lambda: text_to_speech(text))
        return button

    def send_message(self):
        user_input = self.entry_var.get()

        if user_input:
            self.insert_message(user_input, "Sie", tk.RIGHT)

            self.messages.append({'role': 'user', 'content': user_input})
            response = chat_gpt_request(api_key,[{'role': 'user', 'content': user_input}], self.max_tokens_var.get(), self.n_var.get())
            self.messages.append({'role': 'assistant', 'content': response})

            self.insert_message(response, "ChatGPT", tk.LEFT)

        self.entry_var.set("")
        
    def speech_input(self):
        user_input = speech_to_text()

        self.insert_message(user_input, "Sie", tk.RIGHT)

        self.messages.append({'role': 'user', 'content': user_input})
        response = chat_gpt_request(api_key, self.messages, self.max_tokens_var.get(), self.n_var.get())
        self.messages.append({'role': 'assistant', 'content': response})

        self.insert_message(response, "ChatGPT", tk.LEFT)

if __name__ == "__main__":
    api_key = get_api_key()
    app = ChatApp()
    app.mainloop()
