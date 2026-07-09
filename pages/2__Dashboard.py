from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = ROOT / "data"

NEWS_FILE = DATA_ROOT / "한국언론진흥재단_뉴스빅데이터_메타데이터_범죄보도_20231231.csv"
REGION_FILE = DATA_ROOT / "경찰청_범죄 발생 지역별 통계_20241231.csv"
PLACE_FILE = DATA_ROOT / "경찰청_범죄 발생 장소별 통계_20241231.csv"
TIME_FILE = DATA_ROOT / "경찰청_범죄 발생 시간대 및 요일_20191231.csv"


@st.cache_data(show_spinner=False)
def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="cp949")


st.set_page_config(page_title="범죄 데이터 대시보드", page_icon="📊", layout="wide")
st.title("대시보드")
st.write("뉴스, 지역, 장소, 시간대 데이터를 간단히 요약해서 보는 페이지입니다.")

tabs = st.tabs(["뉴스보도", "지역별 통계", "장소별 통계", "시간대 및 요일"])

with tabs[0]:
    if NEWS_FILE.exists():
        df = load_csv(NEWS_FILE)
        df["일자"] = pd.to_datetime(df["일자"], errors="coerce")
        df = df.dropna(subset=["일자"])
        c1, c2, c3 = st.columns(3)
        c1.metric("기사 수", f"{len(df):,}")
        c2.metric("언론사 수", f"{df['언론사'].nunique():,}")
        c3.metric("기간", f"{df['일자'].min().date()} ~ {df['일자'].max().date()}")
        daily = df.groupby(df["일자"].dt.date).size().reset_index(name="기사 수")
        st.plotly_chart(px.line(daily, x="일자", y="기사 수", markers=True), use_container_width=True)
    else:
        st.info("뉴스 CSV가 없습니다.")

with tabs[1]:
    if REGION_FILE.exists():
        df = load_csv(REGION_FILE)
        for col in df.columns[2:]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        totals = df.iloc[:, 2:].sum().sort_values(ascending=False).head(15).reset_index()
        totals.columns = ["지역", "발생 건수"]
        st.plotly_chart(px.bar(totals, x="지역", y="발생 건수"), use_container_width=True)
    else:
        st.info("지역 CSV가 없습니다.")

with tabs[2]:
    if PLACE_FILE.exists():
        df = load_csv(PLACE_FILE)
        for col in df.columns[2:]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        totals = df.iloc[:, 2:].sum().sort_values(ascending=False).head(12).reset_index()
        totals.columns = ["장소", "발생 건수"]
        st.plotly_chart(px.bar(totals, x="장소", y="발생 건수"), use_container_width=True)
    else:
        st.info("장소 CSV가 없습니다.")

with tabs[3]:
    if TIME_FILE.exists():
        df = load_csv(TIME_FILE)
        for col in df.columns[2:]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        hour_cols = [c for c in df.columns if "시" in c and "분" in c]
        totals = df[hour_cols].sum().reset_index()
        totals.columns = ["시간대", "발생 건수"]
        st.plotly_chart(px.line(totals, x="시간대", y="발생 건수", markers=True), use_container_width=True)
    else:
        st.info("시간대 CSV가 없습니다.")
