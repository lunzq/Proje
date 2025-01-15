import os
import requests
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

# .env dosyasındaki ortam değişkenlerini yükle
load_dotenv()

# API anahtarını ortam değişkenlerinden al
GEMINI_API_KEY = "AIzaSyB1hgTYNJ4lyji2WvT-ApHr2FyETSURBi0"
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY ortam değişkeni ayarlanmamış!")

def gemini_soru_sor(soru):
    try:
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            headers={"Content-Type": "application/json"},
            params={"key": GEMINI_API_KEY},
            json={ "contents": [{"parts": [{"text": soru}]}] },
            timeout=10
        )
        response.raise_for_status()  # API isteği başarısız olduğunda hata fırlatır
        response_data = response.json()
        
        # Yanıtın formatını kontrol et
        if "candidates" in response_data and response_data["candidates"]:
            yanit = response_data["candidates"][0]["content"]["parts"][0]["text"]
            try:
                return GoogleTranslator(source='en', target='tr').translate(yanit)
            except Exception as e:
                return f"Çeviri hatası: {str(e)}"
        return "Yanıt alınamadı."

    except requests.exceptions.Timeout:
        return "API yanıt vermedi, lütfen tekrar deneyin."
    except requests.exceptions.RequestException as e:
        return f"API hatası: {str(e)}"
    except Exception as e:
        return f"Beklenmeyen hata: {str(e)}"

def test_gemini():
    soru = "Merhaba, nasılsın?"
    yanit = gemini_soru_sor(soru)
    print("Soru:", soru)
    print("Cevap:", yanit)

# Test fonksiyonunu çağır
if __name__ == "__main__": 
    test_gemini()
