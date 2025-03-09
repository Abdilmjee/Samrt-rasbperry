import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write as write_wav
from scipy.io.wavfile import read as read_wav
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("name")

def record_audio(
    filename: str,
    duration: int = 5,
    fs: int = 44100,
    channels: int = 1,
    device: Optional[int] = None
) -> bool:
    """
    تسجيل صوتي باستخدام الميكروفون الموصول بالرسبيري باي
    
    Args:
        filename: اسم ملف الحفظ (بامتداد wav)
        duration: مدة التسجيل بالثواني (افتراضي 5)
        fs: تردد العينة (افتراضي 44100 هرتز)
        channels: عدد القنوات الصوتية (1 لمونو، 2 لستيريو)
        device: ID لاختيار جهاز تسجيل معين
        
    Returns:
        bool: True إذا نجح التسجيل، False إذا فشل
    """
    try:
        logger.info(f"جارٍ التسجيل لمدة {duration} ثواني...")
        
        # بدء التسجيل
        recording = sd.rec(
            int(duration * fs),
            samplerate=fs,
            channels=channels,
            device=device,
            dtype='float32'
        )
        
        # انتظار انتهاء التسجيل
        sd.wait()
        
        # تحويل البيانات إلى تنسيق 16-bit PCM
        recording = (recording * 32767).astype(np.int16)
        
        # حفظ الملف
        write_wav(filename, fs, recording)
        logger.info(f"تم الحفظ في {filename}")
        return True
    
    except Exception as e:
        logger.error(f"خطأ في التسجيل: {str(e)}")
        return False

def play_audio(
    filename: str,
    device: Optional[int] = None
) -> bool:
    """
    تشغيل ملف صوتي عبر مخرجات الصوت بالرسبيري باي
    
    Args:
        filename: مسار الملف الصوتي (wav)
        device: ID لاختيار جهاز تشغيل معين
        
    Returns:
        bool: True إذا نجح التشغيل، False إذا فشل
    """
    try:
        logger.info(f"جارٍ تشغيل {filename}...")
        
        # قراءة الملف الصوتي
        fs, data = read_wav(filename)
        
        # تحويل البيانات إلى تنسيق float32
        data = data.astype(np.float32) / 32768.0
        
        # تشغيل الصوت
        sd.play(data, fs, device=device)
        sd.wait()
        
        logger.info("تم التشغيل بنجاح")
        return True
    
    except Exception as e:
        logger.error(f"خطأ في التشغيل: {str(e)}")
        return False

# مثال للاستخدام:

#     # تسجيل صوت
# record_audio("test.wav", duration=3)
    
#     # تشغيل الملف
# play_audio("test.wav")