# 🧍‍♂️👁️ Postür ve Yorgunluk Analiz Sistemi

Merhaba! Bu projeyi, bilgisayar başında uzun saatler geçiren (özellikle kodlama yapan) kişilerin postür (duruş) bozukluklarını ve yorgunluk durumlarını gerçek zamanlı olarak tespit edip sağlığımızı korumaya yardımcı olmak amacıyla geliştirdim.

Uygulama, bilgisayar kamerasından alınan görüntüyü gerçek zamanlı olarak işler. Omuz hizasında bir bozulma veya uyku hali (göz kapanması) tespit ettiğinde hem sesli hem de görsel uyarılar verir.

## 🚀 Özellikler

- **Python 3.11.9 ile Geliştirildi:** Kararlı Python sürümlerinden biriyle optimize edilmiştir.
- **Gerçek Zamanlı Postür Analizi:** MediaPipe Pose kullanılarak omuz hizaları takip edilir. Duruşunuz bozulduğunda (omuzlar arası hiza farkı arttığında) sistem sizi uyarır.
- **Yorgunluk ve Uyku Tespiti:** MediaPipe Face Mesh ile göz kapakları arasındaki mesafe düzenli ölçülür. Gözleriniz uzun süre kapalı kalırsa sistem alarm çalarak uyanık kalmanızı veya mola vermenizi tavsiye eder.
- **Çalışma Süresi Takibi:** Uygulamayı başlattığınız andan itibaren geçen süreyi gösteren entegre bir kronometre.
- **Modern Arayüz:** CustomTkinter ile tasarlanmış kullanıcı dostu, şık ve sade masaüstü arayüzü.
- **Anlık Uyarı Sistemi:** Riskli durumlarda Windows sistem sesleriyle (`winsound`) işitsel ve arayüz üzerinden kırmızı uyarı metinleriyle görsel bildirimler verir.

## 🛠️ Kullanılan Teknolojiler ve Kütüphaneler

Bu projeyi geliştirirken aşağıdaki temel teknolojilerden yararlandım:

- **Programlama Dili:** Python 3.11.9
- **Arayüz (GUI):** CustomTkinter (Modern Tkinter sarmalayıcısı)
- **Görüntü İşleme:** OpenCV (`cv2`), Pillow (`PIL`)
- **Yapay Zeka / Landmark:** MediaPipe (Pose ve Face Mesh modelleri)
- **Ses:** Winsound (Windows dahili kütüphanesi)

### 1. Kontrol

Bilgisayarınızda **Python 3.11.9** sürümünün yüklü olduğundan emin olun.
> Python sürümünüzü kontrol etmek için terminale `python --version` yazabilirsiniz.
