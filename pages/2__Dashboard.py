from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from crime_shared import (
    NEWS_FILE,
    PLACE_FILE,
    REGION_FILE,
    TIME_FILE,
    hero,
    inject_theme,
    load_csv,
    metric_row,
    numeric_frame,
    panel,
    render_page_links,
)


st.set_page_config(page_title="범죄 데이터 대시보드", page_icon="📊", layout="wide")
inject_theme()

hero(
    "Analytics Dashboard",
    "핵심 범죄 통계를 요약해서 보는 대시보드",
    "각 데이터셋의 대표 지표를 요약하고, 막대그래프와 선그래프로 패턴을 빠르게 확인합니다.",
    ["요약", "분포", "추이", "탭 기반 탐색"],
)

st.markdown("### 빠른 이동")
render_page_links(current="pages/2__Dashboard.py")

tabs = st.tabs(["뉴스보도", "지역별 통계", "장소별 통계", "시간대 및 요일"])

with tabs[0]:
    panel("뉴스보도", "일자별 기사량과 언론사 분포를 확인합니다.")
    if NEWS_FILE.exists():
        df = load_csv(NEWS_FILE)
        df["일자"] = pd.to_datetime(df["일자"], errors="coerce")
        df = df.dropna(subset=["일자"])
        metric_row(
            [
                ("기사 수", f"{len(df):,}"),
                ("언론사 수", f"{df['언론사'].nunique():,}"),
                ("기간", f"{df['일자'].min().date()} ~ {df['일자'].max().date()}"),
            ]
        )
        daily = df.groupby(df["일자"].dt.date).size().reset_index(name="기사 수")
        fig = px.line(daily, x="일자", y="기사 수", markers=True)
        fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=30, b=20), height=420)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("뉴스 CSV가 없습니다.")

with tabs[1]:
    panel("지역별 통계", "상위 지역의 발생 건수를 비교합니다.")
    if REGION_FILE.exists():
        df = numeric_frame(load_csv(REGION_FILE))
        totals = df.iloc[:, 2:].sum().sort_values(ascending=False).head(15).reset_index()
        totals.columns = ["지역", "발생 건수"]
        st.caption("상위 지역의 누적 발생 건수를 기준으로 비교합니다.")
        fig = px.bar(totals, x="지역", y="발생 건수", text="발생 건수")
        fig.update_traces(textposition="outside")
        fig.update_layout(template="plotly_white", xaxis_tickangle=-35, margin=dict(l=20, r=20, t=30, b=20), height=480)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("지역 CSV가 없습니다.")

with tabs[2]:
    panel("장소별 통계", "상위 장소 유형의 분포를 확인합니다.")
    if PLACE_FILE.exists():
        df = numeric_frame(load_csv(PLACE_FILE))
        totals = df.iloc[:, 2:].sum().sort_values(ascending=False).head(12).reset_index()
        totals.columns = ["장소", "발생 건수"]
        st.caption("장소 유형별 상위 항목을 시각적으로 비교합니다.")
        fig = px.bar(totals, x="장소", y="발생 건수", text="발생 건수")
        fig.update_traces(textposition="outside")
        fig.update_layout(template="plotly_white", xaxis_tickangle=-35, margin=dict(l=20, r=20, t=30, b=20), height=480)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("장소 CSV가 없습니다.")

with tabs[3]:
    panel("시간대 및 요일", "시간 패턴과 요일 패턴을 함께 봅니다.")
    if TIME_FILE.exists():
        df = numeric_frame(load_csv(TIME_FILE))
        hour_cols = [c for c in df.columns if "시" in c and "분" in c]
        totals = df[hour_cols].sum().reset_index()
        totals.columns = ["시간대", "발생 건수"]
        st.caption("시간대별 발생 흐름을 선형으로 보여줍니다.")
        fig = px.line(totals, x="시간대", y="발생 건수", markers=True)
        fig.update_layout(template="plotly_white", xaxis_tickangle=-30, margin=dict(l=20, r=20, t=30, b=20), height=420)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("시간대 CSV가 없습니다.")
