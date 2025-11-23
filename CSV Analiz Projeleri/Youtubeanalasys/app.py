import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

# -------------------------------------------------------------------
# 1. TEMEL AYARLAR ve VERİ YÜKLEME
# -------------------------------------------------------------------

# Dosya Yolunu relative yaptık, klasör içinde çalışırken kolaylık sağlar.
FILE_PATH = r"youtubedata.csv"
OUTPUT_FOLDER = "youtube_analiz_ciktilari"

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Sütun İsimleri
TITLE_COL = 'Title'
VIEWS_COL = 'view_count'
LIKE_COL = 'like_count'
RATIO_COL = 'likes_to_views_ratio'
CHANNEL_COL = 'channel_title'
DURATION_COL = 'duration_seconds'
CATEGORY_COL = 'category_id'
DATE_COL = 'published_at'

try:
    print(f"'{FILE_PATH}' adresindeki CSV dosyasını yüklüyor...")
    df = pd.read_csv(FILE_PATH)
    df.columns = df.columns.str.strip()

    for col in [VIEWS_COL, LIKE_COL, RATIO_COL, DURATION_COL]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df = df.dropna(subset=[TITLE_COL, VIEWS_COL, LIKE_COL, RATIO_COL, CHANNEL_COL, DURATION_COL, CATEGORY_COL])

except Exception as e:
    print(f"❌ Hata: Veri yüklenirken veya temizlenirken hata oluştu: {e}")
    exit()

# -------------------------------------------------------------------
# 2. DİL SÖZLÜKLERİ VE GÖRSELLEŞTİRME FONKSİYONLARI (EKSİK KISIMLAR)
# -------------------------------------------------------------------

# A. DİL SÖZLÜKLERİ

LANG_TR = {
    'title_main': '# YOUTUBE VERİ ANALİZİ VE İÇERİK STRATEJİSİ ÖZETİ', 'file_name': 'TR_STRATEJI_OZETI.txt',
    'section_1_title': '## 1. TEMEL ÇIKARIMLAR VE METRİKLER',
    'short_video_engagement': 'Kısa Video Etkileşimi', 'long_video_engagement': 'Uzun Video Etkileşimi',
    'top_like_content': 'En Beğenilen Konu', 'top_channel': 'En Çok İzlenen Kanal',
    'top_category': 'En Yüksek Oranlı Kategori', 'section_2_title': '## 2. GÖRSEL ANALİZ BULGULARI',
    'critical_point': 'Kritik Nokta', 'critical_point_desc': 'Etkileşim oranları grafiği, en yüksek etkileşimin **2 dakikanın altındaki** içeriklerden geldiğini gösteriyor.',
    'action_point_1': 'Eylem', 'action_desc_1': 'Kısa formata (Shorts) yapılan yatırım, izleyici memnuniyetini (Beğeni oranı) hızla artırır.',
    'topic_analysis': 'Konu Popülaritesi', 'topic_desc': 'En çok beğeni alan videolar genellikle **Fitness/Motivasyon, Pratik Yemek/Tarifler** gibi hızlı tüketilebilen niş konuları içeriyor.',
    'section_3_title': '## 3. ÖNERİLEN İÇERİK STRATEJİSİ VE TAKVİM',
    'strategy_1_title': 'SHORT BOMBING (Kısa İçerik Saldırısı)', 'strategy_1_desc': 'Etkileşim oranınızı yükseltmek için, haftada minimum 3 adet Shorts/1 dakikalık video yükleyin. Konular: Fitness Hileleri, Hızlı Tarifler, Niş Teknoloji İpuçları.',
    'strategy_2_title': 'UZUN İÇERİK', 'strategy_2_desc': 'Haftada 1 adet uzun video (4-8 dakika). Bu video, Shorts\'ta başarılı olan konunun daha derinlemesine ele alındığı ana içerik olmalıdır.',
    'table_title': 'ÖRNEK HAFTALIK TAKVİM', 'table_header_day': 'Gün', 'table_header_focus': 'Odak', 'table_header_aim': 'Amaç',
    'table_row_mon': 'Pazartesi', 'table_row_wed': 'Çarşamba', 'table_row_fri': 'Cuma', 'table_row_sun': 'Pazar',
    'table_aim_1': 'Haftaya yüksek enerjiyle başla.', 'table_aim_2': 'Arama motoru trafiğini ve otoriteyi artır.',
    'table_aim_3': 'Hafta sonuna viral potansiyelle gir.', 'table_aim_4': 'Hafta sonu izleyicisini yakala ve yorumları teşvik et.',
}

