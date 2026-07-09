from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = ROOT / "data"

FILES = [
    ("뉴스보도", DATA_ROOT / "한국언론진흥재단_뉴스빅데이터_메타데이터_범죄보도_20231231.csv"),
    ("지역별 통계", DATA_ROOT / "경찰청_범죄 발생 지역별 통계_20241231.csv"),
    ("장소별 통계", DATA_ROOT / "경찰청_범죄 발생 장소별 통계_20241231.csv"),
    ("시간대 및 요일", DATA_ROOT / "경찰청_범죄 발생 시간대 및 요일_20191231.csv"),
]


@st.cache_data(show_spinner=False)
def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="cp949")


st.set_page_config(page_title="범죄 데이터 분석", page_icon="📊", layout="wide")
st.title("홈")
st.write("범죄 관련 4개 CSV를 한 화면에서 확인할 수 있도록 정리했습니다.")

c1, c2, c3, c4 = st.columns(4)
c1.metric("데이터셋", "4개")
c2.metric("분석 대상", "뉴스/지역/장소/시간")
c3.metric("형식", "CSV")
c4.metric("인코딩", "cp949")

overview = []
loaded = []
for label, path in FILES:
    if path.exists():
        try:
            df = load_csv(path)
            loaded.append(df)
            overview.append({"구분": label, "파일명": path.name, "행 수": len(df), "열 수": len(df.columns)})
        except Exception as exc:
            overview.append({"구분": label, "파일명": path.name, "행 수": "-", "열 수": f"실패: {exc}"})
    else:
        overview.append({"구분": label, "파일명": path.name, "행 수": "-", "열 수": "파일 없음"})

st.subheader("파일 목록")
st.dataframe(pd.DataFrame(overview), use_container_width=True, hide_index=True)

st.subheader("빠른 요약")
if loaded:
    c1, c2, c3 = st.columns(3)
    c1.metric("불러온 파일", f"{len(loaded)}개")
    c2.metric("총 행 수", f"{sum(len(df) for df in loaded):,}")
    c3.metric("총 열 수", f"{sum(len(df.columns) for df in loaded):,}")
else:
    st.info("`data/` 폴더에서 CSV를 찾지 못했습니다.")
