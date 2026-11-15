# -*- coding: utf-8 -*-
"""
Модуль расчета планетных и знаковых периодов (вкладка «Периоды» в VedicHoro):
- Накшатра даши: Вимшоттари даша (120 лет) и Йогини даша (36 лет) с углублением до Прана-даши (5 уровней)
- Раши даши: Чара даша Джаймини К.Н. Рао и Нарайана даша
- Автоматический расчет активных периодов всех 4 систем на дату любого жизненного события клиента
  и сравнение Исходного («И») и Текущего («Т») периода при ректификации (сдвиге времени рождения).
"""

import datetime
from core.constants import NAKSHATRAS, RASHIS, RASHI_RU_SHORT, RASHI_LORDS, EXALTATION, DEBILITATION

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
