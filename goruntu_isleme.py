import os
import time
from PIL import Image

# Resimlerin olduğu klasör
ASSETS_DIR = "/storage/emulated/0/BalikBotProjesi/assets/"

IMG_SOLUCAN = os.path.join(ASSETS_DIR, "yem_solucan.png")
IMG_HAMUR = os.path.join(ASSETS_DIR, "yem_hamur.png")
IMG_OLTA = os.path.join(ASSETS_DIR, "olta_at.png")

def ekran_goruntusu_al():
    """Android sisteminden ekran görüntüsü alıp Pillow formatına çevirir."""
    os.system("screencap -p /sdcard/ekran.png")
    return Image.open("/sdcard/ekran.png")

def sablon_ara(ekran_img, sablon_yolu, esik_degeri=25):
    """Küçük buton resimlerini (yem, olta) ekranda arar ve yerini bulur."""
    if not os.path.exists(sablon_yolu):
        return None
        
    sablon = Image.open(sablon_yolu).convert("RGB")
    s_w, s_h = sablon.size
    s_pikseller = sablon.load()
    
    e_w, e_h = ekran_img.size
    e_pikseller = ekran_img.load()
    
    # Hızlı tarama için 8'er piksel atlayarak bakıyoruz
    for y in range(0, e_h - s_h, 8):
        for x in range(0, e_w - s_w, 8):
            r_e, g_e, b_e = e_pikseller[x, y][:3]
            r_s, g_s, b_s = s_pikseller[0, 0][:3]
            
            if abs(r_e - r_s) < esik_degeri and abs(g_e - g_s) < esik_degeri and abs(b_e - b_s) < esik_degeri:
                return x + (s_w // 2), y + (s_h // 2)
    return None

def kirmizi_cember_kontrol(ekran_img):
    """Ekrandaki kırmızı çemberi tarar, bulduğu an koordinat döner."""
    e_w, e_h = ekran_img.size
    pikseller = ekran_img.load()
    
    # Ekranın orta bölgesini yoğunluklu tarar (Performans için)
    for y in range(int(e_h * 0.2), int(e_h * 0.8), 6):
        for x in range(int(e_w * 0.2), int(e_w * 0.8), 6):
            r, g, b = pikseller[x, y][:3]
            # Saf kırmızı filtre (Metin2'deki o çemberin kırmızı tonu)
            if r > 190 and g < 50 and b < 50:
                return x, y
    return None
