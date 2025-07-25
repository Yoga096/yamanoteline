# 山手線アプリ
import streamlit as st
import time

# すべての駅名: 外回り
sts = ['東京', '有楽町', '新橋', '浜松町', '田町', '高輪ゲートウェイ', '品川', '大崎', '五反田', '目黒', '恵比寿', '渋谷', 
       '原宿', '代々木', '新宿', '新大久保', '高田馬場', '目白', '池袋', '大塚', '巣鴨', '駒込', '田端', '西日暮里', 
       '日暮里', '鶯谷', '上野', '御徒町', '秋葉原', '神田']  # 外回り
stations = (sts, sts.copy())
stations[1].reverse()  # 內回り
n = len(stations[0])  # 駅の数量

# st.session_state 初期化
# st.session_state: セッション単位で保存する変数
def initialize_session_state():
    defaults = {
        'riding': False,  # 状態: 乗車中
        'inside': False,  # 路線: 外回り
        'stations_now': stations[0],  # 駅順: 外回り
        'station_now': "東京",  # 現在の駅: 東京
        'station_i': 0,  # 現在の駅番号: 0
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
initialize_session_state()

# 処理：次の駅へ
def click_next():
    time.sleep(1)
    st.session_state.station_i += 1
    st.session_state.station_i %= n
    st.session_state.station_now = st.session_state.stations_now[st.session_state.station_i]

# 処理：降車
def click_down():
    st.session_state.riding = not st.session_state.riding
    st.write(f"{st.session_state.station_now}、{st.session_state.station_now}です。")
    st.empty().success("ご乗車ありがとうございました。")

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
    next.button("次の駅へ", on_click=click_next)  # 降車しない
    down.button("降車する", on_click=click_down)

    # 次の駅
    station_next = st.session_state.stations_now[
        0 if st.session_state.station_i >= (n - 1) else (
            st.session_state.station_i + 1)]
    st.write(f"次は {station_next}、{station_next}。")
    
    # ドアが閉まっている
    st.image("img/bg_eki_home_train.jpg")

# 乗車前
else:  
    # 外回り/內回り
    outside, inside = st.columns(2)
    outside.button("外回り上車", on_click=click_outside)
    inside.button("內回り上車", on_click=click_inside)
    
    # ドアが開いている
    st.image("img/bg_eki_home_train_open.jpg")