import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Kullanıcıdan NACA girişi al
naca_input = input("Analiz edilecek NACA profilini girin (Örn: 4412): ")
m = int(naca_input[0]) / 100.0
p = int(naca_input[1]) / 10.0
t = int(naca_input[2:]) / 100.0

# 2. Geometri Hesaplama (NACA 4-Digit)
def naca4_geom(m, p, t, c=1.0, n=100):
    x = np.linspace(0, c, n)
    yt = 5 * t * (0.2969*np.sqrt(x) - 0.1260*x - 0.3516*x**2 + 0.2843*x**3 - 0.1015*x**4)
    if p == 0:
        yc = np.zeros_like(x)
    else:
        yc = np.where(x < p*c, m/p**2 * (2*p*x/c - (x/c)**2), 
                      m/(1-p)**2 * ((1-2*p) + 2*p*x/c - (x/c)**2))
    return x, yc + yt, yc - yt

x, y_ust, y_alt = naca4_geom(m, p, t)

# 3. Gerçekçi Havacılık Hesaplamaları (5 Derece Hücum Açısı İçin)
# Taşıma Katsayısı (Cl)
cl = 2 * np.pi * (np.radians(5) + m)

# Sürükleme (Direnç) Katsayısı (Cd) - Gerçekçi Model
cd0 = 0.015 + (t * 0.05)  # Profil direnci
k = 0.05                 # İndüklenmiş direnç faktörü
cd = cd0 + k * (cl**2)

# Verimlilik (L/D)
verimlilik = cl / cd

# 4. Verileri Birleştir (Excel için Noktalı Virgül Ayırıcılı)
df = pd.DataFrame({
    'X_Konumu': x, 
    'Y_Ust': y_ust, 
    'Y_Alt': y_alt,
    'Cl_Katsayisi': [round(cl, 4)]*len(x),
    'Cd_Direnc': [round(cd, 5)]*len(x),
    'LD_Verimlilik': [round(verimlilik, 2)]*len(x)
})

# Sabit dosya adı (Bash için)
df.to_csv("sonuc_raporu.csv", index=False, sep=';')

# 5. Profesyonel Grafik
plt.figure(figsize=(10, 4))
plt.plot(x, y_ust, 'b', label=f'Üst Yüzey (Cl: {cl:.2f})')
plt.plot(x, y_alt, 'r', label=f'Alt Yüzey (Cd: {cd:.4f})')
plt.fill_between(x, y_alt, y_ust, color='gray', alpha=0.3)
plt.title(f'NACA {naca_input} Aerodinamik Analizi - Verimlilik (L/D): {verimlilik:.2f}')
plt.axis('equal')
plt.grid(True, linestyle='--')
plt.legend()
plt.savefig("sonuc_gorsel.png")
plt.close()

print(f"\n>>> {naca_input} Analizi Tamamlandı. Verimlilik: {verimlilik:.2f}")