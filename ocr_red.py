import time
import pytesseract
import cv2
from gtts import gTTS
import os
import arabic_reshaper
from bidi.algorithm import get_display
import tempfile
from picamera import PiCamera
from pygame import mixer

# تهيئة ميكسر الصوت
mixer.init()

def process_text(text):
    """معالجة النص العربي وتحسين عرضه"""
    if not text.strip():
        return None
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

def text_to_speech(text):
    """تحويل النص إلى كلام باستخدام ملف مؤقت"""
    if not text:
        return
    
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as fp:
        try:
            tts = gTTS(text, lang='ar', slow=False)
            tts.save(fp.name)
            fp.close()
            mixer.music.load(fp.name)
            mixer.music.play()
            while mixer.music.get_busy():
                time.sleep(0.1)
        finally:
            os.unlink(fp.name)

def capture_image(camera):
    """التقاط صورة باستخدام كاميرا الرسبيري باي"""
    temp_image = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
    camera.capture(temp_image.name)
    return temp_image.name

def preprocess_image(image_path):
    """معالجة الصورة لتحسين دقة OCR"""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def qcr_read():
    """الوظيفة الرئيسية"""
    # تهيئة الكاميرا
    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    time.sleep(2)  # إعطاء وقت للإضاءة للتكيف

    try:
        start_time = time.time()
        timeout = 20  # ثانية
        
        while True:
            # التقاط الصورة ومعالجتها
            image_path = capture_image(camera)
            processed_image = preprocess_image(image_path)
            
            # استخراج النص
            text = pytesseract.image_to_string(
                processed_image,
                lang='ara',
                config='--psm 6 --oem 3 -c preserve_interword_spaces=1'
            )
            
            # معالجة النص
            processed_text = process_text(text)
            
            if processed_text:
                print("النص الموجود:")
                print(processed_text)
                text_to_speech(text.strip())
                break
            else:
                print("جار البحث عن نص...")
                
            # التحقق من انتهاء المهلة
            if time.time() - start_time > timeout:
                print("انتهى الوقت المحدد دون اكتشاف نص")
                break

    except Exception as e:
        print(f"حدث خطأ: {str(e)}")
    finally:
        camera.stop_preview()
        camera.close()
        mixer.quit()
        os.unlink(image_path)
        print("تم إيقاف البرنامج")

# qcr_read()