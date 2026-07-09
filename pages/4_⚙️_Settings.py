from __future__ import annotations

from pathlib import Path

import streamlit as st


ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = ROOT / "data"

st.set_page_config(page_title="설정", page_icon="⚙️", layout="wide")
st.title("Settings")

st.markdown(
    f"""
    ## 데이터 설정

    - 프로젝트 루트: `{ROOT}`
    - 데이터 폴더: `{DATA_ROOT}`
    - CSV 인코딩: `cp949`

    ## 현재 구성

    1. `1__Home.py`
    2. `2__Dashboard.py`
    3. `3__Analytics.py`
    4. `4_⚙️_Settings.py`
    """
)

if not DATA_ROOT.exists():
    st.warning("`data/` 폴더가 없습니다.")
else:
    st.success("`data/` 폴더를 찾았습니다.")
