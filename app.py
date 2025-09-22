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

# 縣市、鄉鎮區、地籍資料結構
COUNTY_TOWNSHIP_DATA = {
    "台北市": {
        "中正區": {
            "建國段": ["001號", "002號", "003號", "004號", "005號"],
            "忠孝段": ["001號", "002號", "003號", "004號", "005號"],
            "仁愛段": ["001號", "002號", "003號", "004號", "005號"]
        },
        "大安區": {
            "敦化段": ["001號", "002號", "003號", "004號", "005號"],
            "復興段": ["001號", "002號", "003號", "004號", "005號"],
            "信義段": ["001號", "002號", "003號", "004號", "005號"]
        },
        "信義區": {
            "松山段": ["001號", "002號", "003號", "004號", "005號"],
            "世貿段": ["001號", "002號", "003號", "004號", "005號"]
        }
    },
    "新北市": {
        "板橋區": {
            "板橋段": ["001號", "002號", "003號", "004號", "005號"],
            "新板段": ["001號", "002號", "003號", "004號", "005號"]
        },
        "中和區": {
            "中和段": ["001號", "002號", "003號", "004號", "005號"],
            "永和段": ["001號", "002號", "003號", "004號", "005號"]
        },
        "三重區": {
            "三重段": ["001號", "002號", "003號", "004號", "005號"],
            "蘆洲段": ["001號", "002號", "003號", "004號", "005號"]
        }
    },
    "桃園市": {
        "桃園區": {
            "桃園段": ["001號", "002號", "003號", "004號", "005號"],
            "中正段": ["001號", "002號", "003號", "004號", "005號"]
        },
        "中壢區": {
            "中壢段": ["001號", "002號", "003號", "004號", "005號"],
            "內壢段": ["001號", "002號", "003號", "004號", "005號"]
        },
        "八德區": {
            "八德段": ["001號", "002號", "003號", "004號", "005號"]
        }
    },
    "台中市": {
        "西屯區": {
            "西屯段": ["001號", "002號", "003號", "004號", "005號"],
            "逢甲段": ["001號", "002號", "003號", "004號", "005號"]
        },
        "北屯區": {
            "北屯段": ["001號", "002號", "003號", "004號", "005號"],
            "軍功段": ["001號", "002號", "003號", "004號", "005號"]
        },
        "南屯區": {
            "南屯段": ["001號", "002號", "003號", "004號", "005號"]
        }
    },
    "台南市": {
        "中西區": {
            "中西段": ["001號", "002號", "003號", "004號", "005號"],
            "赤崁段": ["001號", "002號", "003號", "004號", "005號"]
        },
        "東區": {
            "東區段": ["001號", "002號", "003號", "004號", "005號"],
            "德高段": ["001號", "002號", "003號", "004號", "005號"]
        },
        "安平區": {
            "安平段": ["001號", "002號", "003號", "004號", "005號"]
        }
    },
    "高雄市": {
        "左營區": {
            "左營段": ["001號", "002號", "003號", "004號", "005號"],
            "新莊段": ["001號", "002號", "003號", "004號", "005號"]
        },
        "三民區": {
            "三民段": ["001號", "002號", "003號", "004號", "005號"],
            "鳳山段": ["001號", "002號", "003號", "004號", "005號"]
        },
        "前金區": {
            "前金段": ["001號", "002號", "003號", "004號", "005號"]
        }
    }
}

# 為沒有詳細資料的縣市提供預設鄉鎮區和地段
def get_default_township_data(county):
    """為沒有詳細資料的縣市生成預設鄉鎮區和地段資料"""
    if county in COUNTY_TOWNSHIP_DATA:
        return COUNTY_TOWNSHIP_DATA[county]

    # 生成預設資料
    townships = [county.replace('市', '區').replace('縣', '區'), "中央區", "新興區"]
    default_data = {}
    for township in townships:
        segments = [township.replace('區', '段'), "中心段", "農業段"]
        default_data[township] = {}
        for segment in segments:
            default_data[township][segment] = ["00{}號".format(i) for i in range(1, 6)]

    return default_data


# 市場價格數據模擬
def get_market_prices():
    """獲取全台甘藍市場價格數據"""
    prices = {}
    for variety in CABBAGE_VARIETIES:
        base_price = np.random.uniform(15, 40)  # 基礎價格
        prices[variety] = round(base_price + np.random.normal(0, 2), 2)
    return prices


