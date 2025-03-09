import time
import cv2
from gtts import gTTS
import os
from picamera.array import PiRGBArray
from picamera import PiCamera

# القاموس المعدل (أضفنا ترجمات للكلمات الفارغة)
dicEnAr = {
    # ... (ابق المحتوى الأصلي كما هو مع إضافة الترجمات المفقودة) ...
   "person": " شخص ", "bicycle": " دراجة هوائيه ", "car": " سيارة ", "motorbike": " دؤاجة نارية ",
   "aeroplane": " طائرة ", "bus": " جافلة ",

   "train": "قطار",
   "truck": "شاحنة",
   "boat": "قارب",
   "traffic light": "اشارة المرور",
   "fire hydrant": "مضخةاطفاء",
   "stop sign": "علامة توقف ",
   "parking meter": "مواقف السيارات",
   "bench": " مقعد ",
   "bird": "طائر",
   "cat": " قطه",
   "dog": " كلب ",
   "horse": " حصان",
   "sheep": "خروف",
   "cow": "بقرة",
   "elephant": "فيل",
   "bear": "دب",
   "zebra": "حمار وحشي",
   "giraffe": "زرافة",
   "backpack": "حقيبة ظهر",
   "umbrella": "مظلة",
   "handbag": "",
   "tie": "",
   "suitcase": "",
   "frisbee": "",
   "skis": "",
   "snowboard": "",
   "sports ball": "",
   "kite": "",
   "baseball bat": "",
   "baseball glove": "",
   "skateboard": "",
   "surfboard": "",
   "tennis racket": "",
   "bottle": "",
   "wine glass": "",
   "cup": "",
   "fork": "",
   "knife": "",
   "spoon": "",
   "bowl": "",
   "banana": "",
   "apple": "",
   "sandwich": "",
   "orange": "",
   "broccoli": "",
   "carrot": "",
   "hot dog": "كلب",
   "pizza": "",
   "donut": "",
   "cake": "",
   "chair": "",
   "sofa": "",
   "pottedplant": "",
   "bed": "",
   "diningtable": "",
   "toilet": "",
   "tvmonitor": "",
   "laptop": "لابتوب",
   "mouse": "",
   "remote": "",
   "keyboard": "لوحة مفاتيح",
   "cell phone": "هاتف محمول",
   "microwave": "",
   "oven": "",
   "toaster": "",
   "sink": "",
   "refrigerator": "",
   "book": "",
   "clock": "",
   "vase": "",
   "scissors": "",
   "teddy bear": "",
   "hair drier": "",
   "toothbrush": "",
}

