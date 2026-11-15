# -*- coding: utf-8 -*-
"""
Модуль специальных расчетов Джйотиш (вкладка «Разное» в VedicHoro):
- 12 Арудха-пад (AL, UL и A2..A11) с выбором: с исключениями (школа Ратха) / без исключений (К.Н. Рао)
- 7 Специальных Лагн (Бхава Лагна, Хора Лагна, Гхатика Лагна, Шри Лагна, Инду Лагна, Варнада Лагна, Каракамша)
- 11 Упаграх (Дхума, Вьятипата, Паривеша, Индрачапа, Упакету, Гулика, Манди, Кала, Мритью, Ардхапрахара, Ямагантака)
- Спхуты (Биджа Спхута, Кшетра Спхута, Йоги Спхута, Авайоги Спхута, Триспхута, Пранапада, Бхригу Бинду, Кунда)
- Критические точки: 22-я Дреккана (кхара), 64-я Навамша, Бадхака, Дагдха Раши.
"""

from core.constants import RASHIS, RASHI_RU_SHORT, RASHI_LORDS, NAKSHATRAS
from core.ephemeris import compute_varga_sign

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
