import sys
import asyncio
import tkinter as tk
import pyaudio
import threading
from vosk import Model, KaldiRecognizer
import pyttsx3

NUMBER_MAP = {
    'zero': '0',
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

def custom_excepthook(type, value, traceback):
    if isinstance(value, RuntimeError) and "main thread is not in main loop" in str(value):
        pass
    else:
        sys.__excepthook__(type, value, traceback)
sys.excepthook = custom_excepthook

async def recognize_speech(cancel_event):
    try:
        model = Model(r"vosk-model-small-en-in-0.4/vosk-model-small-en-in-0.4")
        recognizer = KaldiRecognizer(model, 16000)

        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)

        stream.start_stream()

        while not cancel_event.is_set():
            data = await asyncio.to_thread(stream.read, 4096)
            if recognizer.AcceptWaveform(data):
                text = recognizer.Result()
                transcription = text[14:-3].lower()
                print(transcription)
                await check_transcription(transcription)
    except Exception as e:
        handle_exception(e)

async def check_transcription(transcription):
    if transcription in NUMBER_MAP:
        digit = NUMBER_MAP[transcription]
        await handle_input(digit)
    elif 'add' in transcription or 'plus' in transcription:
        await handle_operation('+')
    elif 'minus' in transcription or 'subtract' in transcription:
        await handle_operation('-')
    elif 'multiply' in transcription:
        await handle_operation('*')
    elif 'divide' in transcription:
        await handle_operation('/')
    elif 'clear' in transcription or 'clean' in transcription:
        await handle_clear()
    elif 'equal' in transcription or 'equals' in transcription:
        await handle_equal()


async def handle_equal():
    current = display_var.get()
    try:
        result = eval(current)
        display_var.set(str(result))
        engine = pyttsx3.init()
        say_text = f'Result is {result}'
        engine.say(say_text)
        engine.runAndWait()
    except:
        display_var.set('Error')

async def handle_input(digit):
    current = display_var.get()
    display_var.set(current + digit)
    

async def handle_clear():
    display_var.set('') 

async def handle_operation(operation):
    current = display_var.get()
    display_var.set(current + operation)

def button_click(symbol):
    current = display_var.get()
    if symbol == 'C':
        display_var.set('')
    elif symbol == '=':
        try:
            result = eval(current)
            display_var.set(str(result))
            engine = pyttsx3.init()
            say_text = f'Result is {result}'
            engine.say(say_text)
            engine.runAndWait()
        except:
            display_var.set("Error")
    else:
        display_var.set(current + symbol)

def on_closing():
    try:
        cancel_event.set()
        cleanup()
    except Exception as e:
        handle_exception(e)

def start_asyncio_loop():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(recognize_speech(cancel_event))
    except Exception as e:
        handle_exception(e)

def start_gui():
    global root
    root = tk.Tk()
    root.title("Basic Calculator")
    root.protocol("WM_DELETE_WINDOW", on_closing)

    global display_var
    display_var = tk.StringVar()

    display_entry = tk.Entry(root, textvariable=display_var, font=('Arial', 20), bd=10, insertwidth=4, width=15, justify='right')
    display_entry.grid(row=0, column=0, columnspan=4)

    buttons = [
        '7', '8', '9', '/',
        '4', '5', '6', '*',
        '1', '2', '3', '-',
        'C', '0', '=', '+'
    ]

    row = 1
    col = 0
    for button in buttons:
        tk.Button(root, text=button, font=('Arial', 14), width=4, height=2, command=lambda b=button: button_click(b)).grid(row=row, column=col)
        col += 1
        if col > 3:
            col = 0
            row += 1

    root.mainloop()

def cleanup():
    display_var.set('')
    root.destroy()

def handle_exception(exception):
    print("Exception occurred:", exception)

if __name__ == "__main__":
    cancel_event = threading.Event()
    gui_thread = threading.Thread(target=start_gui)
    gui_thread.start()
    start_asyncio_loop()
