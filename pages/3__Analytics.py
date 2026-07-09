from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = ROOT / "data"

REGION_FILE = DATA_ROOT / "경찰청_범죄 발생 지역별 통계_20241231.csv"
PLACE_FILE = DATA_ROOT / "경찰청_범죄 발생 장소별 통계_20241231.csv"
TIME_FILE = DATA_ROOT / "경찰청_범죄 발생 시간대 및 요일_20191231.csv"


@st.cache_data(show_spinner=False)
def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="cp949")


st.set_page_config(page_title="범죄 데이터 분석", page_icon="📈", layout="wide")
st.title("Analytics")
st.write("지역, 장소, 시간대별 범죄 패턴을 확인하는 분석 페이지입니다.")

tab1, tab2, tab3 = st.tabs(["지역별", "장소별", "시간대별"])

with tab1:
    if REGION_FILE.exists():
        df = load_csv(REGION_FILE)
        for col in df.columns[2:]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        crime_types = df["범죄대분류"].dropna().astype(str).unique().tolist()
        selected = st.multiselect("범죄대분류", crime_types, default=crime_types[:1], key="region_type")
        filtered = df[df["범죄대분류"].astype(str).isin(selected)] if selected else df
        totals = filtered.iloc[:, 2:].sum().sort_values(ascending=False).head(15).reset_index()
        totals.columns = ["지역", "발생 건수"]
        st.plotly_chart(px.bar(totals, x="지역", y="발생 건수"), use_container_width=True)
    else:
        st.info("지역 CSV가 없습니다.")

with tab2:
    if PLACE_FILE.exists():
        df = load_csv(PLACE_FILE)
        for col in df.columns[2:]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        crime_types = df["범죄대분류"].dropna().astype(str).unique().tolist()
        selected = st.multiselect("범죄대분류", crime_types, default=crime_types[:1], key="place_type")
        filtered = df[df["범죄대분류"].astype(str).isin(selected)] if selected else df
        totals = filtered.iloc[:, 2:].sum().sort_values(ascending=False).head(12).reset_index()
        totals.columns = ["장소", "발생 건수"]
        st.plotly_chart(px.bar(totals, x="장소", y="발생 건수"), use_container_width=True)
        st.plotly_chart(px.pie(totals, names="장소", values="발생 건수", hole=0.4), use_container_width=True)
    else:
        st.info("장소 CSV가 없습니다.")

with tab3:
    if TIME_FILE.exists():
        df = load_csv(TIME_FILE)
        for col in df.columns[2:]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        crime_types = df["범죄대분류"].dropna().astype(str).unique().tolist()
        selected = st.multiselect("범죄대분류", crime_types, default=crime_types[:1], key="time_type")
        filtered = df[df["범죄대분류"].astype(str).isin(selected)] if selected else df
        hour_cols = [c for c in filtered.columns if "시" in c and "분" in c]
        weekday_cols = [c for c in filtered.columns if c in ["일", "월", "화", "수", "목", "금", "토"]]
        hour_totals = filtered[hour_cols].sum().reset_index()
        hour_totals.columns = ["시간대", "발생 건수"]
        weekday_totals = filtered[weekday_cols].sum().reset_index()
        weekday_totals.columns = ["요일", "발생 건수"]
        left, right = st.columns(2)
        with left:
            st.plotly_chart(px.line(hour_totals, x="시간대", y="발생 건수", markers=True), use_container_width=True)
        with right:
            st.plotly_chart(px.bar(weekday_totals, x="요일", y="발생 건수"), use_container_width=True)
    else:
        st.info("시간대 CSV가 없습니다.")
