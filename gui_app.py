import tkinter as tk
from tkinter import PhotoImage
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import webbrowser
import threading

# Initialize text-to-speech
engine = pyttsx3.init()

# Emergency phrases and links
emergency_phrases = {
    "Burn Injury": ["I burned my hand", "my hand is burned", "I have a burn", "burned my skin",
        "I got a burn", "my finger is burned", "I touched something hot", "my skin is burning",
        "I feel a burning sensation", "I burned myself"],
    "Dizziness or Fainting": ["I feel dizzy", "I'm fainting", "I feel weak", "I feel lightheaded",
        "I'm about to pass out", "I feel like I'm going to fall", "I have vertigo", "I'm losing balance",
        "I feel nauseous", "I'm feeling faint"],
    "Breathing Problem": ["I can't breathe", "I'm having trouble breathing", "I'm gasping for air",
        "I'm out of breath", "I can't catch my breath", "I'm having an asthma attack",
        "I can't get enough air", "I'm wheezing", "I'm short of breath", "I have trouble breathing"],
    "Cut or Bleeding": ["I cut myself", "I'm bleeding", "I got a cut", "My hand is bleeding",
        "there is a cut", "I have a cut", "I have a wound", "I'm bleeding from my hand",
        "there's blood coming out", "I injured myself", "I have a deep cut", "my cut is bleeding a lot",
        "I need to stop the bleeding"],
    "Heart Attack": ["I feel chest pain", "I have chest pain", "I'm having a heart attack",
        "my chest hurts", "I'm feeling pressure in my chest", "I feel tightness in my chest",
        "I'm sweating and have chest pain", "I'm experiencing pain in my left arm",
        "I'm having a heart issue", "I feel light-headed and chest pain"],
    "Stroke": ["I feel numb", "I feel paralyzed", "I'm having a stroke", "I can't move my arm",
        "I have sudden weakness", "my face is drooping", "I have trouble speaking", "I feel dizzy and weak",
        "I'm losing control of my body", "I feel a sudden numbness"],
    "Choking": ["I can't breathe", "I'm choking", "I can't swallow", "I have something stuck in my throat",
        "I'm gagging", "I'm choking on food", "I can't cough", "I feel like I'm suffocating",
        "my throat is blocked", "I can't clear my throat"],
    "Severe Allergic Reaction": ["I can't breathe", "I have swelling in my face", "I’m allergic to something",
        "I need an epinephrine shot", "I have hives", "I have a rash", "my throat is closing up",
        "I have a bee sting", "I’m allergic to nuts", "I feel itchy all over"],
    "Severe Head Injury": ["I hit my head", "I have a head injury", "I’m bleeding from my head",
        "my head hurts a lot", "I was hit in the head", "I have a concussion",
        "I’m dizzy after hitting my head", "I feel nausea after a head injury",
        "I fell on my head", "I hit my head hard"],
    "Poisoning": ["I swallowed something poisonous", "I’m feeling sick after eating something",
        "I ingested something toxic", "I’m vomiting after eating", "I have food poisoning",
        "I feel nauseous after eating", "I swallowed chemicals", "I ate something I shouldn't have",
        "I feel weak after eating something", "I’m dizzy after eating something"]
}

emergency_videos = {
    "Burn Injury": "https://youtu.be/iajIQ5C1XyA?si=H0M_TohFEgao0k6K",
    "Dizziness or Fainting": "https://youtu.be/umQ6rJRzY3E?si=3riwg1YOhkgE3xn3",
    "Breathing Problem": "https://youtu.be/8EyYTW-1EP0?si=TUn5VAY7BhIIU2an",
    "Cut or Bleeding": "https://youtu.be/L6jjyikFwmA?si=puw5toKryIrBGqeG",
    "Heart Attack": "https://youtu.be/7Ee1o05x5kw?si=VqcIvo8Qm9gTpQQy",
    "Stroke": "https://youtu.be/7Ee1o05x5kw?si=u7cSW4nEUQ-9B97d",
    "Choking": "https://youtu.be/WeY4KJUnfMc?si=eRvoVdQdWLfg42uv",
    "Severe Allergic Reaction": "https://www.youtube.com/watch?v=sWZms07lD8o",
    "Severe Head Injury": "https://youtu.be/Wu53L0oKkKg?si=BaP9ukWQAIFaP_F5",
    "Poisoning": "https://youtu.be/PgGUSAM6XJw?si=EPktadek4YQSowZq"
}

# Functions
def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        status_label.config(text="Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        status_label.config(text=f"You said: {command}")
        return command
    except sr.UnknownValueError:
        status_label.config(text="Sorry, I couldn't understand your voice.")
        speak("Sorry, I couldn't understand your voice.")
        return None
    except sr.RequestError:
        status_label.config(text="Speech service error.")
        speak("Sorry, I'm having trouble with the speech service.")
        return None

def match_emergency(command):
    if command:
        best_match = None
        highest_ratio = 0
        for emergency, phrases in emergency_phrases.items():
            for phrase in phrases:
                ratio = fuzz.token_set_ratio(command, phrase)
                if ratio > highest_ratio:
                    highest_ratio = ratio
                    best_match = emergency
        if best_match and highest_ratio > 50:
            status_label.config(text=f"Detected: {best_match}")
            speak(f"Emergency detected: {best_match}. Opening instructions.")
            webbrowser.open(emergency_videos[best_match])
        else:
            status_label.config(text="No emergency matched.")
            speak("I couldn't match that to a known emergency.")
    else:
        status_label.config(text="No command received.")

def start_listening():
    threading.Thread(target=lambda: match_emergency(listen()), daemon=True).start()

# GUI setup
root = tk.Tk()
root.title("AI Emergency Assistant")
root.geometry("600x600")
root.configure(bg='lightblue')

# Background image
bg_image = PhotoImage(file="background.png")  # Ensure this image exists in your project folder
background_label = tk.Label(root, image=bg_image)
background_label.place(relwidth=1, relheight=1)

frame = tk.Frame(root, bg='lightpink', bd=3, relief="solid")
frame.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.4, anchor='center')

title_label = tk.Label(frame, text="AI Emergency Assistant", font=("Helvetica", 24, "bold"), fg="darkmagenta", bg="white")
title_label.pack(pady=10)

start_button = tk.Button(frame, text="Start Speaking", font=("Helvetica", 18, "bold"),
                         bg="lavender", fg="black", relief="raised", command=start_listening)
start_button.pack(pady=20, ipadx=10, ipady=5)

# Hover effect
def on_enter(e): start_button.config(bg="yellow")
def on_leave(e): start_button.config(bg="lavender")
start_button.bind("<Enter>", on_enter)
start_button.bind("<Leave>", on_leave)

status_label = tk.Label(frame, text="Please click 'Start Speaking' to begin.",
                        font=("Helvetica", 14), fg="purple", bg="white")
status_label.pack(pady=10)

root.mainloop()
