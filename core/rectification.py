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
from core.constants import RASHIS, RASHI_RU_SHORT
from core.ephemeris import compute_varga_sign, AYANAMSHA_MAP

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
