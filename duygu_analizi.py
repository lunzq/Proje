from transformers import pipeline
from chat import gemini_soru_sor

nlp = pipeline('text-classification', model='savasy/bert-base-turkish-sentiment-cased')

def turkce_duygu_analizi(user_input):
    try:
        result = nlp(user_input)[0]
        duygu = result['label']
        olasılık = result['score']
        
        # Duyguları ve olasılıkları listele
        detayli_olasiliklar = {result['label']: result['score'] for result in nlp(user_input)}
        
        bullying_related_emotions = ["Üzgün", "Duygusuz", "Öfkeli", "Korku", "Korkmuş", "Tedirgin"]
        if duygu in bullying_related_emotions:
            prompt = f"Kullanıcının mesajı: {user_input}\nDuygu analizi sonucu: {duygu} (%{olasılık*100:.2f})\nDetaylı duygu olasılıkları: {detayli_olasiliklar}\nZorbalığa işaret eden duygular tespit edildi. Bu kişinin yaşadıklarını anlayarak ve empati kurarak, ona nasıl destek olabilirim?"
        else:
            prompt = f"Kullanıcının mesajı: {user_input}\nDuygu analizi sonucu: {duygu} (%{olasılık*100:.2f})\nDetaylı duygu olasılıkları: {detayli_olasiliklar}\nBu kişinin yaşadıklarını anlayarak ve empati kurarak, ona nasıl destek olabilirim?"
        gemini_response = gemini_soru_sor(prompt)
        
        return duygu, olasılık, gemini_response
    except Exception as e:
        print(f"Duygu analizi sırasında hata: {e}")
        return "Duygu analizi yapılamadı."


def geri_bildirim(duygu, gemini_response):
    try:
        return f"Tespit edilen duygu: {duygu}\nÖneri: {gemini_response}"
    except Exception as e:
        return f"Geri bildirim oluşturulamadı: {e}"

if __name__ == "__main__":
    user_input = input("Bir cümle girin: ")
    duygu, olasılık, gemini_response = turkce_duygu_analizi(user_input)
    print(f"Duygu: {duygu}, Olasılık: {olasılık:.2f}")
    print(geri_bildirim(duygu, gemini_response))
