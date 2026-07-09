from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from crime_shared import (
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


st.set_page_config(page_title="범죄 데이터 분석", page_icon="📈", layout="wide")
inject_theme()

hero(
    "Crime Analytics",
    "지역·장소·시간대별 범죄 패턴 분석",
    "집계 비교와 비율 시각화를 통해 어떤 범주에 범죄가 집중되는지 전문적으로 살펴봅니다.",
    ["비교", "집중도", "비율", "탐색"],
)

st.markdown("### 빠른 이동")
render_page_links(current="pages/3__Analytics.py")

tab1, tab2, tab3 = st.tabs(["지역별", "장소별", "시간대별"])

with tab1:
    panel("지역별 분석", "상위 지역의 발생 건수를 비교합니다.")
    if REGION_FILE.exists():
        df = numeric_frame(load_csv(REGION_FILE))
        crime_types = df["범죄대분류"].dropna().astype(str).unique().tolist()
        selected = st.multiselect("범죄대분류", crime_types, default=crime_types[:1], key="region_type")
        filtered = df[df["범죄대분류"].astype(str).isin(selected)] if selected else df
        metric_row(
            [
                ("선택 범죄대분류", f"{len(selected) if selected else len(crime_types)}개"),
                ("분석 지역 수", f"{len(df.columns) - 2:,}"),
                ("집계 방식", "시도 합산"),
            ]
        )
        totals = filtered.iloc[:, 2:].sum().sort_values(ascending=False).head(15).reset_index()
        totals.columns = ["지역", "발생 건수"]
        fig = px.bar(totals, x="지역", y="발생 건수", text="발생 건수")
        fig.update_traces(textposition="outside")
        fig.update_layout(template="plotly_white", xaxis_tickangle=-35, margin=dict(l=20, r=20, t=30, b=20), height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("지역 CSV가 없습니다.")

with tab2:
    panel("장소별 분석", "장소 유형별 비중을 함께 확인합니다.")
    if PLACE_FILE.exists():
        df = numeric_frame(load_csv(PLACE_FILE))
        crime_types = df["범죄대분류"].dropna().astype(str).unique().tolist()
        selected = st.multiselect("범죄대분류", crime_types, default=crime_types[:1], key="place_type")
        filtered = df[df["범죄대분류"].astype(str).isin(selected)] if selected else df
        metric_row(
            [
                ("선택 범죄대분류", f"{len(selected) if selected else len(crime_types)}개"),
                ("분석 장소 수", f"{len(df.columns) - 2:,}"),
                ("차트", "막대 + 도넛"),
            ]
        )
        totals = filtered.iloc[:, 2:].sum().sort_values(ascending=False).head(12).reset_index()
        totals.columns = ["장소", "발생 건수"]
        left, right = st.columns(2)
        with left:
            fig = px.bar(totals, x="장소", y="발생 건수", text="발생 건수")
            fig.update_traces(textposition="outside")
            fig.update_layout(template="plotly_white", xaxis_tickangle=-35, margin=dict(l=20, r=20, t=30, b=20), height=480)
            st.plotly_chart(fig, use_container_width=True)
        with right:
            fig = px.pie(totals, names="장소", values="발생 건수", hole=0.5)
            fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=30, b=20), height=480)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("장소 CSV가 없습니다.")

with tab3:
    panel("시간대별 분석", "시간과 요일의 패턴을 동시에 봅니다.")
    if TIME_FILE.exists():
        df = numeric_frame(load_csv(TIME_FILE))
        crime_types = df["범죄대분류"].dropna().astype(str).unique().tolist()
        selected = st.multiselect("범죄대분류", crime_types, default=crime_types[:1], key="time_type")
        filtered = df[df["범죄대분류"].astype(str).isin(selected)] if selected else df
        hour_cols = [c for c in filtered.columns if "시" in c and "분" in c]
        weekday_cols = [c for c in filtered.columns if c in ["일", "월", "화", "수", "목", "금", "토"]]
        metric_row(
            [
                ("시간대 수", f"{len(hour_cols):,}"),
                ("요일 수", f"{len(weekday_cols):,}"),
                ("분석 단위", "동시 비교"),
            ]
        )
        hour_totals = filtered[hour_cols].sum().reset_index()
        hour_totals.columns = ["시간대", "발생 건수"]
        weekday_totals = filtered[weekday_cols].sum().reset_index()
        weekday_totals.columns = ["요일", "발생 건수"]
        left, right = st.columns(2)
        with left:
            fig = px.line(hour_totals, x="시간대", y="발생 건수", markers=True)
            fig.update_layout(template="plotly_white", xaxis_tickangle=-30, margin=dict(l=20, r=20, t=30, b=20), height=470)
            st.plotly_chart(fig, use_container_width=True)
        with right:
            fig = px.bar(weekday_totals, x="요일", y="발생 건수", text="발생 건수")
            fig.update_traces(textposition="outside")
            fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=30, b=20), height=470)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("시간대 CSV가 없습니다.")
