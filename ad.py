from vosk import Model, KaldiRecognizer
import pyaudio
import time
import json

# Constants for configuration
MODEL_PATH = "model"
SAMPLE_RATE = 16000
CHANNELS = 1
FRAMES_PER_BUFFER = 4096
TIMEOUT_LIMIT = 30
SILENCE_TIMEOUT = 2

class SpeechToTextConverter:
    def init(self):
        """
        Initialize speech recognition components
        """
        try:
            self.model = Model(MODEL_PATH)
            self.recognizer = KaldiRecognizer(self.model, SAMPLE_RATE)
            self.audio_interface = pyaudio.PyAudio()
            self.stream = None
            self.last_audio_time = time.time()
            
        except Exception as e:
            print(f"Initialization error: {str(e)}")
            raise

    def _open_stream(self):
        """Initialize and configure audio stream"""
        self.stream = self.audio_interface.open(
            format=pyaudio.paInt16,
            channels=CHANNELS,
            rate=SAMPLE_RATE,
            input=True,
            frames_per_buffer=FRAMES_PER_BUFFER,
            stream_callback=self._audio_callback
        )

    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Process audio data in callback mode"""
        self.last_audio_time = time.time()
        if self.recognizer.AcceptWaveform(in_data):
            return (in_data, pyaudio.paContinue)
        return (in_data, pyaudio.paContinue)

    def process_audio(self):
        """Main method to process audio stream"""
        try:
            self._open_stream()
            print("Listening... (Say 'STOP' to exit)")
            self.stream.start_stream()

            start_time = time.time()
            while True:
                current_time = time.time()
                
                # Timeout handling
                if current_time - start_time > TIMEOUT_LIMIT:
                    print("System timeout reached")
                    break
                
                # Silence detection
                if current_time - self.last_audio_time > SILENCE_TIMEOUT:
                    print("Silence detected, stopping...")
                    break
                
                # Process intermediate results
                partial = json.loads(self.recognizer.PartialResult())
                if partial['partial'] != '':
                    print(f"Interim result: {partial['partial'].upper()}")
                
                time.sleep(0.1)

            return self._get_final_result()

        except Exception as e:
            print(f"Processing error: {str(e)}")
            return None

        finally:
            self._cleanup_resources()

    def _get_final_result(self):
        """Extract and format final recognition result"""
        result = json.loads(self.recognizer.FinalResult())
        return result['text'].upper() if 'text' in result else ""

    def _cleanup_resources(self):
        """Properly release all audio resources"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.audio_interface.terminate()

# if name == "main":
#     stt = SpeechToTextConverter()
    
#     try:
#         while True:
#             result = stt.process_audio()
#             if result:
#                 print(f"Final result: {result}")
#                 if "STOP" in result:
#                     print("Exit command received")
#                     break
#     except KeyboardInterrupt:
#         print("\nProgram terminated by user")