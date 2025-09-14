import streamlit as st
import numpy as np
import pandas as pd

def forecast_model(variety, county, days, iot_volume, typhoon_impact):
    base_price = {"初秋甘藍": 25, "進口甘藍": 20, "芽甘藍": 30}[variety]
    noise = np.random.normal(0, 0.05, size=days)
    impact = 1 - typhoon_impact * 0.3
    forecast = base_price * (1 + noise) * impact + iot_volume * 0.01
    return forecast

st.title("甘藍價格與產量預測模擬")

variety = st.selectbox("選擇甘藍品種", ["初秋甘藍", "進口甘藍", "芽甘藍"])
county = st.selectbox("選擇縣市", ["台東", "台中", "雲林", "高雄"])
days = st.slider("預測天數", 1, 30, 7)
iot_volume = st.number_input("IoT 感測產量（kg）", min_value=0, value=1000)
typhoon_impact = st.slider("颱風影響指數", 0.0, 1.0, 0.2)

forecast = forecast_model(variety, county, days, iot_volume, typhoon_impact)

st.subheader("📈 價格預測結果")
df = pd.DataFrame({
    "日期": pd.date_range(start=pd.Timestamp.today(), periods=days),
    "預測價格 (NT$/kg)": forecast
})
st.line_chart(df.set_index("日期"))

import_cost = 18
profit = np.sum(forecast - import_cost)
st.metric("預估總利潤", f"{profit:.2f} NT$")

nodes = {
    "Farm": 0.9,
    "Transport": 0.8,
    "Market": 0.95
}
st.subheader("🔧 供應鏈韌性模擬")
for name, resilience in nodes.items():
    status = max(0, resilience - typhoon_impact)
    st.write(f"{name} 韌性狀態：{status:.2f}")