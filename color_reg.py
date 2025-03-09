import time
import cv2
import threading
import subprocess
from picamera2 import Picamera2

# تهيئة إعدادات الصوت
SOUNDS = {
    "احمر": 'sounds/RED.wav',
    "برتقالي": 'sounds/ORANGE.wav',
    "اصفر": 'sounds/YELLOW.wav',
    "اخضر": 'sounds/GREEN.wav',
    "ازرق": 'sounds/BLUE.wav',
    "بنفسجي": 'sounds/VIOLET.wav',
    "ابيض": 'sounds/WHITE.wav',
    "اسود": 'sounds/BLACK.wav',
    "لايوجد": 'sounds/NOT.wav'
}

# متغيرات التحكم
last_color = None
sound_lock = threading.Lock()

def play_audio(color):
    with sound_lock:
        try:
            subprocess.Popen(['aplay', SOUNDS[color]], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            print(f"Error playing sound: {e}")

def ColorRec():
    global last_color
    
    # تهيئة كاميرا Raspberry Pi
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"size": (640, 480)})
    picam2.configure(config)
    picam2.start()
    
    color = "Undefined"
    detection_interval = 0.2  # تقليل معدل الكشف لتوفير الموارد
    
    try:
        while True:
            start_time = time.time()
            
            # التقاط صورة من الكاميرا
            frame = picam2.capture_array()
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # معالجة الصورة
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            height, width, _ = frame.shape
            cx, cy = width//2, height//2
            pixel_center = hsv_frame[cy, cx]
            hue, sat, val = pixel_center

            # خوارزمية كشف الألوان
            new_color = "لايوجد"
            
            if sat < 40:
                if val < 20:
                    new_color = "اسود"
                else:
                    new_color = "ابيض"
            elif val < 30:
                new_color = "اسود"
            elif hue < 5 or hue > 175:
                new_color = "احمر"
            elif 5 <= hue < 22:
                new_color = "برتقالي"
            elif 22 <= hue < 33:
                new_color = "اصفر"
            elif 33 <= hue < 78:
                new_color = "اخضر"
            elif 78 <= hue < 131:
                new_color = "ازرق"
            elif 131 <= hue < 170:
                new_color = "بنفسجي"

            # تحديث الصوت والعرض
            if new_color != color:
                color = new_color
                if color != last_color:
                    threading.Thread(target=play_audio, args=(color,)).start()
                    last_color = color

            # عرض النتيجة
            cv2.rectangle(frame, (cx - 220, 10), (cx + 200, 120), (255, 255, 255), -1)
            cv2.putText(frame, color, (cx - 200, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.circle(frame, (cx, cy), 10, (0, 255, 0), 2)
            cv2.imshow("Color Detector", frame)
            
            # التحكم في معدل التحديث
            processing_time = time.time() - start_time
            delay = max(1, int((detection_interval - processing_time) * 1000))
            
            if cv2.waitKey(delay) == ord('q'):
                break

    finally:
        picam2.stop()
        cv2.destroyAllWindows()

# ColorRec()