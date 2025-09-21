import streamlit as st
import numpy as np
import pandas as pd
from i18n import i18n

def forecast_model(variety, county, days, iot_volume, typhoon_impact):
    # Map variety names to internal keys for price calculation
    variety_price_map = {
        i18n.get_text("variety_options.early_autumn"): 25,
        i18n.get_text("variety_options.imported"): 20, 
        i18n.get_text("variety_options.brussels_sprouts"): 30
    }
    base_price = variety_price_map.get(variety, 25)
    noise = np.random.normal(0, 0.05, size=days)
    impact = 1 - typhoon_impact * 0.3
    forecast = base_price * (1 + noise) * impact + iot_volume * 0.01
    return forecast

# Language selector in sidebar
st.sidebar.title(i18n.get_text("language_label"))
available_languages = i18n.get_available_languages()
language_names = list(available_languages.values())
language_codes = list(available_languages.keys())

# Get current language index
current_index = language_codes.index(i18n.current_language) if i18n.current_language in language_codes else 0

selected_language_name = st.sidebar.selectbox(
    i18n.get_text("language_label"),
    language_names,
    index=current_index,
    key="language_selector"
)

# Update language if changed
selected_language_code = language_codes[language_names.index(selected_language_name)]
if selected_language_code != i18n.current_language:
    i18n.set_language(selected_language_code)
    st.rerun()

st.title(i18n.get_text("app_title"))

variety = st.selectbox(
    i18n.get_text("variety_label"), 
    [i18n.get_text("variety_options.early_autumn"), 
     i18n.get_text("variety_options.imported"), 
     i18n.get_text("variety_options.brussels_sprouts")]
)
county = st.selectbox(
    i18n.get_text("county_label"), 
    [i18n.get_text("county_options.taitung"), 
     i18n.get_text("county_options.taichung"), 
     i18n.get_text("county_options.yunlin"), 
     i18n.get_text("county_options.kaohsiung")]
)
days = st.slider(i18n.get_text("days_label"), 1, 30, 7)
iot_volume = st.number_input(i18n.get_text("iot_volume_label"), min_value=0, value=1000)
typhoon_impact = st.slider(i18n.get_text("typhoon_impact_label"), 0.0, 1.0, 0.2)

forecast = forecast_model(variety, county, days, iot_volume, typhoon_impact)

st.subheader(i18n.get_text("forecast_results_title"))
df = pd.DataFrame({
    i18n.get_text("date_column"): pd.date_range(start=pd.Timestamp.today(), periods=days),
    i18n.get_text("price_column"): forecast
})
st.line_chart(df.set_index(i18n.get_text("date_column")))

import_cost = 18
profit = np.sum(forecast - import_cost)
st.metric(i18n.get_text("total_profit_label"), f"{profit:.2f} {i18n.get_text('currency_suffix')}")

nodes = {
    "Farm": 0.9,
    "Transport": 0.8,
    "Market": 0.95
}
st.subheader(i18n.get_text("supply_chain_title"))
for name, resilience in nodes.items():
    status = max(0, resilience - typhoon_impact)
    translated_name = i18n.get_text(f"supply_chain_nodes.{name}")
    st.write(f"{translated_name} {i18n.get_text('resilience_status')}：{status:.2f}")