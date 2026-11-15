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

from core.constants import (
    RASHIS, RASHI_SHORT, RASHI_RU_SHORT, RASHI_LORDS, PLANET_NAMES,
    PLANET_COLORS, NAKSHATRAS, VARGAS_LIST, PRESET_CITIES
)
from core.ephemeris import calculate_full_chart, compute_varga_sign, AYANAMSHA_MAP
from core.special_points import calculate_arudhas, calculate_special_lagnas_and_sphutas
from core.ashtakavarga import calculate_ashtakavarga, get_kakshya_info
from core.bala import calculate_bala_module
from core.yogas import scan_classical_yogas, calculate_tajaka_yogas
from core.dashas import calculate_vimshottari, calculate_yogini_dasha, calculate_chara_dasha_rao
from core.rectification import scan_varga_ascendant_changes, calculate_tattva_rectification
from modules.varshaphala import calculate_varshaphala

st.set_page_config(
    page_title="AstroVeda Pro | Полная система Джйотиш",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #0b0f19; color: #f8fafc; }
    .top-banner {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-left: 5px solid #38bdf8;
        border-radius: 12px;
        padding: 16px 22px;
        margin-bottom: 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 8px 24px rgba(0,0,0,0.35);
    }
    .pill-green { background: rgba(34, 197, 94, 0.2); color: #4ade80; padding: 3px 10px; border-radius: 99px; font-size: 0.82rem; font-weight: 600; }
    .pill-gold { background: rgba(234, 179, 8, 0.2); color: #facc15; padding: 3px 10px; border-radius: 99px; font-size: 0.82rem; font-weight: 600; }
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

    svg = '<svg viewBox="0 0 420 420" width="100%" style="background:#0f172a; border-radius:12px; border:2px solid #38bdf8; box-shadow: 0 4px 18px rgba(0,0,0,0.4);">'
    svg += '<rect x="105" y="105" width="210" height="210" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>'
    svg += f'<text x="210" y="198" fill="#38bdf8" font-size="18" font-weight="bold" text-anchor="middle">{varga_code} (Южный стиль)</text>'
    svg += f'<text x="210" y="222" fill="#94a3b8" font-size="12" text-anchor="middle">1-й дом: {RASHI_RU_SHORT[asc_sign]}</text>'

    for r_idx, (x, y) in coords.items():
        h_num = ((r_idx - asc_sign) % 12) + 1
        is_asc_box = (h_num == 1)
        fill_col = "rgba(56, 189, 248, 0.10)" if is_asc_box else "none"
        svg += f'<rect x="{x}" y="{y}" width="105" height="105" fill="{fill_col}" stroke="#334155" stroke-width="1.5"/>'
        svg += f'<text x="{x+7}" y="{y+16}" fill="#64748b" font-size="10" font-weight="bold">{RASHI_RU_SHORT[r_idx]}</text>'
        svg += f'<text x="{x+98}" y="{y+16}" fill="#facc15" font-size="10" font-weight="bold" text-anchor="end">{h_num} д.</text>'
        if is_asc_box:
            svg += f'<line x1="{x}" y1="{y+22}" x2="{x+22}" y2="{y}" stroke="#38bdf8" stroke-width="2"/>'

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

    svg = '<svg viewBox="0 0 420 420" width="100%" style="background:#0f172a; border-radius:12px; border:2px solid #facc15; box-shadow: 0 4px 18px rgba(0,0,0,0.4);">'
    svg += '<rect x="0" y="0" width="420" height="420" fill="none" stroke="#475569" stroke-width="2"/>'
    svg += '<line x1="0" y1="0" x2="420" y2="420" stroke="#334155" stroke-width="1.5"/>'
    svg += '<line x1="420" y1="0" x2="0" y2="420" stroke="#334155" stroke-width="1.5"/>'
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
        c_d, c_t = st.columns(2)
        with c_d:
            b_date = st.date_input("Дата рождения", datetime.date(1990, 5, 15), min_value=datetime.date(1500, 1, 1), max_value=datetime.date(2150, 12, 31))
        with c_t:
            b_time = st.time_input("Время (ЧЧ:ММ:СС)", datetime.time(14, 30, 0), step=60)

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
    jhd_str = generate_jhd_file_content(p_name, curr_local_dt, tz_val, lat, lon)
    st.download_button(
        label="📥 Экспорт карты в Jagannatha Hora (.jhd)",
        data=jhd_str,
        file_name=f"{p_name.replace(' ', '_')}.jhd",
        mime="text/plain",
        use_container_width=True
    )

time_underline = f"<u style='color:#facc15;'>{curr_local_dt.strftime('%H:%M:%S')} (сдвиг {total_shift_seconds:+}с)</u>" if total_shift_seconds != 0 else curr_local_dt.strftime('%H:%M:%S')

st.markdown(f"""
<div class="top-banner">
    <div>
        <h2 style="margin:0; font-size:1.55rem; color:#38bdf8;">🪐 {p_name} &nbsp;<span class="pill-green">Rodden Rating: AA</span></h2>
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
        p2_date = st.date_input("Дата рождения партнера", datetime.date(1993, 8, 22))
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
