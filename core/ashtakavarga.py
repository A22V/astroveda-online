# -*- coding: utf-8 -*-
"""
Модуль расчета Аштакаварги (Бхиннаштакаварга для 7 планет, Сарваштакаварга и Какшья)
согласно классическим канонам «Брихат Парашара Хора Шастры».
"""

from core.constants import RASHI_RU_SHORT

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
