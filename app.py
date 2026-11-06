import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Autism GBD 2023", page_icon="🧩", layout="wide")

# Цвета из презентации BalakAI
PURPLE = "#7656D8"
CHART_PURPLE = "#7656D8"
PINK = "#E0558D"
SOFT_PINK = "#FF7FA8"
YELLOW = "#FFD84D"
LIGHT_PURPLE = "#DCD2FB"
DARK_PURPLE = "#4F2FB0"
LAVENDER = "#F3EFFF"
BLUSH = "#FFF0F5"
CREAM = "#FFF8DA"
INK = "#211A36"
MUTED = "#6F6880"
GRID = "#E7E1EF"
# Карта: синий (мало) → зелёный → жёлтый → оранжевый → красный (много)
MAP_COLORS = ["#2C7FB8", "#67C5A7", "#F6D55C", "#F2994A", "#D1352B"]
ORDER = ["2-4", "5-9", "10-14", "15-19", "20-34", "35-59", "60+"]

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700;800&family=Open+Sans:wght@400;600;700&display=swap');
    html, body, .stApp, .stMarkdown, p, li, label, input {{font-family: 'Open Sans', sans-serif;}}
    /* иконки Streamlit должны остаться своим шрифтом, иначе вместо стрелки пишется arrow_right */
    [data-testid="stIconMaterial"] {{font-family: 'Material Symbols Rounded' !important;}}
    .block-container {{max-width: 1500px; padding: 1rem 1.6rem .4rem;}}
    #MainMenu, footer, header {{visibility: hidden;}}
    [data-testid="stVerticalBlock"] {{gap: .55rem;}}
    .title {{font-family: 'Montserrat', sans-serif; font-size: 23px; font-weight: 800; color: {INK}; line-height: 1.15;}}
    .title::after {{content: ""; display: block; width: 48px; height: 4px; background: {YELLOW}; margin: 5px 0 4px;}}
    .subtitle {{font-size: 12px; color: {PURPLE}; font-weight: 600; padding-bottom: 8px;}}
    .card {{background: {LAVENDER}; border-radius: 4px; padding: 7px 14px; height: 100%; margin-bottom: 10px;}}
    [data-testid="stColumn"]:nth-child(2) .card {{background: {BLUSH};}}
    [data-testid="stColumn"]:nth-child(4) .card {{background: {CREAM};}}
    .card .label {{color: {INK}; font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 11.5px;}}
    .card .value {{color: {PURPLE}; font-family: 'Montserrat', sans-serif; font-size: 21px; font-weight: 800; line-height: 1.25; margin: 1px 0;}}
    [data-testid="stColumn"]:nth-child(2) .card .value {{color: {SOFT_PINK};}}
    .card .hint {{color: {MUTED}; font-size: 11px; font-weight: 600;}}
    .facts {{margin-top: 8px; background: {LAVENDER}; border-radius: 4px; padding: 6px 14px;}}
    .fact {{display: flex; gap: 12px; align-items: center; padding: 9px 0; border-bottom: 1px solid {GRID};}}
    .fact:last-child {{border-bottom: none;}}
    .fact b {{min-width: 62px; font-family: 'Montserrat', sans-serif; font-size: 17px; color: {PURPLE};}}
    .fact span {{font-size: 12px; color: {MUTED}; line-height: 1.25;}}
    .panel {{font-family: 'Montserrat', sans-serif; font-size: 13.5px; font-weight: 700; color: {INK}; margin: 8px 0 2px;}}
    .panel .num {{color: {PURPLE}; margin-right: 6px;}}
    [data-testid="stExpander"] details {{border: 1px solid {GRID}; border-radius: 6px; background: white;}}
    [data-testid="stExpander"] summary p {{font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 15px; color: {INK};}}
    .rp-lead {{font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 16px; color: {INK}; margin: 0 0 4px;}}
    .rp-note {{font-size: 12.5px; color: {MUTED}; margin: 0 0 8px;}}
    .rp-where {{display: inline-block; font-size: 11px; font-weight: 700; color: {PURPLE}; background: {LAVENDER};
        border-radius: 3px; padding: 2px 8px; margin-bottom: 8px;}}
    .rp-points {{margin: 0 0 10px; padding-left: 18px; font-size: 13.5px; color: {INK}; line-height: 1.5;}}
    .rp-links a {{display: inline-block; margin: 0 6px 6px 0; padding: 5px 11px; border: 1px solid #CFC3F5;
        border-radius: 6px; font-size: 12px; font-weight: 600; color: {PURPLE} !important; text-decoration: none;}}
    .rp-links a:hover {{background: {LAVENDER};}}
    [data-testid="stWidgetLabel"] p {{font-size: 11.5px; color: {MUTED}; letter-spacing: .03em;}}
    </style>
    """,
    unsafe_allow_html=True,
)

TEXT = {
    "ru": {
        "title": "Аутизм в мире",
        "subtitle": "Оценки GBD 2023, возраст 2+. Не число диагнозов.",
        "people": "Людей с аутизмом",
        "people_hint": "в мире, возраст от 2 лет",
        "ratio": "Мужчин на 1 женщину",
        "ratio_hint": "по числу людей",
        "young": "Младше 20 лет",
        "young_hint": "доля людей от 2 лет",
        "country_rate": "на 100 000",
        "map": "01 Географическое распределение: на 100 000, {year}",
        "profile": "02 Возраст: {country}, {year}",
        "age": "03 Распределение по возрасту: мир, {year}",
        "sex": "04 Распределение по полу: мир, {year}",
        "trend": "05 Исторические тренды: мир, млн",
        "from_year": "С ГОДА",
        "to_year": "ДО ГОДА",
        "age_groups": "ВОЗРАСТНЫЕ ГРУППЫ",
        "sex_filter": "ПОЛ НА КАРТЕ",
        "country_filter": "СТРАНА",
        "selected": "выбранные группы",
        "average": "среднее",
        "no_groups": "Выберите хотя бы одну возрастную группу.",
        "male": "Мужчины",
        "female": "Женщины",
        "both": "Оба пола",
        "all": "Все страны",
        "overview": "Обзор",
        "evidence": "Клиника и диагноз",
        "report": "Отчёт",
        "rp_title": "Отчёт: главное об аутизме",
        "rp_subtitle": "Главное по каждому направлению и ссылки на источники.",
        "rp_where": "На сайте",
        "ev_title": "Клиника и диагноз",
        "ev_subtitle": "Данные из статей: разные страны, годы и методы.",
        "ev_levels_card": "Уровень поддержки указан",
        "ev_levels_hint": "дети 4 и 8 лет, США, 2018, 2020",
        "ev_id_card": "Интеллектуальная инвалидность",
        "ev_id_hint": "дети 8 лет, США, 2022",
        "ev_age_card": "Медиана возраста диагноза",
        "ev_age_value": "47 мес.",
        "ev_age_hint": "дети 8 лет, США, 2022",
        "ev_und_card": "Аутичные люди без диагноза",
        "ev_und_hint": "Англия, 2018, проекция",
        "p06a": "06 Уровни поддержки: дети с указанным уровнем, США",
        "p06b": "06 Интеллект: доля аутичных людей",
        "p07": "07 Возраст диагноза, лет",
        "p08": "08 Без диагноза: Англия, 2018, %",
        "p09": "09 Доступность данных",
        "level_range": "Диапазон, %",
        "iq_no": "Без инвалидности",
        "iq_border": "Пограничный уровень",
        "iq_yes": "Интеллектуальная инвалидность",
        "iq_us": "США, 8 лет, 2022",
        "iq_world": "Мир, модель GBD 2021",
        "dx_cdc": "США, дети до 8 лет (медиана)",
        "dx_review": "Мировой обзор, 2012–2019 (среднее)",
        "dx_epic": "США, все возрасты, 2024 (медиана)",
        "dx_epic_mean": "США, все возрасты, 2024 (среднее)",
        "dx_sweden": "Швеция, до 37 лет",
        "und_range": "Оценка без диагноза",
        "d_countries": "стран с исследованиями в модели GBD из 204",
        "d_adults": "исследований взрослых в GBD 2021",
        "d_studies": "исследований в обзоре Zeidan, 34 страны",
        "d_latam": "мировых исследований из Латинской Америки",
        "ev_source": "Источники: Russell 2026; CDC 2025; GBD 2021; van 't Hof 2021; Epic Research 2025 (без рецензирования); Fyfe 2026; O'Nions 2023; Zeidan 2022. Цифры нельзя сравнивать напрямую.",
        "central": "Центральная Азия",
        "ca_title": "Центральная Азия",
        "ca_subtitle": "Модель и официальный учёт: это ориентир.",
        "kz": "Казахстан",
        "kg": "Кыргызстан",
        "uz": "Узбекистан",
        "tj": "Таджикистан",
        "tm": "Туркменистан",
        "model": "Модель GBD, 2–14 лет",
        "registered": "Дети на учёте",
        "ratio_share": "учёт от модели",
        "model_hint": "оценка за 2023 год",
        "kz_hint": "2025 год",
        "kg_hint": "2026 год, Минздрав считает цифру недостоверной",
        "gap": "Модель и официальный учёт, дети",
        "growth": "Казахстан: дети с РАС на учёте",
        "rates": "Стандартизированный показатель, 2023",
        "ca_source": "Источники: GBD 2023, IHME; Kazinform; аналитическая записка РК, 2025; Kaktus.media, 2026. Возраст и годы модели и учёта совпадают не полностью, диапазон модели широкий, а 2025 год взят из другого источника.",
        "all_hint": "оба пола, возраст от 2 лет",
        "group": "Группа",
        "number": "Число людей",
        "range": "Диапазон",
        "million": "млн",
        "source": "Источник: GBD 2023, IHME. Значения для многих стран рассчитаны моделью, карта не является рейтингом.",
    },
    "en": {
        "title": "Autism worldwide",
        "subtitle": "GBD 2023 estimates, age 2+. Not diagnosis counts.",
        "people": "Autistic people",
        "people_hint": "worldwide, age 2+",
        "ratio": "Males per 1 female",
        "ratio_hint": "by number of people",
        "young": "Under 20",
        "young_hint": "share of people aged 2+",
        "country_rate": "per 100,000",
        "map": "01 Geographic distribution: per 100,000, {year}",
        "profile": "02 Age: {country}, {year}",
        "age": "03 Age distribution: world, {year}",
        "sex": "04 Sex distribution: world, {year}",
        "trend": "05 Historical trends: world, millions",
        "from_year": "FROM YEAR",
        "to_year": "TO YEAR",
        "age_groups": "AGE GROUPS",
        "sex_filter": "SEX ON MAP",
        "country_filter": "COUNTRY",
        "selected": "selected groups",
        "average": "average",
        "no_groups": "Select at least one age group.",
        "male": "Males",
        "female": "Females",
        "both": "Both sexes",
        "all": "All countries",
        "overview": "Overview",
        "evidence": "Clinical and diagnosis",
        "report": "Report",
        "rp_title": "Report: key facts on autism",
        "rp_subtitle": "Key points for each research area, with source links.",
        "rp_where": "On the site",
        "ev_title": "Clinical and diagnosis",
        "ev_subtitle": "Data from articles: different countries, years and methods.",
        "ev_levels_card": "Support level documented",
        "ev_levels_hint": "children aged 4 and 8, USA, 2018, 2020",
        "ev_id_card": "Intellectual disability",
        "ev_id_hint": "children aged 8, USA, 2022",
        "ev_age_card": "Median age at diagnosis",
        "ev_age_value": "47 mo",
        "ev_age_hint": "children aged 8, USA, 2022",
        "ev_und_card": "Autistic people without a diagnosis",
        "ev_und_hint": "England, 2018, projection",
        "p06a": "06 Support levels: children with a documented level, USA",
        "p06b": "06 Intellectual ability: share of autistic people",
        "p07": "07 Age at diagnosis, years",
        "p08": "08 Without a diagnosis: England, 2018, %",
        "p09": "09 Data availability",
        "level_range": "Range, %",
        "iq_no": "No intellectual disability",
        "iq_border": "Borderline",
        "iq_yes": "Intellectual disability",
        "iq_us": "USA, age 8, 2022",
        "iq_world": "World, GBD 2021 model",
        "dx_cdc": "USA, children up to 8 (median)",
        "dx_review": "Global review, 2012–2019 (mean)",
        "dx_epic": "USA, all ages, 2024 (median)",
        "dx_epic_mean": "USA, all ages, 2024 (mean)",
        "dx_sweden": "Sweden, up to age 37",
        "und_range": "Estimated without a diagnosis",
        "d_countries": "countries with studies in the GBD model, of 204",
        "d_adults": "studies of adults in GBD 2021",
        "d_studies": "studies in the Zeidan review, 34 countries",
        "d_latam": "of global studies come from Latin America",
        "ev_source": "Sources: Russell 2026; CDC 2025; GBD 2021; van 't Hof 2021; Epic Research 2025 (not peer-reviewed); Fyfe 2026; O'Nions 2023; Zeidan 2022. Figures are not directly comparable.",
        "central": "Central Asia",
        "ca_title": "Central Asia",
        "ca_subtitle": "Model and official registry: a guide only.",
        "kz": "Kazakhstan",
        "kg": "Kyrgyzstan",
        "uz": "Uzbekistan",
        "tj": "Tajikistan",
        "tm": "Turkmenistan",
        "model": "GBD model, ages 2–14",
        "registered": "Registered children",
        "ratio_share": "registry vs model",
        "model_hint": "2023 estimate",
        "kz_hint": "2025",
        "kg_hint": "2026; the Health Ministry considers it unreliable",
        "gap": "Model and official registry, children",
        "growth": "Kazakhstan: registered children with ASD",
        "rates": "Age-standardised rate, 2023",
        "ca_source": "Sources: GBD 2023, IHME; Kazinform; Kazakhstan policy note, 2025; Kaktus.media, 2026. Model and registry ages and years do not fully match, the model range is wide, and 2025 comes from a different source.",
        "all_hint": "both sexes, age 2+",
        "group": "Group",
        "number": "Number of people",
        "range": "Range",
        "million": "M",
        "source": "Source: GBD 2023, IHME. Many country values are modelled; the map is not a ranking.",
    },
}



# ---------- Вкладка "Отчёт" ----------
# Ссылки на источники (названия одинаковые на обоих языках)
SOURCES = {
    "GBD 2023": "https://vizhub.healthdata.org/gbd-results/",
    "GBD 2021": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11750762",
    "CDC 2025": "https://www.cdc.gov/mmwr/volumes/74/ss/ss7402a1.htm",
    "Russell 2026": "https://doi.org/10.1007/s10803-026-07292-6",
    "Zeidan 2022": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9310578/",
    "ABS 2022": "https://www.abs.gov.au/articles/autism-australia-2022",
    "APMS 2023/24": "https://natcen.ac.uk/news/new-research-shows-no-increase-proportion-adults-england-autism-or-psychotic-disorders",
    "Fyfe 2026": "https://bmjgroup.com/rates-of-autism-in-girls-and-boys-may-be-more-equal-than-previously-thought/",
    "Epic Research 2025": "https://www.epicresearch.org/articles/diagnosis-of-autism-occurring-earlier-in-children-though-still-late-for-many-initial-diagnosis-in-adulthood-increasing-in-women",
    "van 't Hof 2021": "https://journals.sagepub.com/doi/10.1177/1362361320971107",
    "Scattoni 2023": "https://doi.org/10.1186/s13034-023-00673-0",
    "Metwally 2025": "https://pmc.ncbi.nlm.nih.gov/articles/PMC12121136/",
    "O'Nions 2023": "https://doaj.org/article/65f230df1b4749338d4c41baab836ba8",
    "PHAC 2022": "https://www.canada.ca/en/public-health/services/publications/diseases-conditions/autism-spectrum-disorder-canadian-health-survey-children-youth-2019.html",
    "Grosvenor 2024": "https://autismspeaks.org/science-news/why-autism-increasing",
    "Записка РК 2025": "https://case.apa.kz/storage/uploads/25/12/29/04/55/52/6706.pdf",
    "Kazinform 2026": "https://www.inform.kz/ru/kak-zhivut-deti-s-autizmom-v-kazahstane-istorii-roditelstva-kotoroe-delaet-silnee",
    "Kaktus 2026": "https://kaktus.media/doc/547902_zamglavy_minzdrava:_v_kyrgyzstane_nabludaetsia_otricatelnaia_dinamika_po_aytizmy.html",
    "TherapyRoute 2026": "https://www.therapyroute.com/article/autism-statistics-worldwide-by-therapyroute",
}

# Каждое направление: заголовок, где на сайте, главный вывод, пояснение, пункты, источники
REPORT = {
    "ru": [
        {"title": "Что такое аутизм", "where": "",
         "lead": "РАС — расстройство развития: трудности в общении и повторяющееся поведение, на всю жизнь.",
         "note": "Это спектр: от почти самостоятельных людей до тех, кому нужна постоянная помощь.",
         "points": ["Level 1 — нужна поддержка; Level 2 — существенная; Level 3 — очень существенная (DSM-5).",
                    "Интеллект — отдельная шкала: интеллектуальная инвалидность (IQ до 70) примерно у трети.",
                    "Надёжно выявляется примерно с 2 лет, поэтому наши данные начинаются с 2 лет."],
         "sources": ["Russell 2026", "CDC 2025"]},
        {"title": "Глобальная распространённость", "where": "Обзор, карточки",
         "lead": "Около 52,3 млн человек в мире (GBD 2023, 2023 год) — примерно 1 из 154.",
         "note": "Это оценка модели, а не число поставленных диагнозов.",
         "points": ["В возрасте от 2 лет — 49,9 млн.",
                    "GBD 2021 давал 61,8 млн (1 из 127): другая методика, с GBD 2023 не смешиваем.",
                    "По прямым исследованиям медиана около 1% (100 на 10 000), но разброс огромный."],
         "sources": ["GBD 2023", "GBD 2021", "Zeidan 2022"]},
        {"title": "Распределение по возрасту", "where": "Обзор, блоки 02–03",
         "lead": "41,4% людей с аутизмом младше 20 лет.",
         "note": "Аутизм не проходит с возрастом, поэтому взрослых тоже много.",
         "points": ["США, 2022: 32,2 на 1 000 детей 8 лет и 29,3 — у 4-летних.",
                    "Австралия, 2022: 4,3% детей 5–14 лет (опрос).",
                    "Англия: около 0,8% взрослых (три опроса APMS вместе)."],
         "sources": ["GBD 2023", "CDC 2025", "ABS 2022", "APMS 2023/24"]},
        {"title": "Распределение по полу", "where": "Обзор, блок 04",
         "lead": "Мужчин с аутизмом примерно в 2,7 раза больше, чем женщин (GBD 2023, возраст 2+).",
         "note": "У девочек аутизм чаще пропускают, поэтому часть разницы — недиагностированные случаи.",
         "points": ["США, 8 лет: 3,4 мальчика на 1 девочку.",
                    "Обзор исследований: медиана 4,2 : 1; GBD 2021: 2,1 : 1.",
                    "Швеция: к 20 годам соотношение диагнозов почти 1 : 1."],
         "sources": ["GBD 2023", "CDC 2025", "Zeidan 2022", "GBD 2021", "Fyfe 2026"]},
        {"title": "Клинические характеристики", "where": "Клиника и диагноз, блок 06",
         "lead": "Level 2 — самая большая группа: 41–51% детей с указанным уровнем (США).",
         "note": "Но уровень записан только у 40,4% детей, поэтому выводы осторожные.",
         "points": ["Level 1 — 21–27%, Level 3 — 23–33%.",
                    "Интеллектуальная инвалидность: 39,6% (США, 8 лет) и 35,8% (мир, GBD 2021).",
                    "При интеллектуальной инвалидности Level 3 по общению встречается чаще: 46,6% против 17,8%."],
         "sources": ["Russell 2026", "CDC 2025", "GBD 2021"]},
        {"title": "Возраст постановки диагноза", "where": "Клиника и диагноз, блок 07",
         "lead": "Медиана — 47 месяцев (почти 4 года) у детей 8 лет в США.",
         "note": "Если учитывать и взрослых, средний возраст диагноза 6–14 лет.",
         "points": ["С интеллектуальной инвалидностью диагноз ставят раньше: 43 против 49 месяцев.",
                    "США, 2024: медиана 6 лет; у женщин 8, у мужчин 5 (Epic, без рецензирования).",
                    "Мировой обзор: в среднем около 5 лет; Швеция — 14,3 года (уточнить: среднее или медиана)."],
         "sources": ["CDC 2025", "Epic Research 2025", "van 't Hof 2021", "Fyfe 2026"]},
        {"title": "Географическое распределение", "where": "Обзор, блок 01",
         "lead": "По модели — от 331 до 1 944 на 100 000 в зависимости от страны (2023).",
         "note": "Карта — не рейтинг: для многих стран значения рассчитаны моделью.",
         "points": ["Даже внутри страны разброс большой: в США от 9,7 до 53,1 на 1 000 по территориям.",
                    "Италия: 13,4 на 1 000 детей 7–9 лет.",
                    "Египет: 1,1% детей 1–12 лет."],
         "sources": ["GBD 2023", "CDC 2025", "Scattoni 2023", "Metwally 2025"]},
        {"title": "Частота диагностики", "where": "Центральная Азия",
         "lead": "В Казахстане на учёте около 39% детей, которых ожидает модель.",
         "note": "Учёт быстро растёт: 3 568 детей в 2020 → 16 700 в 2025.",
         "points": ["Кыргызстан: 380 детей на учёте против ~16 300 по модели; Минздрав считает цифру недостоверной.",
                    "Канада: 2% детей 1–17 лет с диагнозом; Австралия: 1,1% населения.",
                    "США: диагнозов в медсистемах 2,3 → 6,3 на 1 000 (2011 → 2022)."],
         "sources": ["Записка РК 2025", "Kazinform 2026", "Kaktus 2026", "PHAC 2022", "ABS 2022", "Grosvenor 2024"]},
        {"title": "Невыявленные случаи", "where": "Клиника и диагноз, блок 08",
         "lead": "В Англии 59–72% аутичных людей живут без диагноза (оценка на 2018 год).",
         "note": "Больше всего пропущенных среди взрослых. Данные старше нашего периода 2020–2026.",
         "points": ["Это примерно от 435 700 до 1 197 300 человек.",
                    "Других стран с такой оценкой мы не нашли."],
         "sources": ["O'Nions 2023"]},
        {"title": "Доступность данных", "where": "Клиника и диагноз, блок 09",
         "lead": "Исследования есть только в 33–34 странах из 204.",
         "note": "Для остальных стран цифры GBD рассчитаны моделью.",
         "points": ["По взрослым — всего 6 исследований (GBD 2021).",
                    "Обзор Zeidan: 71 исследование из 34 стран.",
                    "Латинская Америка — около 2,3% мировых исследований (вторичный источник)."],
         "sources": ["GBD 2021", "Zeidan 2022", "TherapyRoute 2026"]},
        {"title": "Исторические тренды", "where": "Обзор, блок 05",
         "lead": "Диагнозов всё больше: в США 1 из 150 детей в 2000 году → 1 из 31 в 2022.",
         "note": "А модельная распространённость в мире почти не меняется: 773 → 788 на 100 000 (1990–2021).",
         "points": ["Значит, растёт выявление, а не сам аутизм.",
                    "Состав территорий в США со временем меняется — сравнивать осторожно."],
         "sources": ["CDC 2025", "GBD 2021"]},
        {"title": "Коморбидность — делаем вместе", "where": "",
         "lead": "Аутизм + СДВГ разбираем вместе с Гульаим.",
         "note": "Чтобы две части сошлись, данные берём одинаково.",
         "points": ["Одна версия: GBD 2023 (не 2021).",
                    "Одни метрики: на 100 000 и стандартизированный показатель.",
                    "Те же 7 возрастных групп, старт с 2 лет (уточнить у профессора: с 1 или с 2).",
                    "Период 2020–2026, но GBD есть только до 2023."],
         "sources": []},
        {"title": "Осторожно и что проверить", "where": "",
         "lead": "Не смешиваем модель, учёт и опросы.",
         "note": "Это три разных способа считать, и цифры у них разные.",
         "points": ["Percent в GBD — не доля населения; для сравнения берём на 100 000.",
                    "«1 из 31» в США — только дети 8 лет в 16 территориях.",
                    "Проверить: Швеция 14,3; Epic (без рецензирования); TherapyRoute 2,3%; первичный источник по Казахстану."],
         "sources": []},
        {"title": "Словарик", "where": "",
         "lead": "Главные термины простыми словами.",
         "note": "",
         "points": ["Распространённость — сколько людей имеют аутизм сейчас.",
                    "На 100 000 — 650 значит 0,65%.",
                    "Стандартизированный показатель — пересчитан на одинаковый возраст населения.",
                    "Lower / Upper — интервал, где, скорее всего, настоящее значение.",
                    "Медиана — середина: половина меньше, половина больше.",
                    "Модельные данные — рассчитаны, а не измерены."],
         "sources": []},
    ],
    "en": [
        {"title": "What autism is", "where": "",
         "lead": "ASD is a developmental condition: difficulties in communication and repetitive behaviour, lifelong.",
         "note": "It is a spectrum: from nearly independent people to those who need constant support.",
         "points": ["Level 1 — requires support; Level 2 — substantial; Level 3 — very substantial (DSM-5).",
                    "Intelligence is a separate scale: about a third have intellectual disability (IQ up to 70).",
                    "It is reliably detected from about age 2, so our data start at age 2."],
         "sources": ["Russell 2026", "CDC 2025"]},
        {"title": "Global prevalence", "where": "Overview, cards",
         "lead": "About 52.3 million people worldwide (GBD 2023, year 2023) — roughly 1 in 154.",
         "note": "This is a model estimate, not a count of diagnoses.",
         "points": ["Aged 2 and over — 49.9 million.",
                    "GBD 2021 gave 61.8 million (1 in 127): a different method, not mixed with GBD 2023.",
                    "Direct studies give a median of about 1% (100 per 10,000), with a very wide range."],
         "sources": ["GBD 2023", "GBD 2021", "Zeidan 2022"]},
        {"title": "Age distribution", "where": "Overview, blocks 02–03",
         "lead": "41.4% of autistic people are under 20.",
         "note": "Autism does not go away with age, so there are many adults too.",
         "points": ["US, 2022: 32.2 per 1,000 children aged 8 and 29.3 among 4-year-olds.",
                    "Australia, 2022: 4.3% of children aged 5–14 (survey).",
                    "England: about 0.8% of adults (three APMS surveys combined)."],
         "sources": ["GBD 2023", "CDC 2025", "ABS 2022", "APMS 2023/24"]},
        {"title": "Sex distribution", "where": "Overview, block 04",
         "lead": "There are about 2.7 autistic males per female (GBD 2023, age 2+).",
         "note": "Autism in girls is missed more often, so part of the gap is undiagnosed cases.",
         "points": ["US, age 8: 3.4 boys per girl.",
                    "Review of studies: median 4.2 : 1; GBD 2021: 2.1 : 1.",
                    "Sweden: by age 20 the ratio of diagnoses is close to 1 : 1."],
         "sources": ["GBD 2023", "CDC 2025", "Zeidan 2022", "GBD 2021", "Fyfe 2026"]},
        {"title": "Clinical characteristics", "where": "Clinical and diagnosis, block 06",
         "lead": "Level 2 is the largest group: 41–51% of children with a recorded level (US).",
         "note": "But the level is recorded for only 40.4% of children, so conclusions are cautious.",
         "points": ["Level 1 — 21–27%, Level 3 — 23–33%.",
                    "Intellectual disability: 39.6% (US, age 8) and 35.8% (world, GBD 2021).",
                    "With intellectual disability, Level 3 in communication is more common: 46.6% vs 17.8%."],
         "sources": ["Russell 2026", "CDC 2025", "GBD 2021"]},
        {"title": "Age at diagnosis", "where": "Clinical and diagnosis, block 07",
         "lead": "The median is 47 months (almost 4 years) among 8-year-olds in the US.",
         "note": "When adults are included, the average age at diagnosis is 6–14 years.",
         "points": ["Children with intellectual disability are diagnosed earlier: 43 vs 49 months.",
                    "US, 2024: median 6 years; 8 for women, 5 for men (Epic, not peer-reviewed).",
                    "Global review: about 5 years on average; Sweden — 14.3 years (to check: mean or median)."],
         "sources": ["CDC 2025", "Epic Research 2025", "van 't Hof 2021", "Fyfe 2026"]},
        {"title": "Geographic distribution", "where": "Overview, block 01",
         "lead": "Modelled rates range from 331 to 1,944 per 100,000 across countries (2023).",
         "note": "The map is not a ranking: for many countries the values are modelled.",
         "points": ["Even within a country the range is wide: 9.7 to 53.1 per 1,000 across US sites.",
                    "Italy: 13.4 per 1,000 children aged 7–9.",
                    "Egypt: 1.1% of children aged 1–12."],
         "sources": ["GBD 2023", "CDC 2025", "Scattoni 2023", "Metwally 2025"]},
        {"title": "Diagnosis rates", "where": "Central Asia",
         "lead": "Kazakhstan registers about 39% of the children the model expects.",
         "note": "Registrations are growing fast: 3,568 children in 2020 → 16,700 in 2025.",
         "points": ["Kyrgyzstan: 380 registered vs ~16,300 modelled; the Ministry of Health considers the figure unreliable.",
                    "Canada: 2% of children aged 1–17 diagnosed; Australia: 1.1% of the population.",
                    "US: diagnoses in health systems 2.3 → 6.3 per 1,000 (2011 → 2022)."],
         "sources": ["Записка РК 2025", "Kazinform 2026", "Kaktus 2026", "PHAC 2022", "ABS 2022", "Grosvenor 2024"]},
        {"title": "Undiagnosed cases", "where": "Clinical and diagnosis, block 08",
         "lead": "In England 59–72% of autistic people are undiagnosed (estimate for 2018).",
         "note": "Most missed cases are adults. The data predate our 2020–2026 period.",
         "points": ["That is roughly 435,700 to 1,197,300 people.",
                    "We found no similar estimate for other countries."],
         "sources": ["O'Nions 2023"]},
        {"title": "Data availability", "where": "Clinical and diagnosis, block 09",
         "lead": "Studies exist in only 33–34 of 204 countries.",
         "note": "For the other countries GBD values are modelled.",
         "points": ["Adults: only 6 studies (GBD 2021).",
                    "Zeidan review: 71 studies from 34 countries.",
                    "Latin America — about 2.3% of global studies (secondary source)."],
         "sources": ["GBD 2021", "Zeidan 2022", "TherapyRoute 2026"]},
        {"title": "Historical trends", "where": "Overview, block 05",
         "lead": "Diagnoses keep rising: in the US 1 in 150 children in 2000 → 1 in 31 in 2022.",
         "note": "Yet modelled global prevalence barely changes: 773 → 788 per 100,000 (1990–2021).",
         "points": ["So detection is growing, not autism itself.",
                    "The set of US sites changes over time — compare with care."],
         "sources": ["CDC 2025", "GBD 2021"]},
        {"title": "Comorbidity — done together", "where": "",
         "lead": "Autism + ADHD is analysed jointly with Gulaim.",
         "note": "For the two parts to match, the data are taken the same way.",
         "points": ["One version: GBD 2023 (not 2021).",
                    "Same metrics: per 100,000 and age-standardised rate.",
                    "Same 7 age groups starting at age 2 (to confirm with the professor: age 1 or 2).",
                    "Period 2020–2026, but GBD only goes to 2023."],
         "sources": []},
        {"title": "Be careful and what to check", "where": "",
         "lead": "Do not mix models, registers and surveys.",
         "note": "They are three different ways of counting, and their numbers differ.",
         "points": ["Percent in GBD is not a share of the population; compare per 100,000.",
                    "\"1 in 31\" in the US covers only 8-year-olds in 16 sites.",
                    "To check: Sweden 14.3; Epic (not peer-reviewed); TherapyRoute 2.3%; a primary source for Kazakhstan."],
         "sources": []},
        {"title": "Glossary", "where": "",
         "lead": "Key terms in plain words.",
         "note": "",
         "points": ["Prevalence — how many people have autism now.",
                    "Per 100,000 — 650 means 0.65%.",
                    "Age-standardised rate — recalculated to the same population age structure.",
                    "Lower / Upper — the range where the true value most likely lies.",
                    "Median — the middle: half below, half above.",
                    "Modelled data — estimated, not measured."],
         "sources": []},
    ],
}

@st.cache_data
def load_data():
    age = pd.read_csv("clean/age_groups.csv")
    sex = pd.read_csv("clean/world_sex.csv")
    world_map = pd.read_csv("clean/map.csv").merge(
        pd.read_csv("data/country_codes.csv"), on="location_name"
    )
    articles = pd.read_excel("data/articles_data_en.xlsx", sheet_name="data")
    return age, sex, world_map, articles


age, sex, world_map, articles = load_data()

left, control_0, control_1 = st.columns([3.2, 3.8, 1])
with control_1:
    language = st.radio(
        "language", ["ru", "en"], format_func=str.upper, horizontal=True, label_visibility="collapsed"
    )
t = TEXT[language]
with control_0:
    views = ["overview", "central", "evidence", "report"]
    # Запоминаем вкладку, чтобы при смене языка она не сбрасывалась на "Обзор"
    view = st.radio(
        "view", views, format_func=lambda v: t[v],
        index=views.index(st.session_state.get("saved_view", "overview")),
        horizontal=True, label_visibility="collapsed", key="view_" + language,
    )
    st.session_state["saved_view"] = view

sex_options = {t["both"]: "Both", t["male"]: "Male", t["female"]: "Female"}
choice = t["both"]
country = t["all"]
from_year, to_year = 2019, 2023
groups = ORDER
map_data = world_map[
    (world_map["sex_name"] == "Both") & (world_map["year"] == 2023)
].copy()

page_title = {
    "overview": t["title"], "central": t["ca_title"], "evidence": t["ev_title"], "report": t["rp_title"]
}[view]
page_subtitle = {
    "overview": t["subtitle"], "central": t["ca_subtitle"], "evidence": t["ev_subtitle"],
    "report": t["rp_subtitle"],
}[view]
left.markdown(
    f'<div class="title">{page_title}</div><div class="subtitle">{page_subtitle}</div>',
    unsafe_allow_html=True,
)


def remember(name):
    # Запоминаем выбор человека отдельно от виджета.
    # Streamlit удаляет состояние виджета, когда вкладка с ним скрыта,
    # а "saved_..." остаётся, пока человек сам не поменяет выбор.
    st.session_state["saved_" + name] = st.session_state["widget_" + name]


def saved(name, default):
    return st.session_state.get("saved_" + name, default)


def show_filters():
    global choice, country, from_year, to_year, groups, map_data
    years = sorted(age["year"].unique())
    column_1, column_2, column_3, column_4, column_5 = st.columns([0.8, 0.8, 3, 2.2, 1.5])

    start = saved("from_year", years[-1])
    from_year = column_1.selectbox(
        t["from_year"], years, index=years.index(start) if start in years else len(years) - 1,
        key="widget_from_year", on_change=remember, args=("from_year",),
    )
    later_years = [item for item in years if item >= from_year]
    end = saved("to_year", later_years[-1])
    to_year = column_2.selectbox(
        t["to_year"], later_years,
        index=later_years.index(end) if end in later_years else len(later_years) - 1,
        key="widget_to_year", on_change=remember, args=("to_year",),
    )
    groups = column_3.multiselect(
        t["age_groups"], ORDER, default=saved("groups", ORDER),
        key="widget_groups", on_change=remember, args=("groups",),
    )

    # Для пола сохраняем номер варианта: подписи разные на RU и EN
    sex_labels = list(sex_options)
    sex_number = saved("sex", 0)
    choice = column_4.radio(
        t["sex_filter"], sex_labels, index=sex_number, horizontal=True, key="widget_sex_" + language,
    )
    st.session_state["saved_sex"] = sex_labels.index(choice)

    map_data = period_average(
        world_map[world_map["sex_name"] == sex_options[choice]],
        ["location_name", "iso3"],
        ["rate", "lower", "upper"],
    )
    countries = [t["all"]] + sorted(map_data["location_name"])
    # "Все страны" храним как ALL, чтобы выбор не терялся при смене языка
    kept = saved("country", "Kazakhstan")
    kept = t["all"] if kept == "ALL" else kept
    country = column_5.selectbox(
        t["country_filter"], countries,
        index=countries.index(kept) if kept in countries else countries.index("Kazakhstan"),
        key="widget_country_" + language,
    )
    st.session_state["saved_country"] = "ALL" if country == t["all"] else country
    if not groups:
        st.warning(t["no_groups"])
        st.stop()


def period_average(data, keys, columns):
    # Люди не суммируются по годам: один человек попал бы в расчёт несколько раз.
    period = data[data["year"].between(from_year, to_year)]
    return period.groupby(keys, as_index=False, observed=True)[columns].mean()


def period_label():
    if from_year == to_year:
        return str(to_year)
    return f"{from_year}–{to_year}, {t['average']}"


def show_number(value, digits=0):
    text = f"{value:,.{digits}f}"
    return text.replace(",", " ").replace(".", ",") if language == "ru" else text


def style_chart(fig, height):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": INK, "size": 11, "family": "Open Sans, sans-serif"},
        margin={"l": 4, "r": 4, "t": 6, "b": 4},
        height=height,
        bargap=0.28,
        showlegend=False,
        separators=", " if language == "ru" else ".,",
        hoverlabel={"bgcolor": "white", "font_color": INK},
    )
    fig.update_xaxes(showgrid=False, title=None, linecolor=GRID)
    fig.update_yaxes(
        gridcolor=GRID, zeroline=False, title=None, tickformat="~s", tickfont={"color": MUTED}
    )
    return fig


def show_chart(fig):
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


def panel(title):
    # "06 Интеллект" -> номер "06" фиолетовым, остальное тёмным
    number, _, rest = title.partition(" ")
    if number.isdigit():
        title = f'<span class="num">{number}</span>{rest}'
    st.markdown(f'<p class="panel">{title}</p>', unsafe_allow_html=True)


def overview():
    show_filters()
    selected = [group for group in ORDER if group in groups]
    all_groups = len(selected) == len(ORDER)
    period_text = period_label()
    world_all = period_average(
        age[age["location_name"] == "World"], ["group"], ["number", "population"]
    )
    world = world_all[world_all["group"].isin(selected)]
    sex_2023 = period_average(sex, ["group", "sex_name"], ["number"])
    sex_2023 = sex_2023[sex_2023["group"].isin(selected)].copy()

    if country == t["all"]:
        profile = world
        country_value = world["number"].sum() / world["population"].sum() * 100_000
        country_hint = t["all_hint"]
    else:
        profile = period_average(
            age[age["location_name"] == country], ["group"], ["number", "population"]
        )
        profile = profile[profile["group"].isin(selected)]
        row = map_data[map_data["location_name"] == country].iloc[0]
        country_value = row["rate"]
        country_hint = period_text
        if from_year == to_year:
            country_hint = f"{t['range']}: {show_number(row['lower'])}–{show_number(row['upper'])}"

    total = world["number"].sum()
    males = sex_2023.loc[sex_2023["sex_name"] == "Male", "number"].sum()
    females = sex_2023.loc[sex_2023["sex_name"] == "Female", "number"].sum()
    under_20 = world_all[world_all["group"].isin(ORDER[:4])]["number"].sum()
    under_20 = under_20 / world_all["number"].sum() * 100
    people_hint = t["people_hint"] if all_groups else t["selected"]

    cards = [
        (t["people"], f"{show_number(total / 1_000_000, 1)} {t['million']}", people_hint),
        (t["ratio"], show_number(males / females, 2), t["ratio_hint"]),
        (t["young"], f"{show_number(under_20, 1)}%", t["young_hint"]),
        (
            f"{country}, {t['country_rate']}",
            show_number(country_value),
            country_hint,
        ),
    ]
    for column, (label, value, hint) in zip(st.columns(4), cards):
        column.markdown(
            f'<div class="card"><div class="label">{label}</div>'
            f'<div class="value">{value}</div><div class="hint">{hint}</div></div>',
            unsafe_allow_html=True,
        )

    map_column, profile_column = st.columns([2.5, 1])

    with map_column:
        panel(t["map"].format(year=period_text))
        map_data["level"] = pd.qcut(map_data["rate"], 5)
        levels = list(map_data["level"].cat.categories)
        labels = [f"{show_number(item.left)}–{show_number(item.right)}" for item in levels]
        map_data["level"] = map_data["level"].cat.rename_categories(labels).astype(str)
        fig_map = px.choropleth(
            map_data,
            locations="iso3",
            color="level",
            category_orders={"level": labels},
            color_discrete_sequence=MAP_COLORS,
            custom_data=["location_name", "rate", "lower", "upper"],
        )
        map_hover = "<b>%{customdata[0]}</b><br>%{customdata[1]:,.0f} " + t["country_rate"]
        if from_year == to_year:
            map_hover += "<br>" + t["range"] + ": %{customdata[2]:,.0f}–%{customdata[3]:,.0f}"
        map_hover += "<extra></extra>"
        fig_map.update_traces(
            marker_line_color="white",
            marker_line_width=0.3,
            hovertemplate=map_hover,
        )
        fig_map.update_geos(
            showframe=False,
            showcoastlines=False,
            showcountries=False,
            projection_type="natural earth",
            lataxis_range=[-58, 85],
            bgcolor="rgba(0,0,0,0)",
            landcolor="#ECEAE4",
        )
        fig_map.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            margin={"l": 0, "r": 0, "t": 0, "b": 0},
            height=292,
            separators=", " if language == "ru" else ".,",
            legend={
                "title": None, "orientation": "h", "x": 0.5, "xanchor": "center",
                "y": 0, "yanchor": "top", "font": {"size": 12},
            },
        )
        show_chart(fig_map)

    with profile_column:
        panel(t["profile"].format(country=country, year=period_text))
        fig_profile = px.bar(
            profile, y="group", x="number", orientation="h",
            category_orders={"group": selected}, color_discrete_sequence=[CHART_PURPLE],
        )
        fig_profile.update_traces(
            marker_cornerradius=3,
            hovertemplate=f"%{{y}}<br>{t['number']}: %{{x:,.0f}}<extra></extra>",
        )
        fig_profile = style_chart(fig_profile, 292)
        fig_profile.update_xaxes(tickformat="~s", gridcolor=GRID, showgrid=True, tickfont={"color": MUTED})
        fig_profile.update_yaxes(showgrid=False, tickformat="", title=None, tickfont={"color": INK})
        show_chart(fig_profile)

    age_column, sex_column, trend_column = st.columns(3)

    with age_column:
        panel(t["age"].format(year=period_text))
        fig_age = px.bar(
            world, x="group", y="number",
            category_orders={"group": selected}, color_discrete_sequence=[CHART_PURPLE],
        )
        fig_age.update_traces(
            marker_cornerradius=3,
            hovertemplate=f"%{{x}}<br>{t['number']}: %{{y:,.0f}}<extra></extra>",
        )
        show_chart(style_chart(fig_age, 190))

    with sex_column:
        panel(t["sex"].format(year=period_text))
        sex_2023["sex_label"] = sex_2023["sex_name"].map({"Male": t["male"], "Female": t["female"]})
        fig_sex = px.bar(
            sex_2023, x="group", y="number", color="sex_label", barmode="group",
            category_orders={"group": selected, "sex_label": [t["male"], t["female"]]},
            color_discrete_map={t["male"]: CHART_PURPLE, t["female"]: PINK},
        )
        fig_sex.update_traces(
            marker_cornerradius=3,
            hovertemplate="%{x}<br>%{fullData.name}: %{y:,.0f}<extra></extra>",
        )
        fig_sex = style_chart(fig_sex, 190)
        fig_sex.update_layout(
            showlegend=True, bargroupgap=0.05,
            legend={"title": None, "orientation": "h", "x": 0, "y": 1.16},
        )
        show_chart(fig_sex)

    with trend_column:
        panel(t["trend"])
        trend = age[
            (age["location_name"] == "World")
            & (age["group"].isin(selected))
        ].groupby("year", as_index=False)["number"].sum()
        trend["million"] = trend["number"] / 1_000_000
        fig_trend = px.line(trend, x="year", y="million", markers=True, color_discrete_sequence=[CHART_PURPLE])
        fig_trend.update_traces(
            line_width=2, marker_size=8,
            hovertemplate=f"%{{x}}: %{{y:.1f}} {t['million']}<extra></extra>",
        )
        fig_trend = style_chart(fig_trend, 190)
        fig_trend.update_xaxes(dtick=1)
        fig_trend.add_vrect(
            x0=from_year - 0.35, x1=to_year + 0.35,
            fillcolor=CHART_PURPLE, opacity=0.12, line_width=0,
        )
        fig_trend.update_yaxes(tickformat=".0f", range=[0, trend["million"].max() * 1.15])
        show_chart(fig_trend)

    st.caption(t["source"])


KZ_REGISTERED = {2020: 3568, 2021: 4886, 2022: 6558, 2023: 9611, 2024: 12456, 2025: 16700}
KG_REGISTERED = 380


def model_children(name):
    rows = age[
        (age["location_name"] == name)
        & (age["year"] == 2023)
        & (age["group"].isin(["2-4", "5-9", "10-14"]))
    ]
    return rows["number"].sum()


def central_asia():
    kz_model = model_children("Kazakhstan")
    kg_model = model_children("Kyrgyzstan")
    kz_count = KZ_REGISTERED[2025]

    cards = [
        (f"{t['kz']}: {t['model']}", show_number(kz_model), t["model_hint"]),
        (
            f"{t['kz']}: {t['registered']}",
            show_number(kz_count),
            f"{t['kz_hint']}, ~{kz_count / kz_model:.0%} {t['ratio_share']}",
        ),
        (f"{t['kg']}: {t['model']}", show_number(kg_model), t["model_hint"]),
        (
            f"{t['kg']}: {t['registered']}",
            show_number(KG_REGISTERED),
            t["kg_hint"],
        ),
    ]
    for column, (label, value, hint) in zip(st.columns(4), cards):
        column.markdown(
            f'<div class="card"><div class="label">{label}</div>'
            f'<div class="value">{value}</div><div class="hint">{hint}</div></div>',
            unsafe_allow_html=True,
        )

    gap_column, growth_column = st.columns(2)

    with gap_column:
        panel(t["gap"])
        gap = pd.DataFrame(
            {
                "country": [t["kz"], t["kz"], t["kg"], t["kg"]],
                "kind": [t["model"], t["registered"], t["model"], t["registered"]],
                "value": [kz_model, kz_count, kg_model, KG_REGISTERED],
            }
        )
        fig_gap = px.bar(
            gap, x="country", y="value", color="kind", barmode="group", text="value",
            color_discrete_map={t["model"]: CHART_PURPLE, t["registered"]: PINK},
        )
        fig_gap.update_traces(
            marker_cornerradius=3, texttemplate="%{text:,.0f}", textposition="outside", cliponaxis=False,
            hovertemplate="%{x}<br>%{fullData.name}: %{y:,.0f}<extra></extra>",
        )
        fig_gap = style_chart(fig_gap, 300)
        fig_gap.update_layout(
            showlegend=True, legend={"title": None, "orientation": "h", "x": 0, "y": 1.14}
        )
        show_chart(fig_gap)

    with growth_column:
        panel(t["growth"])
        growth = pd.DataFrame(
            {"year": list(KZ_REGISTERED), "children": list(KZ_REGISTERED.values())}
        )
        fig_growth = px.bar(
            growth, x="year", y="children", text="children", color_discrete_sequence=[PINK]
        )
        fig_growth.update_traces(
            marker_cornerradius=3, texttemplate="%{text:,.0f}", textposition="outside", cliponaxis=False,
            hovertemplate="%{x}: %{y:,.0f}<extra></extra>",
        )
        fig_growth = style_chart(fig_growth, 300)
        fig_growth.update_xaxes(dtick=1)
        show_chart(fig_growth)

    panel(t["rates"])
    names = {
        "Kazakhstan": t["kz"], "Kyrgyzstan": t["kg"], "Uzbekistan": t["uz"],
        "Tajikistan": t["tj"], "Turkmenistan": t["tm"],
    }
    rates = world_map[
        (world_map["sex_name"] == "Both")
        & (world_map["year"] == 2023)
        & (world_map["location_name"].isin(names))
    ].copy()
    rates["name"] = rates["location_name"].map(names)
    rates = rates.sort_values("rate")
    rates["plus"] = rates["upper"] - rates["rate"]
    rates["minus"] = rates["rate"] - rates["lower"]
    fig_rates = px.scatter(
        rates, x="rate", y="name", error_x="plus", error_x_minus="minus",
        color_discrete_sequence=[CHART_PURPLE], custom_data=["lower", "upper"],
    )
    fig_rates.update_traces(
        marker_size=9,
        hovertemplate=(
            "%{y}<br>%{x:,.0f} " + t["country_rate"] + "<br>"
            + t["range"] + ": %{customdata[0]:,.0f}–%{customdata[1]:,.0f}<extra></extra>"
        ),
    )
    fig_rates = style_chart(fig_rates, 190)
    fig_rates.update_xaxes(showgrid=True, gridcolor=GRID, tickformat=",.0f", rangemode="tozero")
    fig_rates.update_yaxes(showgrid=False, tickformat="", tickfont={"color": INK})
    show_chart(fig_rates)
    st.caption(t["ca_source"])


def find(source, indicator, group=None):
    rows = articles[(articles["source"] == source) & (articles["indicator"] == indicator)]
    if group:
        rows = rows[rows["group"] == group]
    return rows.iloc[0]


def evidence():
    documented = find("Russell 2026", "Support level documented in records")
    disability = find("CDC 2025", "Share: IQ up to 70")
    undiagnosed = find("O'Nions 2023", "Share without a diagnosis")

    cards = [
        (t["ev_levels_card"], f"{show_number(documented['value'], 1)}%", t["ev_levels_hint"]),
        (t["ev_id_card"], f"{show_number(disability['value'], 1)}%", t["ev_id_hint"]),
        (t["ev_age_card"], t["ev_age_value"], t["ev_age_hint"]),
        (
            t["ev_und_card"],
            f"{undiagnosed['low']:.0f}–{undiagnosed['high']:.0f}%",
            t["ev_und_hint"],
        ),
    ]
    for column, (label, value, hint) in zip(st.columns(4), cards):
        column.markdown(
            f'<div class="card"><div class="label">{label}</div>'
            f'<div class="value">{value}</div><div class="hint">{hint}</div></div>',
            unsafe_allow_html=True,
        )

    levels_column, iq_column = st.columns(2)

    with levels_column:
        panel(t["p06a"])
        levels = pd.DataFrame(
            [find("Russell 2026", name) for name in ["Level 3", "Level 2", "Level 1"]]
        )
        levels["span"] = levels["high"] - levels["low"]
        fig_levels = px.bar(
            levels, y="indicator", x="span", base="low", orientation="h",
            color_discrete_sequence=[CHART_PURPLE],
            custom_data=["low", "high"],
        )
        fig_levels.update_traces(
            marker_cornerradius=3,
            texttemplate="%{customdata[0]:.1f}–%{customdata[1]:.1f}%",
            textposition="outside", cliponaxis=False,
            hovertemplate="%{y}: %{customdata[0]:.1f}–%{customdata[1]:.1f}%<extra></extra>",
        )
        fig_levels = style_chart(fig_levels, 265)
        fig_levels.update_xaxes(
            range=[0, 62], showgrid=True, gridcolor=GRID, tickfont={"color": MUTED}
        )
        fig_levels.update_yaxes(showgrid=False, tickformat="", tickfont={"color": INK})
        show_chart(fig_levels)

    with iq_column:
        panel(t["p06b"])
        world_values = [
            ("iq_no", find("GBD 2021", "Share: no intellectual disability")["value"]),
            ("iq_border", find("GBD 2021", "Share: borderline")["value"]),
            (
                "iq_yes",
                sum(
                    find("GBD 2021", f"Share: {name}")["value"]
                    for name in ["mild", "moderate", "severe", "profound"]
                ),
            ),
        ]
        us_values = [
            ("iq_no", find("CDC 2025", "Share: IQ above 85")["value"]),
            ("iq_border", find("CDC 2025", "Share: IQ 71–85")["value"]),
            ("iq_yes", disability["value"]),
        ]
        ability = pd.DataFrame(
            [{"source": t["iq_world"], "kind": t[k], "share": v} for k, v in world_values]
            + [{"source": t["iq_us"], "kind": t[k], "share": v} for k, v in us_values]
        )
        fig_iq = px.bar(
            ability, y="source", x="share", color="kind", orientation="h", text="share",
            color_discrete_map={t["iq_no"]: LIGHT_PURPLE, t["iq_border"]: CHART_PURPLE, t["iq_yes"]: DARK_PURPLE},
        )
        fig_iq.update_traces(
            marker_line_color="white", marker_line_width=2,
            texttemplate="%{text:.1f}%", textposition="inside", insidetextfont_color="white",
            hovertemplate="%{y}<br>%{fullData.name}: %{x:.1f}%<extra></extra>",
        )
        fig_iq.update_traces(insidetextfont_color=INK, selector={"name": t["iq_no"]})
        fig_iq = style_chart(fig_iq, 265)
        fig_iq.update_layout(
            showlegend=True, legend={"title": None, "orientation": "h", "x": 0, "y": 1.16}
        )
        fig_iq.update_xaxes(visible=False, range=[0, 100.5])
        fig_iq.update_yaxes(showgrid=False, tickformat="", tickfont={"color": INK})
        show_chart(fig_iq)

    age_column, gap_column, data_column = st.columns([1.6, 1, 1.2])

    with age_column:
        panel(t["p07"])
        ages = pd.DataFrame(
            [
                (t["dx_sweden"], find("Fyfe 2026 (BMJ)", "Age at diagnosis")["value"]),
                (t["dx_epic_mean"], find("Epic Research 2025", "Mean age")["value"]),
                (t["dx_epic"], find("Epic Research 2025", "Median age", "All, first diagnosis")["value"]),
                (t["dx_review"], find("van 't Hof 2021", "Mean age at diagnosis", "All studies")["value"] / 12),
                (t["dx_cdc"], find("CDC 2025", "Median age at diagnosis", "8 years")["value"] / 12),
            ],
            columns=["name", "years"],
        ).sort_values("years")
        fig_ages = px.bar(
            ages, y="name", x="years", orientation="h", text="years",
            color_discrete_sequence=[CHART_PURPLE],
        )
        fig_ages.update_traces(
            marker_cornerradius=3, texttemplate="%{text:.1f}", textposition="outside",
            cliponaxis=False, hovertemplate="%{y}: %{x:.1f}<extra></extra>",
        )
        fig_ages = style_chart(fig_ages, 245)
        fig_ages.update_xaxes(visible=False, range=[0, 17])
        fig_ages.update_yaxes(showgrid=False, tickformat="", tickfont={"color": INK})
        show_chart(fig_ages)

    with gap_column:
        panel(t["p08"])
        gap = pd.DataFrame(
            {
                "name": [t["und_range"]],
                "low": [undiagnosed["low"]],
                "span": [undiagnosed["high"] - undiagnosed["low"]],
            }
        )
        fig_gap = px.bar(
            gap, y="name", x="span", base="low", orientation="h",
            color_discrete_sequence=[PINK],
        )
        fig_gap.update_traces(
            marker_cornerradius=3, width=0.42,
            text=[f"{undiagnosed['low']:.0f}–{undiagnosed['high']:.0f}%"],
            textposition="outside", cliponaxis=False,
            hovertemplate=f"{undiagnosed['low']:.0f}–{undiagnosed['high']:.0f}%<extra></extra>",
        )
        fig_gap = style_chart(fig_gap, 245)
        fig_gap.update_xaxes(range=[0, 100], showgrid=True, gridcolor=GRID, tickfont={"color": MUTED})
        fig_gap.update_yaxes(visible=False)
        show_chart(fig_gap)

    with data_column:
        panel(t["p09"])
        facts = [
            ("33–34", t["d_countries"]),
            (str(int(find("GBD 2021", "Prevalence studies")["value"])), t["d_adults"]),
            (str(int(find("Zeidan 2022", "Included studies")["value"])), t["d_studies"]),
            (f"{show_number(find('TherapyRoute 2026', 'Share of global studies')['value'], 1)}%", t["d_latam"]),
        ]
        rows = "".join(
            f'<div class="fact"><b>{value}</b><span>{text}</span></div>'
            for value, text in facts
        )
        st.markdown(f'<div class="facts">{rows}</div>', unsafe_allow_html=True)

    st.caption(t["ev_source"])


def report():
    # Каждое направление — раскрывающийся блок: вывод, пояснение, пункты, ссылки
    for number, item in enumerate(REPORT[language], start=1):
        with st.expander(f"{number}. {item['title']}", expanded=(number == 1)):
            where = f'<div class="rp-where">{t["rp_where"]}: {item["where"]}</div>' if item["where"] else ""
            note = f'<p class="rp-note">{item["note"]}</p>' if item["note"] else ""
            points = "".join(f"<li>{point}</li>" for point in item["points"])
            links = "".join(
                f'<a href="{SOURCES[name]}" target="_blank">{name} ↗</a>' for name in item["sources"]
            )
            st.markdown(
                f'{where}<p class="rp-lead">{item["lead"]}</p>{note}'
                f'<ul class="rp-points">{points}</ul><div class="rp-links">{links}</div>',
                unsafe_allow_html=True,
            )


if view == "overview":
    overview()
elif view == "central":
    central_asia()
elif view == "evidence":
    evidence()
else:
    report()