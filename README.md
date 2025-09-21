# Selenium HRAI Tests

Bu repo, **otomasyon testleri** içermektedir.  
Testler, **Selenium + Pytest** altyapısı kullanılarak hazırlanmış ve CI/CD entegrasyonuna uygun hale getirilmiştir.  

## 🚀 Amaç
- Şirket web sitesinin kritik fonksiyonlarını test etmek  
- Manuel test süresini azaltmak  
- Hataları daha erken fark ederek yazılım kalitesini artırmak  

## 🧪 Uygulanan Testler
1. **İletişim Formu Testleri**
   - Zorunlu alan boş bırakıldığında uyarı kontrolü  
   - Geçersiz e-posta adresi kontrolü  
   - SQL Injection saldırı denemelerine karşı hata mesajı kontrolü  
   - Geçerli veri ile form gönderme testi  

2. **Demo Formu Testleri**
   - Boş form gönderme senaryosu  
   - Geçersiz e-posta formatı  
   - Geçerli demo talebi gönderme  
   - Çift tıklamaya karşı önlem kontrolü  

3. **Login/Logout Testleri**
   - Geçerli kullanıcı ile başarılı giriş  
   - Yanlış bilgilerle başarısız giriş  
   - Başarılı çıkış senaryosu  

4. **Smoke Test**
   - Ana sayfanın ulaşılabilirliği  

## 🛠️ Kullanılan Teknolojiler
- **Python 3.13+**
- **Selenium WebDriver**
- **Pytest**
- **Pytest-HTML** (raporlama için)
- **Allure Reports** (detaylı rapor için)
- **dotenv** (gizli bilgiler `.env` dosyasında)


## 📊 Raporlama
Test sonuçları hem **HTML raporu** hem de **Allure Report** ile incelenebilir:

- HTML raporu:
  pytest --html=report.html --self-contained-html
  
- Allure raporu:
 pytest --alluredir=allure-results
 allure serve allure-results
