import openai
import speech_recognition as sr
import pyttsx3
import json

# API-Key und Modelname
openai.api_key = "YOUR_API_KEY_HERE"
model_name = "gpt-3.5-turbo"  

# Text-to-Speech-Engine initialise
engine = pyttsx3.init()

# Spracherkennungsfunktion
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Sprechen Sie jetzt:")
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio, language="de-DE")
        print("Sie sagten:", recognized_text)
        return recognized_text
    except Exception as e:
        print("Entschuldigung, ich konnte Sie nicht verstehen.")
        return None

# GPT-3.5 Antwortfunktion
def get_gpt3_response(messages):
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].message['content'].strip()

# Hauptfunktion
def main():
    conversation_history = []

    while True:
        # Benutzereingabe aufnehmen
        user_input = recognize_speech()
        if user_input is None:
            continue

        conversation_history.append({"role": "user", "content": user_input})

        # GPT-3.5 Antwort generieren
        gpt3_response = get_gpt3_response(conversation_history)

        # Antwort in gesprochene Sprache umwandeln
        print("GPT-3.5 antwortet:", gpt3_response)
        engine.say(gpt3_response)
        engine.runAndWait()

        conversation_history.append({"role": "assistant", "content": gpt3_response})

if __name__ == "__main__":
    main()