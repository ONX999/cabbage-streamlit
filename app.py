import streamlit as st
import numpy as np
import pandas as pd

# Language translations
TRANSLATIONS = {
    "zh_TW": {
        "title": "甘藍價格與產量預測模擬",
        "language": "語言",
        "select_variety": "選擇甘藍品種",
        "select_county": "選擇縣市",
        "forecast_days": "預測天數",
        "iot_volume": "IoT 感測產量（kg）",
        "typhoon_impact": "颱風影響指數",
        "price_forecast": "📈 價格預測結果",
        "date": "日期",
        "forecast_price": "預測價格 (NT$/kg)",
        "estimated_profit": "預估總利潤",
        "supply_chain": "🔧 供應鏈韌性模擬",
        "resilience_status": "韌性狀態",
        "varieties": ["初秋甘藍", "進口甘藍", "芽甘藍"],
        "counties": ["台東", "台中", "雲林", "高雄"]
    },
    "en": {
        "title": "Cabbage Price & Yield Forecast Simulation",
        "language": "Language",
        "select_variety": "Select Cabbage Variety",
        "select_county": "Select County",
        "forecast_days": "Forecast Days",
        "iot_volume": "IoT Sensor Volume (kg)",
        "typhoon_impact": "Typhoon Impact Index",
        "price_forecast": "📈 Price Forecast Results",
        "date": "Date",
        "forecast_price": "Forecast Price (NT$/kg)",
        "estimated_profit": "Estimated Total Profit",
        "supply_chain": "🔧 Supply Chain Resilience Simulation",
        "resilience_status": "Resilience Status",
        "varieties": ["Early Autumn Cabbage", "Imported Cabbage", "Brussels Sprouts"],
        "counties": ["Taitung", "Taichung", "Yunlin", "Kaohsiung"]
    }
}

def get_text(key, lang=None):
    """Get translated text for the given key"""
    if lang is None:
        lang = st.session_state.get('language', 'zh_TW')
    return TRANSLATIONS[lang].get(key, key)

def get_variety_mapping(lang=None):
    """Get variety mapping from display names to internal keys"""
    if lang is None:
        lang = st.session_state.get('language', 'zh_TW')
    
    zh_varieties = TRANSLATIONS['zh_TW']['varieties']
    en_varieties = TRANSLATIONS['en']['varieties']
    
    if lang == 'zh_TW':
        return {zh: zh for zh in zh_varieties}
    else:  # English
        return {en: zh for en, zh in zip(en_varieties, zh_varieties)}

# Initialize session state for language
if 'language' not in st.session_state:
    st.session_state.language = 'zh_TW'

def forecast_model(variety, county, days, iot_volume, typhoon_impact):
    base_price = {"初秋甘藍": 25, "進口甘藍": 20, "芽甘藍": 30}[variety]
    noise = np.random.normal(0, 0.05, size=days)
    impact = 1 - typhoon_impact * 0.3
    forecast = base_price * (1 + noise) * impact + iot_volume * 0.01
    return forecast

# Language selector in sidebar
with st.sidebar:
    # Use current language for the language selector label
    current_lang = st.session_state.get('language', 'zh_TW')
    lang_label = "語言" if current_lang == 'zh_TW' else "Language"
    
    lang_options = {"繁體中文": "zh_TW", "English": "en"}
    selected_lang_display = st.selectbox(
        lang_label,
        options=list(lang_options.keys()),
        index=0 if st.session_state.language == 'zh_TW' else 1
    )
    st.session_state.language = lang_options[selected_lang_display]

st.title(get_text("title"))

# Get variety mapping for current language
variety_mapping = get_variety_mapping()
variety_display = st.selectbox(
    get_text("select_variety"), 
    list(variety_mapping.keys())
)
variety = variety_mapping[variety_display]

county = st.selectbox(get_text("select_county"), get_text("counties"))
days = st.slider(get_text("forecast_days"), 1, 30, 7)
iot_volume = st.number_input(get_text("iot_volume"), min_value=0, value=1000)
typhoon_impact = st.slider(get_text("typhoon_impact"), 0.0, 1.0, 0.2)

forecast = forecast_model(variety, county, days, iot_volume, typhoon_impact)

st.subheader(get_text("price_forecast"))
df = pd.DataFrame({
    get_text("date"): pd.date_range(start=pd.Timestamp.today(), periods=days),
    get_text("forecast_price"): forecast
})
st.line_chart(df.set_index(get_text("date")))

import_cost = 18
profit = np.sum(forecast - import_cost)
st.metric(get_text("estimated_profit"), f"{profit:.2f} NT$")

nodes = {
    "Farm": 0.9,
    "Transport": 0.8,
    "Market": 0.95
}
st.subheader(get_text("supply_chain"))
for name, resilience in nodes.items():
    status = max(0, resilience - typhoon_impact)
    st.write(f"{name} {get_text('resilience_status')}：{status:.2f}")