from __future__ import annotations

import streamlit as st

import pandas as pd

from crime_shared import DATASETS, hero, human_count, inject_theme, load_csv, metric_row, panel


st.set_page_config(page_title="범죄 데이터 분석", page_icon="📊", layout="wide")
inject_theme()

hero(
    "Crime Data Overview",
    "범죄 데이터를 빠르게 훑어볼 수 있는 홈",
    "뉴스보도, 지역별 통계, 장소별 통계, 시간대/요일 데이터를 한 번에 확인하도록 구성했습니다.",
    ["Overview", "CSV 4종", "cp949", "Streamlit"],
)

panel("입구 화면", "네 개의 데이터셋 상태를 먼저 확인합니다.")

metric_row(
    [
        ("데이터셋", "4개"),
        ("분석 대상", "뉴스/지역/장소/시간"),
        ("형식", "CSV"),
        ("인코딩", "cp949"),
    ]
)

overview = []
loaded = []
for item in DATASETS:
    path = item["file"]
    label = item["title"]
    if path.exists():
        try:
            df = load_csv(path)
            loaded.append(df)
            overview.append({"구분": label, "파일명": path.name, "행 수": len(df), "열 수": len(df.columns)})
        except Exception as exc:
            overview.append({"구분": label, "파일명": path.name, "행 수": "-", "열 수": f"실패: {exc}"})
    else:
        overview.append({"구분": label, "파일명": path.name, "행 수": "-", "열 수": "파일 없음"})

st.markdown("### 파일 목록")
st.dataframe(pd.DataFrame(overview), use_container_width=True, hide_index=True)

st.markdown("### 빠른 요약")
if loaded:
    metric_row(
        [
            ("불러온 파일", f"{len(loaded)}개"),
            ("총 행 수", f"{sum(len(df) for df in loaded):,}"),
            ("총 열 수", f"{sum(len(df.columns) for df in loaded):,}"),
        ]
    )
else:
    st.info("`data/` 폴더에서 CSV를 찾지 못했습니다.")
