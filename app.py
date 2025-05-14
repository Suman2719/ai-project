import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import webbrowser

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Dictionary of emergency types and matching phrases
emergency_phrases = {
    "Burn Injury": [ "I burned my hand", "my hand is burned", "I have a burn", "burned my skin",
        "I got a burn", "my finger is burned", "I touched something hot", "my skin is burning",
        "I feel a burning sensation", "I burned myself"
    ],
    "Dizziness or Fainting": [
        "I feel dizzy", "I'm fainting", "I feel weak", "I feel lightheaded", "I'm about to pass out",
        "I feel like I'm going to fall", "I have vertigo", "I'm losing balance", "I feel nauseous",
        "I'm feeling faint"
    ],
    "Breathing Problem": [
        "I can't breathe", "I'm having trouble breathing", "I'm gasping for air", "I'm out of breath",
        "I can't catch my breath", "I'm having an asthma attack", "I can't get enough air", "I'm wheezing",
        "I'm short of breath", "I have trouble breathing"
    ],
    "Cut or Bleeding": [
        "I cut myself", "I'm bleeding","I got a cut","My hand is bleeding","there is a cut", "I have a cut", "I have a wound", "I'm bleeding from my hand",
        "there's blood coming out", "I injured myself", "I have a deep cut", "my cut is bleeding a lot",
        "I need to stop the bleeding"
    ],
    "Heart Attack": [
        "I feel chest pain", "I have chest pain", "I'm having a heart attack", "my chest hurts", "I'm feeling pressure in my chest",
        "I feel tightness in my chest", "I'm sweating and have chest pain", "I'm experiencing pain in my left arm", 
        "I'm having a heart issue", "I feel light-headed and chest pain"
    ],
    "Stroke": [
        "I feel numb", "I feel paralyzed", "I'm having a stroke", "I can't move my arm", "I have sudden weakness",
        "my face is drooping", "I have trouble speaking", "I feel dizzy and weak", "I'm losing control of my body",
        "I feel a sudden numbness"
    ],
    "Choking": [
        "I can't breathe", "I'm choking", "I can't swallow", "I have something stuck in my throat", "I'm gagging",
        "I'm choking on food", "I can't cough", "I feel like I'm suffocating", "my throat is blocked",
        "I can't clear my throat"
    ],
    "Severe Allergic Reaction": [
        "I can't breathe", "I have swelling in my face", "I’m allergic to something", "I need an epinephrine shot", 
        "I have hives", "I have a rash", "my throat is closing up", "I have a bee sting", "I’m allergic to nuts", 
        "I feel itchy all over"
    ],
    "Severe Head Injury": [
        "I hit my head", "I have a head injury", "I’m bleeding from my head", "my head hurts a lot", 
        "I was hit in the head", "I have a concussion", "I’m dizzy after hitting my head", "I feel nausea after a head injury",
        "I fell on my head", "I hit my head hard"
    ],
    "Poisoning": [
        "I swallowed something poisonous", "I’m feeling sick after eating something", "I ingested something toxic", 
        "I’m vomiting after eating", "I have food poisoning", "I feel nauseous after eating", "I swallowed chemicals",
        "I ate something I shouldn't have", "I feel weak after eating something", "I’m dizzy after eating something" ],  
}

# YouTube links for the emergency types
emergency_videos = {
    "Burn Injury": "https://youtu.be/iajIQ5C1XyA?si=H0M_TohFEgao0k6K",  # Update with specific, relevant video
    "Dizziness or Fainting": "https://youtu.be/umQ6rJRzY3E?si=3riwg1YOhkgE3xn3",  # Updated video link
    "Breathing Problem": "https://youtu.be/8EyYTW-1EP0?si=TUn5VAY7BhIIU2an",  # Updated link
    "Cut or Bleeding": "https://youtu.be/L6jjyikFwmA?si=puw5toKryIrBGqeG",  # Correct video
    "Heart Attack": "https://youtu.be/7Ee1o05x5kw?si=VqcIvo8Qm9gTpQQy",  # Accurate video link
    "Stroke": "https://youtu.be/7Ee1o05x5kw?si=u7cSW4nEUQ-9B97d",  # Correct video
    "Choking": "https://youtu.be/WeY4KJUnfMc?si=eRvoVdQdWLfg42uv",  # Updated video link
    "Severe Allergic Reaction": "https://www.youtube.com/watch?v=sWZms07lD8o",  # Updated
    "Severe Head Injury": "https://youtu.be/Wu53L0oKkKg?si=BaP9ukWQAIFaP_F5",  # Accurate video
    "Poisoning": "https://youtu.be/PgGUSAM6XJw?si=EPktadek4YQSowZq",  # Updated link
}

# Function to give voice feedback
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to the user's voice command
def listen():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio).lower()
        print(f"Command: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand your voice. Could you please repeat?")
        speak("Sorry, I couldn't understand your voice. Could you please repeat?")
        return None
    except sr.RequestError:
        print("Sorry, I'm having trouble with the speech service.")
        speak("Sorry, I'm having trouble with the speech service.")
        return None

# Function to match the user's input to an emergency type
def match_emergency(command):
    if command:
        best_match = None
        highest_ratio = 0

        for emergency, phrases in emergency_phrases.items():
            for phrase in phrases:
                ratio = fuzz.ratio(command, phrase)
                if ratio > highest_ratio:
                    highest_ratio = ratio
                    best_match = emergency

        if best_match and highest_ratio > 50:
            print(f"Emergency: {best_match}")
            speak(f"Emergency detected: {best_match}. Please follow the necessary steps.")
            webbrowser.open(emergency_videos[best_match])
        else:
            print("I couldn't match it to a known emergency.")
            speak("I couldn't match it to a known emergency.")
    else:
        print("No command detected.")
        speak("No command detected.")

# Function to run the assistant in a way that is friendly to GUI integration
def process_command(command):
    if command:
        match_emergency(command)
    else:
        print("No command detected.")
        speak("No command detected.")

# Main function to run the assistant
def main():
    while True:
        command = listen()
        if command:
            match_emergency(command)
        else:
            break

# This must be at the bottom!
if __name__ == "__main__":
    main()
