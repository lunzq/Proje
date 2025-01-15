import os
import time
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Sadece hata mesajlarını göster
import dlib
import cv2
import threading
from face import initialize_camera, detect_faces, draw_faces, analyze_emotions, translate_emotions, get_dominant_emotion
from chat import gemini_soru_sor
from duygu_analizi import turkce_duygu_analizi  # Türkçe duygu analizi fonksiyonu
import mediapipe as mp
import pandas as pd

def initialize_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise ValueError("Kamera açılamadı. Lütfen kamerayı kontrol edin ve tekrar deneyin.")
    return cap


# Yardımcı fonksiyonları kullanarak sohbet etme ve zorbalık tespiti
def offer_support_for_bullying(dominant_emotion):
    prompt = f"Kullanıcıda zorbalığa işaret eden duygular tespit edildi: {dominant_emotion}\nBu kişinin yaşadıklarını anlayarak ve empati kurarak, ona nasıl destek olabilirim? Ne gibi tavsiyeler verebilirim? Lütfen anlayışlı ve destekleyici bir şekilde cevap ver."
    gemini_response = gemini_soru_sor(prompt)
    print(gemini_response)

def main():
    try:
        print("Duygu analizi başlatılıyor...")  # Başlangıç mesajı
        cap = initialize_camera()  # Kamerayı başlat
        if cap is None:  # Eğer kamera açılamadıysa çık
            return

        print("Kamera başarıyla açıldı.")  # Kamera açıldı mesajı
        emotions_list = []
        start_time = time.time()

        try:
            while time.time() - start_time < 10:  # 10 saniye boyunca döngü
                success, image = cap.read()
                if not success:
                    print("Görüntü alınamadı.")
                    continue

                results = detect_faces(image, mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.2))
                if results:
                    draw_faces(image, results)
                    if results.detections:  # Yüz tespiti başarılı
                        detailed_emotions = analyze_emotions(image)
                        if detailed_emotions:  # Duygu tespit edilirse
                            translated_emotions = translate_emotions(detailed_emotions)
                            emotions_list.append(translated_emotions)

                cv2.imshow("Duygu Analizi", image)
                if cv2.waitKey(5) & 0xFF == ord('q'):
                    break

        finally:
            cap.release()
            cv2.destroyAllWindows()

        bullying_related_emotions = ["Üzgün", "Duygusuz", "Öfkeli", "Korku"]
        dominant_emotion = get_dominant_emotion(emotions_list)

        if dominant_emotion in bullying_related_emotions:
            print("Zorbalığa işaret eden duygular tespit edildi.")
            offer_support_for_bullying(dominant_emotion)
            offer_support_for_bullying(dominant_emotion)
            print("Lütfen bana yaşadığın durumu veya hissettiğin duyguları anlat.")
        else:
            print("Gemini:Sana nasıl yardımcı olabilirim?")
            # Eğer olumlu bir duygu tespit edilirse, kullanıcıya yardımcı olma isteği
            if dominant_emotion in ["Mutlu", "Heyecanlı"]:
                print("Gemini:Bu harika! Nasıl yardımcı olabilirim?")
        # Kullanıcının yazılı metni üzerinden duygu analizi yap ve Gemini'den cevap al
        
        while True:
            user_input = input("Sen: ")
            if user_input.lower() == 'çık':  # Sohbeti sonlandırmak
                print("Sohbet sonlandırıldı.")
                break
            
            # Kullanıcının yazılı metni üzerinden duygu analizi yap ve Gemini'ye gönder
            gemini_response = gemini_soru_sor(user_input)
            print(f"Gemini: {gemini_response}")

        # Duygu tespit edildiğinde o duyguyu Gemini'ye arka planda sor
        threading.Thread(target=gemini_soru_sor, args=(dominant_emotion,)).start()
        print("Duygu analizi başarıyla tamamlandı.")
    except Exception as e:
        print(f"Program hatası: {e}")
        return

if __name__ == "__main__":
    main()
