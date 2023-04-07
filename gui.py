import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import openai
import speech_recognition as sr
import pyttsx3

model_name = "gpt-3.5-turbo"
conversation_history = []
# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# Speech recognition function
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now:")
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio, language="de-DE")
        print("You said:", recognized_text)
        return recognized_text
    except Exception as e:
        print("Sorry, I couldn't understand you.")
        return None

# GPT-3 response function
def get_gpt3_response(messages):
    print(conversation_history)
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].message['content'].strip()

class Message(tk.Frame):
    def __init__(self, master, role, content, tts_engine, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.role = role
        self.content = content
        self.tts_engine = tts_engine

        if self.role == "user":
            self.label = tk.Label(self, text=self.content, wraplength=400, anchor=tk.E, justify=tk.RIGHT, bg="#DDF9C1", padx=10, pady=5)
            self.label.pack(fill=tk.X, padx=(100, 5), pady=(5, 0))
        else:
            self.label = tk.Label(self, text=self.content, wraplength=400, anchor=tk.W, justify=tk.LEFT, bg="#B9E6FF", padx=10, pady=5)
            self.label.pack(fill=tk.X, padx=(5, 100), pady=(5, 0))

        self.speak_button = ttk.Button(self, text="🔊", command=self.read_aloud_message, width=3)
        self.speak_button.pack(side=tk.RIGHT, padx=5)

    def read_aloud_message(self):
        self.tts_engine.stop()
        self.tts_engine.say(self.content)
        self.tts_engine.runAndWait()
def set_api_key():
    global openai
    openai.api_key = api_key_input.get()
    global model_name
    model_name = "gpt-3.5-turbo"

def process_input(text, tts_engine):
    if text:
        conversation_frame = tab_control.children[tab_control.select().split('.')[2]]
        if "conversation_text" not in conversation_frame.children:
            conversation_text = ScrolledText(conversation_frame, wrap=tk.WORD, name="conversation_text")
            conversation_text.pack(fill=tk.BOTH, expand=True)
            conversation_frame.children["conversation_text"] = conversation_text
        else:
            conversation_text = conversation_frame.nametowidget("conversation_text")

        # User message
        user_message = {"role": "user", "content": text}
        conversation_history.append(user_message)
        Message(conversation_text, "user", text, tts_engine).pack(side=tk.TOP, fill=tk.X)
        user_input.delete(0, tk.END)

        # GPT-3 message
        gpt3_response = get_gpt3_response(conversation_history)
        gpt3_message = {"role": "assistant", "text": gpt3_response}
        conversation_history.append(gpt3_message)
        Message(conversation_text, "gpt3", gpt3_response, tts_engine).pack(side=tk.TOP, fill=tk.X)

        conversation_text.yview(tk.END)


def speech_to_text():
    recognized_text = recognize_speech()
    if recognized_text:
        user_input.delete(0, tk.END)
        user_input.insert(tk.END, recognized_text)
        process_input(recognized_text)


def add_tab():
    tab_name = f"Tab {len(tabs) + 1}"
    new_tab = ttk.Frame(tab_control)
    tab_control.add(new_tab, text=tab_name)

    new_conversation_text = ScrolledText(new_tab, wrap=tk.WORD, name="conversation_text")
    new_conversation_text.pack(fill=tk.BOTH, expand=True)
    new_conversation_text.config(state=tk.DISABLED)

    tabs[tab_name] = {
        "conversation_text": new_conversation_text,
        "conversation_history": [],
    }

# Create main window
root = tk.Tk()
root.title("Voice GPT")
root.geometry("400x600")
tab_control = ttk.Notebook(root)
tab_control.pack(fill=tk.BOTH, expand=True)

tabs = {}
add_tab()

add_tab_button = ttk.Button(root, text="+", command=add_tab)
add_tab_button.pack(side=tk.RIGHT)

api_key_label = ttk.Label(root, text="API Key:")
api_key_label.pack(side=tk.LEFT, padx=(5, 0))

api_key_input = ttk.Entry(root)
api_key_input.pack(side=tk.LEFT, padx=(0, 5))

user_input = ttk.Entry(root)
user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
api_key_button = ttk.Button(root, text="Set API Key", command=set_api_key)
api_key_button.pack(side=tk.LEFT, padx=(0,10))


user_input.bind("<Return>", lambda event: process_input(user_input.get()))

send_button = ttk.Button(root, text="Send", command=lambda: process_input(user_input.get(), engine))

send_button.pack(side=tk.RIGHT, padx=(0, 5))

talk_button = ttk.Button(root, text="Talk", command=speech_to_text)
talk_button.pack(side=tk.RIGHT)

root.mainloop()