def Camera():
    # تهيئة كاميرا Raspberry Pi
    camera = PiCamera()
    camera.resolution = (640, 480)  # دقة أقل لأداء أفضل
    raw_capture = PiRGBArray(camera, size=(640, 480))
    time.sleep(0.1)

    # تحميل نموذج الكشف
    classNames = []
    with open('coco.names', 'rt', encoding='utf-8') as f:
        classNames = f.read().rstrip('\n').split('\n')
    
    net = cv2.dnn_DetectionModel('frozen_inference_graph.pb', 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt')
    net.setInputSize(320, 320)  # حجم أكبر لدقة أفضل
    net.setInputScale(1.0/127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)

    start_time = time.time()

    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        img = frame.array
        classIds, confs, bbox = net.detect(img, confThreshold=0.5)  # عتبة ثقة أقل

        detected_objects = []
        if len(classIds) != 0:
            for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
                object_name = classNames[classId-1]
                ar_name = dicEnAr.get(object_name, "شيء غير معروف")
                cv2.putText(img, ar_name, (box[0]+10, box[1]+30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                detected_objects.append(ar_name)

        if detected_objects:
            text = "أرى: " + "، ".join(detected_objects)
            tts = gTTS(text=text, lang='ar')
            filename = "object.mp3"
            tts.save(filename)
            os.system("mpg321 -q " + filename)  # التشغيل بصمت
            os.remove(filename)

        cv2.imshow('Object Detection', img)
        raw_capture.truncate(0)

        # إيقاف بعد 30 ثانية أو بالضغط على q
        if cv2.waitKey(1) == ord('q') or (time.time() - start_time) > 30:
            break

    camera.close()
    cv2.destroyAllWindows()

# Camera()






# import time
# import cv2
# from gtts import gTTS
# import pygame
# from io import BytesIO
# import os

# # إعدادات خاصة برسبيري باي
# os.environ['SDL_AUDIODRIVER'] = 'dummy'  # لإصلاح مشاكل الصوت
# pygame.mixer.init(frequency=22050, size=-16, channels=2)  # إعدادات صوت منخفضة الاستهلاك

# # تحميل القواميس و الملفات مرة واحدة
# classNames = []
# with open('coco.names', 'rt') as f:
#     classNames = f.read().rstrip('\n').split('\n')

# dicEnAr = {
#     # ... (نفس القاموس السابق)
# }

# # تهيئة النموذج مع تحسينات للأداء
# configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
# weightpath = 'frozen_inference_graph.pb'
# net = cv2.dnn_DetectionModel(weightpath, configPath)
# net.setInputSize(160, 120)  # تقليل حجم الإدخال
# net.setInputScale(1.0 / 127.5)
# net.setInputMean((127.5, 127.5, 127.5))
# net.setInputSwapRB(True)

# def text_to_speech(text):
#     """إصدار صوتي خفيف للرسبيري باي"""
#     if not text.strip():
#         return
    
#     try:
#         tts = gTTS(text=text, lang='ar', slow=False)
#         fp = BytesIO()
#         tts.write_to_fp(fp)
#         fp.seek(0)
        
#         pygame.mixer.music.load(fp, 'mp3')
#         pygame.mixer.music.play()
#         # انتظار أقصر للرسبيري باي
#         while pygame.mixer.music.get_busy():
#             pygame.time.Clock().tick(10)
#     except Exception as e:
#         print(f"خطأ في الصوت: {e}")

# def Camera():
#     # استخدام كاميرا Raspberry Pi الخاصة
#     cam = cv2.VideoCapture(0)
#     cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # تقليل دقة الفيديو
#     cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
#     cam.set(cv2.CAP_PROP_FPS, 10)  # تقليل معدل الإطارات
    
#     last_spoken = {}
#     start_time = time.time()
    
#     try:
#         while time.time() - start_time < 30:
#             success, img = cam.read()
#             if not success:
#                 continue
                
#             # معالجة الإطار بخيارات خفيفة
#             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             small_frame = cv2.resize(gray, (160, 120))
            
#             classIds, confs, bbox = net.detect(small_frame, confThreshold=0.5)  # عتبة ثقة أقل
            
#             current_objects = set()
#             if len(classIds) != 0:
#                 for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
#                     obj_name = classNames[classId-1]
#                     current_objects.add(obj_name)
                    
#                     # تحجيم المربعات للإطار الأصلي
#                     scale_x = img.shape[1] / small_frame.shape[1]
#                     scale_y = img.shape[0] / small_frame.shape[0]
#                     box = [
#                         int(box[0] * scale_x),
#                         int(box[1] * scale_y),
#                         int(box[2] * scale_x),
#                         int(box[3] * scale_y)
#                     ]
                    
#                     cv2.rectangle(img, box, (0, 255, 0), 1)
#                     cv2.putText(img, obj_name, 
#                                (box[0] + 5, box[1] + 15), 
#                                cv2.FONT_HERSHEY_SIMPLEX, 
#                                0.5, 
#                                (0, 255, 0), 
#                                1)
                    
#                     ar_name = dicEnAr.get(obj_name, "")
#                     if ar_name and (obj_name not in last_spoken or time.time() - last_spoken[obj_name] > 3):
#                         print(f"الكشف: {obj_name} -> {ar_name}")
#                         text_to_speech(ar_name)
#                         last_spoken[obj_name] = time.time()
            
#             cv2.imshow('Output', img)
#             if cv2.waitKey(1) == ord('q'):
#                 break
#     finally:
#         cam.release()
#         cv2.destroyAllWindows()
#         pygame.mixer.quit()

# Camera()






