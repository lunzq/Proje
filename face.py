import cv2
import mediapipe as mp
from fer import FER
from duygu_analizi import turkce_duygu_analizi, geri_bildirim

# Duygu tespiti nesnesi
emotion_detector = FER()
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

def initialize_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Kamera açılamadı. Lütfen kamerayı kontrol edin ve tekrar deneyin.")
        return None
    return cap

def detect_faces(image, face_detection):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_detection.process(image_rgb)
    return results

def draw_faces(image, results):
    if results.detections:
        for detection in results.detections:
            mp_drawing.draw_detection(image, detection)

def analyze_emotions(image):
    # Mediapipeden yüz tespiti
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = mp_face_detection.FaceDetection(min_detection_confidence=0.5).process(image_rgb)
    if results.detections:
        # Burada mediapipe yüz tespiti ile duygu analizi yapabiliriz
        emotions = emotion_detector.detect_emotions(image)
        if emotions and len(emotions) > 0:
            detailed_emotions = emotions[0]['emotions']
            return detailed_emotions
    return None

def translate_emotions(detailed_emotions):
    emotion_translation = {
        "angry": "Öfkeli",
        "disgust": "Tiksinti",
        "fear": "Korku",
        "happy": "Mutlu",
        "sad": "Üzgün",
        "excited": "Heyecanlı",
        "surprise": "Şaşırmış",
        "neutral": "Nötr",
        "calm": "Sakin",
        "disgust": "İğrenme",
        "confused": "Kafası karışık",
        "frustrated": "Sinirli",
        "anxious": "Endişeli"
    }
    translated = {emotion_translation.get(emotion, emotion): value for emotion, value in detailed_emotions.items()}
    return translated

def get_dominant_emotion(emotions_list):
    if emotions_list:
        from collections import Counter
        average_emotions = Counter()
        for emotion in emotions_list:
            average_emotions.update(emotion)
        dominant_emotion = average_emotions.most_common(1)[0][0]
        return dominant_emotion
    return None

def process_frame(frame):
    results = detect_faces(frame, mp_face_detection.FaceDetection(min_detection_confidence=0.5))
    draw_faces(frame, results)
    
    emotions = analyze_emotions(frame)
    if emotions:
        dominant_emotion = get_dominant_emotion([emotions])
        gemini_response = turkce_duygu_analizi(dominant_emotion)
        feedback = geri_bildirim(dominant_emotion, gemini_response)
        return feedback
    return None
