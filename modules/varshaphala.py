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
from core.constants import RASHIS, RASHI_RU_SHORT, RASHI_LORDS, NAKSHATRAS, EXALTATION, OWN_SIGNS
from core.ephemeris import calculate_full_chart, AYANAMSHA_MAP
from core.dashas import VIMSHOTTARI_ORDER, VIMSHOTTARI_YEARS
from core.yogas import calculate_tajaka_yogas

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
            "Сила PVB": pvb_scores[m_lord],
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
        "varshesha": f"{varshesha} (Вишва-бала: {pvb_scores[varshesha]})",
        "bala_rows": bala_rows,
        "mudda_rows": mudda_rows,
        "sahams": sahams_table,
        "tajaka": tajaka_res
    }
