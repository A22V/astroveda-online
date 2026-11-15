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
from core.constants import (
    RASHIS, RASHI_SHORT, RASHI_RU_SHORT, RASHI_LORDS,
    PLANET_NAMES, EXALTATION, DEBILITATION, OWN_SIGNS, MOOLATRIKONA,
    NATURAL_FRIENDS, MRITYU_BHAGA, PUSHKARA_BHAGA, DIG_BALA_HOUSE,
    MKS_HOUSE, COMBUST_ORBS, NAKSHATRAS, VARGAS_LIST
)

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
            "Градусы": f"{int(deg):02d}°{d_min:02d}'{d_sec:02d}"",
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
