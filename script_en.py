import openai
import speech_recognition as sr
import pyttsx3
import json

# Enter API key and model name for GPT-3.5
openai.api_key = "YOUR_API_KEY_HERE"
model_name = "gpt-3.5-turbo"  # Or another available GPT-3 model

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# Speech recognition function
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now:")
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio, language="en-US")
        print("You said:", recognized_text)
        return recognized_text
    except Exception as e:
        print("Sorry, I couldn't understand you.")
        return None

# GPT-3.5 response function
def get_gpt3_response(messages):
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].message['content'].strip()

# Main function
def main():
    conversation_history = []

    while True:
        # Record user input
        user_input = recognize_speech()
        if user_input is None:
            continue

        conversation_history.append({"role": "user", "content": user_input})

        # Generate GPT-3.5 response
        gpt3_response = get_gpt3_response(conversation_history)

        # Convert response to spoken language
        print("GPT-3.5 replies:", gpt3_response)
        engine.say(gpt3_response)
        engine.runAndWait()

        conversation_history.append({"role": "assistant", "content": gpt3_response})

if __name__ == "__main__":
    main()
