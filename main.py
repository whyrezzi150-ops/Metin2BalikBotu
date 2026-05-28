import time
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window

# SENİN GÖRÜNTÜ SİSTEMİN (AYNEN KALDI)
from goruntu_isleme import (
    ekran_goruntusu_al,
    sablon_ara,
    kirmizi_cember_kontrol,
    IMG_SOLUCAN,
    IMG_HAMUR,
    IMG_OLTA
)

class Metin2BalikBotuApp(App):

    def build(self):
        self.bot_aktif = False

        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)

        self.durum_yazisi = Label(
            text="BOT DURDURULDU\nBaşlatmadan önce izinleri kontrol et.",
            halign="center",
            font_size='16sp'
        )
        layout.add_widget(self.durum_yazisi)

        self.btn_kontrol = Button(
            text="BALIK BOTUNU BAŞLAT",
            background_color=(0, 0.6, 0, 1),
            font_size='18sp'
        )
        self.btn_kontrol.bind(on_press=self.durum_degistir)
        layout.add_widget(self.btn_kontrol)

        return layout

    def durum_degistir(self, instance):
        if not self.bot_aktif:
            self.bot_aktif = True
            self.btn_kontrol.text = "BOTU DURDUR"
            self.btn_kontrol.background_color = (0.8, 0, 0, 1)
            self.durum_yazisi.text = "BOT AKTİF - Görseller taranıyor"

            Window.size = (300, 200)

            self.bot_thread = threading.Thread(target=self.bot_ana_dongu)
            self.bot_thread.daemon = True
            self.bot_thread.start()

        else:
            self.bot_aktif = False
            self.btn_kontrol.text = "BALIK BOTUNU BAŞLAT"
            self.btn_kontrol.background_color = (0, 0.6, 0, 1)
            self.durum_yazisi.text = "BOT DURDURULDU"
            Window.size = (600, 800)

    # ⚠️ SENİN ROOTSUZ TIK FONKSİYONUNU BOZMADIM AMA GÜVENLİ YAPTIM
    def rootsuz_tikla(self, x, y):
        try:
            from jnius import autoclass
            Servis = autoclass('com.metin2.balikbotu.BalikBotuErisilebilirlik')
            Servis.ekranaTikla(int(x), int(y))
        except Exception as e:
            print("Tıklama servisi yok (APK dışında normal):", e)

    def bot_ana_dongu(self):
        while self.bot_aktif:
            try:
                ekran = ekran_goruntusu_al()

                # 1. YEM KONTROL
                yem = sablon_ara(ekran, IMG_SOLUCAN)
                if not yem:
                    yem = sablon_ara(ekran, IMG_HAMUR)

                if yem and self.bot_aktif:
                    self.rootsuz_tikla(yem[0], yem[1])
                    time.sleep(1.2)

                # 2. OLTA
                olta = sablon_ara(ekran, IMG_OLTA)
                if olta and self.bot_aktif:
                    self.rootsuz_tikla(olta[0], olta[1])
                    time.sleep(2.5)

                # 3. BALIK ÇEMBERİ
                start = time.time()
                while time.time() - start < 25 and self.bot_aktif:
                    img = ekran_goruntusu_al()
                    cember = kirmizi_cember_kontrol(img)

                    if cember:
                        for _ in range(3):
                            if self.bot_aktif:
                                self.rootsuz_tikla(cember[0], cember[1])
                                time.sleep(0.05)
                        break

                    time.sleep(0.1)

                time.sleep(2)

            except Exception as e:
                print("Bot hata:", e)
                time.sleep(2)

if __name__ == "__main__":
    Metin2BalikBotuApp().run()
