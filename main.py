import speech_recognition as sr
from gtts import gTTS
import webbrowser
import requests
import time
import os
from playsound import playsound
from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play
import re
from datetime import datetime
import tempfile
import random

r = sr.Recognizer()

news_API_KEY = 

yt_API_KEY = 

client = OpenAI(api_key=)

wheather_API_KEY = 

def microphone():
    with sr.Microphone() as source:
        print("Speak something...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        text = r.recognize_google(audio)
        print("You said:", text)
        return text


def speak_gtts(text, lang="en", speed=1.2):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        filename = tmp.name
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    sound = AudioSegment.from_mp3(filename)
    if speed != 1.0:
        sound = sound.speedup(playback_speed=1.2)
    play(sound)
    os.remove(filename)


while True:

    try:

        if microphone().lower() == "jarvis":
            speak_gtts("Yes", lang="en", speed=1.2)
            command = microphone()
            if command.lower().startswith("open"):
                webbrowser.open(f'www.{command.replace("open", "").strip()}.com')
                print(command.replace("open", "").strip())

            elif command.lower() in [
                "repeat",
                "repeat with me",
                "repeat what i am saying",
                "repeat whatever i am saying",
            ]:
                speak_gtts("Say whatever you want to say", lang="en", speed=1.2)
                saying = microphone()
                speak_gtts(saying)

            elif command.lower() in [
                "news",
                "give me news",
                "give me todays news",
                "give me today news",
            ]:
                speak_gtts("Ok", lang="en", speed=1.2)
                news_url = f"https://newsapi.org/v2/everything?q=India&sortBy=publishedAt&apiKey={news_API_KEY}"
                response = requests.get(news_url)
                data = response.json()

                if data["status"] == "ok":
                    articles = data["articles"]
                    for i, article in enumerate(articles[:5], start=1):
                        print((f"{i}. {article['title']}"))
                        title = f"{i}. {article['title']}"
                        print(f"   Source: {article['source']['name']}")
                        print(f"   URL: {article['url']}\n")
                        clean_news = re.sub(r"[^\w\s\u0900-\u097F]", "", title)
                        speak_gtts(title)

            elif command.lower().startswith("play"):
                speak_gtts("Ok", lang="en", speed=1.2)
                song = command
                yt_query = song.replace(" ", "+")
                yt_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={yt_query}&type=video&maxResults=1&key={yt_API_KEY}"
                yt_res = requests.get(yt_url).json()

                if yt_res["items"]:
                    video_id = yt_res["items"][0]["id"]["videoId"]
                    webbrowser.open(f"https://www.youtube.com/watch?v={video_id}")
                else:
                    print("No song found.")
            elif command.lower() in [
                "i have a question",
                "i have question",
                "have question",
                "question",
                "have a question",
            ]:
                responses_question = [
                    "Sure, go ahead. What’s your question?",
                    "I’m listening. What do you want to ask?",
                    "Ask me anything, I’m ready.",
                    "Alright, tell me your question.",
                    "Go ahead and ask, I’ll do my best to answer.",
                    "What’s on your mind?",
                    "I’m all ears, what do you want to know?",
                ]
                random_sentence_question = random.choice(responses_question)
                speak_gtts(random_sentence_question, lang="en", speed=1.1)

                ai = microphone()
                if ai.lower() in [
                    "jarvis leave",
                    "jarvis exit",
                    "jarvis stop",
                    "jarvis quit",
                    "jarvis go to sleep",
                    "jarvis shutdown",
                    "bye jarvis",
                    "turn off jarvis",
                ]:
                    speak_gtts("good by")
                    break
                response = client.responses.create(
                    model="gpt-4o-mini",
                    input=ai,
                    store=True,
                )
                ai_ans = response.output_text
                clean_ai_ans = re.sub(r"[^A-Za-z0-9\s]", "", ai_ans)
                print(ai_ans)
                speak_gtts(clean_ai_ans)

            elif command.lower() in [
                "date",
                "what is the date of today",
                "what is the time",
                "what is the date",
                "time",
                "date and time",
                "what is the time",
                "what's the date",
            ]:
                now = datetime.now()
                date_time_str = now.strftime(
                    "Today is %A, %d %B %Y. The time is %I:%M %p."
                )
                speak_gtts(date_time_str)
            elif "weather" in command.lower() :
                which_city = [
                "Please provide the city name.",
                "Tell me the name of the city.",
                "What is the city name?",
                "Share the city name.",
                "Can you specify the city?",
                "Name the city, please.",
                "I need the city name.",
                "Could you give me the city name?",
                "Let me know the city name.",
                "State the city name."
            ]
                random_which_city = random.choice(which_city)
                speak_gtts(random_which_city)
                def get_weather(city):
                    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={wheather_API_KEY}&units=metric"
                    response = requests.get(url)
                    if response.status_code == 200:
                        data = response.json()
                        temp = data["main"]["temp"]
                        description = data["weather"][0]["description"]
                        print(f"Temperature in {city} is {temp}°C with {description}.")
                        speak_gtts(f"Temperature in {city} is {temp} degrees Celsius with {description}.")
                    else:
                        print("Sorry, I couldn't get the weather data right now.")
                        speak_gtts("Sorry, I couldn't get the weather data right now.")
                city_name = microphone()        
                get_weather(city_name.replace("in", "").strip())

            elif any(keyword in command.lower() for keyword in ["leave", "exit", "good by", "turn off", "off"]) or ('ai' in locals() and any(keyword in ai.lower() for keyword in ["leave", "exit", "good by", "turn off", "off"])):
                speak_gtts("good by")
                break
    except sr.WaitTimeoutError:
        print("Listening timed out, no speech detected.")

    except sr.UnknownValueError:
        print("Sorry, I could not understand. Please say that again.")

    except sr.RequestError as e:
        print(f"Could not request results; {e}")
