# Capstone project Data Science (Dicoding Bootcamp) - mdavap

## Run Dashboard Model Prediction
```
docker run -p 8501:8501 ghcr.io/imcodingcat/anime-prediction:latest
```

## Data Attribution Notice

The data utilized in this project was obtained through the Jikan API, which interfaces with MyAnimeList's database. All content, including anime titles, descriptions, and associated metadata, remains the intellectual property of MyAnimeList and their respective content creators.

This project is strictly for educational purposes as part of a capstone project. No commercial use is intended or implied. The collection and analysis of this data comply with MyAnimeList's terms of service and API usage guidelines.

For access to the original content or additional information, please visit MyAnimeList (myanimelist.net).

## Latar Belakang
Industri anime telah mengalami pertumbuhan yang signifikan dalam beberapa tahun terakhir, dengan nilai pasar global mencapai $25.71 miliar pada tahun 2023. Namun, tidak semua anime mencapai kesuksesan komersial. Produsen dan studio anime menghadapi tantangan besar dalam menentukan faktor-faktor yang mempengaruhi kesuksesan sebuah anime, mengingat besarnya investasi yang diperlukan dalam produksi. Dengan memanfaatkan data historis dan teknik machine learning, kita dapat mengembangkan model prediktif yang membantu stakeholder dalam industri anime untuk membuat keputusan yang lebih informasi terkait pengembangan dan investasi konten.

### Problem Statement:
- Studio anime dan investor menghadapi kesulitan dalam memprediksi potensi kesuksesan anime sebelum produksi, yang dapat menyebabkan risiko finansial yang signifikan.
- Kurangnya pemahaman kuantitatif tentang faktor-faktor yang berkontribusi terhadap kesuksesan anime menyulitkan proses pengambilan keputusan dalam pengembangan konten.
- Tidak adanya sistem prediksi berbasis data yang dapat membantu stakeholder dalam mengevaluasi potensi keberhasilan proyek anime.

### Research Questions:
1. Faktor-faktor apa saja yang memiliki pengaruh signifikan terhadap kesuksesan sebuah anime?
    - Bagaimana pengaruh genre terhadap tingkat kesuksesan?
    - Apakah durasi episode dan jumlah episode mempengaruhi popularitas?
    - Seberapa besar dampak studio produksi terhadap kesuksesan anime?
2. Bagaimana mengembangkan model prediktif yang akurat untuk memperkirakan kesuksesan anime?
    - Metode machine learning apa yang paling efektif untuk prediksi?
    - Fitur-fitur apa yang harus dipertimbangkan dalam model?
    - Bagaimana mengukur dan mengevaluasi akurasi prediksi?
3. Bagaimana karakteristik pasar mempengaruhi kesuksesan anime?
    - Apakah tren musiman mempengaruhi popularitas?
    - Bagaimana pengaruh platform distribusi terhadap kesuksesan?

### Analisis SWOT
- Strength, Proyek ini tergolong gampang untuk direalisasi seperti data yang tersedia gampang untuk diambil dan pembuatan machine learning tergolong simpel.
- Weakness, Adanya Subjektivitas dalam menentukan kriteria "kesuksesan", Kesulitan mengukur data kualitatif seperti Kualitas cerita dan Karakter.
- Opportunities, Ekspansi pasar membuat pertumbuhan anime pesat serta meningkatkan investasi dalam produksi anime.
- Threats, Perubahan industri seperti tren yang berubah cepat dalam industri anime serta perubahan preferensi penonton.

