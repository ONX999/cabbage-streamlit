import streamlit as st
import numpy as np
import pandas as pd

# 擴展甘藍品種清單
CABBAGE_VARIETIES = [
    "初秋甘藍", "進口甘藍", "芽甘藍", "高麗菜", "紫甘藍", 
    "娃娃菜", "包心白菜", "結球白菜", "冬季甘藍", "春季甘藍"
]

# 擴展縣市清單
COUNTIES = [
    "台北市", "新北市", "桃園市", "台中市", "台南市", "高雄市",
    "基隆市", "新竹市", "嘉義市", "新竹縣", "苗栗縣", "彰化縣",
    "南投縣", "雲林縣", "嘉義縣", "屏東縣", "宜蘭縣", "花蓮縣",
    "台東縣", "澎湖縣", "金門縣", "連江縣"
]

# 市場價格數據模擬
def get_market_prices():
    """獲取全台甘藍市場價格數據"""
    prices = {}
    for variety in CABBAGE_VARIETIES:
        base_price = np.random.uniform(15, 40)  # 基礎價格
        prices[variety] = round(base_price + np.random.normal(0, 2), 2)
    return prices

def get_county_market_data(county):
    """獲取特定縣市的甘藍品種價格數據"""
    county_data = {}
    for variety in CABBAGE_VARIETIES:
        base_price = np.random.uniform(15, 40)
        regional_factor = np.random.uniform(0.8, 1.2)  # 地區因子
        county_data[variety] = round(base_price * regional_factor, 2)
    return county_data

def forecast_model(variety, county, days, iot_volume, typhoon_impact):
    base_prices = {
        "初秋甘藍": 25, "進口甘藍": 20, "芽甘藍": 30, "高麗菜": 22,
        "紫甘藍": 35, "娃娃菜": 28, "包心白菜": 18, "結球白菜": 20,
        "冬季甘藍": 24, "春季甘藍": 26
    }
    base_price = base_prices.get(variety, 25)
    noise = np.random.normal(0, 0.05, size=days)
    impact = 1 - typhoon_impact * 0.3
    forecast = base_price * (1 + noise) * impact + iot_volume * 0.01
    return forecast

st.title("🥬 甘藍價格與產量預測模擬")

# 創建兩個主要區塊
col1, col2 = st.columns(2)

with col1:
    st.header("📊 全台灣甘藍行情")
    
    # 品種選擇下拉選單
    selected_variety_taiwan = st.selectbox(
        "選擇查看品種行情", 
        ["全部品種"] + CABBAGE_VARIETIES,
        key="taiwan_variety"
    )
    
    # 顯示全台行情
    taiwan_prices = get_market_prices()
    
    if selected_variety_taiwan == "全部品種":
        st.subheader("全台各品種當日行情")
        taiwan_df = pd.DataFrame([
            {"品種": variety, "價格 (NT$/kg)": price, "漲跌": f"{np.random.uniform(-2, 3):.1f}"}
            for variety, price in taiwan_prices.items()
        ])
        st.dataframe(taiwan_df, use_container_width=True)
        
        # 價格圖表
        st.bar_chart(taiwan_df.set_index("品種")["價格 (NT$/kg)"])
    else:
        st.subheader(f"{selected_variety_taiwan} 全台行情")
        price = taiwan_prices[selected_variety_taiwan]
        change = np.random.uniform(-2, 3)
        st.metric(
            f"{selected_variety_taiwan} 平均價格", 
            f"{price} NT$/kg", 
            f"{change:+.1f} NT$/kg"
        )

with col2:
    st.header("🗺️ 各縣市甘藍行情")
    
    # 縣市選擇
    selected_county = st.selectbox("選擇縣市", COUNTIES, key="county_select")
    
    # 品種選擇
    selected_variety_county = st.selectbox(
        "選擇品種", 
        ["全部品種"] + CABBAGE_VARIETIES,
        key="county_variety"
    )
    
    # 顯示縣市行情
    county_data = get_county_market_data(selected_county)
    
    if selected_variety_county == "全部品種":
        st.subheader(f"{selected_county} 各品種行情")
        county_df = pd.DataFrame([
            {"品種": variety, "價格 (NT$/kg)": price, "供應量": f"{np.random.randint(100, 1000)}噸"}
            for variety, price in county_data.items()
        ])
        st.dataframe(county_df, use_container_width=True)
    else:
        st.subheader(f"{selected_county} - {selected_variety_county}")
        price = county_data[selected_variety_county]
        supply = np.random.randint(50, 500)
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("當日價格", f"{price} NT$/kg")
        with col_b:
            st.metric("供應量", f"{supply} 噸")

# 原有的預測功能保持在下方
st.divider()
st.header("🔮 價格預測模擬")

variety = st.selectbox("選擇甘藍品種", CABBAGE_VARIETIES, key="forecast_variety")
county = st.selectbox("選擇縣市", COUNTIES, key="forecast_county")
days = st.slider("預測天數", 1, 30, 7)
iot_volume = st.number_input("IoT 感測產量（kg）", min_value=0, value=1000)
typhoon_impact = st.slider("颱風影響指數", 0.0, 1.0, 0.2)

forecast = forecast_model(variety, county, days, iot_volume, typhoon_impact)

col_forecast1, col_forecast2 = st.columns(2)

with col_forecast1:
    st.subheader("📈 價格預測結果")
    df = pd.DataFrame({
        "日期": pd.date_range(start=pd.Timestamp.today(), periods=days),
        "預測價格 (NT$/kg)": forecast
    })
    st.line_chart(df.set_index("日期"))
    
    import_cost = 18
    profit = np.sum(forecast - import_cost)
    st.metric("預估總利潤", f"{profit:.2f} NT$")

with col_forecast2:
    st.subheader("🔧 供應鏈韌性模擬")
    nodes = {
        "農場": 0.9,
        "運輸": 0.8,
        "市場": 0.95
    }
    
    for name, resilience in nodes.items():
        status = max(0, resilience - typhoon_impact)
        color = "normal" if status > 0.7 else "inverse" if status > 0.5 else "off"
        st.metric(
            f"{name} 韌性狀態", 
            f"{status:.2f}",
            delta=f"{(status - resilience):.2f}" if status != resilience else None
        )

# 新增市場分析區塊
st.divider()
st.header("📈 市場趨勢分析")

analysis_col1, analysis_col2 = st.columns(2)

with analysis_col1:
    st.subheader("價格波動分析")
    # 模擬過去30天的價格趨勢
    trend_days = 30
    trend_data = []
    for i in range(trend_days):
        base = taiwan_prices.get(variety, 25)
        daily_price = base + np.random.normal(0, 2)
        trend_data.append(daily_price)
    
    trend_df = pd.DataFrame({
        "日期": pd.date_range(start=pd.Timestamp.today() - pd.Timedelta(days=trend_days), periods=trend_days),
        "歷史價格": trend_data
    })
    st.line_chart(trend_df.set_index("日期"))

with analysis_col2:
    st.subheader("供需狀況")
    supply_demand = {
        "供應量": f"{np.random.randint(800, 1500)} 噸",
        "需求量": f"{np.random.randint(900, 1300)} 噸",
        "庫存水準": f"{np.random.randint(100, 300)} 噸",
        "市場飽和度": f"{np.random.uniform(0.7, 0.95):.1%}"
    }
    
    for metric, value in supply_demand.items():
        st.metric(metric, value)