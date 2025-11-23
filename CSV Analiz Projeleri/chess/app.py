import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import tabulate # Tablo çıktısı için
import io

# ==========================
# 0. AYARLAR VE KLASÖR TANIMLARI
# ==========================

CSV_DOSYA = "games.csv"  # Dosya adının 'games.csv' olduğunu varsayıyoruz
KAYIT_KLASORU = "satranc_analiz_raporu"

if not os.path.exists(KAYIT_KLASORU):
    os.makedirs(KAYIT_KLASORU)

# Matplotlib için Türkçe ve düzenli görünüm ayarları
plt.style.use('ggplot')
plt.rcParams['font.family'] = 'sans-serif' 
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial'] 
plt.rcParams['font.size'] = 10

# ==========================
# 1. VERİYİ YÜKLE VE HAZIRLA
# ==========================
try:
    # Güvenli okuma (virgül veya noktalı virgül ile)
    try:
        df = pd.read_csv(CSV_DOSYA, sep=',')
        if len(df.columns) < 5: 
             df = pd.read_csv(CSV_DOSYA, sep=';')
    except Exception:
        df = pd.read_csv(CSV_DOSYA, sep=';')
        
    # Hamle sayısı ekle (moves kolonundan)
    df["move_count"] = df["moves"].apply(lambda x: len(str(x).split()))
    
    # Kazanma oranı hesaplamaları için tam veri
    df_win = df[df["winner"].isin(['white', 'black'])].copy()

    print(f"✅ Veri Seti Yüklendi: {len(df):,} satır")

except FileNotFoundError:
    print(f"❌ Hata: '{CSV_DOSYA}' dosyası bulunamadı.")
    exit()
except Exception as e:
    print(f"❌ Kritik Hata: Veri yüklenemedi: {e}")
    exit()


# ==========================
# 2. GRAFİK VE TXT FONKSİYONU
# ==========================

def dikey_grafik_ciz(baslik, seri, x_etiketi, y_etiketi, dosya, renk):
    """Veriyi dikey çubuk grafik olarak çizer ve kaydeder."""
    if seri.empty:
        print(f"⚠️ Veri yetersiz: '{baslik}' grafiği atlandı.")
        return None

    plt.figure(figsize=(12, 6)) # Genişlik 12, Yükseklik 6
    seri.head(15).plot(kind="bar", color=renk) # Dikey çubuk grafiğe dönüştürüldü
    
    plt.title(baslik, fontsize=14)
    plt.xlabel(x_etiketi, fontsize=12)
    plt.ylabel(y_etiketi, fontsize=12)
    plt.xticks(rotation=45, ha='right') # Etiketleri eğerek üst üste binmeyi önler
    plt.tight_layout()
    plt.savefig(f"{KAYIT_KLASORU}/{dosya}")
    plt.close()
    
    print(f"✔ Grafik oluşturuldu: {dosya}")
    return seri.head(15).reset_index()


