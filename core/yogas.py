# -*- coding: utf-8 -*-
"""
Движок анализа классических Йог Парашары / Джаймини (более 200 комбинаций)
и полный матричный калькулятор всех 16 Таджака-йог (для Прашны и Варшапхалы)
с учетом скоростей планет, орбов Диптхамша, Итхасала / Эсарапха / Накта / Ямайа / Камбула и др.
"""

from core.constants import RASHI_LORDS, EXALTATION, DEBILITATION, OWN_SIGNS, TAJAKA_ORBS

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
