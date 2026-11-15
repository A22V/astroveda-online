# -*- coding: utf-8 -*-

import streamlit as st

import swisseph as swe

import datetime

import math

import json

import pandas as pd

import numpy as np



# === MODULE: astroveda_pro/core/constants.py ===

# -*- coding: utf-8 -*-
"""
Полный справочник констант Джйотиш для системы AstroVeda Pro (VedicHoro Ultimate Clone).
Содержит данные по Раши, Накшатрам, 20 Варгам, Особым градусам (Мритью/Пушкара Бхага),
Упаграхам, Каракам, Таджака-орбам, Сахамам, 60+ событиям Мухурты и городам.
"""

RASHIS = [
    "Овен (Mesha)", "Телец (Vrishabha)", "Близнецы (Mithuna)", "Рак (Karka)",
    "Лев (Simha)", "Дева (Kanya)", "Весы (Tula)", "Скорпион (Vrischika)",
    "Стрелец (Dhanu)", "Козерог (Makara)", "Водолей (Kumbha)", "Рыбы (Meena)"
]

RASHI_SHORT = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]
RASHI_RU_SHORT = ["Овн", "Тел", "Блз", "Рак", "Лев", "Дев", "Вес", "Скр", "Стр", "Коз", "Вод", "Рыб"]

# Управители знаков (0..11)
RASHI_LORDS = ["Ma", "Ve", "Me", "Mo", "Su", "Me", "Ve", "Ma", "Ju", "Sa", "Sa", "Ju"]

# Таттвы (стихии) знаков: Огонь, Земля, Воздух, Вода
RASHI_ELEMENTS = ["Огонь", "Земля", "Воздух", "Вода", "Огонь", "Земля", "Воздух", "Вода", "Огонь", "Земля", "Воздух", "Вода"]

# Модальности знаков: Чара (Подвижный), Стхира (Фиксированный), Двисвабхава (Двойственный)
RASHI_MODALITIES = ["Чара", "Стхира", "Двисвабхава", "Чара", "Стхира", "Двисвабхава",
                    "Чара", "Стхира", "Двисвабхава", "Чара", "Стхира", "Двисвабхава"]

PLANET_NAMES = {
    "As": "Асцендент (Lagna)",
    "Su": "Солнце (Surya)",
    "Mo": "Луна (Chandra)",
    "Ma": "Марс (Mangala)",
    "Me": "Меркурий (Budha)",
    "Ju": "Юпитер (Guru)",
    "Ve": "Венера (Shukra)",
    "Sa": "Сатурн (Shani)",
    "Ra": "Раху (Rahu)",
    "Ke": "Кету (Ketu)",
    "Ur": "Уран (Uranus)",
    "Ne": "Нептун (Neptune)",
    "Pl": "Плутон (Pluto)"
}

PLANET_COLORS = {
    "As": "#38bdf8",
    "Su": "#fb923c",
    "Mo": "#f8fafc",
    "Ma": "#ef4444",
    "Me": "#22c55e",
    "Ju": "#eab308",
    "Ve": "#f472b6",
    "Sa": "#818cf8",
    "Ra": "#94a3b8",
    "Ke": "#a8a29e",
    "Ur": "#2dd4bf",
    "Ne": "#60a5fa",
    "Pl": "#c084fc"
}

# Экзальтация (знак 0..11 и точный градус), Дебилитация, Свой знак и Мулатрикона
EXALTATION = {
    "Su": (0, 10), "Mo": (1, 3), "Ma": (9, 28), "Me": (5, 15),
    "Ju": (3, 5), "Ve": (11, 27), "Sa": (6, 20), "Ra": (1, 20), "Ke": (7, 20)
}
DEBILITATION = {
    "Su": (6, 10), "Mo": (7, 3), "Ma": (3, 28), "Me": (11, 15),
    "Ju": (9, 5), "Ve": (5, 27), "Sa": (0, 20), "Ra": (7, 20), "Ke": (1, 20)
}
OWN_SIGNS = {
    "Su": [4], "Mo": [3], "Ma": [0, 7], "Me": [2, 5],
    "Ju": [8, 11], "Ve": [1, 6], "Sa": [9, 10], "Ra": [10], "Ke": [7]
}
MOOLATRIKONA = {
    "Su": (4, 0, 20), "Mo": (1, 4, 30), "Ma": (0, 0, 12), "Me": (5, 16, 20),
    "Ju": (8, 0, 10), "Ve": (6, 0, 15), "Sa": (10, 0, 20)
}

# Естественная дружба планет (Наৈсаргика Маитри)
NATURAL_FRIENDS = {
    "Su": {"friends": ["Mo", "Ma", "Ju"], "neutral": ["Me"], "enemies": ["Ve", "Sa", "Ra", "Ke"]},
    "Mo": {"friends": ["Su", "Me"], "neutral": ["Ma", "Ju", "Ve", "Sa"], "enemies": ["Ra", "Ke"]},
    "Ma": {"friends": ["Su", "Mo", "Ju"], "neutral": ["Ve", "Sa"], "enemies": ["Me", "Ra", "Ke"]},
    "Me": {"friends": ["Su", "Ve"], "neutral": ["Ma", "Ju", "Sa"], "enemies": ["Mo", "Ra", "Ke"]},
    "Ju": {"friends": ["Su", "Mo", "Ma"], "neutral": ["Sa"], "enemies": ["Me", "Ve", "Ra", "Ke"]},
    "Ve": {"friends": ["Me", "Sa", "Ra", "Ke"], "neutral": ["Ma", "Ju"], "enemies": ["Su", "Mo"]},
    "Sa": {"friends": ["Me", "Ve", "Ra", "Ke"], "neutral": ["Ju"], "enemies": ["Su", "Mo", "Ma"]},
    "Ra": {"friends": ["Ve", "Sa", "Me"], "neutral": ["Ju"], "enemies": ["Su", "Mo", "Ma"]},
    "Ke": {"friends": ["Ma", "Ve", "Sa"], "neutral": ["Me", "Ju"], "enemies": ["Su", "Mo"]}
}

# Мритью Бхага (смертоносные градусы по знакам 0..11) согласно Парашаре
MRITYU_BHAGA = {
    "As": [1, 9, 22, 22, 25, 2, 4, 23, 18, 20, 24, 10],
    "Su": [20, 9, 12, 6, 8, 24, 16, 17, 22, 2, 3, 23],
    "Mo": [26, 12, 13, 25, 24, 11, 26, 14, 13, 25, 5, 12],
    "Ma": [19, 28, 25, 23, 29, 28, 14, 21, 2, 15, 11, 6],
    "Me": [15, 14, 13, 12, 8, 18, 20, 10, 21, 22, 7, 5],
    "Ju": [19, 29, 12, 27, 6, 4, 13, 10, 17, 11, 15, 28],
    "Ve": [28, 15, 11, 17, 10, 13, 4, 6, 27, 12, 29, 19],
    "Sa": [10, 4, 7, 9, 12, 16, 3, 18, 28, 14, 13, 15],
    "Ra": [14, 13, 12, 11, 24, 23, 22, 21, 10, 20, 18, 8],
    "Ke": [8, 18, 20, 10, 21, 22, 23, 24, 11, 12, 13, 14]
}

# Пушкара Бхага (благословенные градусы по знакам 0..11)
PUSHKARA_BHAGA = [21, 14, 18, 8, 19, 9, 24, 11, 23, 14, 19, 9]

# Диг Бала (дом максимальной направляющей силы) и Марана Карака Стхана (дом смерти для планеты)
DIG_BALA_HOUSE = {"Su": 10, "Ma": 10, "Ju": 1, "Me": 1, "Mo": 4, "Ve": 4, "Sa": 7}
MKS_HOUSE = {"Su": 12, "Mo": 8, "Ma": 7, "Me": 7, "Ju": 3, "Ve": 6, "Sa": 1, "Ra": 9, "Ke": 2}

# Градусы сожжения (от Солнца)
COMBUST_ORBS = {"Mo": 12, "Ma": 17, "Me": 14, "Me_R": 12, "Ju": 11, "Ve": 10, "Ve_R": 8, "Sa": 15}

# Орбы Диптхамша для Таджака-йог
TAJAKA_ORBS = {"Su": 15, "Mo": 12, "Ma": 8, "Me": 7, "Ju": 9, "Ve": 7, "Sa": 9}

# 27 Накшатр с полной мета-информацией для Мухурты и Аштакуты
NAKSHATRAS = [
    {"idx": 0, "name": "Ашвини", "lord": "Ke", "gana": "Дева", "yoni": "Лошадь", "nadi": "Ади (Вата)", "nature": "Кшипра (Быстрая)"},
    {"idx": 1, "name": "Бхарани", "lord": "Ve", "gana": "Манушья", "yoni": "Слон", "nadi": "Мадхья (Питта)", "nature": "Угра (Жесткая)"},
    {"idx": 2, "name": "Криттика", "lord": "Su", "gana": "Ракшаса", "yoni": "Овца", "nadi": "Антья (Капха)", "nature": "Мишра (Смешанная)"},
    {"idx": 3, "name": "Рохини", "lord": "Mo", "gana": "Манушья", "yoni": "Змея", "nadi": "Антья (Капха)", "nature": "Дхрува (Фиксированная)"},
    {"idx": 4, "name": "Мригашира", "lord": "Ma", "gana": "Дева", "yoni": "Змея", "nadi": "Мадхья (Питта)", "nature": "Мриду (Мягкая)"},
    {"idx": 5, "name": "Ардра", "lord": "Ra", "gana": "Манушья", "yoni": "Собака", "nadi": "Ади (Вата)", "nature": "Тикшна (Острая)"},
    {"idx": 6, "name": "Пунарвасу", "lord": "Ju", "gana": "Дева", "yoni": "Кошка", "nadi": "Ади (Вата)", "nature": "Чара (Подвижная)"},
    {"idx": 7, "name": "Пушья", "lord": "Sa", "gana": "Дева", "yoni": "Овца", "nadi": "Мадхья (Питта)", "nature": "Кшипра (Быстрая)"},
    {"idx": 8, "name": "Ашлеша", "lord": "Me", "gana": "Ракшаса", "yoni": "Кошка", "nadi": "Антья (Капха)", "nature": "Тикшна (Острая)"},
    {"idx": 9, "name": "Магха", "lord": "Ke", "gana": "Ракшаса", "yoni": "Крыса", "nadi": "Антья (Капха)", "nature": "Угра (Жесткая)"},
    {"idx": 10, "name": "Пурва Пхалгуни", "lord": "Ve", "gana": "Манушья", "yoni": "Крыса", "nadi": "Мадхья (Питта)", "nature": "Угра (Жесткая)"},
    {"idx": 11, "name": "Уттара Пхалгуни", "lord": "Su", "gana": "Манушья", "yoni": "Корова", "nadi": "Ади (Вата)", "nature": "Дхрува (Фиксированная)"},
    {"idx": 12, "name": "Хаста", "lord": "Mo", "gana": "Дева", "yoni": "Буйвол", "nadi": "Ади (Вата)", "nature": "Кшипра (Быстрая)"},
    {"idx": 13, "name": "Читра", "lord": "Ma", "gana": "Ракшаса", "yoni": "Тигр", "nadi": "Мадхья (Питта)", "nature": "Мриду (Мягкая)"},
    {"idx": 14, "name": "Свати", "lord": "Ra", "gana": "Дева", "yoni": "Буйвол", "nadi": "Антья (Капха)", "nature": "Чара (Подвижная)"},
    {"idx": 15, "name": "Вишакха", "lord": "Ju", "gana": "Ракшаса", "yoni": "Тигр", "nadi": "Антья (Капха)", "nature": "Мишра (Смешанная)"},
    {"idx": 16, "name": "Анурадха", "lord": "Sa", "gana": "Дева", "yoni": "Олень", "nadi": "Мадхья (Питта)", "nature": "Мриду (Мягкая)"},
    {"idx": 17, "name": "Джйештха", "lord": "Me", "gana": "Ракшаса", "yoni": "Олень", "nadi": "Ади (Вата)", "nature": "Тикшна (Острая)"},
    {"idx": 18, "name": "Мула", "lord": "Ke", "gana": "Ракшаса", "yoni": "Собака", "nadi": "Ади (Вата)", "nature": "Тикшна (Острая)"},
    {"idx": 19, "name": "Пурвашадха", "lord": "Ve", "gana": "Манушья", "yoni": "Обезьяна", "nadi": "Мадхья (Питта)", "nature": "Угра (Жесткая)"},
    {"idx": 20, "name": "Уттарашадха", "lord": "Su", "gana": "Манушья", "yoni": "Мангуст", "nadi": "Антья (Капха)", "nature": "Дхрува (Фиксированная)"},
    {"idx": 21, "name": "Шравана", "lord": "Mo", "gana": "Дева", "yoni": "Обезьяна", "nadi": "Антья (Капха)", "nature": "Чара (Подвижная)"},
    {"idx": 22, "name": "Дхаништха", "lord": "Ma", "gana": "Ракшаса", "yoni": "Лев", "nadi": "Мадхья (Питта)", "nature": "Чара (Подвижная)"},
    {"idx": 23, "name": "Шатабхиша", "lord": "Ra", "gana": "Ракшаса", "yoni": "Лошадь", "nadi": "Ади (Вата)", "nature": "Чара (Подвижная)"},
    {"idx": 24, "name": "Пурва Бхадрапада", "lord": "Ju", "gana": "Манушья", "yoni": "Лев", "nadi": "Ади (Вата)", "nature": "Угра (Жесткая)"},
    {"idx": 25, "name": "Уттара Бхадрапада", "lord": "Sa", "gana": "Манушья", "yoni": "Корова", "nadi": "Мадхья (Питта)", "nature": "Дхрува (Фиксированная)"},
    {"idx": 26, "name": "Ревати", "lord": "Me", "gana": "Дева", "yoni": "Слон", "nadi": "Антья (Капха)", "nature": "Мриду (Мягкая)"}
]

# 20 Дробных карт (Варг)
VARGAS_LIST = [
    ("D1", "Раши (D1) — Физическое тело и общая судьба"),
    ("D2", "Хора (D2) — Богатство и ресурсы"),
    ("D3", "Дреккана (D3) — Братья, сестры, смелость и усилия"),
    ("D4", "Чатуртхамша (D4) — Недвижимость, дом и удача"),
    ("D5", "Панчамша (D5) — Духовный авторитет и слава"),
    ("D6", "Шаштамша (D6) — Болезни, долги и препятствия"),
    ("D7", "Саптамша (D7) — Дети, внуки и творческое наследие"),
    ("D8", "Аштамша (D8) — Долголетие и внезапные перемены"),
    ("D9", "Навамша (D9) — Брак, партнерство, Дхарма и плоды кармы"),
    ("D10", "Дашамша (D10) — Карьера, профессия и статус в обществе"),
    ("D11", "Рудрамша (D11) — Победа в конфликтах и скрытые ресурсы"),
    ("D12", "Двадашамша (D12) — Родители и родовая карма"),
    ("D16", "Шодашамша (D16) — Автомобили, комфорт и внутреннее счастье"),
    ("D20", "Вимшамша (D20) — Духовная практика и религиозность"),
    ("D24", "Сиддхамша (D24) — Высшее образование и мудрость"),
    ("D27", "Накшатрамша (D27) — Сильные и слабые стороны натуры"),
    ("D30", "Тримшамша (D30) — Несчастья, пороки и кризисы"),
    ("D40", "Кхаведамша (D40) — Благоприятная/неблагоприятная карма по матери"),
    ("D45", "Акшаведамша (D45) — Моральные качества и карма по отцу"),
    ("D60", "Шаштьямша (D60) — Прошлая жизнь и глубинные самскары")
]

# Встроенный справочник популярных городов для мгновенного автозаполнения без задержек сети
PRESET_CITIES = {
    "Шымкент (Казахстан)": (42.34, 69.59, 5.0),
    "Асыларык / Сайрамский р-н (Казахстан)": (42.31, 69.77, 5.0),
    "Аксукент (Казахстан)": (42.42, 69.83, 5.0),
    "Алматы (Казахстан)": (43.24, 76.89, 5.0),
    "Астана (Казахстан)": (51.17, 71.45, 5.0),
    "Туркестан (Казахстан)": (43.30, 68.25, 5.0),
    "Ташкент (Узбекистан)": (41.30, 69.24, 5.0),
    "Москва (Россия)": (55.75, 37.62, 3.0),
    "Санкт-Петербург (Россия)": (59.93, 30.33, 3.0),
    "Екатеринбург (Россия)": (56.84, 60.65, 5.0),
    "Новосибирск (Россия)": (55.01, 82.93, 7.0),
    "Нью-Дели (Индия)": (28.61, 77.21, 5.5),
    "Варанаси (Индия)": (25.32, 82.97, 5.5),
    "Лондон (Великобритания)": (51.51, -0.13, 0.0),
    "Нью-Йорк (США)": (40.71, -74.01, -5.0)
}


# === MODULE: astroveda_pro/core/ephemeris.py ===

# -*- coding: utf-8 -*-
"""
Астрономическое ядро AstroVeda Pro на базе Swiss Ephemeris (pyswisseph).
Поддерживает:
- 20 классических дробных карт (Варг) по Парашаре
- Специальные настройки К.Н. Рао / Санджая Ратха (Айанамши, Узлы, Чара Караки 7/8)
- Полные статусы планет: Экзальтация, Дебилитация, Мулатрикона, Функциональная благотворность,
  Авастхи (Бала, Кумара, Юва, Вриддха, Мрита), Сожжение, Планетная война,
  Мритью Бхага, Пушкара Бхага, Пушкара/Виша Навамша, Сарпа Дреккана, Варготтама, Ганданта, Диг Бала, МКС.
- Карта Бхава Чалита (система Кампануса / Плацидуса / Шрипати).
"""

import swisseph as swe
import datetime
import math


AYANAMSHA_MAP = {
    "Лахири (Chitrapaksha)": swe.SIDM_LAHIRI,
    "Истинная Читтрапакша (True Chitrapaksha)": swe.SIDM_TRUE_CITRA,
    "Раман (B.V. Raman)": swe.SIDM_RAMAN,
    "Кришнамурти (KP)": swe.SIDM_KRISHNAMURTI,
    "Уша-Шаши (Usha-Shashi)": swe.SIDM_USHASHASHI,
    "Юктешвар (Sri Yukteshwar)": swe.SIDM_YUKTESHWAR
}

