import customtkinter as ctk
import cv2 
from PIL import Image
import mediapipe as mp
import winsound

calisma_suresi = 0
postur_bozuk_suresi = 0
goz_kapali_sayaci = 0

mp_cizim = mp.solutions.drawing_utils

mp_postur = mp.solutions.pose
postur_modeli = mp_postur.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

mp_yuz=mp.solutions.face_mesh
yuz_modeli = mp_yuz.FaceMesh(max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

def zaman():
    global calisma_suresi, postur_bozuk_suresi
    
    if baslat_buton.cget("state") == "disabled":
        calisma_suresi += 1
        dakika = calisma_suresi // 60
        saniye = calisma_suresi % 60
        sure_kutusu_degiskeni.configure(text=f"⏱ {dakika:02d}:{saniye:02d}")
        
        postur_durumu = postur_kutusu_degiskeni.cget("text")
        yorgunluk_durumu = yorgunluk_kutusu_degiskeni.cget("text")

        if "Bozuk" in postur_durumu:
            postur_bozuk_suresi += 1
        else:
            postur_bozuk_suresi = 0

        if "Kapalı" in yorgunluk_durumu:
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
            uyari_kutusu_degiskeni.configure(text="Gözleriniz kapalı! Lütfen uyanık kalın. Veya mola verin.", font=("Arial", 14, "bold"), text_color="#dc2626")
        elif postur_bozuk_suresi >= 3:
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
            uyari_kutusu_degiskeni.configure(text="Postürünüz bozuk. Dik oturun ve ekran hizasını düzeltin.", font=("Arial", 14, "bold"), text_color="#dc2626")
        else:
            uyari_kutusu_degiskeni.configure(text="Şu an her şey normal, iyi çalışmalar.", font=("Arial", 16), text_color="#475569")
            
    pencere.after(1000, zaman)

def cikis():
    pencere.destroy()

def baslat():
    global kamera, goz_kapali_sayaci
    if baslat_buton.cget("state") == "normal":
        zaman()
        kamera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        baslat_buton.configure(state="disabled")
        kamera_alani_yazi.configure(text="")
        kamera_alani_yazi.place(x=0,y=0)
    
    resim = kamera.read()[1]
    resim = cv2.flip(resim,1)
    
    renkli_resim = cv2.cvtColor(resim, cv2.COLOR_BGR2RGB)

    sonuc = postur_modeli.process(renkli_resim)
    yuz_sonuc=yuz_modeli.process(renkli_resim)
    
    if sonuc.pose_landmarks:
        mp_cizim.draw_landmarks(renkli_resim, sonuc.pose_landmarks, mp_postur.POSE_CONNECTIONS)
        
        try:
            sol_omuz = sonuc.pose_landmarks.landmark[11]
            sag_omuz = sonuc.pose_landmarks.landmark[12]

            omuz_hiza_farki = abs(sol_omuz.y - sag_omuz.y)
            if omuz_hiza_farki < 0.05:
                postur_kutusu_degiskeni.configure(text="🧍 Normal", text_color="#16a34a")
            else:
                postur_kutusu_degiskeni.configure(text="🧍 Bozuk", text_color="#dc2626")
        except:
            pass
        
    if yuz_sonuc.multi_face_landmarks:
        try:
            yuz_noktalari = yuz_sonuc.multi_face_landmarks[0]
            sol_ust = yuz_noktalari.landmark[159].y
            sol_alt = yuz_noktalari.landmark[145].y

            goz_mesafe = abs(sol_alt - sol_ust)

            if goz_mesafe < 0.015:
                goz_kapali_sayaci+=1
                if goz_kapali_sayaci>=15:
                    yorgunluk_kutusu_degiskeni.configure(text="👁️ Kapalı", text_color="#dc2626")
            else:
                goz_kapali_sayaci = 0
                yorgunluk_kutusu_degiskeni.configure(text="👁️ Açık", text_color="#2563eb")
        except:
            pass

    duzen_resim = Image.fromarray(renkli_resim)
    ctk_resim = ctk.CTkImage(light_image=duzen_resim, size=(550, 270))
    kamera_alani_yazi.configure(image=ctk_resim)

    pencere.after(15, baslat)

pencere = ctk.CTk()
pencere.geometry("900x600")
pencere.title("Postür ve Yorgunluk Analiz Sistemi")

pencere.configure(fg_color="#eef5f9")

ust_kutu = ctk.CTkFrame(pencere, fg_color="white", corner_radius = 15, height=80, width=860, border_color="#dbeafe",border_width=2)
ust_kutu.place(x=20, y=20)

ust_kutu_yazi = ctk.CTkLabel(ust_kutu, text="Postür ve Yorgunluk Analiz Sistemi", font=("Arial",22,"bold"), text_color="#0f4c81")
ust_kutu_yazi.place(x=25,y=10)

ust_kutu_altyazi = ctk.CTkLabel(ust_kutu, text="Göz kapanması, esneme ve postür süresine göre uyarı verir", font=("Arial",13), text_color="#0f4c81")
ust_kutu_altyazi.place(x=25,y=40)

kamera_kutu = ctk.CTkFrame(pencere, fg_color="white", corner_radius=15, height=350, width=600, border_color="#dbeafe", border_width=2)
kamera_kutu.place(x=20, y=120)

kamera_kutu_yazi = ctk.CTkLabel(kamera_kutu, text="Canlı Kamera Görüntüsü",font=("Arial", 18, "bold"), text_color="#0f4c81")
kamera_kutu_yazi.place(x=25,y=10)

kamera_alani = ctk.CTkFrame(kamera_kutu,fg_color="#e2e8f0", height=270, width=550)
kamera_alani.place(x=25,y=55)

kamera_alani_yazi = ctk.CTkLabel(kamera_alani,text="Kamera görüntüsü burada gösterilecek", font=("Arial",15,"bold"),text_color="#475569")
kamera_alani_yazi.place(x=120,y=120)

durum_kutusu = ctk.CTkFrame(pencere, fg_color="white", corner_radius=15, height = 350, width= 240, border_color="#dbeafe", border_width=2)
durum_kutusu.place(x=640, y=120)

durum_kutusu_yazisi=ctk.CTkLabel(durum_kutusu, text="Analiz Sonuçları",font=("Arial",18,"bold"),text_color="#0f4c81")
durum_kutusu_yazisi.place(x=20,y=10)

postur_kutusu = ctk.CTkFrame(durum_kutusu, fg_color="#ecfdf5",corner_radius=10,width=200,height=75)
postur_kutusu.place(x=20,y=65)

postur_kutusu_yazisi=ctk.CTkLabel(postur_kutusu,text="Postür Durumu",font=("Arial",15,"bold"),text_color="#16a34a")
postur_kutusu_yazisi.place(x=15,y=10)
postur_kutusu_degiskeni=ctk.CTkLabel(postur_kutusu,text="🧍 -- ",font=("Arial",17,"bold"),text_color="#16a34a")
postur_kutusu_degiskeni.place(x=15,y=35)

yorgunluk_kutusu = ctk.CTkFrame(durum_kutusu, fg_color="#eff6ff",corner_radius=10,width=200,height=75)
yorgunluk_kutusu.place(x=20,y=160)
yorgunluk_kutusu_yazisi =ctk.CTkLabel(yorgunluk_kutusu,text="Yorgunluk Durumu",font=("Arial", 15,"bold"),text_color="#2563eb")
yorgunluk_kutusu_yazisi.place(x=15,y=10)

yorgunluk_kutusu_degiskeni=ctk.CTkLabel(yorgunluk_kutusu,text="👁️--",font=("Arial",17,"bold"),text_color="#2563eb")
yorgunluk_kutusu_degiskeni.place(x=15,y=35)

sure_kutusu = ctk.CTkFrame(durum_kutusu, fg_color="#fff7ed",corner_radius=10,width=200,height=75)
sure_kutusu.place(x=20,y=255)

sure_kutusu_yazisi=ctk.CTkLabel(sure_kutusu,text="Çalışma Süresi",font=("Arial",15,"bold"),text_color="#ea580c")
sure_kutusu_yazisi.place(x=15,y=10)

sure_kutusu_degiskeni=ctk.CTkLabel(sure_kutusu,text="⏱ 00:00",font=("Arial",17,"bold"),text_color="#ea580c")
sure_kutusu_degiskeni.place(x=15,y=35)

uyari_kutusu = ctk.CTkFrame(pencere, fg_color="white", border_color="#dbeafe", border_width=2, corner_radius=15, width=600, height=90)
uyari_kutusu.place(x=20, y=490)

uyari_kutusu_yazisi = ctk.CTkLabel(uyari_kutusu, text="Sistem Uyarısı:", font=("Arial", 16, "bold"), text_color="#0f4c81")
uyari_kutusu_yazisi.place(x=25, y=15)

uyari_kutusu_degiskeni = ctk.CTkLabel(uyari_kutusu, text="Şu an her şey normal, iyi çalışmalar.", font=("Arial", 16), text_color="#475569")
uyari_kutusu_degiskeni.place(x=25, y=45)

buton_kutusu = ctk.CTkFrame(pencere, width=240, height=100, corner_radius=20, fg_color="white", border_width=2, border_color="#dbeafe")
buton_kutusu.place(x=640, y=485)

baslat_buton = ctk.CTkButton(buton_kutusu,text="Başlat",width=210,height=34,corner_radius=13,fg_color="#2563eb",hover_color="#1d4ed8",command=baslat)
baslat_buton.place(x=15,y=15)

cikis_buton = ctk.CTkButton(buton_kutusu,text="Çıkış",width=210,height=34,corner_radius=13,fg_color="#dc2626",hover_color="#991b1b",command=cikis)
cikis_buton.place(x=15, y=57)

pencere.mainloop()