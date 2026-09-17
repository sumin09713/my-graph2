import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")


# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # 장르 전처리: '|'로 구분된 여러 장르 중 첫 번째 장르만 extraction
    df["genre"] = df["genre"].fillna("기타").astype(str).str.split("|").str[0]

    return df


df = load_data()

# 데이터 요약 정보 표시
st.sidebar.header("📊 데이터 정보")
st.sidebar.write(f"총 영화 수: **{len(df)}편**")

# 섹션 1: 장르별 영화 편수 (도넛 그래프)
st.subheader("1. 장르별 영화 편수 분포")

# 장르별 편수 집계
genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["장르", "편수"]

# Plotly 도넛 그래프 생성
fig_donut = px.pie(
    genre_counts,
    names="장르",
    values="편수",
    hole=0.4,
    title="장르별 영화 편수 비율",
    hover_data=["편수"],
)

fig_donut.update_traces(
    textposition="inside",
    textinfo="percent+label",
    hovertemplate="<b>장르</b>: %{label}<br><b>편수</b>: %{value}편<br><b>비율</b>: %{percent}",
)

st.plotly_chart(fig_donut, use_container_width=True)

# 그래프 해석 안내 구역
st.divider()
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("박스오피스 상위권 영화 중 특정 장르가 차지하는 비중과 세부 편수 분포를 한눈에 비교할 수 있습니다.")
st.divider()
