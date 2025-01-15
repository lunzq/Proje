# Duygu Analizi Uygulaması

Bu uygulama, kullanıcının yüz ifadelerini analiz ederek duygularını tespit etmeyi amaçlamaktadır. Kullanıcıdan alınan görüntüler üzerinden yapılan analizler sonucunda, aşağıdaki işlevsellikler sağlanmaktadır:

## Özellikler

1. **Duygu Analizi**: 
   - Kullanıcının yüz ifadeleri analiz edilerek, "mutlu", "üzgün", "öfkeli", "korku" gibi duygular tespit edilir.

2. **Zorbalık Tespiti**: 
   - Eğer kullanıcıdan alınan duygu analizi sonucu zorbalık ile ilişkili bir duygu tespit edilirse, uygulama destek mesajları sunar. Örneğin, "Zorbalığa işaret eden duygular tespit edildi. Lütfen bana yaşadığın durumu veya hissettiğin duyguları anlat." gibi mesajlar verilir.

3. **Olumlu Duygular**: 
   - Kullanıcı mutlu veya heyecanlı gibi olumlu duygular yaşıyorsa, uygulama "Bu harika! Nasıl yardımcı olabilirim?" mesajı ile yanıt verir.

## Kullanım
- Uygulama çalıştırıldığında, kullanıcıdan görüntü alınır ve analiz yapılır. Kullanıcı, hissettiği duyguları açıklamak için yönlendirilir.

## Gereksinimler
requests
deep_translator
python-dotenv
transformers
opencv-python
mediapipe
fer
dlib
pandas
moviepy

                                   #KURULUM İŞLEMLERİ#  
## PYTHON KURULUMU

Bu Linkten;https://www.python.org/downloads/release/python-31010/ 
Pythonunun Resmi Sayfasına en alt kısımda indirme seçeneklerinden 64bit.exe olanı indirin.

Kurulum kısmında ADD TO PATH kısmını işaretlemeyi unutmayınız.

Gerekli kütüphaneleri yüklemek için aşağıdaki komutu kullanabilirsiniz:
   ## PYTHON KURULDUKTAN SONRA

## Sanal Ortamda Açmak İçin(Hata oranı azdır.);
python -m venv sanalortam
sanalortam\Scripts\activate.bat
pip install -r requirements.txt 
# Çalıştırmak için;
python main.py 

 ## PİP SÜRÜMÜNÜ YÜKSELTME
Pip Sürümünüz Bu Olmalı = 24.3.1
Yükseltmek için
python.exe -m pip install --upgrade pip

## İletişim
Herhangi bir sorun veya öneri için iletişime geçebilirsiniz.
Mail adresim:kosermehmet13@gmail.com