LANG_EN = {
    'title_main': '# YOUTUBE DATA ANALYSIS AND CONTENT STRATEGY SUMMARY', 'file_name': 'EN_STRATEGY_SUMMARY.txt',
    'section_1_title': '## 1. KEY FINDINGS AND METRICS',
    'short_video_engagement': 'Short Video Engagement', 'long_video_engagement': 'Long Video Engagement',
    'top_like_content': 'Most Liked Topic', 'top_channel': 'Most Viewed Channel',
    'top_category': 'Highest Ratio Category', 'section_2_title': '## 2. VISUAL ANALYSIS FINDINGS',
    'critical_point': 'Critical Insight', 'critical_point_desc': 'The engagement ratio chart indicates that the highest engagement comes from content **under 2 minutes**.',
    'action_point_1': 'Action', 'action_desc_1': 'Investing in short-form content (Shorts) rapidly increases viewer satisfaction (Like Ratio).',
    'topic_analysis': 'Topic Popularity', 'topic_desc': 'Most liked videos typically involve rapidly consumable, niche topics like **Fitness/Motivation, Quick Recipes, or Tech Tips**.',
    'section_3_title': '## 3. RECOMMENDED CONTENT STRATEGY AND CALENDAR',
    'strategy_1_title': 'SHORT BOMBING (Short Content Attack)', 'strategy_1_desc': 'To boost your engagement ratio, upload a minimum of 3 Shorts/1-minute videos per week. Topics: Fitness Hacks, Quick Recipes, Niche Tech Tips.',
    'strategy_2_title': 'LONG-FORM CONTENT', 'strategy_2_desc': 'Upload 1 long-form video (4-8 minutes) per week. This should be the main, in-depth content covering topics successful in your Shorts.',
    'table_title': 'SAMPLE WEEKLY CALENDAR', 'table_header_day': 'Day', 'table_header_focus': 'Focus', 'table_header_aim': 'Aim',
    'table_row_mon': 'Monday', 'table_row_wed': 'Wednesday', 'table_row_fri': 'Friday', 'table_row_sun': 'Sunday',
    'table_aim_1': 'Start the week with high energy and engagement.', 'table_aim_2': 'Increase search traffic and authority.',
    'table_aim_3': 'Enter the weekend with viral potential.', 'table_aim_4': 'Capture weekend viewers and encourage comments.',
}

LANGUAGES = [LANG_TR, LANG_EN]
LANGUAGES_WITH_CODE = [('TR', LANG_TR), ('EN', LANG_EN)]


# B. GÖRSELLEŞTİRME FORMAT VE PLOT FONKSİYONLARI

def format_views(x, pos): # Milyon/Bin formatı
    if x >= 1e9: return f'{x*1e-9:1.1f}B' 
    if x >= 1e6: return f'{x*1e-6:1.1f}M'
    if x >= 1e3: return f'{x*1e-3:1.0f}K'
    return f'{x:1.0f}'

def format_ratio_percent(x, pos): # Yüzde formatı
    return f'{x*100:1.1f}%'

def plot_top_n_bar(data, x_col, y_col, title, filename, color, formatter=None, n=10):
    """Genel çubuk grafik çizim fonksiyonu."""
    top_data = data.sort_values(by=x_col, ascending=False).head(n)
    
    plt.figure(figsize=(12, 7))
    plt.barh(top_data[y_col], top_data[x_col], color=color)
    
    plt.xlabel(x_col.replace('_', ' ').title(), fontsize=12)
    plt.ylabel(y_col.replace('_', ' ').title(), fontsize=12)
    plt.title(title, fontsize=14)
    
    if formatter:
        plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(formatter))
        
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, filename))
    print(f"✅ Grafik kaydedildi: {filename}")
    plt.close()

# -------------------------------------------------------------------
# 3. ANALİZ ve GRAFİK OLUŞTURMA (7 Grafik)
# -------------------------------------------------------------------

print("\n--- Grafik Oluşturma Başladı ---")

