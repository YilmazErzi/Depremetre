from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from .models import Person, BuildingAssessment
from .forms import BuildingAssessmentForm
import json
import os
import unicodedata

# --- YARDIMCI FONKSİYONLAR ---

def normalize_string(s):
    """ Türkçe karakter düzeltme """
    if not s: return ""
    replacements = {
        'İ': 'i', 'I': 'i', 'ı': 'i', 'Ş': 's', 'ş': 's',
        'Ğ': 'g', 'ğ': 'g', 'Ü': 'u', 'ü': 'u',
        'Ö': 'o', 'ö': 'o', 'Ç': 'c', 'ç': 'c'
    }
    s = "".join([replacements.get(c, c) for c in s])
    return s.lower().strip()

def load_city_data():
    """ JSON dosyasını okuma """
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    json_file_path = os.path.join(current_directory, 'data', 'cities.json')
    
    if not os.path.exists(json_file_path):
        return {}

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

# --- VIEW FONKSİYONLARI ---

def index(request):
    # 1. BÖLÜM: KANDİLLİ VERİLERİNİ ÇEKME (Her durumda çalışsın)
    url ='http://www.koeri.boun.edu.tr/scripts/lst0.asp'
    earthquakes = []
    try:
        response = requests.get(url, timeout=3)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')
        data = soup.find("pre").text
        lines = data.splitlines()

        for line in lines:
            if line.strip().startswith("2025.") or line.strip().startswith("2024."):
                parts = line.split()
                try:
                    tarih = parts[0]
                    saat = parts[1]
                    ml = parts[6] if parts[6] != '-.-' else parts[7] if len(parts) > 7 else '-'
                    yer = " ".join(parts[8:-1]) if len(parts) > 8 else "Unknown"
                    earthquakes.append({"tarih": tarih, "saat": saat, "ml": ml, "yer": yer})
                except Exception:
                    continue
        earthquakes = earthquakes[:5]
    except:
        earthquakes = []

    # 2. BÖLÜM: ŞEHİR ARAMA İŞLEMİ
    result = None
    error = None
    city_name_input = ""

    # Eğer kullanıcı butona bastıysa (POST isteği geldiyse)
    if request.method == 'POST':
        query = request.POST.get('city')
        
        # Sadece 'city' inputu doluysa bu işlemi yap (Başka formlarla karışmasın)
        if query is not None:
            city_name_input = query
            if query.strip():
                city_data = load_city_data()
                query_normalized = normalize_string(query)
                
                if query_normalized in city_data:
                    result = city_data[query_normalized]
                    result['name'] = query.upper()
                else:
                    error = f"'{query}' veritabanımızda bulunamadı."
            else:
                error = "Lütfen bir şehir ismi giriniz."

    # Tüm verileri template'e gönderiyoruz
    context = {
        "earthquakes": earthquakes,
        "result": result,
        "error": error,
        "city_name": city_name_input
    }
    return render(request, "index.html", context)

def project(request):
    # (Burası aynı kaldı)
    result = None
    if request.method == 'POST':
        form = BuildingAssessmentForm(request.POST)
        if form.is_valid():
            instance = form.save()
            risk_data = instance.get_risk_level()
            total_score = instance.calculate_total_score()
            result = {
                "score": total_score,
                "level": risk_data["level"],
                "color": risk_data["color"],
                "message": risk_data["message"],
                "building_name": instance.building_name
            }
    else:
        form = BuildingAssessmentForm()
    return render(request, "project.html", {"form": form, "result": result})

def about(request):
    team = Person.objects.all()
    return render(request, "about.html", {"team": team})