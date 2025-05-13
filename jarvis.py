import pyttsx3
import speech_recognition as sr
import requests
import datetime
import os
import time
import webbrowser
import pyautogui
import urllib.parse

# OpenAI API key - replace with your actual key
OPENAI_API_KEY = "sk-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"

# Initialize the speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Default male voice
engine.setProperty('rate', 180)  # Speaking rate

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wish_user():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning, sir!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon, sir!")
    else:
        speak("Good Evening, sir!")
    speak("Jarvis online and ready to assist.")

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("Processing...")
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except Exception as e:
        print("Error processing audio. Please try again.")
        return None

def search_google(query):
    """Search Google for the given query"""
    search_term = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={search_term}"
    speak(f"Searching Google for {query}, sir.")
    webbrowser.open(url)
    speak("Here are the search results. Awaiting your command, sir.")

def search_youtube(query):
    """Search YouTube for the given query"""
    search_term = urllib.parse.quote(query)
    url = f"https://www.youtube.com/results?search_query={search_term}"
    speak(f"Searching YouTube for {query}, sir.")
    webbrowser.open(url)
    speak("Here are the YouTube results. Awaiting your command, sir.")

def control_youtube(command):
    """Control YouTube playback using keyboard shortcuts"""
    if 'pause' in command or 'stop' in command:
        speak("Pausing the video, sir.")
        pyautogui.press('space')  # Space bar to pause/play
    
    elif 'play' in command or 'resume' in command:
        speak("Playing the video, sir.")
        pyautogui.press('space')  # Space bar to pause/play
    
    elif 'full screen' in command:
        speak("Switching to full screen mode, sir.")
        pyautogui.press('f')  # F key for fullscreen
    
    elif 'exit full screen' in command:
        speak("Exiting full screen mode, sir.")
        pyautogui.press('escape')  # Escape to exit fullscreen
    
    elif 'mute' in command:
        speak("Muting the video, sir.")
        pyautogui.press('m')  # M key to mute/unmute
    
    elif 'unmute' in command:
        speak("Unmuting the video, sir.")
        pyautogui.press('m')  # M key to mute/unmute
    
    elif 'forward' in command or 'skip forward' in command:
        speak("Skipping forward, sir.")
        pyautogui.press('right')  # Right arrow to skip forward
    
    elif 'back' in command or 'rewind' in command:
        speak("Rewinding the video, sir.")
        pyautogui.press('left')  # Left arrow to rewind
    
    elif 'volume up' in command:
        speak("Increasing volume, sir.")
        pyautogui.press('up')  # Up arrow for volume up
    
    elif 'volume down' in command:
        speak("Decreasing volume, sir.")
        pyautogui.press('down')  # Down arrow for volume down
    
    elif 'next video' in command:
        speak("Playing next video, sir.")
        pyautogui.press('shift+n')  # Shift+N for next video
    
    elif 'previous video' in command:
        speak("Playing previous video, sir.")
        pyautogui.press('shift+p')  # Shift+P for previous video
    
    else:
        speak("I'm not familiar with that YouTube command. Awaiting your command, sir.")

