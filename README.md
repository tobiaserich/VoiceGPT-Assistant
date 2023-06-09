# VoiceGPT-Assistant

VoiceGPT-Assistant is a voice-enabled personal assistant powered by OpenAI's GPT-3.5-turbo. This application allows users to interact with the AI model through speech input and receive responses audibly. It leverages the `speech_recognition` and `pyttsx3` libraries to provide seamless speech-to-text and text-to-speech functionality.

## Getting Started

### Prerequisites

Before running the VoiceGPT-Assistant, make sure you have Python 3.7 or later installed on your system. Additionally, install the following Python libraries:

- `openai` (For interacting with the OpenAI API)
- `speech_recognition` (For converting speech to text)
- `pyttsx3` (For converting text to speech)

You can install them using the following command:

```
pip install openai speechrecognition pyttsx3
```

### Setup

1. Clone this repository:

```
git clone https://github.com/yourusername/VoiceGPT-Assistant.git
```

2. Open the `main.py` file and insert your OpenAI API key:

```python
openai.api_key = "YOUR_API_KEY_HERE"
```

3. Run the `main.py` script:

```
python main.py
```

The VoiceGPT-Assistant will now listen for your voice input and respond audibly using the GPT-3.5-turbo model.

## Customization Options

### Language

By default, the VoiceGPT-Assistant is configured for English. To change the language, modify the following lines in the `main.py` script:

1. Update the language code in the `recognize_google` function call:

```python
recognized_text = recognizer.recognize_google(audio, language="en-US")  # Change "en-US" to your desired language code
```

2. Update the `pyttsx3` initialization to use a different language by adding these lines after `engine = pyttsx3.init()`:

```python
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[<VOICE_INDEX>].id)  # Replace <VOICE_INDEX> with the index of the desired voice
```

### GPT Model

The VoiceGPT-Assistant uses GPT-3.5-turbo by default. To switch to a different GPT-3 model, modify the `model_name` variable in the `main.py` script:

```python
model_name = "gpt-3.5-turbo"  # Change this to another available GPT-3 model
```

### Response Customization

You can customize the AI response by modifying the parameters in the `openai.ChatCompletion.create()` function call. For example:

- Adjust the `max_tokens` parameter to control the response length.
- Change the `temperature` parameter to alter the randomness of the response (lower values make it more deterministic, higher values make it more random).

```python
response = openai.ChatCompletion.create(
    model=model_name,
    messages=messages,
    max_tokens=50,  # Adjust this value to change response length
    n=1,
    stop=None,
    temperature=0.5,  # Modify this value to change response randomness (0 to 1)
)
```

# VoiceGPT-Assistant GUI

A Graphical User Interface (GUI) program in Python and Tkinter that utilizes the OpenAI ChatGPT API to provide an interactive chat experience.

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/ChatGPT-GUI.git
```

2. Install the required dependencies:

- `openai` (For interacting with the OpenAI API)
- `speech_recognition` (For converting speech to text)
- `pyttsx3` (For converting text to speech)

You can install them using the following command:

```
pip install openai speechrecognition pyttsx3
```

## Usage

1. Run gui.py

```bash
python gui.py
```

2. Insert API-Key

3. Interact with the ChatGPT GUI by typing your message in the text input field and clicking the "Send" button or using the "Voice Input" button for speech-to-text input. Adjust the "Max. Tokens" and "n" sliders to modify the API request parameters.

## Customization

You can modify the following options within the source code:

Change the api_key variable in gui.py to use your OpenAI API key.

Adjust the default values for the "Max. Tokens" and "n" sliders in the create_widgets function.

Modify the colors, fonts, and other appearance-related properties by editing the relevant Tkinter widget configurations.

---

For more information on the available parameters and customization options, refer to the [OpenAI API documentation](https://beta.openai.com/docs/api-reference/chat/create
