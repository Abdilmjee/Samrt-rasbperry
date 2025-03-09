import ad as SpeechToTextConverter
import color_reg
import object
import facere
import ocr_red
import rec
import time_1
ult=SpeechToTextConverter.SpeechToTextConverter()

while True:
    try:
        speech=ult.process_audio()
        print("speech :",speech)
        if 'NUMBER ONE' in speech: 
            object.Camera() #التعرف على الاشياء 

        elif 'NUMBER TWO' in speech:
            color_reg.ColorRec() #التعرف على الالوان  

        elif 'NUMBER THREE' in speech:
            facere.main() #التعرف على الوجوة 
    
        elif 'NUMBER FOUR' in speech:
            ocr_red.qcr_read() #العرف على النصوص 
        
        elif 'TIME' in speech:
            time_1.timme() #معرفة الوقت الحالي  

        elif 'VOICE' in speech:
            filename = "recording0.wav"
            rec.record_audio(filename)
        
        elif 'OPEN ' in speech:    
            filename = "recording0.wav"
            rec.play_audio(filename)
        
        elif 'CLOSE' in speech:
            break
    
        else:
            print(" Again speech ...")
    
    except KeyboardInterrupt:
        print ("Exception during recording process  " + str())