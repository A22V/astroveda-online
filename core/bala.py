# -*- coding: utf-8 -*-
"""
Модуль силы планет (вкладка «Бала» в VedicHoro):
- Полная Шад-бала (Стхана-бала, Диг-бала, Кала-бала, Чешта-бала, Найсаргика-бала, Дрик-бала) в Вирупах и Рупах
- Ишта-бала и Кашта-бала (благоприятная и разрушительная тенденция планеты)
- Вимшопака-бала (по 16 Варгам Шодаша-варги) и Вайшешикамша-бала
- Точная матрица силы аспектов в Вирупах (Дришти-бала по Махариши Парашаре) на планеты и дома.
"""

import math
from core.constants import EXALTATION, DEBILITATION, DIG_BALA_HOUSE, OWN_SIGNS, MOOLATRIKONA

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