# Grafiklerin dosya adlarını bir liste olarak tanımlayalım (GitHub'da linklemek için)
GRAPH_FILENAMES = [
    '1_top_10_views.png',
    '2_top_10_likes.png',
    '3_top_10_ratio.png',
    '4_top_10_channels.png',
    '5_duration_vs_ratio_scatter.png',
    '6_duration_histogram.png',
    '7_category_engagement.png',
]

# A. En Çok Görüntülenen 10 Video (CHART 1)
plot_top_n_bar(df, VIEWS_COL, TITLE_COL, 
                'En Çok Görüntülenen 10 YouTube Videosu', 
                GRAPH_FILENAMES[0], '#FF0000', format_views)

# B. En Çok Beğeni Alan 10 Video (CHART 2)
plot_top_n_bar(df, LIKE_COL, TITLE_COL, 
                'En Çok Beğeni Alan 10 YouTube Videosu', 
                GRAPH_FILENAMES[1], '#1DA1F2', format_views)

# C. En Yüksek Etkileşim Oranına Sahip 10 Video (CHART 3)
plot_top_n_bar(df, RATIO_COL, TITLE_COL, 
                'En Yüksek Etkileşim Oranına Sahip 10 Video (Beğeni/Görüntülenme)', 
                GRAPH_FILENAMES[2], '#3C7D2D', format_ratio_percent)

# D. Toplam Görüntülenmeye Göre En İyi 10 Kanal (CHART 4)
channel_views = df.groupby(CHANNEL_COL)[VIEWS_COL].sum().reset_index()
plot_top_n_bar(channel_views, VIEWS_COL, CHANNEL_COL, 
                'Toplam Görüntülenmeye Göre En İyi 10 YouTube Kanalı', 
                GRAPH_FILENAMES[3], '#FF9900', format_views)

# E. Video Süresi vs. İzleyici Etkileşimi (CHART 5) - Dağılım Grafiği
plt.figure(figsize=(10, 6))
plt.scatter(df[DURATION_COL], df[RATIO_COL], alpha=0.6, color='#5B5AA9', s=20)
plt.xlabel('Video Süresi (Saniye)', fontsize=12)
plt.ylabel('Beğeni/Görüntülenme Oranı', fontsize=12)
plt.title('Video Süresi vs. İzleyici Etkileşimi', fontsize=14)
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(format_ratio_percent))
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_FOLDER, GRAPH_FILENAMES[4]))
print(f"✅ Grafik kaydedildi: {GRAPH_FILENAMES[4]}")
plt.close()

# F. EK ANALİZ: Video Süresi Dağılımı (CHART 6)
plt.figure(figsize=(10, 6))
bins = np.arange(0, 300, 15)
df_short = df[df[DURATION_COL] < 300]
plt.hist(df_short[DURATION_COL], bins=bins, color='#E91E63', edgecolor='black', alpha=0.7)
plt.xlabel('Video Süresi (Saniye)', fontsize=12)
plt.ylabel('Video Sayısı', fontsize=12)
plt.title('Video Süresi Dağılımı (İlk 5 Dakika)', fontsize=14)
plt.xticks(bins)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_FOLDER, GRAPH_FILENAMES[5]))
print(f"✅ Grafik kaydedildi: {GRAPH_FILENAMES[5]}")
plt.close()

# G. EK ANALİZ: Kategoriye Göre Ortalama Etkileşim Oranı (CHART 7)
category_ratio = df.groupby(CATEGORY_COL)[RATIO_COL].mean().reset_index()
category_ratio = category_ratio.sort_values(by=RATIO_COL, ascending=False).head(10)

plt.figure(figsize=(12, 7))
plt.barh(category_ratio[CATEGORY_COL].astype(str), category_ratio[RATIO_COL], color='#009688')
plt.xlabel('Ortalama Beğeni/Görüntülenme Oranı', fontsize=12)
plt.ylabel('Kategori ID', fontsize=12)
plt.title('Kategoriye Göre En Yüksek Ortalama Etkileşim', fontsize=14)
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(format_ratio_percent))
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_FOLDER, GRAPH_FILENAMES[6]))
print(f"✅ Grafik kaydedildi: {GRAPH_FILENAMES[6]}")
plt.close()


print("\n--- Analiz Tamamlandı ---")

# -------------------------------------------------------------------
# 4. PYTHON ANALİZİNE DAYALI ÖZET ÇIKARMA VE METİN DOSYASINA KAYIT
# -------------------------------------------------------------------