def get_county_market_data(county, township=None, land_segment=None, land_number=None):
    """獲取特定縣市的甘藍品種價格數據，包含地籍資料影響"""
    county_data = {}

    # 基礎地區因子
    base_regional_factor = np.random.uniform(0.8, 1.2)

    # 鄉鎮區因子（如果提供）
    township_factor = 1.0
    if township:
        # 不同鄉鎮區可能有不同的價格影響
        township_factors = {
            "中正區": 1.1, "大安區": 1.15, "信義區": 1.2,
            "板橋區": 1.05, "中和區": 1.0, "三重區": 0.95,
            "桃園區": 1.0, "中壢區": 0.98, "八德區": 0.95,
            "西屯區": 1.05, "北屯區": 1.0, "南屯區": 1.02,
            "中西區": 1.0, "東區": 0.98, "安平區": 1.03,
            "左營區": 1.02, "三民區": 1.0, "前金區": 1.05
        }
        township_factor = township_factors.get(township, 1.0)

    # 地段因子（如果提供）
    land_factor = 1.0
    if land_segment:
        # 不同地段可能影響運輸成本等
        if "中心" in land_segment or "中正" in land_segment:
            land_factor = 1.05
        elif "農業" in land_segment:
            land_factor = 0.92
        else:
            land_factor = np.random.uniform(0.95, 1.05)

    for variety in CABBAGE_VARIETIES:
        base_price = np.random.uniform(15, 40)
        final_factor = base_regional_factor * township_factor * land_factor
        county_data[variety] = round(base_price * final_factor, 2)

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
    
    # 取得該縣市的鄉鎮區資料
    township_data = get_default_township_data(selected_county)
    townships = list(township_data.keys())
    
    # 鄉鎮區選擇
    selected_township = st.selectbox("選擇鄉鎮區", ["全部鄉鎮區"] + townships, key="township_select")
    
    # 地段選擇（如果選擇了特定鄉鎮區）
    if selected_township != "全部鄉鎮區":
        segments = list(township_data[selected_township].keys())
        selected_segment = st.selectbox("選擇地段", ["全部地段"] + segments, key="segment_select")
        
        # 地號選擇（如果選擇了特定地段）
        if selected_segment != "全部地段":
            land_numbers = township_data[selected_township][selected_segment]
            selected_land_number = st.selectbox("選擇地號", ["全部地號"] + land_numbers, key="land_number_select")
        else:
            selected_land_number = None
    else:
        selected_segment = None
        selected_land_number = None
    
    # 品種選擇
    selected_variety_county = st.selectbox(
        "選擇品種", 
        ["全部品種"] + CABBAGE_VARIETIES,
        key="county_variety"
    )
    
    # 顯示縣市行情（根據選擇的地籍資料調整）
    county_data = get_county_market_data(
        selected_county, 
        selected_township if selected_township != "全部鄉鎮區" else None,
        selected_segment if selected_segment and selected_segment != "全部地段" else None,
        selected_land_number if selected_land_number and selected_land_number != "全部地號" else None
    )
    
    # 建立標題字串
    location_title = selected_county
    if selected_township != "全部鄉鎮區":
        location_title += f" - {selected_township}"
        if selected_segment and selected_segment != "全部地段":
            location_title += f" - {selected_segment}"
            if selected_land_number and selected_land_number != "全部地號":
                location_title += f" - {selected_land_number}"
    
    if selected_variety_county == "全部品種":
        st.subheader(f"{location_title} 各品種行情")
        county_df = pd.DataFrame([
            {
                "品種": variety, 
                "價格 (NT$/kg)": price, 
                "供應量": f"{np.random.randint(100, 1000)}噸",
                "地籍影響": "已含" if (selected_township != "全部鄉鎮區" or selected_segment or selected_land_number) else "未含"
            }
            for variety, price in county_data.items()
        ])
        st.dataframe(county_df, use_container_width=True)
    else:
        st.subheader(f"{location_title} - {selected_variety_county}")
        price = county_data[selected_variety_county]
        supply = np.random.randint(50, 500)
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("當日價格", f"{price} NT$/kg")
        with col_b:
            st.metric("供應量", f"{supply} 噸")
        
        # 顯示地籍資訊
        if selected_township != "全部鄉鎮區":
            st.info(f"📍 地籍資訊：{location_title}")
            if selected_segment and selected_segment != "全部地段":
                land_info = f"地段：{selected_segment}"
                if selected_land_number and selected_land_number != "全部地號":
                    land_info += f" | 地號：{selected_land_number}"
                st.caption(land_info)

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
