import time
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window

# Görüntü işleme fonksiyonlarımızı dahil ediyoruz
from goruntu_isleme import ekran_goruntusu_al, sablon_ara, kirmizi_cember_kontrol, IMG_SOLUCAN, IMG_HAMUR, IMG_OLTA

class Metin2BalikBotuApp(App):
    def build(self):
        self.bot_aktif = False
        
        # Arayüz Düzeni
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        self.durum_yazisi = Label(
            text="BOT DURDURULDU\n\nBaşlatmadan önce Ayarlar > Erişilebilirlik menüsünden bota izin verdiğinizden emin olun.",
            halign="center",
            font_size='16sp'
        )
        layout.add(self.durum_yazisi)
        
        self.btn_kontrol = Button(
            text="BALIK BOTUNU BAŞLAT",
            background_color=(0, 0.6, 0, 1),
            font_size='18sp'
        )
        self.btn_kontrol.bind(on_press=self.durum_degistir)
        layout.add(self.btn_kontrol)
        
        return layout

    def durum_degistir(self, instance):
        if not self.bot_aktif:
            # Botu AKTİF etme aşaması
            self.bot_aktif = True
            self.btn_kontrol.text = "PASİF (BOTU DURDUR)"
            self.btn_kontrol.background_color = (0.8, 0, 0, 1)
            self.durum_yazisi.text = "BOT AKTİF!\n\nOyuna geçiş yapabilirsiniz, arka planda tarıyor..."
            
            # Ekranı ufaltıp yüzen pencere moduna benzetiyoruz
            Window.size = (300, 200)
            
            # Arka plan döngüsünü thread ile başlatıyoruz
            self.bot_konusu = threading.Thread(target=self.bot_ana_dongu)
            self.bot_konusu.daemon = True
            self.bot_konusu.start()
        else:
            # Botu PASİF etme aşaması
            self.bot_aktif = False
            self.btn_kontrol.text = "BALIK BOTUNU BAŞLAT"
            self.btn_kontrol.background_color = (0, 0.6, 0, 1)
            self.durum_yazisi.text = "BOT DURDURULDU"
            Window.size = (600, 800)

    def rootsuz_ekrana_tikla(self, x, y):
        """Yazdığımız yerel Java Erişilebilirlik Servisini çağırarak rootsuz tıklar."""
        try:
            from jnius import autoclass
            # Oluşturduğumuz Java sınıfını çağırıyoruz
            BalikBotuServis = autoclass('com.metin2.balikbotu.BalikBotuErisilebilirlik')
            # Java içerisindeki static ekranaTikla metodunu tetikliyoruz
            BalikBotuServis.ekranaTikla(int(x), int(y))
        except Exception as e:
            print("Erişilebilirlik Servis bağlantı hatası (Bunu sadece APK içindeyken test edebilirsiniz):", e)

    def bot_ana_dongu(self):
        while self.bot_aktif:
            try:
                ekran = ekran_goruntusu_al()
                
                # 1. YEM TAKMA SEKTÖRÜ
                yem_yeri = sablon_ara(ekran, IMG_SOLUCAN)
                if not yem_yeri:
                    yem_yeri = sablon_ara(ekran, IMG_HAMUR)
                    
                if yem_yeri and self.bot_aktif:
                    self.rootsuz_ekrana_tikla(yem_yeri[0], yem_yeri[1])
                    time.sleep(1.2)
                
                # 2. OLTA ATMA SEKTÖRÜ
                olta_yeri = sablon_ara(ekran, IMG_OLTA)
                if olta_yeri and self.bot_aktif:
                    self.rootsuz_ekrana_tikla(olta_yeri[0], olta_yeri[1])
                    time.sleep(2.5)
                
                # 3. BALIK TUTMA VE ÇEMBER TAKİBİ
                avlanma_zamani = time.time()
                while time.time() - avlanma_zamani < 25 and self.bot_aktif:
                    anlik_ekran = ekran_goruntusu_al()
                    cember_koordinat = kirmizi_cember_kontrol(anlik_ekran)
                    
                    if cember_koordinat:
                        # Kırmızı çemberi yakaladık! Peş peşe çok hızlı 3 kez tıklıyoruz
                        for _ in range(3):
                            if self.bot_aktif:
                                self.rootsuz_ekrana_tikla(cember_koordinat[0], cember_koordinat[1])
                                time.sleep(0.05) 
                        break 
                    time.sleep(0.1)
                
                # Döngüler arası 2 saniyelik bekleme süresi
                time.sleep(2.0)
                
            except Exception as e:
                print("Döngü içerisinde hata:", e)
                time.sleep(2)

if __name__ == "__main__":
    Metin2BalikBotuApp().run()
