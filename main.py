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

    # 장르 전처리: '|'로 구분된 여러 장르 중 첫 번째 장르만 추출
    df["genre"] = df["genre"].fillna("기타").astype(str).str.split("|").str[0]

    return df


df = load_data()

# 데이터 요약 정보 표시
st.sidebar.header("📊 데이터 정보")
st.sidebar.write(f"총 영화 수: **{len(df)}편**")

# ==========================================
# 섹션 1: 장르별 영화 편수 (도넛 그래프)
# ==========================================
st.subheader("1. 장르별 영화 편수 분포")

genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["장르", "편수"]

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

st.divider()
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("박스오피스 상위권 영화 중 특정 장르가 차지하는 비중과 세부 편수 분포를 한눈에 비교할 수 있습니다.")
st.divider()

# ==========================================
# 섹션 2: 장르 및 영화별 총 관객 수 (트리맵)
# ==========================================
st.subheader("2. 장르 및 영화별 총 관객 수 분포")

fig_treemap = px.treemap(
    df,
    path=[px.Constant("전체"), "genre", "movieNm"],
    values="total_audi",
    title="장르 및 영화별 총 관객 수 트리맵",
    color="genre",
    hover_data={"total_audi": ":,d"},
)

fig_treemap.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객 수: %{value:,}명"
)

st.plotly_chart(fig_treemap, use_container_width=True)

st.divider()
st.markdown("💡 **이 GRAPH로 알 수 있는 것**")
st.info("각 장르별 총 관객 수 규모와 함께 장르 내에서 어떤 영화가 전체 흥행을 주도했는지 상대적 크기로 파악할 수 있습니다.")
st.divider()

# ==========================================
# 섹션 3: 총 관객 수 분포 (히스토그램)
# ==========================================
st.subheader("3. 총 관객 수 분포")

fig_hist = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    title="총 관객 수 히스토그램",
    labels={"total_audi": "총 관객 수"},
)

fig_hist.update_traces(
    hovertemplate="<b>관객 수 구간</b>: %{x}<br><b>영화 수</b>: %{y}편"
)

st.plotly_chart(fig_hist, use_container_width=True)

# 최고 관객 수 영화 정보 자동 추출
max_movie = df.loc[df["total_audi"].idxmax()]
max_title = max_movie["movieNm"]
max_audi = max_movie["total_audi"]

st.divider()
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info(
    f"대부분의 영화가 관객 수 하위 구간(약 100만~200만 명 이하)에 촘촘히 몰려 있는 롱테일 분포를 보입니다. "
    f"한편, 데이터셋에서 가장 많은 관객을 동원한 최고 흥행작은 **'{max_title}'**({max_audi:,}명)입니다."
)
st.divider()

# ==========================================
# 섹션 4: 개봉일 스크린수 vs 총 관객 수 (산점도)
# ==========================================
st.subheader("4. 개봉일 스크린수와 총 관객 수의 관계")

fig_scatter = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린수 vs 총 관객 수 산점도",
    labels={"first_scrn": "개봉일 스크린수", "total_audi": "총 관객 수", "genre": "장르"},
    hover_data={"first_scrn": ":,d", "total_audi": ":,d"},
)

fig_scatter.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객 수: %{y:,}명"
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("개봉일 스크린수가 많을수록 대체로 총 관객 수도 증가하는 양의 상관관계를 보이지만, 스크린수가 적음에도 높은 관객 수를 기록하며 흥행에 성공한 반전 영화들도 확인할 수 있습니다.")
st.divider()

# ==========================================
# 섹션 5: 영화 10편 이상 주요 장르별 총 관객 수 (박스플롯)
# ==========================================
st.subheader("5. 주요 장르별 총 관객 수 분포 (10편 이상 장르)")

# 10편 이상인 장르만 필터링
genre_counts_series = df["genre"].value_counts()
major_genres = genre_counts_series[genre_counts_series >= 10].index
df_major = df[df["genre"].isin(major_genres)]

fig_box = px.box(
    df_major,
    x="genre",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    points="outliers",
    title="주요 장르별 총 관객 수 박스플롯",
    labels={"genre": "장르", "total_audi": "총 관객 수"},
    hover_data={"total_audi": ":,d"},
)

fig_box.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객 수: %{y:,}명"
)

st.plotly_chart(fig_box, use_container_width=True)

st.divider()
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("영화가 10편 이상인 주요 장르 간 중앙값과 흥행 편차를 비교할 수 있으며, 박스 바깥으로 튀어나온 이상치(Outlier) 점을 통해 해당 장르에서 초대형 흥행을 기록한 대표 작품을 확인할 수 있습니다.")
st.divider()