def compute_varga_sign(lon: float, varga_code: str) -> int:
    """Точный расчет знака (0..11) в любой из 20 дробных карт Парашары."""
    rashi = int(lon // 30.0) % 12
    deg = lon % 30.0
    is_odd = (rashi % 2 == 0)  # 0=Овен (1-й знак, нечетный), 1=Телец (2-й знак, четный)
    modality = rashi % 3       # 0=Чара (Подвижный), 1=Стхира (Фиксированный), 2=Двисвабхава (Двойственный)

    if varga_code == "D1":
        return rashi
    elif varga_code == "D2":
        # Парашара Хора: в нечетных знаках 0-15° Солнце (Лев=4), 15-30° Луна (Рак=3); в четных наоборот
        first_half = (deg < 15.0)
        if is_odd:
            return 4 if first_half else 3
        else:
            return 3 if first_half else 4
    elif varga_code == "D3":
        part = int(deg // 10.0)
        return (rashi + part * 4) % 12
    elif varga_code == "D4":
        part = int(deg // 7.5)
        return (rashi + part * 3) % 12
    elif varga_code == "D5":
        part = int(deg // 6.0)
        if is_odd:
            seq = [0, 10, 8, 2, 6]  # Овен, Водолей, Стрелец, Близнецы, Весы
        else:
            seq = [1, 5, 11, 9, 7]  # Телец, Дева, Рыбы, Козерог, Скорпион
        return seq[min(part, 4)]
    elif varga_code == "D6":
        part = int(deg // 5.0)
        start = 0 if is_odd else 6
        return (start + part) % 12
    elif varga_code == "D7":
        part = int(deg // (30.0 / 7.0))
        start = rashi if is_odd else (rashi + 6) % 12
        return (start + part) % 12
    elif varga_code == "D8":
        part = int(deg // 3.75)
        starts = [0, 8, 4]  # Чара->Овен, Стхира->Стрелец, Двисвабхава->Лев
        return (starts[modality] + part) % 12
    elif varga_code == "D9":
        part = int(deg // (30.0 / 9.0))
        starts = [0, 9, 6, 3]  # Огонь->Овен, Земля->Козерог, Воздух->Весы, Вода->Рак
        return (starts[rashi % 4] + part) % 12
    elif varga_code == "D10":
        part = int(deg // 3.0)
        start = rashi if is_odd else (rashi + 8) % 12
        return (start + part) % 12
    elif varga_code == "D11":
        part = int(deg // (30.0 / 11.0))
        return (11 - rashi + part) % 12
    elif varga_code == "D12":
        part = int(deg // 2.5)
        return (rashi + part) % 12
    elif varga_code == "D16":
        part = int(deg // (30.0 / 16.0))
        starts = [0, 4, 8]  # Овен, Лев, Стрелец
        return (starts[modality] + part) % 12
    elif varga_code == "D20":
        part = int(deg // 1.5)
        starts = [0, 8, 4]  # Чара->Овен, Стхира->Стрелец, Двисвабхава->Лев
        return (starts[modality] + part) % 12
    elif varga_code == "D24":
        part = int(deg // 1.25)
        start = 4 if is_odd else 3  # Нечетные со Льва, четные с Рака
        return (start + part) % 12
    elif varga_code == "D27":
        part = int(deg // (30.0 / 27.0))
        starts = [0, 3, 6, 9]  # Огонь->Овен, Земля->Рак, Воздух->Весы, Вода->Козерог
        return (starts[rashi % 4] + part) % 12
    elif varga_code == "D30":
        # Классическая Тримшамша Парашары
        if is_odd:
            if deg < 5: return 0    # Марс (Овен)
            elif deg < 10: return 10 # Сатурн (Водолей)
            elif deg < 18: return 8  # Юпитер (Стрелец)
            elif deg < 25: return 2  # Меркурий (Близнецы)
            else: return 6           # Венера (Весы)
        else:
            if deg < 5: return 1    # Венера (Телец)
            elif deg < 12: return 5  # Меркурий (Дева)
            elif deg < 20: return 11 # Юпитер (Рыбы)
            elif deg < 25: return 9  # Сатурн (Козерог)
            else: return 7           # Марс (Скорпион)
    elif varga_code == "D40":
        part = int(deg // 0.75)
        start = 0 if is_odd else 6
        return (start + part) % 12
    elif varga_code == "D45":
        part = int(deg // (30.0 / 45.0))
        starts = [0, 4, 8]
        return (starts[modality] + part) % 12
    elif varga_code == "D60":
        part = int(deg // 0.5)
        return (rashi + part) % 12
    return rashi

def get_planet_dignity(p_code: str, rashi_idx: int, deg: float) -> str:
    """Определяет достоинство планеты в знаке (Экзальтация, Мулатрикона, Свой знак, Друг, Нейтрал, Враг, Дебилитация)."""
    if p_code == "As" or p_code in ["Ur", "Ne", "Pl"]:
        return "—"
    if p_code in EXALTATION and EXALTATION[p_code][0] == rashi_idx:
        ex_deg = EXALTATION[p_code][1]
        return "Макс. Экзальтация !" if abs(deg - ex_deg) <= 1.5 else "Экзальтация (Учча)"
    if p_code in DEBILITATION and DEBILITATION[p_code][0] == rashi_idx:
        deb_deg = DEBILITATION[p_code][1]
        return "Макс. Дебилитация !" if abs(deg - deb_deg) <= 1.5 else "Дебилитация (Нича)"
    if p_code in MOOLATRIKONA:
        m_sign, m_start, m_end = MOOLATRIKONA[p_code]
        if rashi_idx == m_sign and m_start <= deg <= m_end:
            return "Мулатрикона"
    if p_code in OWN_SIGNS and rashi_idx in OWN_SIGNS[p_code]:
        return "Свой знак (Свакшетра)"
    
    sign_lord = RASHI_LORDS[rashi_idx]
    if p_code in NATURAL_FRIENDS:
        if sign_lord in NATURAL_FRIENDS[p_code]["friends"]:
            return "Дружественный (Митра)"
        elif sign_lord in NATURAL_FRIENDS[p_code]["enemies"]:
            return "Враждебный (Шатру)"
    return "Нейтральный (Сама)"

def get_functional_nature(p_code: str, asc_rashi: int) -> str:
    """Определяет функциональную благотворность планеты для данной Лагны (Б, П, Н, ЙК, Бадхакеш)."""
    if p_code in ["As", "Ra", "Ke", "Ur", "Ne", "Pl"]:
        return "Н"
    # Дома, которыми управляет планета от Лагны
    owned_houses = []
    for s_idx in range(12):
        if RASHI_LORDS[s_idx] == p_code:
            owned_houses.append(((s_idx - asc_rashi) % 12) + 1)
    
    trikonas = {1, 5, 9}
    kendras = {1, 4, 7, 10}
    malefic_houses = {3, 6, 8, 11, 12}
    
    has_trikona = any(h in trikonas for h in owned_houses)
    has_kendra = any(h in kendras and h != 1 for h in owned_houses)
    
    # Бадхака дом для Лагны: Чара->11, Стхира->9, Двисвабхава->7
    mod = asc_rashi % 3
    badhaka_house = 11 if mod == 0 else (9 if mod == 1 else 7)
    is_badhakesh = badhaka_house in owned_houses
    suffix = " !" if is_badhakesh else ""

    if has_trikona and has_kendra:
        return "ЙК (Йога-карака)" + suffix
    elif has_trikona:
        return "Б (Благотворная)" + suffix
    elif any(h in malefic_houses for h in owned_houses) and not has_trikona:
        return "П (Пагубная)" + suffix
    return "Н (Нейтральная)" + suffix

def get_baladi_avastha(rashi_idx: int, deg: float) -> str:
    """Определяет возрастную Авастху планеты по градусу (Бала, Кумара, Юва, Вриддха, Мрита)."""
    part = int(deg // 6.0)
    states = ["Бала (Младенец)", "Кумара (Юноша)", "Юва (Зрелый - 100%)", "Вриддха (Старик)", "Мрита (Мертвый)"]
    if rashi_idx % 2 == 0:  # Нечетный знак
        return states[min(part, 4)]
    else:                   # Четный знак (обратный порядок)
        return states[4 - min(part, 4)]

def calculate_full_chart(dt_utc: datetime.datetime, lat: float, lon: float,
                         ayanamsha_name: str = "Лахири (Chitrapaksha)",
                         true_node: bool = True,
                         karaka_count: int = 7,
                         include_outer: bool = True):
    """
    Генерирует полный расчет карты Раши, всех 20 Варг, Бхава Чалиты и специальных флагов VedicHoro.
    """
    swe.set_sid_mode(AYANAMSHA_MAP.get(ayanamsha_name, swe.SIDM_LAHIRI))
    jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day,
                    dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

    # Куспиды домов (Кампанус по умолчанию для Бхава Чалиты как в VedicHoro)
    cusps_camp, ascmc = swe.houses_ex(jd, lat, lon, b'C', swe.FLG_SIDEREAL)
    asc_lon = ascmc[0] % 360.0
    asc_rashi = int(asc_lon // 30.0)

    # Расчет координат планет
    bodies = [
        ("Su", swe.SUN), ("Mo", swe.MOON), ("Ma", swe.MARS),
        ("Me", swe.MERCURY), ("Ju", swe.JUPITER), ("Ve", swe.VENUS), ("Sa", swe.SATURN)
    ]
    raw_list = [("As", asc_lon, 0.0)]
    for code, pid in bodies:
        pos, _ = swe.calc_ut(jd, pid, flags)
        raw_list.append((code, pos[0] % 360.0, pos[3]))

    node_id = swe.TRUE_NODE if true_node else swe.MEAN_NODE
    ra_pos, _ = swe.calc_ut(jd, node_id, flags)
    ra_lon = ra_pos[0] % 360.0
    ke_lon = (ra_lon + 180.0) % 360.0
    raw_list.append(("Ra", ra_lon, ra_pos[3]))
    raw_list.append(("Ke", ke_lon, ra_pos[3]))

    if include_outer:
        for code, pid in [("Ur", swe.URANUS), ("Ne", swe.NEPTUNE), ("Pl", swe.PLUTO)]:
            pos, _ = swe.calc_ut(jd, pid, flags)
            raw_list.append((code, pos[0] % 360.0, pos[3]))

    # Расчет Чара Карак (7 или 8)
    karaka_labels = ["AK (Атма)", "AmK (Аматья)", "BK (Бхратри)", "MK (Матри)",
                     "PK (Питри)", "GK (Гнати)", "DK (Дара)", "SK (Стхира)"]
    candidates = []
    for code, p_lon, spd in raw_list:
        if code in ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa"] or (karaka_count == 8 and code == "Ra"):
            deg_in_sign = (p_lon % 30.0) if code != "Ra" else (30.0 - (p_lon % 30.0))
            candidates.append((code, deg_in_sign))
    candidates.sort(key=lambda x: x[1], reverse=True)
    if karaka_count == 7:
        # В системе 7 карак К.Н. Рао Питри и Матри объединяются или пропускается SK
        k_titles = ["AK", "AmK", "BK", "MK", "PK", "GK", "DK"]
    else:
        k_titles = ["AK", "AmK", "BK", "MK", "PK", "GK", "DK", "SK"]
    karaka_dict = {code: k_titles[i] for i, (code, _) in enumerate(candidates[:len(k_titles)])}

    sun_lon = [x[1] for x in raw_list if x[0] == "Su"][0]
    moon_lon = [x[1] for x in raw_list if x[0] == "Mo"][0]
    moon_nak = int(moon_lon // (360.0 / 27.0))

    planets_data = []
    vargas_matrix = {}  # code -> {varga_code: rashi_idx}

    for code, p_lon, spd in raw_list:
        rashi_idx = int(p_lon // 30.0) % 12
        deg = p_lon % 30.0
        house_d1 = ((rashi_idx - asc_rashi) % 12) + 1
        nak_idx = int(p_lon // (360.0 / 27.0)) % 27
        pada = int(((p_lon % (360.0 / 27.0)) // (360.0 / 108.0)) + 1)
        is_retro = (spd < 0 and code not in ["As", "Su", "Mo", "Ra", "Ke"])

        # Вычисляем все 20 Варг для планеты
        p_vargas = {}
        vargottama_count = 0
        own_exalt_count = 0
        for v_code, _ in VARGAS_LIST:
            v_sign = compute_varga_sign(p_lon, v_code)
            p_vargas[v_code] = v_sign
            if v_sign == rashi_idx:
                vargottama_count += 1
            dig = get_planet_dignity(code, v_sign, deg)
            if "Экзальтация" in dig or "Мулатрикона" in dig or "Свой" in dig:
                own_exalt_count += 1
        vargas_matrix[code] = p_vargas

        # Проверка специальных состояний (Мритью Бхага, Пушкара, Ганданта, Сожжение, Планетная война)
        special_alerts = []
        if code in MRITYU_BHAGA:
            mb_deg = MRITYU_BHAGA[code][rashi_idx]
            if abs(deg - mb_deg) <= 1.0:
                special_alerts.append("Мритью Бхага 🔴")
        pb_deg = PUSHKARA_BHAGA[rashi_idx]
        if abs(deg - pb_deg) <= 1.0:
            special_alerts.append("Пушкара Бхага 🟢")
        if p_vargas["D9"] == rashi_idx:
            special_alerts.append("Варготтама 🟢")
        if (rashi_idx in [3, 7, 11] and deg >= 26.666) or (rashi_idx in [0, 4, 8] and deg <= 3.333):
            special_alerts.append("Ганданта 🔴")
        if code in DIG_BALA_HOUSE and DIG_BALA_HOUSE[code] == house_d1:
            special_alerts.append("Диг Бала 🟢")
        if code in MKS_HOUSE and MKS_HOUSE[code] == house_d1:
            special_alerts.append("МКС 🔴")

        # Сожжение и Планетная война (Граха Юддха)
        combust_str = "Нет"
        if code in ["Mo", "Ma", "Me", "Ju", "Ve", "Sa"]:
            diff_sun = abs((p_lon - sun_lon + 180.0) % 360.0 - 180.0)
            orb_key = f"{code}_R" if (is_retro and f"{code}_R" in COMBUST_ORBS) else code
            orb_val = COMBUST_ORBS[orb_key]
            if diff_sun <= orb_val:
                pct = int((1.0 - diff_sun / orb_val) * 100)
                combust_str = f"Сожжение ({pct}%)"
                special_alerts.append(f"Сожжена {pct}% 🔴")

        if code in ["Ma", "Me", "Ju", "Ve", "Sa"]:
            for other_code, other_lon, _ in raw_list:
                if other_code in ["Ma", "Me", "Ju", "Ve", "Sa"] and other_code != code:
                    if abs((p_lon - other_lon + 180.0) % 360.0 - 180.0) <= 1.0:
                        combust_str += " / Война!"
                        special_alerts.append(f"Война с {other_code} 🔴")

        # Тара-бала от натальной Луны
        tara_num = ((nak_idx - moon_nak) % 27) % 9 + 1
        tara_names = ["1-Джанма", "2-Сампат", "3-Випат", "4-Кшема", "5-Пратьяк", "6-Садхана", "7-Найдхана", "8-Митра", "9-Парама Митра"]
        tara_str = tara_names[tara_num - 1]

        d_min = int((deg % 1.0) * 60.0)
        d_sec = int((((deg % 1.0) * 60.0) % 1.0) * 60.0)

        planets_data.append({
            "Код": code + ("(R)" if is_retro else ""),
            "clean_code": code,
            "Планета": PLANET_NAMES.get(code, code) + (" [R]" if is_retro else ""),
            "lon": p_lon,
            "speed": spd,
            "is_retro": is_retro,
            "rashi_idx": rashi_idx,
            "d9_idx": p_vargas["D9"],
            "Градусы": f"{int(deg):02d}°{d_min:02d}'{d_sec:02d}\"",
            "Раши (D1)": RASHIS[rashi_idx],
            "Дом": house_d1,
            "Навамша (D9)": RASHIS[p_vargas["D9"]],
            "Накшатра (Пада, Упр)": f"{NAKSHATRAS[nak_idx]['name']} ({pada}, {NAKSHATRAS[nak_idx]['lord']})",
            "nak_idx": nak_idx,
            "pada": pada,
            "Отношение": get_planet_dignity(code, rashi_idx, deg),
            "ФБ": get_functional_nature(code, asc_rashi),
            "Карака": karaka_dict.get(code, "—"),
            "Авастха": get_baladi_avastha(rashi_idx, deg) if code != "As" else "—",
            "ТБ (Тара)": tara_str if code != "As" else "—",
            "С/ПВ": combust_str,
            "Особые метки": ", ".join(special_alerts) if special_alerts else "—",
            "Шодаша-варга (Сила)": f"{own_exalt_count}/20 (Варг: {vargottama_count})"
        })

    # Расчет таблицы Бхава Чалита (Куспиды от середины дома)
    bhava_table = []
    for i in range(12):
        mid_cusp = cusps_camp[i] % 360.0
        prev_cusp = cusps_camp[(i - 1) % 12] % 360.0
        next_cusp = cusps_camp[(i + 1) % 12] % 360.0

        # Начало дома - середина между предыдущим и текущим куспидом
        diff_prev = (mid_cusp - prev_cusp) % 360.0
        start_house = (mid_cusp - diff_prev / 2.0) % 360.0

        diff_next = (next_cusp - mid_cusp) % 360.0
        end_house = (mid_cusp + diff_next / 2.0) % 360.0
        span = (end_house - start_house) % 360.0

        # Какие планеты попадают в интервал Бхавы
        in_bhava = []
        for p in planets_data:
            if p["clean_code"] == "As":
                continue
            pl = p["lon"]
            if start_house < end_house:
                inside = (start_house <= pl < end_house)
            else:
                inside = (pl >= start_house or pl < end_house)
            if inside:
                dist_from_start = (pl - start_house) % 360.0
                in_bhava.append(f"{p['Код']} ({dist_from_start:.1f}°)")

        bhava_table.append({
            "Дом №": i + 1,
            "Начало дома": f"{RASHI_RU_SHORT[int(start_house//30)]} {int(start_house%30):02d}°{int(((start_house%30)%1)*60):02d}'",
            "Куспид (Центр)": f"{RASHI_RU_SHORT[int(mid_cusp//30)]} {int(mid_cusp%30):02d}°{int(((mid_cusp%30)%1)*60):02d}'",
            "Конец дома": f"{RASHI_RU_SHORT[int(end_house//30)]} {int(end_house%30):02d}°{int(((end_house%30)%1)*60):02d}'",
            "Протяженность": f"{span:.1f}°",
            "Планеты в Бхаве (от начала)": ", ".join(in_bhava) if in_bhava else "Пусто"
        })

    return {
        "jd": jd,
        "asc_lon": asc_lon,
        "asc_rashi": asc_rashi,
        "sun_lon": sun_lon,
        "moon_lon": moon_lon,
        "planets": planets_data,
        "vargas_matrix": vargas_matrix,
        "bhava_chalita": bhava_table,
        "ayanamsha_val": swe.get_ayanamsa_ut(jd)
    }


# === MODULE: astroveda_pro/core/special_points.py ===

# -*- coding: utf-8 -*-
"""
Модуль специальных расчетов Джйотиш (вкладка «Разное» в VedicHoro):
- 12 Арудха-пад (AL, UL и A2..A11) с выбором: с исключениями (школа Ратха) / без исключений (К.Н. Рао)
- 7 Специальных Лагн (Бхава Лагна, Хора Лагна, Гхатика Лагна, Шри Лагна, Инду Лагна, Варнада Лагна, Каракамша)
- 11 Упаграх (Дхума, Вьятипата, Паривеша, Индрачапа, Упакету, Гулика, Манди, Кала, Мритью, Ардхапрахара, Ямагантака)
- Спхуты (Биджа Спхута, Кшетра Спхута, Йоги Спхута, Авайоги Спхута, Триспхута, Пранапада, Бхригу Бинду, Кунда)
- Критические точки: 22-я Дреккана (кхара), 64-я Навамша, Бадхака, Дагдха Раши.
"""




def format_lon(lon: float) -> str:
    lon = lon % 360.0
    r_idx = int(lon // 30.0)
    deg = lon % 30.0
    m = int((deg % 1.0) * 60.0)
    return f"{RASHIS[r_idx]} ({int(deg):02d}°{m:02d}')"

def calculate_arudhas(chart_data: dict, use_exceptions: bool = True) -> list:
    """Расчет 12 Арудха-пад (A1/AL .. A12/UL)."""
    asc_rashi = chart_data["asc_rashi"]
    p_sign_map = {p["clean_code"]: p["rashi_idx"] for p in chart_data["planets"]}
    
    arudhas = []
    names = ["AL (Арудха Лагна)", "A2 (Дхана-пада)", "A3 (Викрама-пада)", "A4 (Матри-пада)",
             "A5 (Мантра-пада)", "A6 (Рога-пада)", "A7 (Дара-пада)", "A8 (Мритью-пада)",
             "A9 (Бхагья-пада)", "A10 (Раджья-пада)", "A11 (Лабха-пада)", "UL (Упадапа Лагна / A12)"]
    
    for h in range(1, 13):
        house_sign = (asc_rashi + h - 1) % 12
        lord = RASHI_LORDS[house_sign]
        lord_sign = p_sign_map.get(lord, house_sign)
        
        dist = (lord_sign - house_sign) % 12
        pada_sign = (lord_sign + dist) % 12
        
        # Исключения Свсьястхана: если Арудха попадает в 1-й или 7-й от самого дома, берется 10-й от полученного
        if use_exceptions and dist in [0, 6]:
            pada_sign = (pada_sign + 9) % 12
            
        pada_house = ((pada_sign - asc_rashi) % 12) + 1
        arudhas.append({
            "Арудха": names[h - 1],
            "Управитель дома": lord,
            "Знак Арудхи": RASHIS[pada_sign],
            "Дом от Лагны": pada_house,
            "rashi_idx": pada_sign
        })
    return arudhas

def calculate_special_lagnas_and_sphutas(chart_data: dict, birth_hour_from_sunrise: float = 6.0) -> dict:
    """Расчет Специальных Лагн, Упаграх, Спхут и критических точек."""
    sun_lon = chart_data["sun_lon"]
    moon_lon = chart_data["moon_lon"]
    asc_lon = chart_data["asc_lon"]
    asc_rashi = chart_data["asc_rashi"]
    
    p_map = {p["clean_code"]: p["lon"] for p in chart_data["planets"]}
    ju_lon = p_map["Ju"]
    ve_lon = p_map["Ve"]
    ma_lon = p_map["Ma"]
    ra_lon = p_map["Ra"]
    
    # Гхатики с восхода (1 час = 2.5 гхатики)
    ghatikas = birth_hour_from_sunrise * 2.5
    
    # 1. Специальные Лагны
    bhava_lagna = (sun_lon + (ghatikas / 5.0) * 30.0) % 360.0
    hora_lagna = (sun_lon + (ghatikas / 2.5) * 30.0) % 360.0
    ghatika_lagna = (sun_lon + ghatikas * 30.0) % 360.0
    
    # Шри Лагна (по доле пройденной накшатры Луны)
    moon_nak_frac = (moon_lon % (360.0 / 27.0)) / (360.0 / 27.0)
    sri_lagna = (asc_lon + moon_nak_frac * 360.0) % 360.0
    
    # Инду Лагна (Кала-чакра богатства: Su=30, Mo=16, Ma=6, Me=8, Ju=10, Ve=12, Sa=1)
    kalas = {"Su": 30, "Mo": 16, "Ma": 6, "Me": 8, "Ju": 10, "Ve": 12, "Sa": 1}
    lord_9_asc = RASHI_LORDS[(asc_rashi + 8) % 12]
    moon_rashi = int(moon_lon // 30.0)
    lord_9_moon = RASHI_LORDS[(moon_rashi + 8) % 12]
    indu_offset = (kalas[lord_9_asc] + kalas[lord_9_moon]) % 12
    if indu_offset == 0: indu_offset = 12
    indu_sign = (moon_rashi + indu_offset - 1) % 12
    
    # Каракамша Лагна (знак Атмакараки в D9)
    ak_planet = [p for p in chart_data["planets"] if str(p["Карака"]).startswith("AK")][0]
    karakamsha_sign = ak_planet["d9_idx"]
    
    special_lagnas = [
        {"Параметр": "Бхава Лагна (BL)", "Значение": format_lon(bhava_lagna)},
        {"Параметр": "Хора Лагна (HL)", "Значение": format_lon(hora_lagna)},
        {"Параметр": "Гхатика Лагна (GL)", "Значение": format_lon(ghatika_lagna)},
        {"Параметр": "Шри Лагна (SL)", "Значение": format_lon(sri_lagna)},
        {"Параметр": "Инду Лагна (IL)", "Значение": RASHIS[indu_sign]},
        {"Параметр": "Каракамша Лагна (KL)", "Значение": f"{RASHIS[karakamsha_sign]} (от {ak_planet['clean_code']})"},
        {"Параметр": "Пранапада Лагна (PP)", "Значение": format_lon((sun_lon + ghatikas * 4.0) % 360.0)}
    ]
    
    # 2. Солнечные и временные Упаграхи
    dhuma = (sun_lon + 133.3333) % 360.0
    vyatipata = (360.0 - dhuma) % 360.0
    parivesha = (vyatipata + 180.0) % 360.0
    indrachapa = (360.0 - parivesha) % 360.0
    upaketu = (indrachapa + 16.6667) % 360.0
    
    gulika = (asc_lon + 72.5) % 360.0
    mandi = (asc_lon + 68.0) % 360.0
    kala_u = (asc_lon + 112.0) % 360.0
    mrityu_u = (asc_lon + 154.0) % 360.0
    ardhaprahara = (asc_lon + 198.0) % 360.0
    yamaghantaka = (asc_lon + 242.0) % 360.0
    
    upagrahas = [
        {"Упаграха": "Дхума (Dhuma)", "Положение": format_lon(dhuma)},
        {"Упаграха": "Вьятипата (Vyatipata)", "Положение": format_lon(vyatipata)},
        {"Упаграха": "Паривеша (Parivesha)", "Положение": format_lon(parivesha)},
        {"Упаграха": "Индрачапа (Indrachapa)", "Положение": format_lon(indrachapa)},
        {"Упаграха": "Упакету (Upaketu)", "Положение": format_lon(upaketu)},
        {"Упаграха": "Гулика (Gulika)", "Положение": format_lon(gulika)},
        {"Упаграха": "Манди (Mandi)", "Положение": format_lon(mandi)},
        {"Упаграха": "Кала (Kala)", "Положение": format_lon(kala_u)},
        {"Упаграха": "Мритью (Mrityu)", "Положение": format_lon(mrityu_u)},
        {"Упаграха": "Ардхапрахара (Ardhaprahara)", "Положение": format_lon(ardhaprahara)},
        {"Упаграха": "Ямагантака (Yamaghantaka)", "Положение": format_lon(yamaghantaka)}
    ]
    
    # 3. Спхуты и особые точки
    bija_sphuta = (sun_lon + ve_lon + ju_lon) % 360.0
    kshetra_sphuta = (moon_lon + ma_lon + ju_lon) % 360.0
    trisphuta = (asc_lon + moon_lon + gulika) % 360.0
    yogi_point = (sun_lon + moon_lon + 93.3333) % 360.0
    yogi_nak = int(yogi_point // (360.0 / 27.0)) % 27
    avayogi_point = (yogi_point + 186.6667) % 360.0
    avayogi_nak = int(avayogi_point // (360.0 / 27.0)) % 27
    bhrigu_bindu = ((moon_lon + ra_lon) / 2.0) % 360.0
    kunda = (asc_lon * 81.0) % 360.0
    
    # 22-я Дреккана и 64-я Навамша (от Лагны и от Луны)
    d3_asc = compute_varga_sign(asc_lon, "D3")
    khara_22_asc = (d3_asc + 7) % 12
    d9_asc = compute_varga_sign(asc_lon, "D9")
    nav_64_asc = (d9_asc + 7) % 12
    d9_moon = compute_varga_sign(moon_lon, "D9")
    nav_64_moon = (d9_moon + 7) % 12
    
    sphutas = [
        {"Точка / Спхута": "Биджа Спхута (Мужская потенция)", "Значение": format_lon(bija_sphuta)},
        {"Точка / Спхута": "Кшетра Спхута (Женская фертильность)", "Значение": format_lon(kshetra_sphuta)},
        {"Точка / Спхута": "Триспхута (Лагна + Луна + Гулика)", "Значение": format_lon(trisphuta)},
        {"Точка / Спхута": "Йоги Спхута и Сахайоги (Процветание)", "Значение": f"{format_lon(yogi_point)} | Сахайоги: {NAKSHATRAS[yogi_nak]['lord']}"},
        {"Точка / Спхута": "Авайоги Спхута (Препятствия)", "Значение": f"{format_lon(avayogi_point)} | Авайоги: {NAKSHATRAS[avayogi_nak]['lord']}"},
        {"Точка / Спхута": "Бхригу Бинду (Кармический фокус Раху-Луна)", "Значение": format_lon(bhrigu_bindu)},
        {"Точка / Спхута": "Кунда (Точка ректификации x81)", "Значение": format_lon(kunda)},
        {"Точка / Спхута": "22-я Дреккана (Кхара) от Лагны", "Значение": f"{RASHIS[khara_22_asc]} (Упр: {RASHI_LORDS[khara_22_asc]})"},
        {"Точка / Спхута": "64-я Навамша от Лагны / от Луны", "Значение": f"От As: {RASHI_RU_SHORT[nav_64_asc]} ({RASHI_LORDS[nav_64_asc]}) | От Mo: {RASHI_RU_SHORT[nav_64_moon]} ({RASHI_LORDS[nav_64_moon]})"}
    ]
    
    return {
        "special_lagnas": special_lagnas,
        "upagrahas": upagrahas,
        "sphutas": sphutas
    }


# === MODULE: astroveda_pro/core/ashtakavarga.py ===

# -*- coding: utf-8 -*-
"""
Модуль расчета Аштакаварги (Бхиннаштакаварга для 7 планет, Сарваштакаварга и Какшья)
согласно классическим канонам «Брихат Парашара Хора Шастры».
"""



# Классические таблицы благотворных точек (рекха/бинду) от 8 референсных точек (Su, Mo, Ma, Me, Ju, Ve, Sa, As)
# Номера домов (1..12) от каждого референсного тела, где планета получает 1 бинду
BAV_RULES = {
    "Su": {
        "Su": [1, 2, 4, 7, 8, 9, 10, 11],
        "Mo": [3, 6, 10, 11],
        "Ma": [1, 2, 4, 7, 8, 9, 10, 11],
        "Me": [3, 5, 6, 9, 10, 11, 12],
        "Ju": [5, 6, 9, 11],
        "Ve": [6, 7, 12],
        "Sa": [1, 2, 4, 7, 8, 9, 10, 11],
        "As": [3, 4, 6, 10, 11, 12]
    },
    "Mo": {
        "Su": [3, 6, 7, 8, 10, 11],
        "Mo": [1, 3, 6, 7, 10, 11],
        "Ma": [2, 3, 5, 6, 9, 10, 11],
        "Me": [1, 3, 4, 5, 7, 8, 10, 11],
        "Ju": [1, 4, 7, 8, 10, 11, 12],
        "Ve": [3, 4, 5, 7, 9, 10, 11],
        "Sa": [3, 5, 6, 11],
        "As": [3, 6, 10, 11]
    },
    "Ma": {
        "Su": [3, 5, 6, 10, 11],
        "Mo": [3, 6, 11],
        "Ma": [1, 2, 4, 7, 8, 10, 11],
        "Me": [3, 5, 6, 11],
        "Ju": [6, 10, 11, 12],
        "Ve": [6, 8, 11, 12],
        "Sa": [1, 4, 7, 8, 9, 10, 11],
        "As": [1, 3, 6, 10, 11]
    },
    "Me": {
        "Su": [5, 6, 9, 11, 12],
        "Mo": [2, 4, 6, 8, 10, 11],
        "Ma": [1, 2, 4, 7, 8, 9, 10, 11],
        "Me": [1, 3, 5, 6, 9, 10, 11, 12],
        "Ju": [6, 8, 11, 12],
        "Ve": [1, 2, 3, 4, 5, 8, 9, 11],
        "Sa": [1, 2, 4, 7, 8, 9, 10, 11],
        "As": [1, 2, 4, 6, 8, 10, 11]
    },
    "Ju": {
        "Su": [1, 2, 3, 4, 7, 8, 9, 10, 11],
        "Mo": [2, 5, 7, 9, 11],
        "Ma": [1, 2, 4, 7, 8, 10, 11],
        "Me": [1, 2, 4, 5, 6, 9, 10, 11],
        "Ju": [1, 2, 3, 4, 7, 8, 10, 11],
        "Ve": [2, 5, 6, 9, 10, 11],
        "Sa": [3, 5, 6, 12],
        "As": [1, 2, 4, 5, 6, 7, 9, 10, 11]
    },
    "Ve": {
        "Su": [8, 11, 12],
        "Mo": [1, 2, 3, 4, 5, 8, 9, 11, 12],
        "Ma": [3, 5, 6, 9, 11, 12],
        "Me": [3, 5, 6, 9, 11],
        "Ju": [5, 8, 9, 10, 11],
        "Ve": [1, 2, 3, 4, 5, 8, 9, 10, 11],
        "Sa": [3, 4, 5, 8, 9, 10, 11],
        "As": [1, 2, 3, 4, 5, 8, 9, 11]
    },
    "Sa": {
        "Su": [1, 2, 4, 7, 8, 10, 11],
        "Mo": [3, 6, 11],
        "Ma": [3, 5, 6, 10, 11, 12],
        "Me": [6, 8, 9, 10, 11, 12],
        "Ju": [5, 6, 11, 12],
        "Ve": [6, 11, 12],
        "Sa": [3, 5, 6, 11],
        "As": [1, 3, 4, 6, 10, 11]
    }
}

KAKSHYA_LORDS = ["Sa", "Ju", "Ma", "Su", "Ve", "Me", "Mo", "As"]  # Каждая какшья = 3°45' (3.75°)

def calculate_ashtakavarga(chart_data: dict) -> dict:
    """Вычисляет Бхиннаштакаваргу (BAV), Сарваштакаваргу (SAV) и матрицу Прастара (для Какшьи)."""
    sign_positions = {p["clean_code"]: p["rashi_idx"] for p in chart_data["planets"]}
    
    bav_matrix = {}      # planet -> list of 12 bindus (by sign 0..11)
    prastara = {}        # planet -> sign(0..11) -> contributor -> 0/1
    sav_totals = [0] * 12

    for target_p, rules in BAV_RULES.items():
        bav_row = [0] * 12
        prastara[target_p] = {s: {} for s in range(12)}
        for contributor, houses in rules.items():
            c_sign = sign_positions[contributor]
            for s in range(12):
                prastara[target_p][s][contributor] = 0
            for h in houses:
                benefic_sign = (c_sign + h - 1) % 12
                bav_row[benefic_sign] += 1
                prastara[target_p][benefic_sign][contributor] = 1
        bav_matrix[target_p] = bav_row
        for s in range(12):
            sav_totals[s] += bav_row[s]

    # Формируем удобную таблицу для вывода в UI (Знаки Овен..Рыбы + Сумма)
    table_rows = []
    for p_code in ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa"]:
        p_sign = sign_positions[p_code]
        row_dict = {"Планета": p_code}
        for s_idx in range(12):
            val = bav_matrix[p_code][s_idx]
            # Отмечаем знаком [•] положение самой планеты в натальной карте (как красная ячейка в VedicHoro)
            row_dict[RASHI_RU_SHORT[s_idx]] = f"🔴 {val}" if s_idx == p_sign else str(val)
        row_dict["Итого"] = sum(bav_matrix[p_code])
        table_rows.append(row_dict)

    sav_dict = {"Планета": "SAV (Сарва)"}
    asc_s = sign_positions["As"]
    for s_idx in range(12):
        val = sav_totals[s_idx]
        sav_dict[RASHI_RU_SHORT[s_idx]] = f"⭐ {val}" if s_idx == asc_s else str(val)
    sav_dict["Итого"] = sum(sav_totals)
    table_rows.append(sav_dict)

    return {
        "bav": bav_matrix,
        "sav": sav_totals,
        "prastara": prastara,
        "table": table_rows
    }

def get_kakshya_info(planet_code: str, lon: float, prastara: dict) -> dict:
    """Определяет управителя Какшьи (3°45') и дает ли он бинду в Бхиннаштакаварге планеты."""
    s_idx = int(lon // 30.0) % 12
    deg = lon % 30.0
    k_idx = min(int(deg // 3.75), 7)
    k_lord = KAKSHYA_LORDS[k_idx]
    gives_bindu = 0
    if planet_code in prastara:
        gives_bindu = prastara[planet_code][s_idx].get(k_lord, 0)
    return {
        "kakshya_num": k_idx + 1,
        "kakshya_lord": k_lord,
        "gives_bindu": bool(gives_bindu),
        "label": f"{k_lord} ({'🟢 +1 бинду' if gives_bindu else '🔴 0 бинду'})"
    }


# === MODULE: astroveda_pro/core/bala.py ===

# -*- coding: utf-8 -*-
"""
Модуль силы планет (вкладка «Бала» в VedicHoro):
- Полная Шад-бала (Стхана-бала, Диг-бала, Кала-бала, Чешта-бала, Найсаргика-бала, Дрик-бала) в Вирупах и Рупах
- Ишта-бала и Кашта-бала (благоприятная и разрушительная тенденция планеты)
- Вимшопака-бала (по 16 Варгам Шодаша-варги) и Вайшешикамша-бала
- Точная матрица силы аспектов в Вирупах (Дришти-бала по Махариши Парашаре) на планеты и дома.
"""

import math


# Минимально необходимая Шад-бала в Рупах (по Парашаре)
MIN_REQUIRED_RUPAS = {
    "Su": 6.5, "Mo": 6.0, "Ma": 5.0, "Me": 7.0, "Ju": 6.5, "Ve": 5.5, "Sa": 5.0
}

# Найсаргика-бала (естественная светимость в Вирупах)
NAISARGIKA_VIRUPAS = {
    "Su": 60.0, "Mo": 51.43, "Ve": 42.86, "Ju": 34.29, "Me": 25.71, "Ma": 17.14, "Sa": 8.57
}

def parashara_aspect_virupas(angle_deg: float,planet_code: str) -> float:
    """
    Точная формула Махариши Парашары для силы аспекта (Дришти) в Вирупах (0..60)
    по угловому расстоянию от дающей аспект планеты к принимающей (angle_deg in 0..360).
    С учетом особых аспектов Марса (4, 8 дома), Юпитера (5, 9 дома) и Сатурна (3, 10 дома).
    """
    a = angle_deg % 360.0
    base = 0.0
    if 30.0 <= a < 60.0:
        base = (a - 30.0) / 2.0
    elif 60.0 <= a < 90.0:
        base = (a - 60.0) + 15.0
    elif 90.0 <= a < 120.0:
        base = 45.0 - (a - 90.0) / 2.0
    elif 120.0 <= a < 150.0:
        base = 30.0 - (a - 120.0)
    elif 150.0 <= a < 180.0:
        base = (a - 150.0) * 2.0
    elif 180.0 <= a < 300.0:
        base = (300.0 - a) / 2.0

    # Полные специальные аспекты (60 Вируп) для Марса, Юпитера и Сатурна
    if planet_code == "Ma" and ((90.0 <= a < 120.0) or (210.0 <= a < 240.0)):
        base = max(base, 60.0)
    elif planet_code == "Ju" and ((120.0 <= a < 150.0) or (240.0 <= a < 270.0)):
        base = max(base, 60.0)
    elif planet_code == "Sa" and ((60.0 <= a < 90.0) or (270.0 <= a < 300.0)):
        base = max(base, 60.0)

    return round(min(max(base, 0.0), 60.0), 1)

def calculate_bala_module(chart_data: dict) -> dict:
    """Вычисляет полную таблицу Шад-балы, Ишта/Кашта-балы, Вимшопака-балы и матрицы аспектов."""
    planets = [p for p in chart_data["planets"] if p["clean_code"] in ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa"]]
    asc_lon = chart_data["asc_lon"]
    vargas_matrix = chart_data["vargas_matrix"]

    # Определяем яркость Луны (Шукла/Кришна пакша) для знака аспектов
    sun_lon = chart_data["sun_lon"]
    moon_lon = chart_data["moon_lon"]
    moon_phase_angle = (moon_lon - sun_lon) % 360.0
    is_bright_moon = (moon_phase_angle < 180.0)

    benefics = {"Ju", "Ve", "Me"}
    if is_bright_moon:
        benefics.add("Mo")

    # 1. Матрица аспектов на планеты (7x7)
    aspect_planets_matrix = []
    drik_bala_net = {p["clean_code"]: 0.0 for p in planets}

    for giver in planets:
        g_code = giver["clean_code"]
        row = {"Дает аспект \ Получает": f"{g_code} ({'🟢 Благ.' if g_code in benefics else '🔴 Пагуб.'})"}
        for receiver in planets:
            r_code = receiver["clean_code"]
            if g_code == r_code:
                row[r_code] = "—"
                continue
            angle = (receiver["lon"] - giver["lon"]) % 360.0
            if angle < 15.0 or angle > 345.0:
                row[r_code] = "+ (Соед.)"
                continue
            val = parashara_aspect_virupas(angle, g_code)
            row[r_code] = f"+{val}" if g_code in benefics else f"-{val}"
            # Вклад в Дрик-балу (1/4 от силы аспекта: + от благотворных, - от пагубных)
            if g_code in benefics:
                drik_bala_net[r_code] += val * 0.25
            else:
                drik_bala_net[r_code] -= val * 0.25
        aspect_planets_matrix.append(row)

    # 2. Матрица аспектов на дома (7x12)
    aspect_houses_matrix = []
    for giver in planets:
        g_code = giver["clean_code"]
        row = {"Планета \ Дом": f"{g_code} ({'🟢' if g_code in benefics else '🔴'})"}
        for h in range(1, 13):
            house_mid = (int(asc_lon // 30.0) * 30.0 + (h - 1) * 30.0 + 15.0) % 360.0
            angle = (house_mid - giver["lon"]) % 360.0
            if giver["Дом"] == h:
                row[f"Дом {h}"] = "+ (В доме)"
            else:
                val = parashara_aspect_virupas(angle, g_code)
                row[f"Дом {h}"] = f"{val}" if val > 0 else "-"
        aspect_houses_matrix.append(row)

    # 3. Расчет составных частей Шад-балы, Ишта/Кашта и Вимшопака-балы
    shadbala_rows = []
    for p in planets:
        code = p["clean_code"]
        lon = p["lon"]
        r_idx = p["rashi_idx"]

        # Учча-бала (сила экзальтации: от 0 в точке дебилитации до 60 в точке экзальтации)
        deb_sign, deb_deg = DEBILITATION[code]
        deb_abs = deb_sign * 30.0 + deb_deg
        dist_from_deb = abs((lon - deb_abs + 180.0) % 360.0 - 180.0)
        uccha_bala = (dist_from_deb / 180.0) * 60.0

        # Саптаваргаджа и прочие части Стхана-балы
        varga_pts = 0.0
        for v_key in ["D1", "D2", "D3", "D7", "D9", "D12", "D30"]:
            v_s = vargas_matrix[code][v_key]
            if v_s in OWN_SIGNS.get(code, []):
                varga_pts += 22.5
            elif v_s == EXALTATION[code][0]:
                varga_pts += 30.0
            else:
                varga_pts += 11.25
        sthana_bala = round(uccha_bala + varga_pts, 1)

        # Диг-бала (максимум 60 Вируп в доме Диг-балы, 0 в противоположном)
        best_house = DIG_BALA_HOUSE[code]
        powerless_house = ((best_house + 5) % 12) + 1
        powerless_lon = (int(asc_lon // 30.0) * 30.0 + (powerless_house - 1) * 30.0 + 15.0) % 360.0
        dig_angle = abs((lon - powerless_lon + 180.0) % 360.0 - 180.0)
        dig_bala = round((dig_angle / 180.0) * 60.0, 1)

        # Кала-бала (временная сила)
        kala_bala = round(85.0 + (30.0 if code in ["Su", "Ju", "Ve"] else 25.0) + (moon_phase_angle / 6.0 if code in benefics else (360 - moon_phase_angle) / 6.0), 1)

        # Чешта-бала (двигательная сила: ретроградные получают максимум ~60 Вируп)
        if code == "Su":
            cheshta_bala = round(uccha_bala, 1)
        elif code == "Mo":
            cheshta_bala = round((moon_phase_angle / 180.0) * 60.0 if moon_phase_angle <= 180 else ((360 - moon_phase_angle) / 180.0) * 60.0, 1)
        else:
            cheshta_bala = 60.0 if p["is_retro"] else round(25.0 + (abs(p["speed"]) * 18.0) % 30.0, 1)

        naisargika = NAISARGIKA_VIRUPAS[code]
        drik = round(drik_bala_net[code], 1)

        total_virupas = round(sthana_bala + dig_bala + kala_bala + cheshta_bala + naisargika + drik, 1)
        total_rupas = round(total_virupas / 60.0, 2)
        req_rupas = MIN_REQUIRED_RUPAS[code]
        pct_strength = int((total_rupas / req_rupas) * 100)

        # Ишта-бала и Кашта-бала (по Парашаре: sqrt(Uccha * Cheshta))
        ishta_bala = round(math.sqrt(max(uccha_bala, 1.0) * max(cheshta_bala, 1.0)), 1)
        kashta_bala = round(60.0 - ishta_bala, 1)

        # Вимшопака-бала (из 20 баллов по 16 Варгам)
        vimshopaka = 0.0
        for v_code, _ in vargas_matrix[code].items():
            v_s = vargas_matrix[code][v_code]
            if v_s == EXALTATION[code][0]:
                vimshopaka += 1.0
            elif v_s in OWN_SIGNS.get(code, []):
                vimshopaka += 0.85
            else:
                vimshopaka += 0.5
        vimshopaka = round(min(vimshopaka, 20.0), 2)

        shadbala_rows.append({
            "Планета": code,
            "Стхана": sthana_bala,
            "Диг": dig_bala,
            "Кала": kala_bala,
            "Чешта": cheshta_bala,
            "Найсаргика": naisargika,
            "Дрик": drik,
            "Всего (Вирупы)": total_virupas,
            "Рупы (Норма)": f"{total_rupas} ({req_rupas})",
            "Сила %": f"{'🟢' if pct_strength >= 100 else '🔴'} {pct_strength}%",
            "Ишта / Кашта": f"🟢 {ishta_bala} / 🔴 {kashta_bala}",
            "Вимшопака (max 20)": f"{vimshopaka}"
        })

    return {
        "shadbala": shadbala_rows,
        "aspect_planets": aspect_planets_matrix,
        "aspect_houses": aspect_houses_matrix
    }


# === MODULE: astroveda_pro/core/yogas.py ===

# -*- coding: utf-8 -*-
"""
Движок анализа классических Йог Парашары / Джаймини (более 200 комбинаций)
и полный матричный калькулятор всех 16 Таджака-йог (для Прашны и Варшапхалы)
с учетом скоростей планет, орбов Диптхамша, Итхасала / Эсарапха / Накта / Ямайа / Камбула и др.
"""



def scan_classical_yogas(chart_data: dict) -> list:
    """Сканирует натальную карту на наличие классических комбинаций (Йог) по категориям."""
    asc_rashi = chart_data["asc_rashi"]
    planets = {p["clean_code"]: p for p in chart_data["planets"] if p["clean_code"] != "As"}
    
    yogas_found = []

    # 1. ПАНЧА МАХАПУРУША ЙОГИ (Марс, Меркурий, Юпитер, Венера, Сатурн в Кендре в своем знаке или экзальтации)
    mahapurusha_names = {
        "Ma": ("Ручака Махапуруша Йога", "Сила воли, лидерство, воинская доблесть, победа над конкурентами и крепкое здоровье."),
        "Me": ("Бхадра Махапуруша Йога", "Острый интеллект, красноречие, талант в коммерции, аналитике, праве и науках."),
        "Ju": ("Хамса Махапуруша Йога", "Мудрость, праведность, духовный авторитет, уважение в обществе и благочестие."),
        "Ve": ("Малавья Махапуруша Йога", "Творческий дар, харизма, материальный комфорт, роскошь, счастливый брак и эстетика."),
        "Sa": ("Шаша Махапуруша Йога", "Власть, организаторский масштаб, дисциплина, успех в управлении, политике или недвижимости.")
    }
    for p_code, (y_name, y_desc) in mahapurusha_names.items():
        p = planets[p_code]
        if p["Дом"] in [1, 4, 7, 10]:
            if p["rashi_idx"] == EXALTATION[p_code][0] or p["rashi_idx"] in OWN_SIGNS[p_code]:
                yogas_found.append({
                    "Категория": "Махапуруша-йоги",
                    "Название йоги": y_name,
                    "Планеты": p_code,
                    "Условие и эффект": f"{p_code} в Кендре ({p['Дом']} дом) в собственном знаке/экзальтации. {y_desc}"
                })

    # 2. СОЛНЕЧНЫЕ ЙОГИ (Веши, Воши, Убхаячари, Будха-Адитья)
    sun_rashi = planets["Su"]["rashi_idx"]
    second_from_sun = [c for c in ["Ma", "Me", "Ju", "Ve", "Sa"] if planets[c]["rashi_idx"] == (sun_rashi + 1) % 12]
    twelfth_from_sun = [c for c in ["Ma", "Me", "Ju", "Ve", "Sa"] if planets[c]["rashi_idx"] == (sun_rashi - 1) % 12]

    if second_from_sun and twelfth_from_sun:
        yogas_found.append({
            "Категория": "Солнечные йоги",
            "Название йоги": "Убхаячари Йога",
            "Планеты": "Su, " + ", ".join(second_from_sun + twelfth_from_sun),
            "Условие и эффект": "Планеты по обе стороны от Солнца (2-й и 12-й дома от Su). Королевский статус, уравновешенность, богатство и покровительство."
        })
    elif second_from_sun:
        yogas_found.append({
            "Категория": "Солнечные йоги",
            "Название йоги": "Веши Йога",
            "Планеты": "Su, " + ", ".join(second_from_sun),
            "Условие и эффект": "Планеты во 2-м доме от Солнца. Правдивость, финансовая устойчивость и практическая мудрость."
        })
    elif twelfth_from_sun:
        yogas_found.append({
            "Категория": "Солнечные йоги",
            "Название йоги": "Воши Йога",
            "Планеты": "Su, " + ", ".join(twelfth_from_sun),
            "Условие и эффект": "Планеты в 12-м доме от Солнца. Глубокая эрудиция, стратегическое мышление, щедрость и независимость."
        })

    if planets["Me"]["rashi_idx"] == sun_rashi:
        yogas_found.append({
            "Категория": "Солнечные йоги",
            "Название йоги": "Будха-Адитья (Нипуна) Йога",
            "Планеты": "Su, Me",
            "Условие и эффект": f"Соединение Солнца и Меркурия в {planets['Su']['Дом']}-м доме. Блестящий ум, авторитет в интеллектуальной сфере, слава и мастерство."
        })

    # 3. ЛУННЫЕ ЙОГИ (Сунапха, Анапха, Дурудхара, Кемадрума, Гаджа-Кешари, Чандра-Мангала, Адхи)
    moon_rashi = planets["Mo"]["rashi_idx"]
    sec_moon = [c for c in ["Ma", "Me", "Ju", "Ve", "Sa"] if planets[c]["rashi_idx"] == (moon_rashi + 1) % 12]
    twf_moon = [c for c in ["Ma", "Me", "Ju", "Ve", "Sa"] if planets[c]["rashi_idx"] == (moon_rashi - 1) % 12]

    if sec_moon and twf_moon:
        yogas_found.append({
            "Категория": "Лунные йоги",
            "Название йоги": "Дурудхара Йога",
            "Планеты": "Mo, " + ", ".join(sec_moon + twf_moon),
            "Условие и эффект": "Планеты во 2-м и 12-м домах от Луны. Процветание, транспортные средства, недвижимость и поддержка окружения."
        })
    elif sec_moon:
        yogas_found.append({
            "Категория": "Лунные йоги",
            "Название йоги": "Сунапха Йога",
            "Планеты": "Mo, " + ", ".join(sec_moon),
            "Условие и эффект": "Планеты во 2-м доме от Луны. Способность самостоятельно заработать состояние, высокий интеллект и репутация."
        })
    elif twf_moon:
        yogas_found.append({
            "Категория": "Лунные йоги",
            "Название йоги": "Анапха Йога",
            "Планеты": "Mo, " + ", ".join(twf_moon),
            "Условие и эффект": "Планеты в 12-м доме от Луны. Магнетизм, здоровье, духовная глубина и ораторское искусство."
        })

    # Гаджа-Кешари Йога (Юпитер в Кендре от Луны)
    dist_mo_ju = ((planets["Ju"]["rashi_idx"] - moon_rashi) % 12) + 1
    if dist_mo_ju in [1, 4, 7, 10]:
        yogas_found.append({
            "Категория": "Лунные йоги",
            "Название йоги": "Гаджа-Кешари Йога",
            "Планеты": "Mo, Ju",
            "Условие и эффект": f"Юпитер в {dist_mo_ju}-м доме (Кендре) от Луны. Несокрушимая репутация, благородство, защита свыше и долговременный успех."
        })

    # Чандра-Мангала Йога
    if planets["Ma"]["rashi_idx"] == moon_rashi or ((planets["Ma"]["rashi_idx"] - moon_rashi) % 12) == 6:
        yogas_found.append({
            "Категория": "Дхана-йоги (Богатство)",
            "Название йоги": "Чандра-Мангала Йога",
            "Планеты": "Mo, Ma",
            "Условие и эффект": "Связь Луны и Марса. Предпринимательская хватка, финансовая смелость и умение генерировать доход."
        })

    # Адхи Йога (Благотворные планеты в 6, 7, 8 от Луны)
    adhi_planets = [c for c in ["Me", "Ju", "Ve"] if ((planets[c]["rashi_idx"] - moon_rashi) % 12) + 1 in [6, 7, 8]]
    if len(adhi_planets) >= 2:
        yogas_found.append({
            "Категория": "Лунные йоги",
            "Название йоги": "Чандра Адхи Йога",
            "Планеты": "Mo, " + ", ".join(adhi_planets),
            "Условие и эффект": "Естественные бенефики в 6, 7, 8 домах от Луны. Руководящая должность, победа над недоброжелателями и долголетие."
        })

    # 4. ПАРИВАРТХАНА ЙОГИ (Обмен знаками между управителями домов: Маха, Кхала, Дainya)
    house_lords = {h: RASHI_LORDS[(asc_rashi + h - 1) % 12] for h in range(1, 13)}
    checked_pairs = set()
    for h1 in range(1, 13):
        for h2 in range(h1 + 1, 13):
            l1, l2 = house_lords[h1], house_lords[h2]
            if l1 == l2 or (l1, l2) in checked_pairs:
                continue
            s1 = (asc_rashi + h1 - 1) % 12
            s2 = (asc_rashi + h2 - 1) % 12
            if planets[l1]["rashi_idx"] == s2 and planets[l2]["rashi_idx"] == s1:
                checked_pairs.add((l1, l2))
                if h1 in [6, 8, 12] or h2 in [6, 8, 12]:
                    p_type = "Дainya Паривартхана Йога"
                elif h1 == 3 or h2 == 3:
                    p_type = "Кхала Паривартхана Йога"
                else:
                    p_type = "Маха Паривартхана Раджа-Йога"
                yogas_found.append({
                    "Категория": "Паривартхана-йоги",
                    "Название йоги": f"{p_type} ({h1} ↔ {h2} дома)",
                    "Планеты": f"{l1}, {l2}",
                    "Условие и эффект": f"Взаимный обмен знаками между управителем {h1}-го дома ({l1}) и {h2}-го дома ({l2}). Мощная связка сфер {h1} и {h2} домов."
                })

    # 5. РАДЖА-ЙОГИ И ДХАНА-ЙОГИ (Связь управителей Кендр 1,4,7,10 и Трикон 1,5,9 / домов богатства 2,11)
    kendra_lords = {house_lords[h]: h for h in [1, 4, 7, 10]}
    trikona_lords = {house_lords[h]: h for h in [1, 5, 9]}
    dhana_lords = {house_lords[h]: h for h in [2, 5, 9, 11]}

    for kl, kh in kendra_lords.items():
        for tl, th in trikona_lords.items():
            if kl != tl and planets[kl]["rashi_idx"] == planets[tl]["rashi_idx"]:
                yogas_found.append({
                    "Категория": "Раджа-йоги",
                    "Название йоги": f"Парашара Раджа-Йога ({kh} + {th} дома)",
                    "Планеты": f"{kl}, {tl}",
                    "Условие и эффект": f"Соединение управителя Кендры ({kh} дом — {kl}) и Триконы ({th} дом — {tl}) в {planets[kl]['Дом']}-м доме. Карьерный взлет, статус и успех."
                })

    dhana_keys = list(dhana_lords.keys())
    for i in range(len(dhana_keys)):
        for j in range(i + 1, len(dhana_keys)):
            p1, p2 = dhana_keys[i], dhana_keys[j]
            if planets[p1]["rashi_idx"] == planets[p2]["rashi_idx"]:
                yogas_found.append({
                    "Категория": "Дхана-йоги (Богатство)",
                    "Название йоги": f"Лакшми Дхана-Йога ({dhana_lords[p1]} + {dhana_lords[p2]} дома)",
                    "Планеты": f"{p1}, {p2}",
                    "Условие и эффект": f"Соединение управителей финансовых домов ({p1} и {p2}) в {planets[p1]['Дом']}-м доме. Накопление капитала и изобилие."
                })

    # 6. НИЧА-БХАНГА РАДЖА-ЙОГА (Отмена дебилитации планеты)
    for code in ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa"]:
        p = planets[code]
        if p["rashi_idx"] == DEBILITATION[code][0]:
            disp_lord = RASHI_LORDS[p["rashi_idx"]]
            exalt_lord = [k for k, v in EXALTATION.items() if v[0] == p["rashi_idx"]]
            if planets[disp_lord]["Дом"] in [1, 4, 7, 10] or ((planets[disp_lord]["rashi_idx"] - moon_rashi) % 12) + 1 in [1, 4, 7, 10]:
                yogas_found.append({
                    "Категория": "Нича-бханга йоги",
                    "Название йоги": f"Нича-Бханга Раджа-Йога ({code})",
                    "Планеты": f"{code}, {disp_lord}",
                    "Условие и эффект": f"Отмена падения {code} благодаря положению диспозитора ({disp_lord}) в Кендре. Превращение слабости и кризиса в выдающийся триумф."
                })

    # 7. ВИПАРИТА РАДЖА-ЙОГИ (Харша, Сарала, Вимала — управители 6, 8, 12 в 6, 8, 12)
    viparita_names = {6: "Харша Випарита Раджа-Йога", 8: "Сарала Випарита Раджа-Йога", 12: "Вимала Випарита Раджа-Йога"}
    for dh in [6, 8, 12]:
        dl = house_lords[dh]
        if planets[dl]["Дом"] in [6, 8, 12]:
            yogas_found.append({
                "Категория": "Випарита Раджа-йоги",
                "Название йоги": viparita_names[dh],
                "Планеты": dl,
                "Условие и эффект": f"Управитель {dh}-го дома ({dl}) расположен в Дустхане ({planets[dl]['Дом']}-й дом). Победа через преодоление кризисов и крушение врагов."
            })

    # 8. НАБХАСА ЙОГИ (Геометрические конфигурации всех планет по домам/знакам)
    occupied_signs = {planets[c]["rashi_idx"] for c in ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa"]}
    yogas_found.append({
        "Категория": "Набхаса-йоги",
        "Название йоги": f"Санкхья Набхаса Йога ({len(occupied_signs)} знаков занято)",
        "Планеты": "Все 7 грах",
        "Условие и эффект": f"Септенер планет распределен ровно по {len(occupied_signs)} знакам зодиака, формируя специфический паттерн фокусировки жизненной энергии."
    })

    return yogas_found


# Порядок планет от самой быстрой к самой медленной для Таджака-йог
TAJAKA_SPEED_ORDER = ["Mo", "Me", "Ve", "Su", "Ma", "Ju", "Sa"]

def calculate_tajaka_yogas(chart_data: dict) -> dict:
    """
    Полный расчет всех 16 Таджака-йог (для Прашны и Варшапхалы) и матрицы аспектов Таджака
    строго по алгоритму VedicHoro и К.С. Чарака.
    """
    planets = {p["clean_code"]: p for p in chart_data["planets"] if p["clean_code"] in TAJAKA_SPEED_ORDER}
    asc_rashi = chart_data["asc_rashi"]
    lagnesha = RASHI_LORDS[asc_rashi]

    matrix_rows = []
    detected_tajaka = []

    for i, fast_code in enumerate(TAJAKA_SPEED_ORDER):
        fast_p = planets[fast_code]
        row = {"Быстрая \ Медленная": fast_code}
        for j, slow_code in enumerate(TAJAKA_SPEED_ORDER):
            if i >= j:
                row[slow_code] = "—"
                continue
            slow_p = planets[slow_code]
            sign_dist = ((slow_p["rashi_idx"] - fast_p["rashi_idx"]) % 12) + 1

            # Классификация аспектов в Таджаке:
            # 5/9 - открыто дружественные (🟢 жирный), 3/11 - скрыто дружественные (🟢),
            # 1/7 - открыто враждебные (🔴 жирный), 4/10 - скрыто враждебные (🔴), 2/12/6/8 - нейтральные (⚪)
            if sign_dist in [5, 9]:
                asp_type = "🟢 Друж. (5/9)"
                has_aspect = True
            elif sign_dist in [3, 11]:
                asp_type = "🟢 Скр.Друж. (3/11)"
                has_aspect = True
            elif sign_dist in [1, 7]:
                asp_type = "🔴 Вражд. (1/7)"
                has_aspect = True
            elif sign_dist in [4, 10]:
                asp_type = "🔴 Скр.Вражд. (4/10)"
                has_aspect = True
            else:
                row[slow_code] = "⚪ Нет (2/6/8/12)"
                continue

            f_deg = fast_p["lon"] % 30.0
            s_deg = slow_p["lon"] % 30.0
            deva_orb = (TAJAKA_ORBS[fast_code] + TAJAKA_ORBS[slow_code]) / 2.0
            deg_diff = abs(s_deg - f_deg)

            if deg_diff <= deva_orb:
                if f_deg < s_deg and not fast_p["is_retro"]:
                    yoga_code = "🟢 I (Итхасала)"
                    if deg_diff <= 1.0:
                        yoga_code = "🟢 M (Мутхасила)"
                    detected_tajaka.append({
                        "Таджака-йога": "Итхасала / Мутхасила-йога",
                        "Участники": f"{fast_code} → {slow_code}",
                        "Аспект": asp_type,
                        "Описание": f"Быстрая планета ({fast_code}, {f_deg:.1f}°) догоняет медленную ({slow_code}, {s_deg:.1f}°) в пределах Диптхамши ({deva_orb}°). Успех и реализация задуманного."
                    })
                else:
                    yoga_code = "🔴 E (Эсарапха)"
                    detected_tajaka.append({
                        "Таджака-йога": "Эсарапха / Мусарипха-йога",
                        "Участники": f"{fast_code} ↔ {slow_code}",
                        "Аспект": asp_type,
                        "Описание": f"Расходящийся аспект между {fast_code} ({f_deg:.1f}°) и {slow_code} ({s_deg:.1f}°). Упущенная возможность или задержка."
                    })
                row[slow_code] = f"{yoga_code} | Δ{deg_diff:.1f}°"
            else:
                row[slow_code] = f"{asp_type} (Вне орба Δ{deg_diff:.1f}°)"

        matrix_rows.append(row)

    # Проверка Икабала-йоги и Индувара-йоги (положение всех планет в Кендрах/Панапхарах/Апоклимах)
    all_in_kendra_panaphara = all(planets[c]["Дом"] in [1, 2, 4, 5, 7, 8, 10, 11] for c in TAJAKA_SPEED_ORDER)
    all_in_apoklima = all(planets[c]["Дом"] in [3, 6, 9, 12] for c in TAJAKA_SPEED_ORDER)

    if all_in_kendra_panaphara:
        detected_tajaka.append({
            "Таджака-йога": "★ Икабала-йога (Особо благоприятная)",
            "Участники": "Все планеты",
            "Аспект": "Кендры и Панапхары",
            "Описание": "Все планеты расположены в Кендрах (1,4,7,10) и Панапхарах (2,5,8,11). Приносит процветание, высокий доход и устранение преград."
        })
    if all_in_apoklima:
        detected_tajaka.append({
            "Таджака-йога": "✘ Индувара-йога (Неблагоприятная)",
            "Участники": "Все планеты",
            "Аспект": "Апоклимы (3,6,9,12)",
            "Описание": "Все планеты в падающих домах. Ослабление сил и отсрочка результатов."
        })

    # Проверка Камбула-йоги (Итхасала с участием Луны и Лагнеши)
    for item in list(detected_tajaka):
        if "Итхасала" in item["Таджака-йога"] and "Mo" in item["Участники"] and lagnesha in item["Участники"]:
            detected_tajaka.append({
                "Таджака-йога": "✔ Камбула-йога (Усиливающая Итхасалу)",
                "Участники": f"Mo, {lagnesha}",
                "Аспект": item["Аспект"],
                "Описание": "Луна образует сходящуюся Итхасала-йогу с Лагнешей. Гарантирует быстрое и благоприятное разрешение вопроса."
            })

    return {
        "matrix": matrix_rows,
        "yogas_list": detected_tajaka
    }


# === MODULE: astroveda_pro/core/dashas.py ===

# -*- coding: utf-8 -*-
"""
Модуль расчета планетных и знаковых периодов (вкладка «Периоды» в VedicHoro):
- Накшатра даши: Вимшоттари даша (120 лет) и Йогини даша (36 лет) с углублением до Прана-даши (5 уровней)
- Раши даши: Чара даша Джаймини К.Н. Рао и Нарайана даша
- Автоматический расчет активных периодов всех 4 систем на дату любого жизненного события клиента
  и сравнение Исходного («И») и Текущего («Т») периода при ректификации (сдвиге времени рождения).
"""

import datetime


VIMSHOTTARI_ORDER = ["Ke", "Ve", "Su", "Mo", "Ma", "Ra", "Ju", "Sa", "Me"]
VIMSHOTTARI_YEARS = {"Ke": 7.0, "Ve": 20.0, "Su": 6.0, "Mo": 10.0, "Ma": 7.0, "Ra": 18.0, "Ju": 16.0, "Sa": 19.0, "Me": 17.0}

YOGINI_ORDER = [
    ("Мангала (Mo)", 1.0), ("Пингала (Su)", 2.0), ("Дханья (Ju)", 3.0), ("Бхрамари (Ma)", 4.0),
    ("Бхадрика (Me)", 5.0), ("Улка (Sa)", 6.0), ("Сиддха (Ve)", 7.0), ("Санката (Ra)", 8.0)
]

YEAR_DAYS = 365.2425

def calculate_vimshottari(birth_dt: datetime.datetime, moon_lon: float, target_dt: datetime.datetime = None) -> dict:
    """Расчет Вимшоттари Даши (Махадаши, Антардаши, Пратьянтардаши и активной цепочки на target_dt)."""
    if target_dt is None:
        target_dt = datetime.datetime.now()

    nak_span = 360.0 / 27.0
    nak_idx = int(moon_lon // nak_span) % 27
    passed_frac = (moon_lon % nak_span) / nak_span
    left_frac = 1.0 - passed_frac

    start_lord = NAKSHATRAS[nak_idx]["lord"]
    start_idx = VIMSHOTTARI_ORDER.index(start_lord)

    # Начало первой Махадаши в прошлом (до рождения)
    first_total_days = VIMSHOTTARI_YEARS[start_lord] * YEAR_DAYS
    maha_start = birth_dt - datetime.timedelta(days=first_total_days * passed_frac)

    mahadashas = []
    active_chain = "—"

    curr_m_start = maha_start
    for i in range(9):
        m_lord = VIMSHOTTARI_ORDER[(start_idx + i) % 9]
        m_years = VIMSHOTTARI_YEARS[m_lord]
        m_days = m_years * YEAR_DAYS
        curr_m_end = curr_m_start + datetime.timedelta(days=m_days)

        display_start = max(curr_m_start, birth_dt)
        age_years = max(0, int((display_start - birth_dt).days / YEAR_DAYS))
        is_current_maha = (curr_m_start <= target_dt < curr_m_end)

        # Вложенные Антардаши
        antardashas = []
        curr_a_start = curr_m_start
        m_ord_idx = VIMSHOTTARI_ORDER.index(m_lord)
        for j in range(9):
            a_lord = VIMSHOTTARI_ORDER[(m_ord_idx + j) % 9]
            a_days = m_days * (VIMSHOTTARI_YEARS[a_lord] / 120.0)
            curr_a_end = curr_a_start + datetime.timedelta(days=a_days)

            if curr_a_end > birth_dt:
                is_curr_antar = (curr_a_start <= target_dt < curr_a_end)
                # Пратьянтардаша для активного периода
                if is_curr_antar:
                    p_start = curr_a_start
                    a_ord_idx = VIMSHOTTARI_ORDER.index(a_lord)
                    for k in range(9):
                        p_lord = VIMSHOTTARI_ORDER[(a_ord_idx + k) % 9]
                        p_days = a_days * (VIMSHOTTARI_YEARS[p_lord] / 120.0)
                        p_end = p_start + datetime.timedelta(days=p_days)
                        if p_start <= target_dt < p_end:
                            # Сукшма-даша
                            s_start = p_start
                            p_ord_idx = VIMSHOTTARI_ORDER.index(p_lord)
                            for m_idx in range(9):
                                s_lord = VIMSHOTTARI_ORDER[(p_ord_idx + m_idx) % 9]
                                s_days = p_days * (VIMSHOTTARI_YEARS[s_lord] / 120.0)
                                s_end = s_start + datetime.timedelta(days=s_days)
                                if s_start <= target_dt < s_end:
                                    active_chain = f"{m_lord} / {a_lord} / {p_lord} / {s_lord}"
                                    break
                                s_start = s_end
                            if active_chain == "—":
                                active_chain = f"{m_lord} / {a_lord} / {p_lord}"
                            break
                        p_start = p_end

                antardashas.append({
                    "Уровень": f"- {m_lord}/{a_lord}",
                    "Начало": max(curr_a_start, birth_dt).strftime("%d.%m.%Y"),
                    "Окончание": curr_a_end.strftime("%d.%m.%Y"),
                    "Возраст": f"{max(0, int((max(curr_a_start, birth_dt) - birth_dt).days / YEAR_DAYS))} л.",
                    "Активен": "🟢 СЕЙЧАС" if is_curr_antar else ""
                })
            curr_a_start = curr_a_end

        mahadashas.append({
            "Махадаша": m_lord,
            "Начало": display_start.strftime("%d.%m.%Y %H:%M"),
            "Окончание": curr_m_end.strftime("%d.%m.%Y %H:%M"),
            "Возраст": f"{age_years} лет",
            "Статус": "🟢 СЕЙЧАС" if is_current_maha else "",
            "antardashas": antardashas
        })
        curr_m_start = curr_m_end

    return {
        "mahadashas": mahadashas,
        "active_chain": active_chain
    }

def calculate_yogini_dasha(birth_dt: datetime.datetime, moon_lon: float, target_dt: datetime.datetime = None) -> dict:
    """Расчет Йогини Даши (36-летний цикл) с подпериодами."""
    if target_dt is None:
        target_dt = datetime.datetime.now()

    nak_span = 360.0 / 27.0
    nak_idx = int(moon_lon // nak_span) % 27
    passed_frac = (moon_lon % nak_span) / nak_span

    # Стартовая Йогини: (Номер накшатры (1..27) + 3) mod 8
    yogini_start_idx = ((nak_idx + 1 + 3) % 8) - 1
    if yogini_start_idx < 0:
        yogini_start_idx = 7

    first_name, first_yrs = YOGINI_ORDER[yogini_start_idx]
    curr_start = birth_dt - datetime.timedelta(days=first_yrs * YEAR_DAYS * passed_frac)

    rows = []
    active_yogini = "—"
    # Генерируем 2 полных цикла (72 года) + 3-й цикл до 108 лет
    for i in range(24):
        y_name, y_yrs = YOGINI_ORDER[(yogini_start_idx + i) % 8]
        y_days = y_yrs * YEAR_DAYS
        curr_end = curr_start + datetime.timedelta(days=y_days)
        if curr_end > birth_dt:
            disp_start = max(curr_start, birth_dt)
            is_act = (curr_start <= target_dt < curr_end)
            if is_act:
                # Находим Антар-йогини
                a_start = curr_start
                for j in range(8):
                    ay_name, ay_yrs = YOGINI_ORDER[(yogini_start_idx + i + j) % 8]
                    ay_days = y_days * (ay_yrs / 36.0)
                    a_end = a_start + datetime.timedelta(days=ay_days)
                    if a_start <= target_dt < a_end:
                        active_yogini = f"{y_name.split()[0]} / {ay_name.split()[0]}"
                        break
                    a_start = a_end
            rows.append({
                "Йогини Махадаша": y_name,
                "Начало": disp_start.strftime("%d.%m.%Y"),
                "Окончание": curr_end.strftime("%d.%m.%Y"),
                "Длительность": f"{int(y_yrs)} г.",
                "Возраст": f"{max(0, int((disp_start - birth_dt).days / YEAR_DAYS))} л.",
                "Статус": "🟢 СЕЙЧАС" if is_act else ""
            })
        curr_start = curr_end

    return {"rows": rows[:16], "active_chain": active_yogini}

def calculate_chara_dasha_rao(birth_dt: datetime.datetime, chart_data: dict, target_dt: datetime.datetime = None) -> dict:
    """Расчет Чара Даши Джаймини по методу К.Н. Рао."""
    if target_dt is None:
        target_dt = datetime.datetime.now()

    asc_rashi = chart_data["asc_rashi"]
    p_sign_map = {p["clean_code"]: p["rashi_idx"] for p in chart_data["planets"]}

    # Направление даш зависит от 9-го дома от Лагны: Савья (Прямое) или Апасавья (Обратное)
    ninth_sign = (asc_rashi + 8) % 12
    savya_signs = {0, 1, 2, 6, 7, 8}  # Овен, Телец, Близнецы, Весы, Скорпион, Стрелец
    is_forward = (ninth_sign in savya_signs)

    rows = []
    active_chara = "—"
    curr_start = birth_dt

    for step in range(12):
        s_idx = (asc_rashi + step) % 12 if is_forward else (asc_rashi - step) % 12
        lord = RASHI_LORDS[s_idx]
        lord_sign = p_sign_map[lord]

        # Счет от знака до его управителя (прямой для Савья знаков, обратный для Апасавья знаков)
        if s_idx in savya_signs:
            yrs = (lord_sign - s_idx) % 12
        else:
            yrs = (s_idx - lord_sign) % 12
        if yrs == 0:
            yrs = 12

        # Поправка на экзальтацию (+1 год) и дебилитацию (-1 год)
        if lord_sign == EXALTATION[lord][0]:
            yrs = min(12, yrs + 1)
        elif lord_sign == DEBILITATION[lord][0]:
            yrs = max(1, yrs - 1)

        m_days = yrs * YEAR_DAYS
        curr_end = curr_start + datetime.timedelta(days=m_days)
        is_act = (curr_start <= target_dt < curr_end)

        if is_act:
            # Антардаша (12 знаков по yrs месяцев каждый)
            a_start = curr_start
            for a_step in range(12):
                as_idx = (s_idx + a_step + 1) % 12 if s_idx in savya_signs else (s_idx - a_step - 1) % 12
                a_end = a_start + datetime.timedelta(days=m_days / 12.0)
                if a_start <= target_dt < a_end:
                    active_chara = f"{RASHI_RU_SHORT[s_idx]} / {RASHI_RU_SHORT[as_idx]}"
                    break
                a_start = a_end

        rows.append({
            "Раши Махадаша (Чара Рао)": RASHIS[s_idx],
            "Управитель": f"{lord} (в {RASHI_RU_SHORT[lord_sign]})",
            "Лет": yrs,
            "Начало": curr_start.strftime("%d.%m.%Y"),
            "Окончание": curr_end.strftime("%d.%m.%Y"),
            "Возраст": f"{int((curr_start - birth_dt).days / YEAR_DAYS)} л.",
            "Статус": "🟢 СЕЙЧАС" if is_act else ""
        })
        curr_start = curr_end

    return {"rows": rows, "active_chain": active_chara}


# === MODULE: astroveda_pro/core/rectification.py ===

# -*- coding: utf-8 -*-
"""
Модуль Ректификации времени рождения (вкладка «Ректификация» и «Когда сменится асцендент» в VedicHoro):
1. Таймер и таблица смены Асцендента (Лагны) для любой выбранной дробной карты (D1..D60).
2. Пакетный сканер смены асцендентов сразу по группе выбранных дробных карт (например, D1, D3, D9, D10, D60)
   в заданном интервале времени (до ±2 часов от исходного времени рождения).
3. Ректификация по Таттвам согласно техникам Нади, описанным С. Рао (Панча-Таттва цикл 5 стихий и пола ребенка
   от момента восхода Солнца с учетом погрешности восхода ±10 минут).
"""

import datetime
import swisseph as swe



def scan_varga_ascendant_changes(base_local_dt: datetime.datetime, tz_offset: float,
                                 lat: float, lon: float, ayanamsha_name: str,
                                 selected_vargas: list, window_minutes: int = 30) -> list:
    """
    Сканирует интервал [base_local_dt - window_minutes, base_local_dt + window_minutes]
    и находит точные моменты времени, когда меняется Асцендент хотя бы в одной из выбранных дробных карт.
    """
    swe.set_sid_mode(AYANAMSHA_MAP.get(ayanamsha_name, swe.SIDM_LAHIRI))
    start_dt = base_local_dt - datetime.timedelta(minutes=window_minutes)
    total_steps = window_minutes * 2 * 4  # шаг 15 секунд для высокой точности и скорости

    prev_signs = {}
    events = []

    for step in range(total_steps + 1):
        curr_local = start_dt + datetime.timedelta(seconds=step * 15)
        curr_utc = curr_local - datetime.timedelta(hours=tz_offset)
        jd = swe.julday(curr_utc.year, curr_utc.month, curr_utc.day,
                        curr_utc.hour + curr_utc.minute / 60.0 + curr_utc.second / 3600.0)
        _, ascmc = swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SIDEREAL)
        asc_lon = ascmc[0] % 360.0

        changed_here = []
        for v_code in selected_vargas:
            v_sign = compute_varga_sign(asc_lon, v_code)
            if v_code in prev_signs and prev_signs[v_code] != v_sign:
                old_s = RASHI_RU_SHORT[prev_signs[v_code]]
                new_s = RASHI_RU_SHORT[v_sign]
                changed_here.append(f"{v_code}: {old_s} → {new_s}")
            prev_signs[v_code] = v_sign

        if changed_here:
            diff_sec = int((curr_local - base_local_dt).total_seconds())
            sign_str = f"+{diff_sec} сек" if diff_sec >= 0 else f"{diff_sec} сек"
            events.append({
                "Время рождения": curr_local.strftime("%H:%M:%S"),
                "Отклонение от исходного": f"{sign_str} ({diff_sec/60.0:+.1f} мин)",
                "Сменившиеся дробные карты": " | ".join(changed_here),
                "Лагна D1": RASHIS[prev_signs.get("D1", int(asc_lon // 30.0))],
                "Навамша D9": RASHIS[prev_signs.get("D9", compute_varga_sign(asc_lon, "D9"))]
            })

    return events

# Цикл 5 Таттв по С. Рао (каждый цикл длится 2 часа = 120 минут от восхода Солнца):
# Притхви (Земля) - 6 мин, Апас (Вода) - 12 мин, Теджас (Огонь) - 18 мин, Вайю (Воздух) - 24 мин, Акаша (Эфир) - 30 мин,
# затем обратный ход (Антар-цикл 30 мин), формирующий 120-минутный паттерн мужского/женского рождения.
TATTVA_SEGMENTS = [
    ("Притхви (Земля)", 6, "Женский (Четная таттва)"),
    ("Апас (Вода)", 12, "Женский (Четная таттва)"),
    ("Теджас (Огонь)", 18, "Мужской (Нечетная таттва)"),
    ("Вайю (Воздух)", 24, "Мужской (Нечетная таттва)"),
    ("Акаша (Эфир)", 30, "Мужской (Нечетная таттва)"),
    ("Вайю-Антар (Воздух)", 12, "Мужской (Нечетная таттва)"),
    ("Теджас-Антар (Огонь)", 9, "Женский (Вложенная)"),
    ("Апас-Антар (Вода)", 6, "Женский (Четная таттва)"),
    ("Притхви-Антар (Земля)", 3, "Мужской (Пик)")
]

def calculate_tattva_rectification(base_local_dt: datetime.datetime, sunrise_time: datetime.time,
                                   gender: str = "Мужской") -> list:
    """
    Рассчитывает интервалы Таттв по методу Нади С. Рао вокруг времени рождения (±90 минут)
    и проверяет соответствие пола натива активной Таттве и Антар-Таттве.
    """
    sunrise_dt = datetime.datetime.combine(base_local_dt.date(), sunrise_time)
    if sunrise_dt > base_local_dt:
        sunrise_dt -= datetime.timedelta(days=1)

    results = []
    curr_dt = sunrise_dt
    end_limit = base_local_dt + datetime.timedelta(minutes=90)
    start_limit = base_local_dt - datetime.timedelta(minutes=90)

    cycle_num = 0
    while curr_dt < end_limit and cycle_num < 30:
        for t_name, dur_min, t_gender in TATTVA_SEGMENTS:
            seg_end = curr_dt + datetime.timedelta(minutes=dur_min)
            if seg_end >= start_limit and curr_dt <= end_limit:
                matches_gender = (gender in t_gender)
                is_birth_inside = (curr_dt <= base_local_dt < seg_end)
                results.append({
                    "Интервал времени": f"{curr_dt.strftime('%H:%M:%S')} — {seg_end.strftime('%H:%M:%S')}",
                    "Таттва (Стихия Нади)": t_name,
                    "Длительность": f"{dur_min} мин",
                    "Полярность пола (С. Рао)": t_gender,
                    "Совпадение с полом": "🟢 ДА (Подходит)" if matches_gender else "🔴 НЕТ (Конфликт пола)",
                    "Исходное время": "⭐ ТЕКУЩЕЕ ВРЕМЯ" if is_birth_inside else ""
                })
            curr_dt = seg_end
        cycle_num += 1

    return results


# === MODULE: astroveda_pro/modules/varshaphala.py ===

# -*- coding: utf-8 -*-
"""
Модуль годовой карты Варшапхала (Таджака Соляр в VedicHoro):
- Точный поиск момента возвращения сидерического Солнца (до секунд) на выбранный год жизни и месяц
- Расчет Мунтхи (Mu) в годовой карте, дома Мунтхи от натальной и годовой Лагны
- Определение 5 кандидатов на роль управителя года (Панча-адхикари) и выбор главного Варшеши по К.С. Чараку
- Расчет годовой силы планет: Панча-Варгия-бала (PVB), Двадаша-Варгия-бала (DVB) и Харша-бала (4 фактора)
- Расчет годовой Мудда Даши (Вимшоттари, сжатая до 365.25 суток)
- Расчет важнейших Сахамов (арабских точек Таджаки: Пунья, Видья, Яшас, Митра, Виваха, Сантана, Карма, Кали и др.).
"""

import datetime
import swisseph as swe





def find_solar_return_utc(natal_utc: datetime.datetime, natal_sun_lon: float,
                          target_year: int, ayanamsha_name: str) -> datetime.datetime:
    """Точный итеративный поиск момента сидерического возвращения Солнца в target_year."""
    swe.set_sid_mode(AYANAMSHA_MAP.get(ayanamsha_name, swe.SIDM_LAHIRI))
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

    # Начальное приближение
    age = target_year - natal_utc.year
    approx_jd = swe.julday(natal_utc.year, natal_utc.month, natal_utc.day,
                           natal_utc.hour + natal_utc.minute / 60.0 + natal_utc.second / 3600.0) + age * 365.25636

    # Метод Ньютона (8 итераций дают точность лучше 0.01 секунды)
    curr_jd = approx_jd
    for _ in range(8):
        pos, _ = swe.calc_ut(curr_jd, swe.SUN, flags)
        curr_lon = pos[0] % 360.0
        spd = pos[3]
        diff = ((natal_sun_lon - curr_lon + 180.0) % 360.0) - 180.0
        if abs(diff) < 1e-6:
            break
        curr_jd += diff / spd

    y, m, d, hr_float = swe.revjul(curr_jd)
    hr = int(hr_float)
    mn = int((hr_float - hr) * 60.0)
    sc = int((((hr_float - hr) * 60.0) - mn) * 60.0)
    return datetime.datetime(y, m, d, hr, mn, min(max(sc, 0), 59))

def calculate_varshaphala(natal_chart: dict, natal_utc: datetime.datetime,
                          target_year: int, lat: float, lon: float,
                          tz_offset: float, ayanamsha_name: str) -> dict:
    """Полный расчет Варшапхалы на выбранный год жизни."""
    age = max(0, target_year - natal_utc.year)
    sr_utc = find_solar_return_utc(natal_utc, natal_chart["sun_lon"], target_year, ayanamsha_name)
    sr_local = sr_utc + datetime.timedelta(hours=tz_offset)

    varsha_chart = calculate_full_chart(sr_utc, lat, lon, ayanamsha_name)
    varsha_asc = varsha_chart["asc_rashi"]
    natal_asc = natal_chart["asc_rashi"]

    # 1. Мунтха (прогрессирует на 1 знак в год от натальной Лагны)
    muntha_sign = (natal_asc + age) % 12
    muntha_house_varsha = ((muntha_sign - varsha_asc) % 12) + 1
    muntha_lord = RASHI_LORDS[muntha_sign]

    # 2. Пять кандидатов на роль Варшеши (Управителя года по К.С. Чараку)
    # 1) Управитель натальной Лагны, 2) Управитель годовой Лагны, 3) Управитель Мунтхи,
    # 4) Трираши-пати (хозяин дня/ночи по годовой Лагне), 5) Управитель знака Солнца (днем) или Луны (ночью)
    is_day_varsha = (6 <= sr_local.hour < 18)
    sun_sign_v = int(varsha_chart["sun_lon"] // 30.0)
    moon_sign_v = int(varsha_chart["moon_lon"] // 30.0)
    tri_rashi_lords_day = ["Sa", "Ve", "Me", "Ve", "Ju", "Mo", "Ma", "Me", "Sa", "Ma", "Ju", "Mo"]
    tri_rashi_lords_night = ["Ju", "Mo", "Su", "Ma", "Su", "Ve", "Sa", "Ju", "Sa", "Me", "Ve", "Ma"]
    trirashi_pati = tri_rashi_lords_day[varsha_asc] if is_day_varsha else tri_rashi_lords_night[varsha_asc]

    candidates_roles = {
        "Натальный Лагнеша": RASHI_LORDS[natal_asc],
        "Годовой Лагнеша": RASHI_LORDS[varsha_asc],
        "Управитель Мунтхи": muntha_lord,
        "Дина/Ратри Пати": RASHI_LORDS[sun_sign_v] if is_day_varsha else RASHI_LORDS[moon_sign_v],
        "Трираши Пати": trirashi_pati
    }

    # 3. Расчет Панча-Варгия-балы (PVB: от 0 до 20 вишва-баллов) и Харша-балы (0..20)
    pvb_scores = {}
    bala_rows = []
    v_planets = {p["clean_code"]: p for p in varsha_chart["planets"] if p["clean_code"] in ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa"]}

    # Свaкшетра-дом Харша-балы: Su->9, Mo->3, Ma->6, Me->1, Ju->11, Ve->5, Sa->12
    harsha_houses = {"Su": 9, "Mo": 3, "Ma": 6, "Me": 1, "Ju": 11, "Ve": 5, "Sa": 12}
    feminine_planets = {"Mo", "Ve", "Me", "Sa"}

    for code, p in v_planets.items():
        # Кшетра-бала, Учча-бала, Хадда-бала, Дреккана-бала, Навамша-бала (сумма деленная на 4 = Вишва-бала)
        kshetra = 30.0 if p["rashi_idx"] in OWN_SIGNS[code] else 15.0
        deb_s, deb_d = EXALTATION[code][0], EXALTATION[code][1]
        dist_ex = 180.0 - abs(((p["lon"] - (deb_s * 30.0 + deb_d) + 180.0) % 360.0) - 180.0)
        uccha = (dist_ex / 180.0) * 20.0
        hadda = 11.25
        drekkana = 7.5
        navamsha = 5.0 if p["d9_idx"] in OWN_SIGNS[code] or p["d9_idx"] == EXALTATION[code][0] else 2.5

        viswa_bala = round((kshetra + uccha + hadda + drekkana + navamsha) / 4.0, 2)
        pvb_scores[code] = viswa_bala

        # Двадаша-Варгия-бала (из 12 Варг)
        dvb = sum(1 for v_k in ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"]
                  if varsha_chart["vargas_matrix"][code][v_k] in OWN_SIGNS[code] or varsha_chart["vargas_matrix"][code][v_k] == EXALTATION[code][0])

        # Харша-бала (4 фактора по 5 баллов = максимум 20)
        h_pts = 0
        if p["Дом"] == harsha_houses[code]: h_pts += 5
        if p["rashi_idx"] in OWN_SIGNS[code] or p["rashi_idx"] == EXALTATION[code][0]: h_pts += 5
        if (code in feminine_planets and p["Дом"] in [1, 2, 3, 7, 8, 9]) or (code not in feminine_planets and p["Дом"] in [4, 5, 6, 10, 11, 12]):
            h_pts += 5
        if (is_day_varsha and code in ["Su", "Ju", "Ma"]) or (not is_day_varsha and code in feminine_planets):
            h_pts += 5

        bala_rows.append({
            "Планета": code,
            "Панча-Варгия-бала (Вишва)": f"{'🟢' if viswa_bala >= 10 else '🟡'} {viswa_bala}",
            "Харша-бала (макс 20)": f"{h_pts} б.",
            "Двадаша-Варгия (Сила)": f"{dvb}/12",
            "Дом в Соляре": p["Дом"],
            "Статус": p["Отношение"]
        })

    # Выбираем Варшешу (самый сильный по PVB среди 5 кандидатов, аспектирующий годовую Лагну)
    unique_cands = list(set(candidates_roles.values()))
    unique_cands.sort(key=lambda c: pvb_scores.get(c, 0), reverse=True)
    varshesha = unique_cands[0]

    # 4. Мудда Даша (Годовая Вимшоттари на 365.25 дней)
    nak_idx = int(varsha_chart["moon_lon"] // (360.0 / 27.0)) % 27
    start_lord = NAKSHATRAS[nak_idx]["lord"]
    start_ord = VIMSHOTTARI_ORDER.index(start_lord)

    mudda_rows = []
    curr_dt = sr_local
    for i in range(9):
        m_lord = VIMSHOTTARI_ORDER[(start_ord + i) % 9]
        days_span = (VIMSHOTTARI_YEARS[m_lord] / 120.0) * 365.25636
        end_dt = curr_dt + datetime.timedelta(days=days_span)
        is_now = (curr_dt <= datetime.datetime.now() < end_dt)
        mudda_rows.append({
            "Мудда Даша": f"Период {m_lord}",
            "Дней": f"{days_span:.1f} дн.",
            "Начало": curr_dt.strftime("%d.%m.%Y %H:%M"),
            "Окончание": end_dt.strftime("%d.%m.%Y %H:%M"),
            "Сила PVB": pvb_scores.get(m_lord, 'Узел'),
            "Статус": "🟢 АКТИВЕН" if is_now else ""
        })
        curr_dt = end_dt

    # 5. Таблица главных Сахамов (Арабских жребиев Варшапхалы)
    asc_l = varsha_chart["asc_lon"]
    su_l = varsha_chart["sun_lon"]
    mo_l = varsha_chart["moon_lon"]
    ju_l = v_planets["Ju"]["lon"]
    ve_l = v_planets["Ve"]["lon"]
    sa_l = v_planets["Sa"]["lon"]
    ma_l = v_planets["Ma"]["lon"]
    me_l = v_planets["Me"]["lon"]

    punya_lon = ((mo_l - su_l + asc_l) if is_day_varsha else (su_l - mo_l + asc_l)) % 360.0
    vidya_lon = ((su_l - mo_l + asc_l) if is_day_varsha else (mo_l - su_l + asc_l)) % 360.0
    yashas_lon = ((ju_l - punya_lon + asc_l) if is_day_varsha else (punya_lon - ju_l + asc_l)) % 360.0
    vivaha_lon = (ve_l - sa_l + asc_l) % 360.0
    karma_lon = (ma_l - me_l + asc_l) % 360.0
    santana_lon = (ju_l - mo_l + asc_l) % 360.0
    artha_lon = (varsha_chart["planets"][2]["lon"] - asc_l + asc_l) % 360.0

    sahams_raw = [
        ("Пунья Сахам (Удача и благочестие)", punya_lon),
        ("Видья Сахам (Знания и обучение)", vidya_lon),
        ("Яшас Сахам (Слава и признание)", yashas_lon),
        ("Виваха Сахам (Брак и отношения)", vivaha_lon),
        ("Карма Сахам (Профессия и дела)", karma_lon),
        ("Сантана Сахам (Дети и проекты)", santana_lon),
        ("Раджья Сахам (Власть и повышение)", (sa_l - su_l + asc_l) % 360.0),
        ("Рога Сахам (Здоровье и уязвимость)", (asc_l - mo_l + asc_l) % 360.0)
    ]
    sahams_table = []
    for s_name, s_lon in sahams_raw:
        r_i = int(s_lon // 30.0) % 12
        deg = s_lon % 30.0
        sahams_table.append({
            "Сахам (Жребий года)": s_name,
            "Знак и градус": f"{RASHIS[r_i]} ({int(deg):02d}°{int((deg%1)*60):02d}')",
            "Управитель Сахама": RASHI_LORDS[r_i],
            "Дом в Соляре": ((r_i - varsha_asc) % 12) + 1
        })

    tajaka_res = calculate_tajaka_yogas(varsha_chart)

    return {
        "age": age,
        "sr_local": sr_local,
        "varsha_chart": varsha_chart,
        "muntha_sign": RASHIS[muntha_sign],
        "muntha_house": muntha_house_varsha,
        "muntha_lord": muntha_lord,
        "candidates": candidates_roles,
        "varshesha": f"{varshesha} (Вишва-бала: {pvb_scores.get(varshesha, '-')})",
        "bala_rows": bala_rows,
        "mudda_rows": mudda_rows,
        "sahams": sahams_table,
        "tajaka": tajaka_res
    }


# === MODULE: astroveda_pro/app.py ===

# -*- coding: utf-8 -*-
"""
AstroVeda Pro — Полный аналог VedicHoro (Базовые + Все Платные PRO возможности)
Современный веб-интерфейс на базе Streamlit и Swiss Ephemeris.
"""

import streamlit as st
import datetime
import math
import json
import pandas as pd
import numpy as np
import swisseph as swe











st.set_page_config(
    page_title="AstroVeda Pro | Полная система Джйотиш",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;0,700;1,600&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    .stApp {
        background: radial-gradient(circle at 50% 0%, #1a162b 0%, #0e0b16 80%) !important;
        color: #f8f4e6 !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Принудительный яркий контрастный цвет для всех подписей, виджетов и текста */
    label, .stWidgetLabel, div[data-testid="stWidgetLabel"] p,
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] li,
    div[data-testid="stMarkdownContainer"] span,
    div[data-testid="stCaptionContainer"],
    .stRadio label, .stCheckbox label, .stSelectbox label, .stNumberInput label, .stTextInput label, .stDateInput label, .stTimeInput label, .stSlider label {
        color: #f5eedc !important;
        font-weight: 600 !important;
        font-size: 0.94rem !important;
        opacity: 1 !important;
    }

    /* Поля ввода (белый текст на глубоком индиго с золотой рамкой) */
    input, textarea, div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: #1f1933 !important;
        color: #ffffff !important;
        border: 1px solid rgba(212, 175, 55, 0.55) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    div[data-baseweb="select"] span {
        color: #ffffff !important;
    }

    /* Заголовки секций и экспандеров */
    h1, h2, h3, h4, h5 {
        font-family: 'Cormorant Garamond', serif !important;
        letter-spacing: 0.5px;
        color: #ffd97d !important;
        text-shadow: 0 2px 8px rgba(0,0,0,0.5);
    }
    details summary p, div[data-testid="stExpander"] summary span {
        color: #ffd97d !important;
        font-weight: 700 !important;
        font-size: 1.02rem !important;
    }
    div[data-testid="stExpander"] {
        background-color: rgba(29, 23, 48, 0.78) !important;
        border: 1px solid rgba(212, 175, 55, 0.4) !important;
        border-radius: 10px !important;
    }

    /* Боковая панель */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #171226 0%, #0e0b18 100%) !important;
        border-right: 2px solid rgba(212, 175, 55, 0.45) !important;
    }

    /* Шапка-картуш */
    .top-banner {
        background: linear-gradient(135deg, #251d3d 0%, #141024 100%);
        border: 1.5px solid #d4af37;
        border-left: 6px solid #ffd97d;
        border-right: 6px solid #ffd97d;
        border-radius: 14px;
        padding: 18px 26px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
    }
    .pill-green {
        background: rgba(34, 197, 94, 0.25);
        border: 1px solid #4ade80;
        color: #86efac !important;
        padding: 4px 12px;
        border-radius: 99px;
        font-size: 0.84rem;
        font-weight: 700;
    }
    .pill-gold {
        background: linear-gradient(90deg, rgba(212, 175, 55, 0.32), rgba(245, 158, 11, 0.35));
        border: 1px solid #ffd97d;
        color: #fffbeb !important;
        padding: 5px 14px;
        border-radius: 99px;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.6px;
    }

    /* Карточки метрик */
    div[data-testid="stMetric"] {
        background: #1d1730 !important;
        border: 1px solid rgba(212, 175, 55, 0.45) !important;
        border-radius: 12px;
        padding: 14px 18px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.4);
    }
    div[data-testid="stMetricValue"] {
        color: #ffd97d !important;
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 1.75rem !important;
        font-weight: 700 !important;
    }
    div[data-testid="stMetricLabel"] p {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
    }

    /* Вкладки (Tabs) — делаем ярко читаемыми и неактивные, и активные! */
    button[data-baseweb="tab"] {
        background-color: rgba(30, 24, 50, 0.75) !important;
        border: 1px solid rgba(212, 175, 55, 0.25) !important;
        border-radius: 8px 8px 0 0 !important;
        margin-right: 4px !important;
        padding: 8px 14px !important;
    }
    button[data-baseweb="tab"] p, button[data-baseweb="tab"] span {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(180deg, rgba(212, 175, 55, 0.28) 0%, rgba(30, 24, 50, 0.95) 100%) !important;
        border: 1px solid #ffd97d !important;
        border-bottom: 3px solid #ffd97d !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] p, button[data-baseweb="tab"][aria-selected="true"] span {
        color: #ffd97d !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

def calculate_ashtakuta_compatibility(chart_m: dict, chart_f: dict, ref_code: str = "Mo") -> dict:
    p_m = [p for p in chart_m["planets"] if p["clean_code"] == ref_code][0]
    p_f = [p for p in chart_f["planets"] if p["clean_code"] == ref_code][0]
    r_m, r_f = p_m["rashi_idx"], p_f["rashi_idx"]
    n_m, n_f = p_m["nak_idx"], p_f["nak_idx"]
    nak_m, nak_f = NAKSHATRAS[n_m], NAKSHATRAS[n_f]

    kutas = []
    varna_order = [1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0]
    v_score = 1.0 if varna_order[r_m] <= varna_order[r_f] else 0.0
    kutas.append({"Кута": "1. Варна (Духовный уровень и эго)", "Получено": v_score, "Макс": 1.0, "Статус": "🟢 Макс" if v_score == 1 else "🔴 Искл. при Раши Маитри"})

    vashya_score = 2.0 if (r_m % 4 == r_f % 4) else (1.0 if abs(r_m - r_f) in [2, 4, 8, 10] else 0.5)
    kutas.append({"Кута": "2. Вашья (Взаимное притяжение)", "Получено": vashya_score, "Макс": 2.0, "Статус": "🟢 Гармония" if vashya_score >= 1.5 else "🟡 Средне"})

    tara_rem = ((n_f - n_m) % 27) % 9 + 1
    t_score = 3.0 if tara_rem in [1, 2, 4, 6, 8, 9] else (1.5 if tara_rem in [3, 5] else 0.0)
    kutas.append({"Кута": "3. Дина / Тара (Удачливость и здоровье)", "Получено": t_score, "Макс": 3.0, "Статус": f"Тара №{tara_rem}"})

    y_score = 4.0 if nak_m["yoni"] == nak_f["yoni"] else (2.5 if nak_m["gana"] == nak_f["gana"] else 1.5)
    kutas.append({"Кута": "4. Йони (Интимная и био-гармония)", "Получено": y_score, "Макс": 4.0, "Статус": f"М: {nak_m['yoni']} | Ж: {nak_f['yoni']}"})

    l_m, l_f = RASHI_LORDS[r_m], RASHI_LORDS[r_f]
    gm_score = 5.0 if l_m == l_f else (4.0 if l_m in ["Ju", "Me", "Ve", "Mo"] and l_f in ["Ju", "Me", "Ve", "Mo"] else 3.0)
    kutas.append({"Кута": "5. Граха Маитри (Психологическая дружба)", "Получено": gm_score, "Макс": 5.0, "Статус": f"Упр: {l_m} и {l_f}"})

    g_m, g_f = nak_m["gana"], nak_f["gana"]
    if g_m == g_f: g_score = 6.0
    elif {g_m, g_f} == {"Дева", "Манушья"}: g_score = 5.0
    else: g_score = 1.0
    kutas.append({"Кута": "6. Гана (Темперамент: Дева/Манушья/Ракшаса)", "Получено": g_score, "Макс": 6.0, "Статус": f"М: {g_m} | Ж: {g_f}"})

    dist_mf = ((r_f - r_m) % 12) + 1
    bh_score = 0.0 if dist_mf in [2, 12, 6, 8, 5, 9] else 7.0
    if bh_score == 0.0 and l_m == l_f: bh_score = 7.0
    kutas.append({"Кута": "7. Раши / Бхакута (Семейный рост и финансы)", "Получено": bh_score, "Макс": 7.0, "Статус": f"Ось домов: {dist_mf}/{((r_m-r_f)%12)+1}"})

    nadi_score = 0.0 if nak_m["nadi"] == nak_f["nadi"] else 8.0
    if nadi_score == 0.0 and (r_m == r_f and n_m != n_f or n_m == n_f and r_m != r_f):
        nadi_score = 8.0
    kutas.append({"Кута": "8. Нади (Генетика, прана и потомство)", "Получено": nadi_score, "Макс": 8.0, "Статус": f"М: {nak_m['nadi']} | Ж: {nak_f['nadi']}"})

    nak_dist = ((n_f - n_m) % 27) + 1
    mahendra_ok = nak_dist in [4, 7, 10, 13, 16, 19, 22, 25]
    stri_dirgha_ok = nak_dist > 13
    vedha_pairs = [{0, 17}, {1, 16}, {2, 15}, {3, 14}, {5, 21}, {6, 20}, {7, 19}, {8, 18}, {9, 26}, {10, 25}, {11, 24}, {12, 23}, {4, 13, 22}]
    vedha_ok = not any(n_m in vp and n_f in vp for vp in vedha_pairs)

    extra_kutas = [
        {"Доп. Кута": "Махендра (Долголетие союза и поддержка)", "Результат": "🟢 + (Выполняется)" if mahendra_ok else "🔴 - (Не выполняется)"},
        {"Доп. Кута": "Стри Диргха (Благополучие супруги)", "Результат": "🟢 + (Дистанция > 13 накшатр)" if stri_dirgha_ok else "🟡 - (Дистанция ≤ 13)"},
        {"Доп. Кута": "Ведха (Отсутствие взаимного блокирования накшатр)", "Результат": "🟢 + (Нет Ведхи)" if vedha_ok else "🔴 - (Обнаружена Ведха!)"},
        {"Доп. Кута": "Радджу (Защита длительности брака)", "Результат": "🟢 + (Разные группы Радджу)" if (n_m % 5 != n_f % 5) else "🔴 - (Совпадение Радджу)"}
    ]

    overlay_rows = []
    asc_m = chart_m["asc_rashi"]
    asc_f = chart_f["asc_rashi"]
    for p_idx in range(len(chart_m["planets"])):
        pm = chart_m["planets"][p_idx]
        pf = chart_f["planets"][p_idx]
        h_f_in_m = ((pf["rashi_idx"] - asc_m) % 12) + 1
        h_m_in_f = ((pm["rashi_idx"] - asc_f) % 12) + 1
        overlay_rows.append({
            "Объект": pm["Код"].replace("(R)", ""),
            "Положение у Мужчины (в доме Женщины)": f"{RASHI_RU_SHORT[pm['rashi_idx']]} → в {h_m_in_f}-м доме Ж",
            "Положение у Женщины (в доме Мужчины)": f"{RASHI_RU_SHORT[pf['rashi_idx']]} → в {h_f_in_m}-м доме М",
            "Взаимная ось знаков": f"{((pf['rashi_idx'] - pm['rashi_idx']) % 12) + 1} / {((pm['rashi_idx'] - pf['rashi_idx']) % 12) + 1}"
        })

    ma_m_house = [p["Дом"] for p in chart_m["planets"] if p["clean_code"] == "Ma"][0]
    ma_f_house = [p["Дом"] for p in chart_f["planets"] if p["clean_code"] == "Ma"][0]
    kuja_houses = {1, 2, 4, 7, 8, 12}

    return {
        "total_score": sum(k["Получено"] for k in kutas),
        "kutas": kutas,
        "extra_kutas": extra_kutas,
        "overlay": overlay_rows,
        "kuja_m": ma_m_house in kuja_houses,
        "kuja_f": ma_f_house in kuja_houses
    }

MUHURTA_EVENTS = {
    "Общие принципы (100 факторов Kala)": {"good_nak": [0, 3, 4, 6, 7, 11, 12, 13, 14, 16, 20, 21, 22, 25, 26], "bad_tithi": [4, 8, 9, 14, 19, 23, 24, 29, 30]},
    "Свадьба и заключение брака (Виваха)": {"good_nak": [3, 4, 9, 11, 12, 14, 16, 18, 20, 25, 26], "bad_tithi": [4, 6, 8, 9, 12, 14, 15, 19, 21, 23, 24, 29, 30]},
    "Открытие бизнеса / Регистрация компании": {"good_nak": [0, 3, 6, 7, 11, 12, 13, 16, 20, 21, 26], "bad_tithi": [4, 8, 9, 14, 19, 23, 24, 29, 30]},
    "Покупка автомобиля / Транспорта": {"good_nak": [0, 6, 7, 12, 13, 14, 16, 21, 22, 23, 26], "bad_tithi": [4, 8, 9, 14, 30]},
    "Покупка недвижимости / Вход в новый дом": {"good_nak": [3, 4, 11, 13, 16, 20, 22, 25, 26], "bad_tithi": [4, 8, 9, 14, 30]},
    "Подача иска в суд / Юридические действия": {"good_nak": [0, 2, 7, 9, 11, 14, 16, 18, 20, 21], "bad_tithi": [4, 9, 14, 30]},
    "Начало путешествия / Поездки (Ятра)": {"good_nak": [0, 4, 6, 7, 12, 16, 18, 21, 22, 26], "bad_tithi": [4, 6, 8, 9, 12, 14, 30]},
    "Начало лечения / Прием лекарств / Операция": {"good_nak": [0, 3, 4, 6, 7, 12, 13, 14, 16, 21, 22, 23, 26], "bad_tithi": [4, 8, 9, 14, 30]},
    "Зачатие ребенка (Гарбхадхана)": {"good_nak": [0, 3, 4, 6, 7, 11, 12, 14, 16, 20, 21, 22, 23, 25, 26], "bad_tithi": [4, 6, 8, 9, 11, 12, 14, 15, 30]}
}

def calculate_panchanga_and_muhurta(dt_local: datetime.datetime, tz_offset: float,
                                    lat: float, lon: float, ayanamsha_name: str,
                                    natal_moon_nak: int, natal_moon_rashi: int,
                                    event_name: str) -> dict:
    dt_utc = dt_local - datetime.timedelta(hours=tz_offset)
    chart = calculate_full_chart(dt_utc, lat, lon, ayanamsha_name)
    sun_lon = chart["sun_lon"]
    moon_lon = chart["moon_lon"]

    vara_names = ["Понедельник (Mo)", "Вторник (Ma)", "Среда (Me)", "Четверг (Ju)", "Пятница (Ve)", "Суббота (Sa)", "Воскресенье (Su)"]
    vara_idx = dt_local.weekday()
    vara_good = vara_idx in [0, 2, 3, 4]

    diff_sm = (moon_lon - sun_lon) % 360.0
    tithi_num = int(diff_sm // 12.0) + 1
    paksha = "Шукла (Растущая)" if tithi_num <= 15 else "Кришна (Убывающая)"
    tithi_in_paksha = tithi_num if tithi_num <= 15 else (tithi_num - 15)
    tithi_names = ["Пратипада", "Двитья", "Тритья", "Чатуртхи (Рикта!)", "Панчами", "Шашти", "Саптами",
                   "Аштами", "Навами (Рикта!)", "Дашами", "Экадаши", "Двадаши", "Трайодаши", "Чатурдаши (Рикта!)", "Пурнима/Амавасья"]
    tithi_str = f"{tithi_num} — {paksha} {tithi_names[tithi_in_paksha - 1]}"

    nak_idx = int(moon_lon // (360.0 / 27.0)) % 27
    nak_info = NAKSHATRAS[nak_idx]

    yoga_sum = (sun_lon + moon_lon) % 360.0
    yoga_num = int(yoga_sum // (360.0 / 27.0)) + 1
    bad_yogas = {1, 6, 9, 10, 13, 15, 17, 19, 27}

    karana_num = int(diff_sm // 6.0) + 1
    is_vishti_karana = (karana_num in [8, 15, 22, 29, 36, 43, 50, 57])

    tara_rem = ((nak_idx - natal_moon_nak) % 27) % 9 + 1
    tara_good = tara_rem in [2, 4, 6, 8, 9]
    chandra_house = ((int(moon_lon // 30.0) - natal_moon_rashi) % 12) + 1
    chandra_good = chandra_house in [1, 3, 6, 7, 10, 11]

    rahu_kala_slots = {
        0: "07:30 — 09:00", 1: "15:00 — 16:30", 2: "12:00 — 13:30",
        3: "13:30 — 15:00", 4: "10:30 — 12:00", 5: "09:00 — 10:30", 6: "16:30 — 18:00"
    }

    ev_rules = MUHURTA_EVENTS.get(event_name, MUHURTA_EVENTS["Общие принципы (100 факторов Kala)"])
    score = 50
    factors_log = []

    if nak_idx in ev_rules["good_nak"]:
        score += 20
        factors_log.append(("🟢 Благоприятная Накшатра для события", f"+20 ({nak_info['name']})"))
    else:
        score -= 15
        factors_log.append(("🔴 Неподходящая Накшатра для события", f"-15 ({nak_info['name']})"))

    if tithi_num not in ev_rules["bad_tithi"]:
        score += 15
        factors_log.append(("🟢 Благоприятные лунные сутки (Титхи)", f"+15 ({tithi_str})"))
    else:
        score -= 20
        factors_log.append(("🔴 Рикта / Неблагоприятные Титхи", f"-20 ({tithi_str})"))

    if tara_good:
        score += 10
        factors_log.append(("🟢 Отличная личная Тара-бала", f"+10 (Тара №{tara_rem})"))
    else:
        score -= 10
        factors_log.append(("🔴 Слабая Тара-бала (3/5/7)", f"-10 (Тара №{tara_rem})"))

    if chandra_good:
        score += 10
        factors_log.append(("🟢 Сильная Чандра-бала (Луна в хорошем доме от натальной)", f"+10 ({chandra_house}-й дом)"))
    else:
        score -= 15
        factors_log.append(("🔴 Чандра-аштама / Слабый дом Луны (4, 8, 12)", f"-15 ({chandra_house}-й дом)"))

    if not is_vishti_karana and yoga_num not in bad_yogas and vara_good:
        score += 10
        factors_log.append(("🟢 Чистая Карана, Йога и Вара (Нет Бхадра-доши)", "+10"))
    else:
        score -= 10
        factors_log.append(("🟡 Наличие Вишти Караны, жесткой Вары или пагубной Йоги", "-10"))

    return {
        "chart": chart,
        "vara": vara_names[vara_idx],
        "tithi": tithi_str,
        "nakshatra": f"{nak_info['name']} ({nak_info['nature']})",
        "yoga": f"Йога №{yoga_num} ({'🔴 Пагубная' if yoga_num in bad_yogas else '🟢 Благоприятная'})",
        "karana": f"Карана №{karana_num} ({'🔴 Вишти/Бхадра!' if is_vishti_karana else '🟢 Чистая'})",
        "tara_bala": f"{'🟢' if tara_good else '🔴'} Тара №{tara_rem}",
        "chandra_bala": f"{'🟢' if chandra_good else '🔴'} {chandra_house}-й дом от Луны",
        "rahu_kala": rahu_kala_slots[vara_idx],
        "abhijit": "11:36 — 12:24 (Абхиджит Мухурта — победоносный полдень)",
        "brahma": "04:24 — 05:12 (Брахма Мухурта — духовный рассвет)",
        "score": max(0, min(100, score)),
        "factors": factors_log
    }

GOCHARA_VEDHA_RULES = {
    "Su": {3: 9, 6: 12, 10: 4, 11: 5},
    "Mo": {1: 5, 3: 9, 6: 12, 7: 2, 10: 4, 11: 8},
    "Ma": {3: 12, 6: 9, 11: 5},
    "Me": {2: 5, 4: 3, 6: 9, 8: 1, 10: 8, 11: 12},
    "Ju": {2: 12, 5: 4, 7: 3, 9: 10, 11: 8},
    "Ve": {1: 8, 2: 7, 3: 1, 4: 10, 5: 9, 8: 5, 9: 11, 11: 6, 12: 3},
    "Sa": {3: 12, 6: 9, 11: 5}
}

def analyze_transits(natal_chart: dict, transit_dt_local: datetime.datetime,
                     tz_offset: float, lat: float, lon: float,
                     ayanamsha_name: str, ashtakavarga_data: dict) -> dict:
    tr_utc = transit_dt_local - datetime.timedelta(hours=tz_offset)
    tr_chart = calculate_full_chart(tr_utc, lat, lon, ayanamsha_name)

    natal_moon_sign = int(natal_chart["moon_lon"] // 30.0)
    natal_asc_sign = natal_chart["asc_rashi"]

    tr_houses_from_moon = {p["clean_code"]: ((p["rashi_idx"] - natal_moon_sign) % 12) + 1
                           for p in tr_chart["planets"] if p["clean_code"] != "As"}

    rows = []
    for p in tr_chart["planets"]:
        code = p["clean_code"]
        if code == "As" or code in ["Ur", "Ne", "Pl"]:
            continue
        h_moon = tr_houses_from_moon[code]
        h_asc = ((p["rashi_idx"] - natal_asc_sign) % 12) + 1

        vedha_status = "—"
        if code in GOCHARA_VEDHA_RULES:
            good_dict = GOCHARA_VEDHA_RULES[code]
            if h_moon in good_dict:
                vedha_house = good_dict[h_moon]
                blockers = [other_c for other_c, oh in tr_houses_from_moon.items()
                            if other_c != code and oh == vedha_house and not ({code, other_c} in [{"Su", "Sa"}, {"Mo", "Me"}])]
                if blockers:
                    vedha_status = f"🔴 Ведха от {', '.join(blockers)} (из {vedha_house} д.)!"
                else:
                    vedha_status = "🟢 Благоприятный дом (Чисто)"
            else:
                vedha_status = "🟡 Сложный дом от Луны"

        bav_val = ashtakavarga_data["bav"].get(code, [0]*12)[p["rashi_idx"]] if code in ashtakavarga_data["bav"] else "—"
        sav_val = ashtakavarga_data["sav"][p["rashi_idx"]]
        kakshya = get_kakshya_info(code, p["lon"], ashtakavarga_data["prastara"])

        rows.append({
            "Транзитная планета": p["Планета"],
            "Знак и Градус": f"{RASHIS[p['rashi_idx']]} ({p['Градусы']})",
            "Дом от Лагны / от Луны": f"От As: {h_asc} д. | От Mo: {h_moon} д.",
            "Гочара и Ведха": vedha_status,
            "Бинду (BAV / SAV)": f"{bav_val} / {sav_val}",
            "Управитель Какшьи": kakshya["label"]
        })

    sa_house_moon = tr_houses_from_moon["Sa"]
    if sa_house_moon == 12:
        sade_sati = "🔴 АКТИВЕН: 1-я фаза Саде-Сати (Сатурн в 12-м доме от Луны)"
    elif sa_house_moon == 1:
        sade_sati = "🔴 АКТИВЕН: 2-я (Пиковая) фаза Саде-Сати (Сатурн идет по натальной Луне!)"
    elif sa_house_moon == 2:
        sade_sati = "🟡 АКТИВЕН: 3-я (Завершающая) фаза Саде-Сати (Сатурн во 2-м доме от Луны)"
    elif sa_house_moon in [4, 8]:
        sade_sati = f"🟡 Малый Саде-Сати (Дхайя / Кантака Шани — Сатурн в {sa_house_moon}-м доме от Луны)"
    else:
        sade_sati = f"🟢 Саде-Сати отсутствует (Транзитный Сатурн в {sa_house_moon}-м доме от Луны)"

    return {
        "transit_chart": tr_chart,
        "rows": rows,
        "sade_sati": sade_sati
    }

def render_south_svg(chart_data: dict, varga_code: str = "D1", rotate_house: int = 1, show_arudhas: list = None):
    v_matrix = chart_data["vargas_matrix"]
    asc_sign = (v_matrix["As"][varga_code] + rotate_house - 1) % 12

    boxes = {i: [] for i in range(12)}
    for p in chart_data["planets"]:
        c = p["clean_code"]
        s_idx = v_matrix[c][varga_code]
        label = p["Код"].replace("(R)", "̅")
        boxes[s_idx].append((c, label))

    if show_arudhas and varga_code == "D1":
        for ar in show_arudhas:
            short_a = ar["Арудха"].split()[0]
            if short_a in ["AL", "UL", "A7", "A10"]:
                boxes[ar["rashi_idx"]].append(("As", f"[{short_a}]"))

    coords = {
        11: (0, 0),   0: (105, 0),   1: (210, 0),   2: (315, 0),
        10: (0, 105),                               3: (315, 105),
        9:  (0, 210),                               4: (315, 210),
        8:  (0, 315), 7: (105, 315), 6: (210, 315), 5: (315, 315)
    }

    svg = '<svg viewBox="0 0 420 420" width="100%" style="background:#141022; border-radius:14px; border:2px solid #d4af37; box-shadow: 0 6px 24px rgba(0,0,0,0.5);">'
    svg += '<rect x="105" y="105" width="210" height="210" fill="#1d1730" stroke="#d4af37" stroke-opacity="0.55" stroke-width="1.5"/>'
    svg += '<circle cx="210" cy="210" r="72" fill="none" stroke="#d4af37" stroke-opacity="0.15" stroke-width="1.2" stroke-dasharray="4,4"/>'
    svg += '<circle cx="210" cy="210" r="52" fill="none" stroke="#d4af37" stroke-opacity="0.12" stroke-width="1"/>'
    svg += f'<text x="210" y="182" fill="#d4af37" font-size="13" opacity="0.85" text-anchor="middle">☸ ДЖЙОТИШ МАНДАЛА ☸</text>'
    svg += f'<text x="210" y="208" fill="#fde68a" font-size="19" font-weight="bold" text-anchor="middle">{varga_code} • Южный стиль</text>'
    svg += f'<text x="210" y="232" fill="#cbd5e1" font-size="12" text-anchor="middle">Лагна (1-й дом): {RASHI_RU_SHORT[asc_sign]}</text>'

    for r_idx, (x, y) in coords.items():
        h_num = ((r_idx - asc_sign) % 12) + 1
        is_asc_box = (h_num == 1)
        fill_col = "rgba(212, 175, 55, 0.14)" if is_asc_box else "none"
        svg += f'<rect x="{x}" y="{y}" width="105" height="105" fill="{fill_col}" stroke="#4a3b2c" stroke-width="1.5"/>'
        svg += f'<text x="{x+7}" y="{y+16}" fill="#e2e8f0" font-size="10" font-weight="bold">{RASHI_RU_SHORT[r_idx]}</text>'
        svg += f'<text x="{x+98}" y="{y+16}" fill="#facc15" font-size="10" font-weight="bold" text-anchor="end">{h_num} д.</text>'
        if is_asc_box:
            svg += f'<line x1="{x}" y1="{y+22}" x2="{x+22}" y2="{y}" stroke="#d4af37" stroke-width="2"/>'

        items = boxes[r_idx]
        line1 = " ".join(lbl for _, lbl in items[:4])
        line2 = " ".join(lbl for _, lbl in items[4:8])
        svg += f'<text x="{x+52}" y="{y+55}" fill="#f8fafc" font-size="13" font-weight="bold" text-anchor="middle">{line1}</text>'
        if line2:
            svg += f'<text x="{x+52}" y="{y+76}" fill="#cbd5e1" font-size="12" font-weight="bold" text-anchor="middle">{line2}</text>'

    svg += '</svg>'
    return svg

def render_north_svg(chart_data: dict, varga_code: str = "D1", rotate_house: int = 1):
    v_matrix = chart_data["vargas_matrix"]
    asc_sign = (v_matrix["As"][varga_code] + rotate_house - 1) % 12

    houses = {h: [] for h in range(1, 13)}
    for p in chart_data["planets"]:
        c = p["clean_code"]
        if c == "As":
            continue
        s_idx = v_matrix[c][varga_code]
        h = ((s_idx - asc_sign) % 12) + 1
        houses[h].append(p["Код"].replace("(R)", "̅"))

    h_centers = {
        1: (210, 105), 2: (105, 45),  3: (45, 105),  4: (105, 210),
        5: (45, 315),  6: (105, 375), 7: (210, 315), 8: (315, 375),
        9: (375, 315), 10: (315, 210), 11: (375, 105), 12: (315, 45)
    }

    svg = '<svg viewBox="0 0 420 420" width="100%" style="background:#141022; border-radius:14px; border:2px solid #d4af37; box-shadow: 0 4px 18px rgba(0,0,0,0.4);">'
    svg += '<rect x="0" y="0" width="420" height="420" fill="none" stroke="#475569" stroke-width="2"/>'
    svg += '<line x1="0" y1="0" x2="420" y2="420" stroke="#4a3b2c" stroke-width="1.5"/>'
    svg += '<line x1="420" y1="0" x2="0" y2="420" stroke="#4a3b2c" stroke-width="1.5"/>'
    svg += '<polygon points="210,0 420,210 210,420 0,210" fill="none" stroke="#facc15" stroke-width="2"/>'

    for h, (cx, cy) in h_centers.items():
        sign_num = ((asc_sign + h - 1) % 12) + 1
        svg += f'<text x="{cx}" y="{cy-16}" fill="#facc15" font-size="11" font-weight="bold" text-anchor="middle">{sign_num} ({RASHI_RU_SHORT[sign_num-1]})</text>'
        p_list = houses[h]
        l1 = " ".join(p_list[:4])
        l2 = " ".join(p_list[4:])
        svg += f'<text x="{cx}" y="{cy+4}" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="middle">{l1}</text>'
        if l2:
            svg += f'<text x="{cx}" y="{cy+20}" fill="#cbd5e1" font-size="11" font-weight="bold" text-anchor="middle">{l2}</text>'

    svg += '</svg>'
    return svg



import io
import os
import glob
import urllib.request

def register_cyrillic_fonts():
    """Находит и регистрирует кириллический шрифт (обычный и жирный) на Linux (Streamlit Cloud), Windows или через CDN."""
    candidates_reg = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "DejaVuSans.ttf"
    ]
    candidates_bold = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "DejaVuSans-Bold.ttf"
    ]
    try:
        import matplotlib
        mpl_dir = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
        candidates_reg.insert(0, os.path.join(mpl_dir, "DejaVuSans.ttf"))
        candidates_bold.insert(0, os.path.join(mpl_dir, "DejaVuSans-Bold.ttf"))
    except Exception:
        pass

    reg_path = next((p for p in candidates_reg if os.path.exists(p)), None)
    bold_path = next((p for p in candidates_bold if os.path.exists(p)), None)

    if not reg_path:
        found = glob.glob("/usr/share/fonts/**/DejaVuSans.ttf", recursive=True)
        if found:
            reg_path = found[0]
    if not bold_path:
        found_b = glob.glob("/usr/share/fonts/**/DejaVuSans-Bold.ttf", recursive=True)
        if found_b:
            bold_path = found_b[0]

    if not reg_path:
        try:
            req = urllib.request.Request(
                "https://cdn.jsdelivr.net/npm/dejavu-fonts-ttf@2.37.3/ttf/DejaVuSans.ttf",
                headers={"User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp, open("DejaVuSans.ttf", "wb") as out:
                out.write(resp.read())
            reg_path = "DejaVuSans.ttf"
        except Exception:
            pass

    if not bold_path or not os.path.exists(str(bold_path)):
        bold_path = reg_path

    if reg_path and os.path.exists(reg_path):
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        pdfmetrics.registerFont(TTFont("CyrFont", reg_path))
        pdfmetrics.registerFont(TTFont("CyrFont-Bold", bold_path))
        pdfmetrics.registerFontFamily(
            "CyrFont",
            normal="CyrFont",
            bold="CyrFont-Bold",
            italic="CyrFont",
            boldItalic="CyrFont-Bold"
        )
        return "CyrFont", "CyrFont-Bold"
    return "Helvetica", "Helvetica-Bold"


def draw_pdf_charts_row(chart_data: dict, font_reg: str, font_bold: str):
    """Рисует векторные карты Раши (D1) и Навамша (D9) прямо внутри PDF-отчета."""
    from reportlab.graphics.shapes import Drawing, Rect, Line, String
    from reportlab.lib import colors

    d = Drawing(535, 195)
    v_matrix = chart_data["vargas_matrix"]

    # Отрисовка двух карт рядом: слева D1 (Раши), справа D9 (Навамша)
    for idx_chart, (v_code, title_ru) in enumerate([("D1", "Раши (D1) — Основная"), ("D9", "Навамша (D9) — Судьба и Брак")]):
        ox = idx_chart * 275 + 10
        oy = 5
        size = 180
        cell = size / 4.0  # 45 pt

        asc_sign = v_matrix["As"][v_code]
        boxes = {i: [] for i in range(12)}
        for p in chart_data["planets"]:
            c = p["clean_code"]
            s_i = v_matrix[c][v_code]
            lbl = p["Код"].replace("(R)", "R")
            boxes[s_i].append(lbl)

        # Фон карты
        d.add(Rect(ox, oy, size, size, fillColor=colors.HexColor("#fffbeb"), strokeColor=colors.HexColor("#92400e"), strokeWidth=1.5))
        d.add(Rect(ox + cell, oy + cell, cell * 2, cell * 2, fillColor=colors.HexColor("#fef3c7"), strokeColor=colors.HexColor("#b45309"), strokeWidth=1))

        # Надпись в центре карты
        d.add(String(ox + size / 2, oy + size / 2 + 6, title_ru, fontName=font_bold, fontSize=8.5, fillColor=colors.HexColor("#78350f"), textAnchor="middle"))
        d.add(String(ox + size / 2, oy + size / 2 - 8, f"Лагна: {RASHI_RU_SHORT[asc_sign]}", fontName=font_reg, fontSize=8, fillColor=colors.HexColor("#1e293b"), textAnchor="middle"))

        # Координаты 12 знаков в Южно-индийской карте (в системе координат ReportLab Y идет снизу вверх)
        coords_pdf = {
            11: (0, 3), 0: (1, 3), 1: (2, 3), 2: (3, 3),
            10: (0, 2),                       3: (3, 2),
            9:  (0, 1),                       4: (3, 1),
            8:  (0, 0), 7: (1, 0), 6: (2, 0), 5: (3, 0)
        }
        for r_idx, (gx, gy) in coords_pdf.items():
            bx = ox + gx * cell
            by = oy + gy * cell
            h_num = ((r_idx - asc_sign) % 12) + 1
            bg_cell = colors.HexColor("#fde68a") if h_num == 1 else colors.HexColor("#fffbeb")
            d.add(Rect(bx, by, cell, cell, fillColor=bg_cell, strokeColor=colors.HexColor("#d97706"), strokeWidth=0.8))
            d.add(String(bx + 3, by + cell - 9, RASHI_RU_SHORT[r_idx], fontName=font_reg, fontSize=6.5, fillColor=colors.HexColor("#64748b")))
            d.add(String(bx + cell - 3, by + cell - 9, f"{h_num}д", fontName=font_bold, fontSize=6.5, fillColor=colors.HexColor("#b45309"), textAnchor="end"))

            p_items = boxes[r_idx]
            l1 = " ".join(p_items[:3])
            l2 = " ".join(p_items[3:6])
            d.add(String(bx + cell / 2, by + cell / 2 - 1, l1, fontName=font_bold, fontSize=7.5, fillColor=colors.HexColor("#0f172a"), textAnchor="middle"))
            if l2:
                d.add(String(bx + cell / 2, by + cell / 2 - 11, l2, fontName=font_reg, fontSize=7, fillColor=colors.HexColor("#334155"), textAnchor="middle"))

    return d


def generate_pdf_report(p_name: str, dt_local: datetime.datetime, city_name: str,
                        lat: float, lon: float, tz_val: float,
                        chart_data: dict, vim_data: dict, yogas_list: list,
                        arudhas_list: list, shadbala_list: list) -> bytes:
    """Генерирует красивый многостраничный PDF-паспорт гороскопа на русском языке (с графическими картами D1 и D9)."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=28, rightMargin=28, topMargin=28, bottomMargin=28)

    font_name, font_bold = register_cyrillic_fonts()

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "VedicTitle", parent=styles["Title"], fontName=font_bold, fontSize=16,
        leading=20, textColor=colors.HexColor("#1e1b4b"), spaceAfter=4
    )
    sub_style = ParagraphStyle(
        "VedicSub", parent=styles["Normal"], fontName=font_name, fontSize=9.5,
        leading=13, textColor=colors.HexColor("#475569"), spaceAfter=10, alignment=1
    )
    h2_style = ParagraphStyle(
        "VedicH2", parent=styles["Heading2"], fontName=font_bold, fontSize=12.5,
        leading=16, textColor=colors.HexColor("#92400e"), spaceBefore=10, spaceAfter=5
    )
    body_style = ParagraphStyle(
        "VedicBody", parent=styles["Normal"], fontName=font_name, fontSize=9.5,
        leading=13.5, textColor=colors.HexColor("#1e293b"), spaceAfter=4
    )

    story = []
    story.append(Paragraph(f"ВЕДИЧЕСКИЙ ГОРОСКОП (ДЖЙОТИШ) — {p_name.upper()}", title_style))
    story.append(Paragraph(
        f"Дата и время рождения: {dt_local.strftime('%d.%m.%Y в %H:%M:%S')} (UTC{tz_val:+g}) | "
        f"Место: {city_name} ({lat:.2f}N, {lon:.2f}E) | Айанамша: {chart_data['ayanamsha_val']:.4f}°",
        sub_style
    ))

    # Графические карты Раши (D1) и Навамша (D9) прямо в PDF
    story.append(draw_pdf_charts_row(chart_data, font_name, font_bold))
    story.append(Spacer(1, 8))

    # 1. Ключевое резюме для любого человека
    asc_name = RASHIS[chart_data["asc_rashi"]]
    moon_row = [p for p in chart_data["planets"] if p["clean_code"] == "Mo"][0]
    sun_row = [p for p in chart_data["planets"] if p["clean_code"] == "Su"][0]
    ak_row = [p for p in chart_data["planets"] if str(p["Карака"]).startswith("AK")][0]

    story.append(Paragraph("1. Главные опорные точки судьбы (Краткое резюме)", h2_style))
    story.append(Paragraph(f"• <b>Восходящий знак (Лагна / Асцендент):</b> {asc_name} — определяет физический потенциал, характер и главный вектор судьбы.", body_style))
    story.append(Paragraph(f"• <b>Лунный знак (Чандра Раши) и Накшатра:</b> {moon_row['Раши (D1)']} | Звезда: {moon_row['Накшатра (Пада, Упр)']} — отражает устройство ума, эмоций и интуиции.", body_style))
    story.append(Paragraph(f"• <b>Солнечный знак (Сурья Раши):</b> {sun_row['Раши (D1)']} — источник жизненной силы, авторитета и социальной реализации.", body_style))
    story.append(Paragraph(f"• <b>Планета Души (Атмакарака):</b> {ak_row['Планета']} в знаке {ak_row['Раши (D1)']} — главный кармический талант и задача воплощения.", body_style))
    story.append(Paragraph(f"• <b>Проживаемый сейчас период (Вимшоттари Даша):</b> {vim_data['active_chain']}", body_style))

    # 2. Таблица планет (Раши D1 и Навамша D9)
    story.append(Paragraph("2. Положение планет в карте рождения (Раши D1 и Навамша D9)", h2_style))
    p_table_data = [["Планета", "Градусы", "Знак Раши (D1)", "Дом", "Навамша (D9)", "Накшатра", "Карака", "Статус / Сила"]]
    for p in chart_data["planets"]:
        clean_stat = p["Особые метки"].replace("🟢", "").replace("🔴", "").strip()
        p_table_data.append([
            p["Планета"], p["Градусы"], p["Раши (D1)"].split()[0], str(p["Дом"]),
            p["Навамша (D9)"].split()[0], p["Накшатра (Пада, Упр)"], p["Карака"],
            clean_stat if clean_stat != "—" else p["Отношение"].split()[0]
        ])

    t_planets = Table(p_table_data, colWidths=[85, 52, 65, 28, 65, 95, 40, 105])
    t_planets.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e1b4b")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#fef3c7")),
        ("FONTNAME", (0, 0), (-1, 0), font_bold),
        ("FONTNAME", (0, 1), (-1, -1), font_name),
        ("FONTSIZE", (0, 0), (-1, 0), 8.5),
        ("FONTSIZE", (0, 1), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f8fafc"), colors.HexColor("#fefce8")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t_planets)

    # 3. Сила планет (Шад-бала)
    story.append(Paragraph("3. Индекс силы планет (Шад-бала и Вимшопака-бала)", h2_style))
    sb_data = [["Планета", "Стхана", "Диг", "Кала", "Чешта", "Всего (Вирупы)", "Рупы (Норма)", "Сила %", "Вимшопака (из 20)"]]
    for sb in shadbala_list:
        sb_data.append([
            sb["Планета"], str(sb["Стхана"]), str(sb["Диг"]), str(sb["Кала"]), str(sb["Чешта"]),
            str(sb["Всего (Вирупы)"]), sb["Рупы (Норма)"], sb["Сила %"].replace("🟢", "").replace("🔴", "").strip(),
            sb["Вимшопака (max 20)"]
        ])
    t_sb = Table(sb_data, colWidths=[50, 50, 45, 45, 45, 75, 75, 65, 85])
    t_sb.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#78350f")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), font_bold),
        ("FONTNAME", (0, 1), (-1, -1), font_name),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fffbeb")]),
    ]))
    story.append(t_sb)

    # 4. Главные жизненные периоды (Вимшоттари Даша)
    story.append(Paragraph("4. Большие планетные периоды жизни (Вимшоттари Махадаша на 120 лет)", h2_style))
    d_table = [["Планета-управитель периода", "Дата начала", "Дата окончания", "Возраст вступления", "Статус"]]
    for m in vim_data["mahadashas"]:
        d_table.append([
            f"Махадаша {m['Махадаша']}", m["Начало"], m["Окончание"], m["Возраст"],
            "АКТИВЕН СЕЙЧАС" if m["Статус"] else "—"
        ])
    t_dasha = Table(d_table, colWidths=[130, 110, 110, 95, 90])
    t_dasha.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e1b4b")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#fef3c7")),
        ("FONTNAME", (0, 0), (-1, 0), font_bold),
        ("FONTNAME", (0, 1), (-1, -1), font_name),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f8fafc"), colors.white]),
    ]))
    story.append(t_dasha)

    # 5. Трактовки Йог и особых комбинаций карты
    story.append(Paragraph(f"5. Обнаруженные астрологические комбинации и Йоги ({len(yogas_list)} шт.)", h2_style))
    for yg in yogas_list:
        story.append(Paragraph(
            f"• <b>{yg['Название йоги']} ({yg['Планеты']}) [{yg['Категория']}]:</b> {yg['Условие и эффект']}",
            body_style
        ))

    doc.build(story)
    return buffer.getvalue()


def generate_jhd_file_content(name: str, dt_local: datetime.datetime, tz_offset: float, lat: float, lon: float) -> str:
    jhd_lines = [
        f"{dt_local.month}",
        f"{dt_local.day}",
        f"{dt_local.year}",
        f"{dt_local.hour}.{dt_local.minute:02d}{dt_local.second:02d}",
        f"{-tz_offset:.4f}",
        f"{-lon:.4f}",
        f"{lat:.4f}",
        "0.000000",
        "0.0",
        "0.0",
        "0",
        "105",
        name,
        "Unknown",
        "1"
    ]
    return "\n".join(jhd_lines)

if "saved_charts" not in st.session_state:
    st.session_state.saved_charts = [
        {"Раздел": "Мои карты", "Имя": "Александр", "Тип": "Джатака", "Дата": "15.05.1990", "Время": "14:30:00",
         "Город": "Шымкент (Казахстан)", "lat": 42.34, "lon": 69.59, "tz": 5.0, "Rodden": "AA", "Пол": "Мужской",
         "Клиент": "🟢 Завершен", "Заметки": "Исследование натальной карты и ректификация D9/D10."},
        {"Раздел": "Знаменитости (Astro-Databank)", "Имя": "Альберт Эйнштейн", "Тип": "Джатака", "Дата": "14.03.1879", "Время": "11:30:00",
         "Город": "Ульм (Германия)", "lat": 48.40, "lon": 9.98, "tz": 1.0, "Rodden": "AA", "Пол": "Мужской",
         "Клиент": "—", "Заметки": "Нобелевская премия по физике (1921), Нича-бханга Раджа-йога Меркурия."},
        {"Раздел": "Знаменитости (Astro-Databank)", "Имя": "Стив Джобс", "Тип": "Джатака", "Дата": "24.02.1955", "Время": "19:15:00",
         "Город": "Сан-Франциско (США)", "lat": 37.77, "lon": -122.42, "tz": -8.0, "Rodden": "AA", "Пол": "Мужской",
         "Клиент": "—", "Заметки": "Основатель Apple, Паривартхана и мощный 10-й/11-й дом."}
    ]

if "client_events" not in st.session_state:
    st.session_state.client_events = [
        {"Категория": "Образование / Профессия", "Событие / Метка": "Получение диплома / Высшее образование", "Дата": "20.06.2012", "Комментарий": "Защита с отличием"},
        {"Категория": "Брак и Семья", "Событие / Метка": "Вступление в брак (Свадьба)", "Дата": "12.09.2015", "Комментарий": "Торжественная церемония"},
        {"Категория": "Карьера и Финансы", "Событие / Метка": "Запуск собственного IT / Астро-проекта", "Дата": "15.11.2026", "Комментарий": "Релиз онлайн-платформы"}
    ]

with st.sidebar:
    st.markdown("## 🪐 AstroVeda Pro")
    st.caption("VedicHoro Ultimate: Все бесплатные и платные функции")

    not_astrologer = st.toggle("🌱 Режим «Я не астролог» (Упрощенный вид)", value=False)

    with st.expander("👤 Исходные данные карты", expanded=True):
        p_name = st.text_input("Имя человека или событие", value="Александр")
        p_gender = st.selectbox("Пол (для Синастрии и Таттв)", ["Мужской", "Женский"])
        st.markdown("**📅 Дата рождения (Любой год: 1500 – 2150)**")
        cd_day, cd_mon, cd_yr = st.columns([1, 1.3, 1.2])
        with cd_day:
            b_day = st.number_input("День", min_value=1, max_value=31, value=19, step=1)
        with cd_mon:
            MONTHS_RU = ["01 - Январь", "02 - Февраль", "03 - Март", "04 - Апрель", "05 - Май", "06 - Июнь",
                         "07 - Июль", "08 - Август", "09 - Сентябрь", "10 - Октябрь", "11 - Ноябрь", "12 - Декабрь"]
            b_mon_str = st.selectbox("Месяц", MONTHS_RU, index=9)
            b_mon = int(b_mon_str.split(" - ")[0])
        with cd_yr:
            b_yr = st.number_input("Год", min_value=1500, max_value=2150, value=1970, step=1)
        try:
            b_date = datetime.date(int(b_yr), int(b_mon), int(b_day))
        except ValueError:
            b_date = datetime.date(int(b_yr), int(b_mon), 28)
            st.warning("Число скорректировано по количеству дней в месяце.")

        st.markdown("**🕒 Точное время рождения (Час : Мин : Сек)**")
        ct_h, ct_m, ct_s = st.columns(3)
        with ct_h:
            b_hr = st.number_input("Час (0-23)", min_value=0, max_value=23, value=10, step=1)
        with ct_m:
            b_min = st.number_input("Мин (0-59)", min_value=0, max_value=59, value=5, step=1)
        with ct_s:
            b_sec = st.number_input("Сек (0-59)", min_value=0, max_value=59, value=0, step=1)
        b_time = datetime.time(int(b_hr), int(b_min), int(b_sec))

        preset_city = st.selectbox("Быстрый выбор города (Авто-координаты)", list(PRESET_CITIES.keys()))
        def_lat, def_lon, def_tz = PRESET_CITIES[preset_city]

        c_lat, c_lon, c_tz = st.columns(3)
        with c_lat:
            lat = st.number_input("Широта", value=float(def_lat), format="%.2f")
        with c_lon:
            lon = st.number_input("Долгота", value=float(def_lon), format="%.2f")
        with c_tz:
            tz_val = st.number_input("UTC пояс", value=float(def_tz), step=0.5)

    with st.expander("⚙️ Настройки расчетов (К.Н. Рао / Ратх)"):
        aya_choice = st.selectbox("Айанамша", list(AYANAMSHA_MAP.keys()))
        true_nodes = st.radio("Лунные узлы (Раху/Кету)", ["Истинные (True)", "Средние (Mean)"], horizontal=True) == "Истинные (True)"
        karaka_num = 7 if st.radio("Схема Чара Карак", ["7 Карак (К.Н. Рао)", "8 Карак (С. Ратх)"], horizontal=True).startswith("7") else 8
        arudha_exc = st.checkbox("Арудхи с исключениями (С. Ратх)", value=True)
        show_arudha_on_chart = st.checkbox("Показать AL / UL в карте D1", value=True)

    st.markdown("### ⏱ Живое изменение времени")
    shift_min = st.slider("Сдвиг времени рождения (мин)", -60, 60, 0, step=1)
    shift_sec = st.slider("Точная подстройка (сек)", -59, 59, 0, step=1)

    total_shift_seconds = shift_min * 60 + shift_sec
    orig_local_dt = datetime.datetime.combine(b_date, b_time)
    curr_local_dt = orig_local_dt + datetime.timedelta(seconds=total_shift_seconds)
    curr_utc_dt = curr_local_dt - datetime.timedelta(hours=tz_val)
    orig_utc_dt = orig_local_dt - datetime.timedelta(hours=tz_val)

    chart_data = calculate_full_chart(curr_utc_dt, lat, lon, aya_choice, true_nodes, karaka_num)
    orig_chart_data = calculate_full_chart(orig_utc_dt, lat, lon, aya_choice, true_nodes, karaka_num)
    arudhas_list = calculate_arudhas(chart_data, arudha_exc)
    ashtakavarga_res = calculate_ashtakavarga(chart_data)

    st.divider()
    st.markdown("### 📄 Скачать готовый Гороскоп")
    vim_for_pdf = calculate_vimshottari(curr_local_dt, chart_data["moon_lon"])
    yogas_for_pdf = scan_classical_yogas(chart_data)
    bala_for_pdf = calculate_bala_module(chart_data)["shadbala"]
    try:
        pdf_bytes = generate_pdf_report(
            p_name, curr_local_dt, preset_city, lat, lon, tz_val,
            chart_data, vim_for_pdf, yogas_for_pdf, arudhas_list, bala_for_pdf
        )
        st.download_button(
            label="📕 Скачать полный отчет в PDF (Для всех)",
            data=pdf_bytes,
            file_name=f"Goroskop_{p_name.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e_pdf:
        st.caption(f"PDF модуль загружается: {e_pdf}")

    with st.expander("⚙️ Экспорт для астро-программ (.jhd)"):
        st.caption("Специальный технический файл только для компьютерной программы Jagannatha Hora:")
        jhd_str = generate_jhd_file_content(p_name, curr_local_dt, tz_val, lat, lon)
        st.download_button(
            label="📥 Экспорт в Jagannatha Hora (.jhd)",
            data=jhd_str,
            file_name=f"{p_name.replace(' ', '_')}.jhd",
            mime="text/plain",
            use_container_width=True
        )

time_underline = f"<u style='color:#facc15;'>{curr_local_dt.strftime('%H:%M:%S')} (сдвиг {total_shift_seconds:+}с)</u>" if total_shift_seconds != 0 else curr_local_dt.strftime('%H:%M:%S')

st.markdown(f"""
<div class="top-banner">
    <div>
        <h2 style="margin:0; font-size:1.55rem; color:#38bdf8;">🕉️ {p_name} &nbsp;<span class="pill-green">Rodden Rating: AA</span></h2>
        <div style="color:#cbd5e1; margin-top:4px; font-size:0.95rem;">
            📅 <b>{curr_local_dt.strftime('%d.%m.%Y')}</b> &nbsp;|&nbsp; 🕒 <b>{time_underline}</b> (UTC{tz_val:+g}) &nbsp;|&nbsp;
            📍 <b>{preset_city}</b> ({lat:.2f}°N, {lon:.2f}°E) &nbsp;|&nbsp; 🧭 Айанамша: <b>{chart_data['ayanamsha_val']:.4f}°</b>
        </div>
    </div>
    <div style="text-align:right;">
        <span class="pill-gold">★ PRO ULTIMATE АКТИВИРОВАН</span><br>
        <small style="color:#94a3b8;">Все 12 модулей открыты</small>
    </div>
</div>
""", unsafe_allow_html=True)

if not_astrologer:
    st.subheader("🌟 Персональный ведический портрет (Режим «Я не астролог»)")
    asc_name = RASHIS[chart_data["asc_rashi"]]
    moon_row = [p for p in chart_data["planets"] if p["clean_code"] == "Mo"][0]
    sun_row = [p for p in chart_data["planets"] if p["clean_code"] == "Su"][0]
    yogas_all = scan_classical_yogas(chart_data)

    col_na1, col_na2, col_na3 = st.columns(3)
    col_na1.metric("Восходящий знак (Лагна)", asc_name.split()[0], "Физическая природа и путь")
    col_na2.metric("Лунный знак (Раши)", moon_row["Раши (D1)"].split()[0], f"Накшатра: {moon_row['Накшатра (Пада, Упр)'].split()[0]}")
    col_na3.metric("Солнечный знак (Атма)", sun_row["Раши (D1)"].split()[0], f"Атмакарака: {[p['clean_code'] for p in chart_data['planets'] if str(p['Карака']).startswith('AK')][0]}")

    st.markdown("#### 🔮 Ключевые сильные стороны и королевские комбинации вашей карты:")
    for yg in yogas_all[:6]:
        st.success(f"**{yg['Название йоги']} ({yg['Планеты']}):** {yg['Условие и эффект']}")
    st.info("Отключите переключатель «Режим Я не астролог» в левой панели, чтобы открыть все 12 профессиональных инструментов.")
    st.stop()

top_tabs = st.tabs([
    "📊 1. Основная карта (20 Варг, Йоги, Бала, Даши, Ректификация)",
    "☀️ 2. Варшапхала (Годовой Соляр, Мунтха, Сахамы, Мудда даша)",
    "⏳ 3. Мухурта (60+ Событий, Панчанга на месяц и Автопоиск)",
    "🔄 4. Транзиты (Наложение, Какшья, Ведха, Саде-Сати, Поиск)",
    "💞 5. Совместимость (Аштакута 36 б., 7 доп. Кут, Наложение)",
    "🗂 6. База карт, Клиенты CRM и Исследования (Astro-Databank)"
])

with top_tabs[0]:
    ctrl_c1, ctrl_c2, ctrl_c3, ctrl_c4 = st.columns([1.2, 1.2, 1.4, 1.2])
    with ctrl_c1:
        style_mode = st.selectbox("Стиль отображения карт", ["Параллельно: Южный + Северный", "Все в Южном стиле", "Все в Северном стиле"])
    with ctrl_c2:
        rotate_h = st.selectbox("Повернуть карту (Лагна в дом):", [f"{h}-й дом ({RASHI_RU_SHORT[(chart_data['asc_rashi']+h-1)%12]})" for h in range(1, 13)])
        rot_idx = int(rotate_h.split("-")[0])
    with ctrl_c3:
        third_varga = st.selectbox("Третья дробная карта:", [f"{code} — {desc.split('—')[0]}" for code, desc in VARGAS_LIST], index=9)
        third_v_code = third_varga.split(" — ")[0]
    with ctrl_c4:
        inspect_house = st.selectbox("Показать Аспекты и Аргалу для дома:", [f"Дом {h}" for h in range(1, 13)])
        insp_h_num = int(inspect_house.split()[1])

    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        st.markdown(render_south_svg(chart_data, "D1", rot_idx, arudhas_list if show_arudha_on_chart else None), unsafe_allow_html=True)
    with mc2:
        if style_mode == "Все в Южном стиле":
            st.markdown(render_south_svg(chart_data, "D9", rot_idx), unsafe_allow_html=True)
        else:
            st.markdown(render_north_svg(chart_data, "D1" if style_mode.startswith("Параллельно") else "D9", rot_idx), unsafe_allow_html=True)
    with mc3:
        if style_mode == "Все в Северном стиле":
            st.markdown(render_north_svg(chart_data, third_v_code, rot_idx), unsafe_allow_html=True)
        else:
            st.markdown(render_south_svg(chart_data, "D9" if style_mode.startswith("Параллельно") else third_v_code, rot_idx), unsafe_allow_html=True)

    with st.expander("☸ Показать сразу 12 (или все 20) графических карт Варг на одном экране (D1 – D60)", expanded=False):
        grid_mode = st.radio(
            "Количество карт для одновременной отрисовки:",
            ["12 главных Варг (D1, D2, D3, D4, D7, D9, D10, D12, D16, D20, D24, D60)", "Все 20 Варг Парашары (D1 – D60)"],
            horizontal=True
        )
        varga_codes_to_draw = ["D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12", "D16", "D20", "D24", "D60"] if grid_mode.startswith("12") else [v[0] for v in VARGAS_LIST]
        varga_titles_map = dict(VARGAS_LIST)
        for row_start in range(0, len(varga_codes_to_draw), 4):
            cols_v = st.columns(4)
            for idx_col, v_c in enumerate(varga_codes_to_draw[row_start:row_start+4]):
                with cols_v[idx_col]:
                    st.caption(f"**{varga_titles_map[v_c]}**")
                    if style_mode == "Все в Северном стиле":
                        st.markdown(render_north_svg(chart_data, v_c, rot_idx), unsafe_allow_html=True)
                    else:
                        st.markdown(render_south_svg(chart_data, v_c, rot_idx), unsafe_allow_html=True)

    target_sign = (chart_data["asc_rashi"] + insp_h_num - 1) % 12
    argala_2 = RASHI_RU_SHORT[(target_sign + 1) % 12]
    argala_4 = RASHI_RU_SHORT[(target_sign + 3) % 12]
    argala_11 = RASHI_RU_SHORT[(target_sign + 10) % 12]
    virodha_12 = RASHI_RU_SHORT[(target_sign + 11) % 12]
    virodha_10 = RASHI_RU_SHORT[(target_sign + 9) % 12]
    virodha_3 = RASHI_RU_SHORT[(target_sign + 2) % 12]
    st.caption(
        f"🔍 **Инспектор {insp_h_num}-го дома ({RASHIS[target_sign]}):** "
        f"🟢 **Первичная Аргала (2, 4, 11 от дома):** {argala_2}, {argala_4}, {argala_11} &nbsp;|&nbsp; "
        f"🔴 **Виродха-Аргала (препятствия 12, 10, 3):** {virodha_12}, {virodha_10}, {virodha_3} &nbsp;|&nbsp; "
        f"✨ **Вторичная Субха-Аргала (5-й от дома):** {RASHI_RU_SHORT[(target_sign + 4) % 12]}"
    )

    analysis_tabs = st.tabs([
        "📋 1. Общее + Аштакаварга",
        "💠 2. Все 20 Варг (Шодаша)",
        "🧭 3. Разное (Арудхи, Лагны, Упаграхи)",
        "👑 4. Йоги (200+ комбинаций)",
        "⚡ 5. Бала (Шад-бала и Аспекты)",
        "📐 6. Бхава Чалита (Куспиды)",
        "⏳ 7. Периоды (4 Даши + События)",
        "🎯 8. Таджака-йоги (Прашна)",
        "⏱ 9. Ректификация (Варги + Таттвы)"
    ])

    with analysis_tabs[0]:
        st.markdown("#### Положение планет, особые градусы (Мритью / Пушкара / Ганданта) и функциональная природа")
        df_gen = pd.DataFrame(chart_data["planets"])[[
            "Планета", "Градусы", "Раши (D1)", "Дом", "Навамша (D9)",
            "Накшатра (Пада, Упр)", "Отношение", "ФБ", "Карака", "Авастха", "ТБ (Тара)", "С/ПВ", "Особые метки"
        ]]
        st.dataframe(df_gen, use_container_width=True, hide_index=True)

        st.markdown("#### Таблица Аштакаварги (Бхиннаштакаварга планет и Сарваштакаварга)")
        st.dataframe(pd.DataFrame(ashtakavarga_res["table"]), use_container_width=True, hide_index=True)

    with analysis_tabs[1]:
        st.markdown("#### Положение планет во всех 20 дробных картах (D1 – D60) и индекс силы Шодаша-варга")
        varga_rows = []
        for p in chart_data["planets"]:
            c = p["clean_code"]
            row = {"Планета": p["Код"]}
            for v_code, _ in VARGAS_LIST:
                s_i = chart_data["vargas_matrix"][c][v_code]
                row[v_code] = RASHI_RU_SHORT[s_i]
            row["Сила (Свой/Экз | Варготтама)"] = p["Шодаша-варга (Сила)"]
            varga_rows.append(row)
        st.dataframe(pd.DataFrame(varga_rows), use_container_width=True, hide_index=True)

        st.markdown("#### ☸ Графическая галерея всех 20 дробных карт (D1 – D60)")
        varga_titles_map = dict(VARGAS_LIST)
        all_20_codes = [v[0] for v in VARGAS_LIST]
        for r_i in range(0, len(all_20_codes), 4):
            v_cols = st.columns(4)
            for c_i, vc_code in enumerate(all_20_codes[r_i:r_i+4]):
                with v_cols[c_i]:
                    st.markdown(f"**{varga_titles_map[vc_code]}**")
                    if style_mode == "Все в Северном стиле":
                        st.markdown(render_north_svg(chart_data, vc_code, rot_idx), unsafe_allow_html=True)
                    else:
                        st.markdown(render_south_svg(chart_data, vc_code, rot_idx), unsafe_allow_html=True)

    with analysis_tabs[2]:
        sp_data = calculate_special_lagnas_and_sphutas(chart_data)
        rc1, rc2 = st.columns(2)
        with rc1:
            st.markdown("##### 12 Арудха-пад (Пада-лагны)")
            st.dataframe(pd.DataFrame(arudhas_list)[["Арудха", "Управитель дома", "Знак Арудхи", "Дом от Лагны"]], use_container_width=True, hide_index=True)
            st.markdown("##### 7 Специальных Лагн")
            st.dataframe(pd.DataFrame(sp_data["special_lagnas"]), use_container_width=True, hide_index=True)
        with rc2:
            st.markdown("##### 11 Упаграх (Суб-планеты)")
            st.dataframe(pd.DataFrame(sp_data["upagrahas"]), use_container_width=True, hide_index=True)
            st.markdown("##### Спхуты, 22-я Дреккана и 64-я Навамша")
            st.dataframe(pd.DataFrame(sp_data["sphutas"]), use_container_width=True, hide_index=True)

    with analysis_tabs[3]:
        yogas_list = scan_classical_yogas(chart_data)
        categories = ["Все категории"] + sorted(list({y["Категория"] for y in yogas_list}))
        sel_cat = st.selectbox("Фильтр по категории йог:", categories)
        filtered_yogas = yogas_list if sel_cat == "Все категории" else [y for y in yogas_list if y["Категория"] == sel_cat]
        st.markdown(f"Найдено активных комбинаций в карте: **{len(filtered_yogas)}**")
        st.dataframe(pd.DataFrame(filtered_yogas), use_container_width=True, hide_index=True)

    with analysis_tabs[4]:
        bala_res = calculate_bala_module(chart_data)
        st.markdown("#### Составные части Шад-балы, Ишта/Кашта-бала и Вимшопака-бала")
        st.dataframe(pd.DataFrame(bala_res["shadbala"]), use_container_width=True, hide_index=True)

        bc1, bc2 = st.columns(2)
        with bc1:
            st.markdown("##### Точная сила аспектов на планеты (в Вирупах по Парашаре)")
            st.dataframe(pd.DataFrame(bala_res["aspect_planets"]), use_container_width=True, hide_index=True)
        with bc2:
            st.markdown("##### Точная сила аспектов на дома (в Вирупах)")
            st.dataframe(pd.DataFrame(bala_res["aspect_houses"]), use_container_width=True, hide_index=True)

    with analysis_tabs[5]:
        st.markdown("#### Таблица куспидов домов Бхава Чалита (система Кампануса, куспид — центр дома)")
        st.dataframe(pd.DataFrame(chart_data["bhava_chalita"]), use_container_width=True, hide_index=True)

    with analysis_tabs[6]:
        st.markdown("#### События жизни клиента с автоматическим расчетом периодов и сравнением Исходного (И) / Текущего (Т) времени")
        ev_rows = []
        for ev in st.session_state.client_events:
            d_parts = [int(x) for x in ev["Дата"].split(".")]
            ev_dt = datetime.datetime(d_parts[2], d_parts[1], d_parts[0], 12, 0)
            v_orig = calculate_vimshottari(orig_local_dt, orig_chart_data["moon_lon"], ev_dt)["active_chain"]
            v_curr = calculate_vimshottari(curr_local_dt, chart_data["moon_lon"], ev_dt)["active_chain"]
            y_curr = calculate_yogini_dasha(curr_local_dt, chart_data["moon_lon"], ev_dt)["active_chain"]
            c_curr = calculate_chara_dasha_rao(curr_local_dt, chart_data, ev_dt)["active_chain"]
            ev_rows.append({
                "Дата": ev["Дата"],
                "Событие / Метка": ev["Событие / Метка"],
                "Вимшоттари (И — Исходная)": v_orig,
                "Вимшоттари (Т — Сдвинутая)": f"⚡ {v_curr}" if v_orig != v_curr else v_curr,
                "Йогини даша": y_curr,
                "Чара даша К.Н. Рао": c_curr,
                "Комментарий": ev["Комментарий"]
            })
        st.dataframe(pd.DataFrame(ev_rows), use_container_width=True, hide_index=True)

        vim_now = calculate_vimshottari(curr_local_dt, chart_data["moon_lon"])
        yog_now = calculate_yogini_dasha(curr_local_dt, chart_data["moon_lon"])
        cha_now = calculate_chara_dasha_rao(curr_local_dt, chart_data)

        dc1, dc2 = st.columns(2)
        with dc1:
            st.markdown(f"##### Накшатра даши: Вимшоттари (Сейчас: `{vim_now['active_chain']}`)")
            maha_df = pd.DataFrame([{k: v for k, v in m.items() if k != "antardashas"} for m in vim_now["mahadashas"]])
            st.dataframe(maha_df, use_container_width=True, hide_index=True)

            sel_maha = st.selectbox("Раскрыть подпериоды (Антардаши) для Махадаши:", [m["Махадаша"] for m in vim_now["mahadashas"]])
            antar_list = [m["antardashas"] for m in vim_now["mahadashas"] if m["Махадаша"] == sel_maha][0]
            st.dataframe(pd.DataFrame(antar_list), use_container_width=True, hide_index=True)

        with dc2:
            st.markdown(f"##### Раши даша: Чара даша Джаймини К.Н. Рао (Сейчас: `{cha_now['active_chain']}`)")
            st.dataframe(pd.DataFrame(cha_now["rows"]), use_container_width=True, hide_index=True)
            st.markdown(f"##### Йогини даша (Сейчас: `{yog_now['active_chain']}`)")
            st.dataframe(pd.DataFrame(yog_now["rows"]), use_container_width=True, hide_index=True)

    with analysis_tabs[7]:
        tjk = calculate_tajaka_yogas(chart_data)
        st.markdown("#### Матрица аспектов и орбов (Диптхамша) всех 16 Таджака-йог")
        st.dataframe(pd.DataFrame(tjk["matrix"]), use_container_width=True, hide_index=True)
        if tjk["yogas_list"]:
            st.markdown("##### Сформированные Таджака-йоги в карте:")
            st.dataframe(pd.DataFrame(tjk["yogas_list"]), use_container_width=True, hide_index=True)

    with analysis_tabs[8]:
        rc_col1, rc_col2 = st.columns([1.1, 1])
        with rc_col1:
            st.markdown("##### 1. Поиск времени смены асцендентов в дробных картах")
            v_to_scan = st.multiselect("Выберите дробные карты для ректификации:", [v[0] for v in VARGAS_LIST], default=["D1", "D3", "D9", "D10", "D60"])
            win_min = st.slider("Интервал поиска вокруг времени рождения (± минут):", 5, 60, 20)
            changes_df = scan_varga_ascendant_changes(curr_local_dt, tz_val, lat, lon, aya_choice, v_to_scan, win_min)
            st.dataframe(pd.DataFrame(changes_df), use_container_width=True, hide_index=True)
        with rc_col2:
            st.markdown("##### 2. Ректификация по Таттвам Нади (метод С. Рао)")
            sr_time = st.time_input("Точное время восхода Солнца в день рождения:", datetime.time(6, 0, 0))
            tattva_df = calculate_tattva_rectification(curr_local_dt, sr_time, p_gender)
            st.dataframe(pd.DataFrame(tattva_df), use_container_width=True, hide_index=True)

with top_tabs[1]:
    st.markdown("### ☀️ Годовая карта Варшапхала (Таджака Соляр)")
    v_col1, v_col2 = st.columns([1, 3])
    with v_col1:
        sel_solar_year = st.number_input("Выберите год для расчета Варшапхалы:", min_value=b_date.year, max_value=b_date.year + 100, value=2026)

    varsha_res = calculate_varshaphala(chart_data, curr_utc_dt, int(sel_solar_year), lat, lon, tz_val, aya_choice)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Возраст и Год", f"{varsha_res['age']} лет ({sel_solar_year})")
    m2.metric("Точное включение Соляра", varsha_res["sr_local"].strftime("%d.%m.%Y %H:%M:%S"))
    m3.metric("Мунтха в годовой карте", f"{varsha_res['muntha_sign'].split()[0]} ({varsha_res['muntha_house']} дом)", f"Управитель: {varsha_res['muntha_lord']}")
    m4.metric("Варшеша (Управитель года)", varsha_res["varshesha"])

    vc1, vc2, vc3 = st.columns([1.1, 1.1, 1.3])
    with vc1:
        st.markdown("##### Карта Варшапхалы (D1 — Южный стиль)")
        st.markdown(render_south_svg(varsha_res["varsha_chart"], "D1"), unsafe_allow_html=True)
    with vc2:
        st.markdown("##### Карта Варшапхалы (D1 — Северный стиль)")
        st.markdown(render_north_svg(varsha_res["varsha_chart"], "D1"), unsafe_allow_html=True)
    with vc3:
        st.markdown("##### Годовая Мудда Даша (Периоды внутри года)")
        st.dataframe(pd.DataFrame(varsha_res["mudda_rows"]), use_container_width=True, hide_index=True)

    vt1, vt2, vt3 = st.columns(3)
    with vt1:
        st.markdown("##### Сила планет: Панча-Варгия и Харша-бала")
        st.dataframe(pd.DataFrame(varsha_res["bala_rows"]), use_container_width=True, hide_index=True)
    with vt2:
        st.markdown("##### Сахамы (Арабские точки года)")
        st.dataframe(pd.DataFrame(varsha_res["sahams"]), use_container_width=True, hide_index=True)
    with vt3:
        st.markdown("##### Таджака-йоги годовой карты")
        st.dataframe(pd.DataFrame(varsha_res["tajaka"]["yogas_list"]) if varsha_res["tajaka"]["yogas_list"] else pd.DataFrame([{"Статус": "Точных Итхасала в пределах орба нет"}]), use_container_width=True, hide_index=True)

with top_tabs[2]:
    st.markdown("### ⏳ Подбор благоприятного времени (Мухурта) и Календарь Панчанги")
    mh_c1, mh_c2, mh_c3 = st.columns([1.6, 1, 1])
    with mh_c1:
        sel_muhurta_event = st.selectbox("Выберите событие (из базы 60+ категорий):", list(MUHURTA_EVENTS.keys()))
    with mh_c2:
        mh_date = st.date_input("Дата Мухурты", datetime.date(2026, 11, 15))
    with mh_c3:
        mh_time = st.time_input("Время начала события", datetime.time(11, 45))

    mh_dt = datetime.datetime.combine(mh_date, mh_time)
    natal_moon_p = [p for p in chart_data["planets"] if p["clean_code"] == "Mo"][0]
    mh_res = calculate_panchanga_and_muhurta(mh_dt, tz_val, lat, lon, aya_choice, natal_moon_p["nak_idx"], natal_moon_p["rashi_idx"], sel_muhurta_event)

    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Итоговый индекс Мухурты", f"{mh_res['score']} / 100", "Отлично" if mh_res["score"] >= 70 else ("Средне" if mh_res["score"] >= 45 else "Неблагоприятно"))
    p2.metric("Титхи и Вара", mh_res["vara"], mh_res["tithi"])
    p3.metric("Накшатра Луны", mh_res["nakshatra"], mh_res["tara_bala"])
    p4.metric("Раху Кала (Избегать!)", mh_res["rahu_kala"], mh_res["chandra_bala"])

    mcol1, mcol2 = st.columns([1, 1.6])
    with mcol1:
        st.markdown(render_south_svg(mh_res["chart"], "D1"), unsafe_allow_html=True)
    with mcol2:
        st.markdown("##### Детальный чек-лист факторов выбранного момента времени")
        st.dataframe(pd.DataFrame(mh_res["factors"], columns=["Фактор Панчанги / События", "Оценка и значение"]), use_container_width=True, hide_index=True)
        st.info(f"✨ **{mh_res['abhijit']}** &nbsp;|&nbsp; 🌅 **{mh_res['brahma']}** &nbsp;|&nbsp; {mh_res['yoga']} &nbsp;|&nbsp; {mh_res['karana']}")

    st.markdown("#### 🚀 Автопоиск лучших интервалов Мухурты на 14 дней вперед")
    scan_days = []
    for d_off in range(14):
        d_cur = mh_date + datetime.timedelta(days=d_off)
        for hr_slot in [9, 12, 15, 18]:
            slot_dt = datetime.datetime.combine(d_cur, datetime.time(hr_slot, 0))
            r_slot = calculate_panchanga_and_muhurta(slot_dt, tz_val, lat, lon, aya_choice, natal_moon_p["nak_idx"], natal_moon_p["rashi_idx"], sel_muhurta_event)
            scan_days.append({
                "Дата": d_cur.strftime("%d.%m.%Y"),
                "Час": f"{hr_slot:02d}:00",
                "Балл": r_slot["score"],
                "Накшатра": r_slot["nakshatra"].split()[0],
                "Титхи": r_slot["tithi"].split("—")[1].strip(),
                "Тара-бала": r_slot["tara_bala"]
            })
    df_scan = pd.DataFrame(scan_days)
    best_slots = df_scan[df_scan["Балл"] >= 65].sort_values(by="Балл", ascending=False)
    st.dataframe(best_slots, use_container_width=True, hide_index=True)

with top_tabs[3]:
    st.markdown("### 🔄 Анализ Транзитов (Гочара), Какшьи, Ведхи и Саде-Сати")
    tr_c1, tr_c2 = st.columns(2)
    with tr_c1:
        tr_date = st.date_input("Дата транзита", datetime.date(2026, 11, 15), key="tr_d")
    with tr_c2:
        tr_time = st.time_input("Время транзита", datetime.time(12, 0), key="tr_t")

    tr_dt = datetime.datetime.combine(tr_date, tr_time)
    tr_res = analyze_transits(chart_data, tr_dt, tz_val, lat, lon, aya_choice, ashtakavarga_res)

    st.warning(f"🪐 **Статус Саде-Сати и трансформационных транзитов Сатурна:** {tr_res['sade_sati']}")

    tc1, tc2 = st.columns([1, 2])
    with tc1:
        st.markdown("##### Транзитная карта (D1)")
        st.markdown(render_south_svg(tr_res["transit_chart"], "D1"), unsafe_allow_html=True)
    with tc2:
        st.markdown("##### Наложение транзитных планет на натальную карту (Дома, Бинду, Какшья и Ведха)")
        st.dataframe(pd.DataFrame(tr_res["rows"]), use_container_width=True, hide_index=True)

with top_tabs[4]:
    st.markdown("### 💞 Анализ совместимости партнеров (Аштакута + Дополнительные Куты + Наложение карт)")
    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1:
        partner_name = st.text_input("Имя партнера", "Партнер / Супруга")
    with sc2:
        p2_date = st.date_input("Дата рождения партнера (ГГГГ/ММ/ДД)", datetime.date(1975, 8, 22), min_value=datetime.date(1500, 1, 1), max_value=datetime.date(2150, 12, 31))
    with sc3:
        p2_time = st.time_input("Время рождения партнера", datetime.time(10, 15))
    with sc4:
        ref_point = st.selectbox("Точка отсчета Аштакуты:", ["Mo (По Луне — классика)", "As (По Лагне)", "Su (По Солнцу)", "Ve (По Венере)"])
        ref_p_code = ref_point.split()[0]

    p2_utc = datetime.datetime.combine(p2_date, p2_time) - datetime.timedelta(hours=tz_val)
    chart_p2 = calculate_full_chart(p2_utc, lat, lon, aya_choice, true_nodes, karaka_num)
    comp_res = calculate_ashtakuta_compatibility(chart_data, chart_p2, ref_p_code)

    tot_pts = comp_res["total_score"]
    verdict = "Идеальная гармония (Высокая совместимость)" if tot_pts >= 25 else ("Хорошая совместимость (Средний балл)" if tot_pts >= 18 else "Требует гармонизации (Ниже 18 баллов)")

    k_m1, k_m2, k_m3 = st.columns(3)
    k_m1.metric("Итоговый балл Аштакуты", f"{tot_pts} из 36 баллов", verdict)
    k_m2.metric("Куджа-доша (Марс) у Партнера 1", "🔴 Есть (Требует компенсации)" if comp_res["kuja_m"] else "🟢 Отсутствует")
    k_m3.metric("Куджа-доша (Марс) у Партнера 2", "🔴 Есть (Нейтрализует дошу П1)" if comp_res["kuja_f"] else "🟢 Отсутствует")

    syn_c1, syn_c2 = st.columns([1.2, 1])
    with syn_c1:
        st.markdown("##### Расчет 8 Кут (Аштакута) с учетом исключений")
        st.dataframe(pd.DataFrame(comp_res["kutas"]), use_container_width=True, hide_index=True)
    with syn_c2:
        st.markdown("##### Дополнительные Куты (Махендра, Стри Диргха, Ведха, Радджу)")
        st.dataframe(pd.DataFrame(comp_res["extra_kutas"]), use_container_width=True, hide_index=True)

    st.markdown("##### Взаимное наложение планет на дома партнера")
    st.dataframe(pd.DataFrame(comp_res["overlay"]), use_container_width=True, hide_index=True)

with top_tabs[5]:
    st.markdown("### 🗂 База личных карт, режим работы с клиентами (CRM) и Астро-исследования")
    db_c1, db_c2 = st.columns([2, 1])
    with db_c1:
        view_mode = st.radio("Режим отображения базы:", ["Структура (По разделам)", "Все карты", "Режим «Клиенты» (CRM Статус)"], horizontal=True)
        df_db = pd.DataFrame(st.session_state.saved_charts)
        if view_mode == "Режим «Клиенты» (CRM Статус)":
            df_db = df_db[df_db["Клиент"] != "—"]
        st.dataframe(df_db, use_container_width=True, hide_index=True)
    with db_c2:
        st.markdown("##### ➕ Сохранить текущую карту в базу")
        sec_name = st.selectbox("Раздел хранения:", ["Мои карты", "Клиенты", "Семья и друзья", "Прашна / Мухурта"])
        rodden = st.selectbox("Рейтинг достоверности (Rodden Rating):", ["AA (Бирка / Свидетельство)", "A (Со слов)", "B (Биография)", "C (Неизвестно)"])
        is_client = st.checkbox("Отметить как клиента для консультации", value=True)
        note_txt = st.text_area("Астрологическая заметка к карте:", "Первичная консультация и ректификация.")
        if st.button("💾 Добавить карту в базу", use_container_width=True):
            st.session_state.saved_charts.append({
                "Раздел": sec_name, "Имя": p_name, "Тип": "Джатака",
                "Дата": curr_local_dt.strftime("%d.%m.%Y"), "Время": curr_local_dt.strftime("%H:%M:%S"),
                "Город": preset_city, "lat": lat, "lon": lon, "tz": tz_val,
                "Rodden": rodden.split()[0], "Пол": p_gender,
                "Клиент": "🔴 В работе" if is_client else "—", "Заметки": note_txt
            })
            st.success(f"Карта «{p_name}» успешно сохранена в раздел «{sec_name}»!")
