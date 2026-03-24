#!/bin/bash

# 1. Analizi Başlat
python3 kanat_raporu.py

# 2. Klasör İsmi (Saat ve Dakika)
TARIH=$(date +%H%M)
KLASOR="Analiz_Raporu_$TARIH"
mkdir -p "$KLASOR"

# 3. Dosyaları Güvenli Şekilde Taşı
if [ -f "sonuc_raporu.csv" ]; then
    mv sonuc_raporu.csv "$KLASOR/Kanat_Verileri.csv"
    mv sonuc_gorsel.png "$KLASOR/Kanat_Grafigi.png"
    
    echo "------------------------------------------"
    echo -e "\033[0;32m [BAŞARILI] Rapor Hazır: $KLASOR \033[0m"
    echo "------------------------------------------"
else
    echo -e "\033[0;31m [HATA] Python dosyası oluşturamadı! \033[0m"
fi