# Hesaplamalar
short_video_engagement = df[df[DURATION_COL] <= 120][RATIO_COL].mean() * 100
long_video_engagement = df[df[DURATION_COL] > 120][RATIO_COL].mean() * 100
top_like_title = df.sort_values(by=LIKE_COL, ascending=False).iloc[0][TITLE_COL]
top_channel = channel_views.sort_values(by=VIEWS_COL, ascending=False).iloc[0][CHANNEL_COL]
top_category_ratio = category_ratio.iloc[0][CATEGORY_COL]


# GÖRSEL BAĞLANTILARI OLUŞTURMA FONKSİYONU
def generate_graph_links(lang_code):
    """GitHub Markdown formatında PNG bağlantılarını oluşturur."""
    links = "\n\n## GÖRSEL ANALİZ ÇIKTILARI (PNG)\n" if lang_code == 'TR' else "\n\n## VISUAL ANALYSIS OUTPUTS (PNG)\n"
    for filename in GRAPH_FILENAMES:
        if lang_code == 'TR':
             link_title = f"{filename[:-4]} Grafiği" 
        else:
             link_title = f"{filename[:-4]} Chart"
             
        links += f"\n### {link_title}\n"
        # Not: GitHub'da görselin görünmesi için yolu düzenliyoruz. 
        # PNG dosyasının kendisini metin dosyasına dahil etmek mümkün değil, sadece linkini veriyoruz.
        links += f"![{link_title}]({OUTPUT_FOLDER}/{filename})\n"
    return links


def create_summary_content(lang_dict, lang_code, short_eng, long_eng, top_title, top_chan, top_cat):
    """Belirtilen dil sözlüğüne göre özet metni oluşturur."""
    
    table_rows = f"""
| {lang_dict['table_header_day']} | {lang_dict['table_header_focus']} | {lang_dict['table_header_aim']} |
| :--- | :--- | :--- |
| {lang_dict['table_row_mon']} | Shorts (Motivation) | {lang_dict['table_aim_1']} |
| {lang_dict['table_row_wed']} | LONG-FORM VIDEO | {lang_dict['table_aim_2']} |
| {lang_dict['table_row_fri']} | Shorts (Quick Tip) | {lang_dict['table_aim_3']} |
| {lang_dict['table_row_sun']} | Shorts (Community) | {lang_dict['table_aim_4']} |
"""
    
    summary = f"""
{lang_dict['title_main']}
# Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Dataset: {os.path.basename(FILE_PATH)}
# ------------------------------------------------------------------

{lang_dict['section_1_title']}
- **{lang_dict['short_video_engagement']}:** 120 saniyeden kısa videoların ortalama etkileşim oranı: {short_eng:.2f}%
- **{lang_dict['long_video_engagement']}:** 120 saniyeden uzun videoların ortalama etkileşim oranı: {long_eng:.2f}%
- **{lang_dict['top_like_content']}:** "{top_title[:60]}..."
- **{lang_dict['top_channel']}:** "{top_chan}"
- **{lang_dict['top_category']}:** {top_cat}

{lang_dict['section_2_title']}
- **{lang_dict['critical_point']}:** {lang_dict['critical_point_desc']}
- **{lang_dict['action_point_1']}:** {lang_dict['action_desc_1']}
- **{lang_dict['topic_analysis']}:** {lang_dict['topic_desc']}

{lang_dict['section_3_title']}
### {lang_dict['strategy_1_title']}
{lang_dict['strategy_1_desc']}

### {lang_dict['strategy_2_title']}
{lang_dict['strategy_2_desc']}

#### {lang_dict['table_title']}
{table_rows}

{generate_graph_links(lang_code)}
"""
    return summary

# Her dil için özet oluştur ve kaydet
for lang_code, lang in LANGUAGES_WITH_CODE:
    summary_content = create_summary_content(
        lang, 
        lang_code,
        short_video_engagement, 
        long_video_engagement, 
        top_like_title, 
        top_channel, 
        top_category_ratio
    )
    
    output_file = os.path.join(OUTPUT_FOLDER, lang['file_name'])
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)

    print(f"\n✅ {lang['file_name']} dosyası (PNG bağlantıları dahil) başarıyla kaydedildi.")