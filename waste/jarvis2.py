#!/usr/bin/env python3
"""
Jarvis (Voice Assistant) - Python
- Listens to your voice commands
- Speaks responses (offline TTS)
- Answers with Wikipedia summaries (spoken aloud)
- Opens websites and basic apps
- Keeps the conversation going (continuation mode)
"""

import os
import sys
import platform
import webbrowser
import subprocess
from datetime import datetime

# ---------- Third-party libraries ----------
try:
    import speech_recognition as sr
except Exception as e:
    print("ERROR: SpeechRecognition not installed. Install with: pip install SpeechRecognition")
    raise

try:
    import pyttsx3
except Exception as e:
    print("ERROR: pyttsx3 not installed. Install with: pip install pyttsx3")
    raise

try:
    import wikipedia
except Exception as e:
    print("ERROR: wikipedia not installed. Install with: pip install wikipedia")
    raise

# ---------- TTS (pyttsx3) ----------
def init_tts():
    engine = pyttsx3.init()
    try:
        engine.setProperty("rate", 175)
        engine.setProperty("volume", 1.0)
        voices = engine.getProperty("voices")
        if voices:
            preferred = None
            for v in voices:
                name = (v.name or "").lower()
                if "zira" in name or "female" in name:
                    preferred = v.id
                    break
            engine.setProperty("voice", preferred or voices[0].id)
    except Exception:
        pass
    return engine

engine = init_tts()

def speak(text: str):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

# ---------- STT (SpeechRecognition) ----------
recognizer = sr.Recognizer()

def listen(timeout=3, phrase_time_limit=8) -> str:
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.6)
        print("🎤 Listening...")
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

    try:
        print("🧠 Recognizing...")
        query = recognizer.recognize_google(audio, language="en-IN")
        print(f"You: {query}")
        return query.lower().strip()
    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Speech service is unavailable right now.")
        return ""

# ---------- Wikipedia helper ----------
def wiki_answer(question: str, sentences: int = 2):
    wikipedia.set_lang("en")
    q = question.strip()
    for prefix in ("who is", "what is", "tell me about", "define", "wikipedia"):
        if q.startswith(prefix):
            q = q[len(prefix):].strip(" ?")
            break

    if not q:
        speak("Please tell me what to search on Wikipedia.")
        return

    try:
        summary = wikipedia.summary(q, sentences=sentences, auto_suggest=True, redirect=True)
        speak(summary)   # ✅ always speaks the Wikipedia answer
    except wikipedia.DisambiguationError as e:
        option = e.options[0]
        try:
            summary = wikipedia.summary(option, sentences=sentences)
            speak(summary)
        except Exception:
            opts = ", ".join(e.options[:5])
            speak(f"That has multiple meanings. For example: {opts}.")
    except wikipedia.PageError:
        speak(f"I couldn't find anything about '{q}' on Wikipedia.")
    except Exception:
        speak("Sorry, I had trouble reaching Wikipedia.")

# ---------- Command handlers ----------
def open_website(name_or_url: str):
    sites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "whatsapp": "https://web.whatsapp.com",
        "gmail": "https://mail.google.com",
        "github": "https://github.com",
        "stackoverflow": "https://stackoverflow.com",
    }
    url = sites.get(name_or_url.lower(), name_or_url)
    if not url.startswith("http"):
        url = "https://www.google.com/search?q=" + url.replace(" ", "+")
    webbrowser.open(url)
    speak(f"Opening {name_or_url}.")

def open_app(app: str):
    system = platform.system().lower()
    
    try:
        if system == "windows":
            mapping = {
                "chrome": "chrome",
                "edge": "msedge",
                "firefox": "firefox",
                "vs code": "code",
                "code": "code",
                "file explorer": "explorer",
                "notepad": "notepad",
            }
            cmd = mapping.get(app.lower(), app)
            subprocess.run(["cmd", "/c", "start", "", cmd], shell=True)
        elif system == "darwin":
            mapping = {
                "chrome": "Google Chrome",
                "vs code": "Visual Studio Code",
                "code": "Visual Studio Code",
                "safari": "Safari",
                "notes": "Notes",
                "finder": "Finder",
            }
            target = mapping.get(app.lower(), app)
            subprocess.Popen(["open", "-a", target])
        else:
            mapping = {
                "chrome": "google-chrome",
                "firefox": "firefox",
                "vs code": "code",
                "code": "code",
                "files": "nautilus",
            }
            cmd = mapping.get(app.lower(), app)
            subprocess.Popen([cmd])
        speak(f"Opening {app}.")
    except Exception:
        speak(f"Sorry, I couldn't open {app} on this system.")

def say_time():
    now = datetime.now()
    speak("The time is " + now.strftime("%I:%M %p"))

def say_date():
    today = datetime.now()
    speak("Today is " + today.strftime("%A, %B %d, %Y"))

def google_search(query: str):
    q = query.strip().replace(" ", "+")
    url = f"https://www.google.com/search?q={q}"
    webbrowser.open(url)
    speak(f"Searching for {query} on Google.")

# ---------- Main intent parser ----------
def handle_intent(query: str) -> bool:
    if not query:
        return True

    if any(w in query for w in ["exit", "quit", "stop", "goodbye", "bye"]):
        speak("Goodbye!")
        return False

    if any(w in query for w in ["hello", "hi jarvis", "hey jarvis", "wake up jarvis"]):
        speak("Hello! How can I help you?")

    elif "time" in query:
        say_time()
    elif "date" in query:
        say_date()

    elif query.startswith("open "):
        target = query.split("open ", 1)[1]
        if target in ["youtube", "google", "whatsapp", "gmail", "github", "stackoverflow"]:
            open_website(target)
        else:
            open_app(target)

    elif query.startswith("search for "):
        q = query.split("search for ", 1)[1]
        google_search(q)

    elif "wikipedia" in query or query.startswith(("who is", "what is", "tell me about", "define ")):
        wiki_answer(query, sentences=2)

    elif query.startswith(("who", "what", "when", "where", "why", "how", "tell me")):
        wiki_answer(query, sentences=2)

    else:
        google_search(query)

    # 🔥 Continuation prompt
    speak("Would you like to ask me something else?")
    return True

# ---------- Run ----------
def main():
    speak("Friday online sir. How may I assist you today!")
    try:
        while True:
            query = listen(timeout=4, phrase_time_limit=10)
            if not handle_intent(query):
                break
    except KeyboardInterrupt:
        print("\n^C")
        speak("Stopping now. Bye!")

if __name__ == "__main__":
    main()