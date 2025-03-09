
import os 
# The text that you want to convert to audio 
import time
from datetime import datetime
from gtts import gTTS

# import pyttsx3
# # import pygame
# engine = pyttsx3.init()
# engine.setProperty('rate', 100) 
# engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_arSA_NaayfM',)


def timme():
# mytext = time.asctime(time.localtime() )
    dt = datetime.now()

    dt=dt.strftime("%H:%M:%S")
#mytext = date_time.strftime("%c")
    
    tts = gTTS(text=dt, lang='ar')
    filename = "time.mp3"
    tts.save(filename)
    os.system("mpg321 -q " + filename)  # التشغيل بصمت
    os.remove(filename)
    

# timme()
  
# Language in which you want to convert 
# language = 'en'
  
# Passing the text and language to the engine,  
# here we have marked slow=False. Which tells  
# the module that the converted audio should  
# have a high speed 
# myobj = gTTS(text=mytext, lang=language, slow=False) 
  
# Saving the converted audio in a mp3 file named 
# welcome  
# myobj.save("timee.mp3")
# pygame.init()

# pygame.mixer.music.load("timee.mp3")

# pygame.mixer.music.play()
