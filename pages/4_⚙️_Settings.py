from __future__ import annotations

import streamlit as st

from crime_shared import DATA_ROOT, ROOT, hero, inject_theme, metric_row, panel, render_page_links

st.set_page_config(page_title="설정", page_icon="⚙️", layout="wide")
inject_theme()

hero(
    "Workspace Settings",
    "프로젝트 구성과 데이터 경로 확인",
    "현재 앱이 어떤 폴더를 바라보는지, 데이터가 정상적으로 연결되는지 한눈에 확인합니다.",
    ["ROOT", "data/", "cp949", "구성 점검"],
)

st.markdown("### 빠른 이동")
render_page_links(current="pages/4_⚙️_Settings.py")

panel("데이터 설정", "실행 환경과 데이터 폴더 경로를 확인합니다.")

metric_row(
    [
        ("프로젝트 루트", str(ROOT.name)),
        ("데이터 폴더", "data/"),
        ("CSV 인코딩", "cp949"),
    ]
)

st.markdown("### 현재 구성")
st.code(
    "1__Home.py\n2__Dashboard.py\n3__Analytics.py\n4_⚙️_Settings.py",
    language="text",
)

if not DATA_ROOT.exists():
    st.warning("`data/` 폴더가 없습니다.")
else:
    st.success("`data/` 폴더를 찾았습니다.")