def txt_raporu_olustur(analiz_sonuclari):
    """Tüm analiz sonuçlarını tek bir TXT dosyasına yazar."""
    rapor_dosyasi = os.path.join(KAYIT_KLASORU, "Analiz_Raporu.txt")
    
    with open(rapor_dosyasi, 'w', encoding='utf-8') as f:
        f.write("# SATRANÇ VERİ SETİ DETAYLI ANALİZ RAPORU\n")
        f.write(f"# Analiz Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("-" * 50 + "\n\n")

        for baslik, df_result in analiz_sonuclari.items():
            f.write(f"## {baslik}\n")
            f.write(df_result.to_markdown(index=False) + "\n\n")
            f.write("-" * 50 + "\n\n")

    print(f"\n✅ TXT Raporu başarıyla oluşturuldu: {rapor_dosyasi}")


# ==========================
# 3. ANALİZLERİ ÇALIŞTIRMA
# ==========================

analiz_sonuclari = {}

# 1) EN ÇOK OYNANAN AÇILIŞLAR
en_cok_acilis = df["opening_name"].value_counts()
df_en_cok = dikey_grafik_ciz(
    "1. En Çok Oynanan Açılışlar (Sıklık)",
    en_cok_acilis,
    "Açılış Adı",
    "Oyun Sayısı",
    "1_en_cok_acilislar.png",
    "#007bff"
)
analiz_sonuclari["1. En Çok Oynanan Açılışlar"] = df_en_cok.rename(columns={'opening_name': 'Açılış Adı', 'count': 'Oyun Sayısı'})


# 2) BEYAZ KAZANMA ORANLARI
toplam_oyun = df_win.groupby("opening_name").size()
beyaz_kazanan = df_win[df_win["winner"] == "white"].groupby("opening_name").size()
beyaz_oran = (beyaz_kazanan / toplam_oyun * 100).fillna(0).sort_values(ascending=False)

df_beyaz_oran = dikey_grafik_ciz(
    "2. Beyaz İçin En Yüksek Kazanma Oranı",
    beyaz_oran,
    "Açılış Adı",
    "Kazanma Oranı (%)",
    "2_beyaz_kazanma_oranlari.png",
    "#28a745"
)
analiz_sonuclari["2. Beyaz Kazanma Oranları"] = df_beyaz_oran.rename(columns={'opening_name': 'Açılış Adı', 0: 'Kazanma Oranı (%)'})


# 3) SİYAH KAZANMA ORANLARI
siyah_kazanan = df_win[df_win["winner"] == "black"].groupby("opening_name").size()
siyah_oran = (siyah_kazanan / toplam_oyun * 100).fillna(0).sort_values(ascending=False)

df_siyah_oran = dikey_grafik_ciz(
    "3. Siyah İçin En Yüksek Kazanma Oranı",
    siyah_oran,
    "Açılış Adı",
    "Kazanma Oranı (%)",
    "3_siyah_kazanma_oranlari.png",
    "#dc3545"
)
analiz_sonuclari["3. Siyah Kazanma Oranları"] = df_siyah_oran.rename(columns={'opening_name': 'Açılış Adı', 0: 'Kazanma Oranı (%)'})


# 4) EN UZUN OYUNLAR
en_uzun = df.sort_values("move_count", ascending=False).head(15)[["opening_name", "move_count"]]
en_uzun_seri = en_uzun.set_index("opening_name")["move_count"]

df_en_uzun = dikey_grafik_ciz(
    "4. En Uzun Oyun Açılışları (Hamle Sayısı)",
    en_uzun_seri,
    "Açılış Adı",
    "Hamle Sayısı",
    "4_en_uzun_oyunlar.png",
    "#ffc107"
)
analiz_sonuclari["4. En Uzun Oyunlar"] = df_en_uzun.rename(columns={'opening_name': 'Açılış Adı', 'move_count': 'Hamle Sayısı'})


# 5) EN KISA OYUNLAR
en_kisa = df.sort_values("move_count", ascending=True).head(15)[["opening_name", "move_count"]]
en_kisa_seri = en_kisa.set_index("opening_name")["move_count"]

df_en_kisa = dikey_grafik_ciz(
    "5. En Kısa Oyun Açılışları (Hızlı Matlar)",
    en_kisa_seri,
    "Açılış Adı",
    "Hamle Sayısı",
    "5_en_kisa_oyunlar.png",
    "#6f42c1"
)
analiz_sonuclari["5. En Kısa Oyunlar"] = df_en_kisa.rename(columns={'opening_name': 'Açılış Adı', 'move_count': 'Hamle Sayısı'})

# ==========================
# 4. RAPORU OLUŞTUR
# ==========================

txt_raporu_olustur(analiz_sonuclari)

print("\n🎉 Tüm grafikler ve rapor tamamlandı!")
print(f"📁 Kayıt klasörü: {KAYIT_KLASORU}")