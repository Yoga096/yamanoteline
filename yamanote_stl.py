# 山手線アプリ
import streamlit as st

# すべての駅名
sts = ['東京', '有楽町', '新橋', '浜松町', '田町', '高輪ゲートウェイ', '品川', '大崎', '五反田', '目黒', '恵比寿', '渋谷', 
       '原宿', '代々木', '新宿', '新大久保', '高田馬場', '目白', '池袋', '大塚', '巣鴨', '駒込', '田端', '西日暮里', 
       '日暮里', '鶯谷', '上野', '御徒町', '秋葉原', '神田']  # 外回り
stations = (sts, sts.copy())
stations[1].reverse()  # 內回り
n = len(stations[0])  # 駅の数量

# 初期化
def initialize_session_state():
    defaults = {
        'riding': False,  # 乗車中
        'inside': False,  # 內回り
        'stations_now': stations[0],  # 路線
        'station_now': "東京",  # 現在の駅
        'station_i': 0,  # 現在の駅番号
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
initialize_session_state()

# 処理：降車しない
def click_next():
    st.session_state.station_i += 1
    st.session_state.station_i %= n
    st.session_state.station_now = st.session_state.stations_now[st.session_state.station_i]

# 処理：降車
def click_down():
    st.session_state.riding = not st.session_state.riding
    st.write(f"{st.session_state.station_now}、{st.session_state.station_now}です。")
    st.write("ご乗車ありがとうございました。")

# 処理：上車
def ride_on():
    st.session_state.stations_now = stations[int(st.session_state.inside)]
    st.session_state.station_i = st.session_state.stations_now.index(st.session_state.station_now)
    st.session_state.riding = True

# 処理：外回り上車
def click_outside():
    st.session_state.inside = False
    ride_on()
    click_next()

# 処理：內回り上車
def click_inside():
    st.session_state.inside = True
    ride_on()
    click_next()

# Title
st.header(f"山手線：{st.session_state.station_now}駅")

# 乗車中
if st.session_state.riding:
    # 路線、当駅
    st.write('內回り' if st.session_state.inside else '外回り')
    st.progress(st.session_state.station_i / n)
    st.write(f"まもなく {st.session_state.station_now} に到着します。")

    # 降車する/しない
    next, down = st.columns(2)
    next.button("降車しない", on_click=click_next)
    down.button("降車する", on_click=click_down)

    # 次の駅
    station_next = st.session_state.stations_now[
        0 if st.session_state.station_i >= (n - 1) else (
            st.session_state.station_i + 1)]
    st.write(f"次は {station_next}、{station_next}。")
    
    # ドアが閉まっている
    st.image("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjFTnTDiLS1MFk63zIdXH95ukA-12iH0JZcrL7scKBptBZEYCCmbBSI5k14AN3nC32mtvhUM7sqoRBxZ-Pd4YXaixOLmxunLLN-PTKvSeGfCUqXVfhad6w3OW58Yp8Q76ViJN-dXbXWJycu/s1200/bg_eki_home_train.jpg")

# 未乗車
else:  
    # 外回り/內回り
    outside, inside = st.columns(2)
    outside.button("外回り上車", on_click=click_outside)
    inside.button("內回り上車", on_click=click_inside)
    
    # ドアが開いている
    st.image("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj6QdUhR8fDVTc8luwsJm2HD_a9nxJd6SjLNk5NYW0x1iaXrKwJvzXwfibn2IsBMP8EeHlOpeRhymaChyaG7Fcxebj5EiGy3IIi1SJ9CaplQMTwkKiIL0-Zd1sBJQlttLABDKgbrXXRrC9-/s1200/bg_eki_home_train_open.jpg")