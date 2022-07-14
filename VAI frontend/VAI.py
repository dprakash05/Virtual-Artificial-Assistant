# importing libraries 
import pandas as pd
import pyttsx3
import datetime
import wikipedia
import requests
import speech_recognition as sr
import pyaudio
import pyjokes
import pywhatkit
from bs4 import BeautifulSoup
import webbrowser
import os
import random
import sys
import shutil
import cv2
import wolframalpha
from twilio.rest import Client
import googletrans
from googletrans import Translator
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtCore import QTimer,QTime,QDate,Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from VAIui import Ui_VAIGUI

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
print(voices[1].id)

engine.setProperty('voice',voices[1].id)
speak('how are you sir')
# this function will greet
def wishme():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour <12:
        speak('good morning')
    elif hour>=12 and hour<16:
        speak('good afternoon')
    elif hour >=16 and hour<19:
        speak('good evening')
    else:
        speak('good night')
    speak('I am VAI, your virtual artificial intelegence,  All my systems are fully functioning, how may i help you?')
    
#wishme()
class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()
        
    def run(self):
        self.TaskExecution()
    # It will take command from user
    def takecommand(self):
        r=sr.Recognizer()

        with sr.Microphone() as source:
            print('listening..')
            r.pause_threshold=1
            audio=r.listen(source) 
        try:
            print('recognizing')
            query=r.recognize_google(audio,language='en-in')
            print(f'user said:{query}\n')
        except Exception as e:
            print(e)
            print('say that again please')
            return 'None'
        return query
    """ We can give command like search in wikipedia, open youtube and play music, play song in youtube.
    we can ask current time,jokes and translate in any language, I have selected Hindi language.
    we can extract similarity snetences from embeded dataframe using cosine similarity.
    """
    def news(self):
        main_url='https://newsapi.org/v2/top-headlines?sources=techcrunch&apikey=c03e1581b08d4921b5d082aef0a11b80'
        main_page=requests.get(main_url).json()
        #print(main_page)
        articles=main_page['articles']
        #print(articles)
        head=[]
        day=['first','second','third','fourth','fifth']
        for ar in articles:
            head.append(ar['title'])
        for i in range(len(day)):
            print(f'todays {day[i]} news is :{head[i]}')
            speak(f'todays {day[i]} news is :{head[i]}')
    
    def TaskExecution(self):
        wishme()
        while True:
            self.query=self.takecommand().lower()

            if  'who is' in self.query:
                speak('searching wikipedia...')
                query=query.replace('wikipedia','')
                results=wikipedia.summary(query,sentences=2)
                speak('according to wikipedia')
                print(results)
                speak(results)
            elif 'open youtube' in self.query:
                webbrowser.open('youtube.com')
            elif 'open google' in self.query:
                webbrowser.open('google.com')
            elif 'play music' in self.query:
                music_dir='D:\\songs'
                songs=os.listdir(music_dir)
                rd=random.choice(songs)
                os.startfile(os.path.join(music_dir,rd))
                print(songs)
                os.startfile(os.path.join(music_dir,songs[0]))
            elif 'time' in self.query:
                strTime=datetime.datetime.now().strftime('%H:%M:%S')
                speak(f'time is {strTime}')
            elif 'play' in self.query:
                song = query.replace('play', '')
                speak (song)
                pywhatkit.playonyt(song)
            elif 'joke' in self.query:
                jokes=(pyjokes.get_joke())
                print(jokes)
                speak(jokes) 
           
            elif 'temperature' in self.query:
                speak('searching temperature')
                temp='temperature in mumbai'
                url=f'https://google.com/search?q={temp}'
                rs=requests.get(url)
                data=BeautifulSoup(rs.text,'html.parser' )
                temps=data.find('div', class_='BNeawe').text
                print(temps)
                speak(f'currenr {temp} is {temps}')
            elif 'translate' in self.query:
                translator=Translator()
                sen=query.replace('translate','')
                sen=translator.translate(sen,src='en',dest='hi')
                print(sen)
                speak(sen.pronunciation)
            elif 'send message' in self.query:
                pywhatkit.sendwhatmsg_instantly('+919820676422','this is test message')
            elif 'exit' in self.query:
                break
            elif 'open camera' in self.query:
                cap=cv2.VideoCapture(0)
                while True:
                    ret,img=cap.read()
                    cv2.imshow('webcam',img)
                    if cv2.waitKey(1)& 0xFF==ord('q'):
                # k=cv2.waitKey(50)
                    #if k==27:
                    # press q foe quit
                        break;
                cap.release()
                cv2.destroyAllWindows()
            elif 'news' in self.query:
                self.news()
            
            elif "where is" in self.query:
                    query = query.replace("where is", "")
                    location = query
                    speak("User asked to Locate")
                    speak(location)
                    webbrowser.open("https://www.google.com/maps/place/'" + location + "")
                    #('https://www.google.com/maps/place/' + map_string)
            elif "calculate" in self.queryquery:
                    
                    app_id = "5QVV3E-GYRWXY8UV5"
                    client = wolframalpha.Client(app_id)
                    indx = query.lower().split().index('calculate')
                    query = query.split()[indx + 1:]
                    res = client.query(' '.join(query))
                    answer = next(res.results).text
                    print("The answer is " + answer)
                    speak("The answer is " + answer)
    """wolframalpha- we can calculate, find GDP ,weather,conversion almost anything we can ask from it.
    """
startExecution=MainThread()
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_VAIGUI()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)
        
    def startTask(self):
        self.ui.movie=QtGui.QMovie("C:/Users/HP/Downloads/Imarticus/Python/VAI/7LP8.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer=QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()
    def showTime(self):
        current_time=QTime.currentTime()
        current_date=QDate.currentDate()
        label_time=current_time.toString('hh:mm:ss')
        label_date=current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

app=QApplication(sys.argv)
vai=Main()
vai.show()
exit(app.exec_())

        
        
    
    
#APPID: 5QVV3E-GYRWXY8UV5
     
        