def get_response_from_openai(query):
    """Send query to OpenAI API and get response"""
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    
    data = {
        "model": "gpt-3.5-turbo",  # You can use other models like gpt-4 if you have access
        "messages": [
            {
                "role": "system",
                "content": "You are JARVIS, an advanced AI assistant. Respond directly to queries in a helpful, concise, and slightly formal tone. Always end your responses with 'Awaiting your command, sir.' or similar phrase."
            },
            {
                "role": "user",
                "content": query
            }
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    # Add processing delay to simulate thinking (about 10 seconds)
    print("Processing request...")
    time.sleep(10)
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            response_text = result["choices"][0]["message"]["content"]
            
            # Ensure response ends with command prompt if not already present
            command_phrases = ["awaiting your command", "at your service", "what else can i do"]
            if not any(phrase in response_text.lower() for phrase in command_phrases):
                response_text += " Awaiting your command, sir."
                
            return response_text.strip()
        else:
            print(f"API Error: {response.status_code}, {response.text}")
            return "I'm experiencing a temporary system issue. Please try again in a moment. Awaiting your command, sir."
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return "I'm experiencing a connection issue. Please check your internet connection. Awaiting your command, sir."

def get_local_response(query):
    """Provide basic responses without using an external API"""
    query = query.lower()
    
    # Time
    if any(word in query for word in ["time", "hour", "clock"]):
        current_time = datetime.datetime.now().strftime("%H:%M")
        return f"The current time is {current_time}, sir. Awaiting your command."
    
    # Date
    elif any(word in query for word in ["date", "day", "today"]):
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {current_date}, sir. Awaiting your command."
    
    # Greetings
    elif any(word in query for word in ["hello", "hi", "hey"]):
        return "Hello, sir. How may I assist you today? Awaiting your command."
        
    # About Jarvis
    elif "who are you" in query or "what are you" in query:
        return "I am Jarvis, your personal AI assistant. I'm here to help you with information and tasks. Awaiting your command, sir."
    
    # Basic questions
    elif "how are you" in query:
        return "I'm functioning at optimal capacity, sir. Thank you for asking. Awaiting your command."
    
    # Weather (simulated)
    elif "weather" in query:
        return "I'm sorry, I don't have access to real-time weather data at the moment. Would you like me to open a weather website for you? Awaiting your command, sir."
    
    # Default response
    else:
        return "I'm processing that query locally with limited capabilities. To provide a better response, I would need to connect to an AI service. Awaiting your command, sir."

def perform_action(command):
    """Process the command and take appropriate action"""
    # Handle system commands directly
    if 'exit' in command or 'goodbye' in command or 'bye' in command:
        speak("Shutting down Jarvis. Have a good day, sir.")
        exit()
    
    # YouTube Controls    
    elif any(term in command for term in ['pause video', 'play video', 'full screen', 'mute', 'volume', 'rewind', 'forward', 'next video']):
        control_youtube(command)
        
    # Open YouTube and search
    elif 'search youtube for' in command or 'find on youtube' in command:
        # Extract search query
        search_query = command.replace('search youtube for', '').replace('find on youtube', '').strip()
        search_youtube(search_query)
        
    elif 'open youtube' in command:
        if len(command) > 12:  # If there's more text after "open youtube"
            search_query = command[12:].strip()
            search_youtube(search_query)
        else:
            speak("Opening YouTube, sir.")
            webbrowser.open("https://www.youtube.com")
            speak("YouTube is now open. Awaiting your command, sir.")
    
    # Google search
    elif 'search google for' in command or 'find on google' in command or 'look up' in command:
        # Extract search query
        if 'search google for' in command:
            search_query = command.replace('search google for', '').strip()
        elif 'find on google' in command:
            search_query = command.replace('find on google', '').strip()
        elif 'look up' in command:
            search_query = command.replace('look up', '').strip()
        search_google(search_query)
        
    elif 'open google' in command:
        if len(command) > 11:  # If there's more text after "open google"
            search_query = command[11:].strip()
            search_google(search_query)
        else:
            speak("Opening Google, sir.")
            webbrowser.open("https://www.google.com")
            speak("Google is now open. Awaiting your command, sir.")
    
    # Music player commands
    elif 'play music' in command:
        speak("Playing your favorite playlist, sir.")
        webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")  # Replace with preferred music link
        speak("Music playback initiated. Awaiting your command, sir.")

    # Time queries
    elif 'what is the time' in command or 'current time' in command:
        str_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The current time is {str_time}, sir. Awaiting your command.")

    # Computer shutdown
    elif 'shutdown computer' in command or 'turn off computer' in command:
        speak("Initiating system shutdown. Goodbye, sir.")
        os.system('shutdown /s /t 1')

    # For all other queries - try API or fall back to local
    else:
        # Indicate processing but don't mention the API
        print("Processing...")
        
        # Choose one of these approaches:
        
        # Option 1: Try OpenAI API (requires valid API key)
        # response = get_response_from_openai(command)
        
        # Option 2: Use local response function (no API required)
        response = get_local_response(command)
        
        speak(response)

def main():
    # Check if required packages are installed
    try:
        import pyautogui
    except ImportError:
        print("Installing required packages...")
        os.system("pip install pyautogui")
        import pyautogui
        
    wish_user()
    
    while True:
        command = take_command()
        if command:
            perform_action(command)
        else:
            speak("I didn't catch that. Awaiting your command, sir.")

if __name__ == "__main__":
    main()