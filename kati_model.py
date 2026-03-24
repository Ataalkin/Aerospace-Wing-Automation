import numpy as np

# 1. Kullanıcıdan NACA girişi al
naca_input = input("SolidWorks için hangi NACA profilini hazırlayalım? (Örn: 4412): ")
m = int(naca_input[0]) / 100.0
p = int(naca_input[1]) / 10.0
t = int(naca_input[2:]) / 100.0

# 2. Geometri Hesaplama Fonksiyonu
def naca4_geom(m, p, t, c=1.0, n=100):
    x = np.linspace(0, c, n)
    # Kalınlık dağılımı
    yt = 5 * t * (0.2969*np.sqrt(x) - 0.1260*x - 0.3516*x**2 + 0.2843*x**3 - 0.1015*x**4)
    # Kamburluk hattı
    if p == 0:
        yc = np.zeros_like(x)
    else:
        yc = np.where(x < p*c, m/p**2 * (2*p*x/c - (x/c)**2), 
                      m/(1-p)**2 * ((1-2*p) + 2*p*x/c - (x/c)**2))
    
    return x, yc + yt, yc - yt

x, y_ust, y_alt = naca4_geom(m, p, t)

# --- KRİTİK DÜZELTME: Pürüzsüz Çevrim (Kuyruktan Buruna, Burundan Kuyruğa) ---
# Solidworks'ün ucu açık bırakmaması veya kanca yapmaması için:
# Üst yüzeyi arkadan öne (1.0 -> 0.0) diziyoruz
# Alt yüzeyi önden arkaya (0.0 -> 1.0) diziyoruz

x_ust_ters = x[::-1]
y_ust_ters = y_ust[::-1]

# Burun noktasının (0,0) çakışmaması için alt yüzeyin ilk noktasını atlıyoruz [1:]
x_alt_duz = x[1:]
y_alt_duz = y_alt[1:]

# Koordinatları birleştir
final_x = np.concatenate([x_ust_ters, x_alt_duz])
final_y = np.concatenate([y_ust_ters, y_alt_duz])
final_z = np.zeros_like(final_x)

# 3. SolidWorks Formatında Yazdır (X [TAB] Y [TAB] Z)
file_name = f"NACA_{naca_input}_SolidWorks.txt"
with open(file_name, "w") as f:
    for xi, yi, zi in zip(final_x, final_y, final_z):
        # Solidworks noktalar arasında TAB (sekme) bekler
        f.write(f"{xi:.6f}\t{yi:.6f}\t{zi:.6f}\n")

print("-" * 40)
print(f"BAŞARILI: {file_name} dosyası oluşturuldu.")
print("Solidworks Adımları:")
print("1. Insert > Curve > Curve Through XYZ Points")
print(f"2. Gözat diyerek {file_name} dosyasını seç.")
print("3. OK de ve pürüzsüz kanadın tadını çıkar!")
print("-" * 40)