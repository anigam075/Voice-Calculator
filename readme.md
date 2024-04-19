# Voice Controlled Calculator

## Overview
This project implements a basic calculator with voice recognition capabilities. It allows users to perform arithmetic operations by speaking commands such as "add", "subtract", "multiply", "divide", and provides feedback via both text and speech synthesis.

## Features
- Voice recognition for arithmetic commands and numerical inputs.
- Graphical User Interface (GUI) for traditional button-based input.
- Real-time evaluation and display of calculations.
- Error handling for invalid inputs.
- Speech synthesis for providing calculation results, with the ability to read results aloud.

## Requirements
- Python 3.x
- tkinter (GUI toolkit for Python)
- pyaudio (Python bindings for PortAudio, used for audio I/O)
- vosk (Speech recognition toolkit)
- pyttsx3 (Text-to-speech conversion library)

## Usage
1. Run the `voice_calculator.py` file.
2. The GUI window will appear, showing a text entry field and buttons for numerical input and arithmetic operations.
3. Speak commands like "one", "two", "three", etc. to type numbers using voice recognition
4. Speak commands such as "add", "subtract", "multiply", "divide" followed by numbers to perform calculations using voice recognition.
5. Alternatively, use the buttons in the GUI to input numbers and perform calculations traditionally.
6. Results will be displayed in the text entry field and announced using speech synthesis.

## Acknowledgments
- Vosk: Open source speech recognition toolkit.
- pyttsx3: Text-to-speech conversion library for Python.
- tkinter: Standard GUI toolkit for Python.
- pyaudio: Python bindings for PortAudio, used for audio I/O.

