# Smart glasses for the blind

Overview
--------
The Smart Glasses project aims to improve the lives of blind and visually impaired people and enable greater independence. The system combines speech, computer vision, and OCR to provide audio assistance for everyday tasks such as reading text, recognizing people and objects, identifying colors and currency, recording audio notes, and giving the current time.

Core features
-------------
- Reading, recognizing, and translating text
  - Convert printed or photographed text to speech so users can listen to books, signs, documents, or labels.
  - Support for Arabic text shaping and bidirectional display handling; text can be translated / adapted to Arabic for easier understanding.

- People recognition
  - Identify nearby people using a small database of known faces (images) or voice samples and announce known names.

- Object recognition
  - Describe objects in the environment (furniture, appliances, daily items) and announce them to the user.

- Time and date
  - Provide the current time and date on request.

- Color detection and clothing description
  - Detect colors in the environment and provide an audio description. Useful for clothing decisions and color identification.

- Currency recognition
  - Detect banknotes and coins and announce their value to help the user make independent cash transactions.

- Audio note recording and reminders
  - Record short audio notes and use them as reminders for tasks or important information.

Value proposition
-----------------
This project helps reduce barriers for blind users by increasing their ability to interact with the physical world independently. It improves social participation, daily autonomy, and confidence by providing non-visual access to information.

Tech stack and libraries
------------------------
- Language: Python 3
- Speech-to-text: Vosk
- Computer vision: OpenCV (DNN) and face_recognition (dlib)
- Text-to-speech: gTTS (cloud) or espeak (local)
- OCR: Tesseract via pytesseract (requires tesseract-ocr and Arabic language pack)
- Audio I/O: sounddevice, scipy, pygame, mpg321/aplay
- Arabic support: arabic_reshaper, python-bidi
- Camera: picamera or picamera2 (Raspberry Pi)

Prerequisites
-------------
Hardware:
- Raspberry Pi 3/4 or later (recommended)
- Raspberry Pi Camera or compatible USB camera
- Microphone and speaker (or headset)
- Sufficient disk space for ML models (models are large)

System / Software:
- Python 3.7+
- apt, git, pip
- mpg321 or another MP3 player
- tesseract-ocr plus tesseract-ocr-ara for Arabic OCR
- Build tools for dlib (cmake, build-essential) if installing dlib from source

Large model files included (or referenced):
- Object detection model weights: frozen_inference_graph.pb
- Object detection config: ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt
- COCO class names: coco.names
- Vosk speech model archive: model.rar (extract to model/)

Installation & setup (example for Raspberry Pi OS)
--------------------------------------------------
1. Update the system:
   sudo apt update && sudo apt upgrade -y

2. Install system dependencies:
   sudo apt install -y python3 python3-venv python3-pip git build-essential cmake libopenjp2-7-dev libtiff5-dev libjpeg-dev libatlas-base-dev libblas-dev liblapack-dev libffi-dev libssl-dev libsndfile1 portaudio19-dev libportaudio2 mpg321 tesseract-ocr tesseract-ocr-ara

3. Create and activate a Python virtual environment:
   python3 -m venv venv
   source venv/bin/activate

4. Install Python dependencies:
   pip install --upgrade pip
   pip install numpy scipy opencv-python-headless pillow vosk sounddevice gTTS pygame face_recognition dlib pytesseract arabic_reshaper python-bidi picamera picamera2

Notes:
- Installing `dlib` and `opencv` via pip may require more system packages or building from source. If `opencv-python` fails, consider installing the system package: `sudo apt install python3-opencv`.
- gTTS requires internet. For offline TTS, use `espeak` or `pyttsx3`.

5. Prepare models and resources:
- Extract `model.rar` into a `model/` directory next to `ad.py` or update `ad.py`'s MODEL_PATH to point to your model.
- Ensure `frozen_inference_graph.pb`, the `.pbtxt` file and `coco.names` are present in the repository root or correct the paths in `object.py`.
- Place color WAV files in the `sounds/` directory referenced by `color_reg.py`.
- Ensure images for face recognition are placed in `img/` as referenced by `facere.py`.

Running the project
-------------------
1. Activate the virtual environment:
   source venv/bin/activate

2. Run the main program:
   python3 main.py

3. Voice commands recognized by the example main loop (the speech output is converted to uppercase before matching):
   - "NUMBER ONE"  → Start object detection
   - "NUMBER TWO"  → Start color recognition
   - "NUMBER THREE"→ Start face recognition
   - "NUMBER FOUR" → Start OCR and read detected text
   - "TIME"        → Speak current time
   - "VOICE"       → Record an audio note to `recording0.wav`
   - "OPEN "       → Play `recording0.wav`
   - "CLOSE"       → Stop the program

Tip: If you use or train an Arabic speech model, update the command detection logic in `main.py` to accept Arabic phrases.

Configuration and environment variables
---------------------------------------
There is no dedicated `.env` file. Important configuration values are defined in code files:
- ad.py: MODEL_PATH, SAMPLE_RATE, TIMEOUT_LIMIT, SILENCE_TIMEOUT
- color_reg.py: SOUNDS (map of color names to WAV files)
- object.py, facere.py, ocr_red.py, time_1.py: output filenames and model paths

Project structure
-----------------
- ad.py                         — Speech-to-text (Vosk)
- main.py                       — Main loop that maps voice commands to functions
- object.py                     — Object detection (OpenCV DNN) + TTS
- color_reg.py                  — Color detection and audio feedback
- facere.py                     — Face recognition and name announcement
- ocr_red.py                    — Capture images and OCR Arabic text
- rec.py                        — Record and play audio files
- time_1.py                     — Speak current time
- coco.names                    — COCO class names for object detection
- frozen_inference_graph.pb     — Object detection model weights
- ssd_mobilenet_v3...pbtxt      — Model configuration
- model.rar                     — Vosk speech model archive (extract to model/)
- img/                          — Known face images (used by facere)
- sounds/                       — WAV files for color announcements

Operational tips
----------------
- Replace gTTS with espeak or pyttsx3 for offline TTS and lower latency.
- Reduce DNN input size (net.setInputSize) to improve performance on a Pi.
- Keep large models out of the repository (use Git LFS or provide download links in releases).
- Consider training or obtaining an Arabic speech model for better command recognition in Arabic.

Contributing
------------
1. Open an issue to request features or report bugs.
2. Fork the repository and create a feature/bugfix branch.
3. Commit changes with clear messages and open a Pull Request describing what you changed and how to test.

License
-------
No license is included in the repository currently. It is recommended to add a license such as the MIT License if you want others to freely use and contribute to the project. I can add a LICENSE file for you if you want.

Next steps I can help with
-------------------------
- Add a requirements.txt (or Pipfile) listing Python dependencies.
- Add a LICENSE file (MIT or other) and commit it.
- Update `main.py` to support Arabic voice commands alongside English.
- Provide small setup scripts (e.g., setup.sh) to automate environment preparation.

