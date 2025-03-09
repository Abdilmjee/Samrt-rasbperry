import time
import cv2
import os
import face_recognition
import pygame
from picamera2 import Picamera2
from gpiozero import CPUTemperature
import numpy as np

# ---------- إعدادات خاصة بـ Raspberry Pi ----------
# تهيئة الكاميرا
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(config)

# تهيئة الصوت
pygame.mixer.init()

# تحميل الوجوه مسبقاً
KNOWN_FACES = {
    "abdilmjeed": ("عبدالمجيد", "img/abdilmjeed.jpg"),
    "amjed": ("امجد المهلل", "img/amjed.jpg"),
    "mohmmed": ("محمد عصام", "img/mohmmed.jpg")
}

def load_encodings():
    encodings = []
    names = []
    for name, (ar_name, path) in KNOWN_FACES.items():
        image = cv2.imread(path)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb)
        if face_locations:
            encoding = face_recognition.face_encodings(rgb, face_locations)[0]
            encodings.append(encoding)
            names.append(name)
    return encodings, names

known_encodings, known_names = load_encodings()

# ---------- دوال مساعدة ----------
def speak(text):
    # استخدام espeak للأفضل أداء على Pi (يجب تثبيته)
    os.system(f'espeak -v ar "{text}" --stdout | aplay -q')

def process_frame(frame):
    small_frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
    rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    
    # اكتشاف الوجوه باستخدام Haar Cascade للأداء الأفضل
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    names = []
    for (x,y,w,h) in faces:
        encoding = face_recognition.face_encodings(rgb, [(y,x+h,y+w,x)])[0]
        matches = face_recognition.compare_faces(known_encodings, encoding)
        name = "Unknown"
        if True in matches:
            name = known_names[matches.index(True)]
        names.append((x,y,w,h,name))
    return names

# ---------- الدورة الرئيسية ----------
def main():
    picam2.start()
    last_names = set()
    start_time = time.time()
    
    try:
        while time.time() - start_time < 20:  # تشغيل لمدة 20 ثانية
            frame = picam2.capture_array()
            
            # معالجة الإطار كل 3 لقطات
            if int(time.time()*10) % 3 == 0:
                faces = process_frame(frame)
                
                # التعرف على الأسماء الجديدة
                current_names = {name for (_,_,_,_,name) in faces}
                new_names = current_names - last_names
                
                for name in new_names:
                    if name in KNOWN_FACES:
                        speak(KNOWN_FACES[name][0])
                    else:
                        speak("غير معروف")
                last_names = current_names.copy()
            
            # العرض (اختياري)
            # cv2.imshow('Face Recognition', frame)
            if cv2.waitKey(1) == ord('q'):
                break
            
            # مراقبة درجة الحرارة
            cpu = CPUTemperature()
            if cpu.temperature > 70:
                print("تحذير: درجة الحرارة مرتفعة!")
                
    finally:
        picam2.stop()
        cv2.destroyAllWindows()

# main()



# import time
# import face_recognition
# import cv2
# import os
# from gtts import gTTS
# from picamera import PiCamera
# from picamera.array import PiRGBArray

# # تهيئة كاميرا Raspberry Pi
# camera = PiCamera()
# camera.resolution = (640, 480)
# raw_capture = PiRGBArray(camera, size=(640, 480))
# time.sleep(0.1)

# # القاموس العربي
# dicEnAr = {
#     "abdilmjeed": "عبدالمجيد",
#     "amjed": "أمجد المهلل",
#     "mohmmed": "محمد عصام",
#     "unknown": "شخص غير معروف"
# }

# # تحميل الصور المعروفة مسبقًا
# def load_known_faces():
#     known_encodings = []
#     known_names = []
    
#     # تحميل الصور من مجلد faces
#     faces_dir = "faces/"
#     for filename in os.listdir(faces_dir):
#         if filename.endswith(".jpg"):
#             image = face_recognition.load_image_file(faces_dir + filename)
#             encoding = face_recognition.face_encodings(image)[0]
#             known_encodings.append(encoding)
#             known_names.append(filename.split(".")[0])
    
#     return known_encodings, known_names

# known_face_encodings, known_face_names = load_known_faces()

# def speak_arabic(text):
#     try:
#         tts = gTTS(text=text, lang='ar')
#         tts.save("temp.mp3")
#         os.system("mpg321 -q temp.mp3")
#         os.remove("temp.mp3")
#     except Exception as e:
#         print(f"خطأ في توليد الصوت: {e}")

# def face_rec():
#     start_time = time.time()
    
#     for frame in camera.capture_continuous(
#         raw_capture, format="bgr", use_video_port=True):
        
#         img = frame.array
#         small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
#         rgb_small_frame = small_frame[:, :, ::-1]

#         # معالجة الوجوه كل إطارين لتحسين الأداء
#         face_locations = face_recognition.face_locations(rgb_small_frame)
#         face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

#         face_names = []
#         for face_encoding in face_encodings:
#             matches = face_recognition.compare_faces(
#                 known_face_encodings, face_encoding, tolerance=0.5)
#             name = "unknown"

#             if True in matches:
#                 first_match_index = matches.index(True)
#                 name = known_face_names[first_match_index]
            
#             face_names.append(name)
#             ar_name = dicEnAr.get(name, dicEnAr["unknown"])
            
#             # عرض النتائج
#             (top, right, bottom, left) = face_locations[0]
#             top *= 4
#             right *= 4
#             bottom *= 4
#             left *= 4
            
#             cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
#             cv2.putText(img, ar_name, 
#                         (left + 6, bottom - 6), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 
#                         0.8, (255, 255, 255), 2)
            
#             # نطق النتيجة
#             speak_arabic(f"أهلا وسهلا {ar_name}")

#         cv2.imshow('Face Recognition', img)
#         raw_capture.truncate(0)

#         # الخروج بعد 20 ثانية أو بالضغط على q
#         if cv2.waitKey(1) == ord('q') or (time.time() - start_time) > 20:
#             break

#     camera.close()
#     cv2.destroyAllWindows()

# if name == "main":
#     face_rec()