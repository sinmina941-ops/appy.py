from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parent
DATA_ROOT = ROOT / "data"

NEWS_FILE = DATA_ROOT / "한국언론진흥재단_뉴스빅데이터_메타데이터_범죄보도_20231231.csv"
REGION_FILE = DATA_ROOT / "경찰청_범죄 발생 지역별 통계_20241231.csv"
PLACE_FILE = DATA_ROOT / "경찰청_범죄 발생 장소별 통계_20241231.csv"
TIME_FILE = DATA_ROOT / "경찰청_범죄 발생 시간대 및 요일_20191231.csv"

DATASETS = [
    {
        "key": "news",
        "title": "한국언론진흥재단 뉴스빅데이터 메타데이터 - 범죄보도",
        "file": NEWS_FILE,
        "description": "범죄 보도 기사 메타데이터를 기반으로 뉴스 관점의 흐름을 확인하는 자료입니다.",
    },
    {
        "key": "region",
        "title": "경찰청 범죄 발생 지역별 통계",
        "file": REGION_FILE,
        "description": "시도/지역 단위로 범죄 발생 분포를 비교하는 자료입니다.",
    },
    {
        "key": "place",
        "title": "경찰청 범죄 발생 장소별 통계",
        "file": PLACE_FILE,
        "description": "범죄가 발생한 장소 유형을 기준으로 패턴을 확인하는 자료입니다.",
    },
    {
        "key": "time",
        "title": "경찰청 범죄 발생 시간대 및 요일",
        "file": TIME_FILE,
        "description": "시간대와 요일에 따른 범죄 발생 추이를 확인하는 자료입니다.",
    },
]

PAGE_LINKS = [
    ("메인", "appy.py", ""),
    ("홈", "pages/1__Home.py", ""),
    ("Dashboard", "pages/2__Dashboard.py", ""),
    ("Analytics", "pages/3__Analytics.py", ""),
    ("Settings", "pages/4_⚙️_Settings.py", "⚙️"),
]


def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="cp949")


def human_count(value: int) -> str:
    return f"{value:,}"


def numeric_frame(df: pd.DataFrame, skip: int = 2) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns[skip:]:
        out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0)
    return out


def inject_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg-1: #f5f2ea;
            --bg-2: #eef3f6;
            --ink: #0f172a;
            --muted: #64748b;
            --card: rgba(255, 255, 255, 0.78);
            --border: rgba(15, 23, 42, 0.10);
            --accent: #0f766e;
            --accent-2: #c2410c;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(15, 118, 110, 0.10), transparent 28%),
                radial-gradient(circle at top right, rgba(194, 65, 12, 0.08), transparent 26%),
                linear-gradient(180deg, var(--bg-1) 0%, var(--bg-2) 100%);
            font-family: "Aptos", "Segoe UI", "Noto Sans KR", "Apple SD Gothic Neo", sans-serif;
            color: var(--ink);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(16, 42, 67, 0.98) 0%, rgba(15, 23, 42, 0.98) 100%);
            border-right: 1px solid rgba(255, 255, 255, 0.06);
        }

        [data-testid="stSidebar"] * {
            color: #f8fafc !important;
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4 {
            color: #ffffff !important;
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 1280px;
        }

        h1, h2, h3 {
            letter-spacing: -0.03em;
        }

        .hero {
            position: relative;
            overflow: hidden;
            padding: 2.1rem 2rem 1.5rem 2rem;
            border-radius: 30px;
            background:
                linear-gradient(135deg, rgba(255, 255, 255, 0.88), rgba(255, 255, 255, 0.68)),
                radial-gradient(circle at top right, rgba(15, 118, 110, 0.08), transparent 38%);
            border: 1px solid rgba(15, 23, 42, 0.08);
            box-shadow: 0 18px 48px rgba(15, 23, 42, 0.08);
            margin-bottom: 1rem;
        }

        .hero-kicker {
            display: inline-block;
            padding: 0.35rem 0.75rem;
            border-radius: 999px;
            background: linear-gradient(90deg, rgba(15, 118, 110, 0.12), rgba(249, 115, 22, 0.12));
            color: var(--accent);
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            margin-bottom: 0.75rem;
        }

        .hero-title {
            margin: 0;
            font-size: 2.25rem;
            line-height: 1.08;
            font-weight: 800;
        }

        .hero-subtitle {
            margin-top: 0.75rem;
            color: var(--muted);
            font-size: 1rem;
            line-height: 1.65;
            max-width: 820px;
        }

        .tag-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 1rem;
        }

        .tag {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.42rem 0.72rem;
            border-radius: 999px;
            border: 1px solid rgba(15, 23, 42, 0.08);
            background: rgba(255, 255, 255, 0.88);
            font-size: 0.82rem;
            color: var(--ink);
        }

        .panel {
            position: relative;
            border-radius: 22px;
            background: var(--card);
            border: 1px solid var(--border);
            box-shadow: 0 16px 38px rgba(15, 23, 42, 0.06);
            padding: 1rem 1.1rem;
            margin: 0.35rem 0 0.85rem 0;
        }

        .panel::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, var(--accent), rgba(249, 115, 22, 0.92));
        }

        .panel-title {
            font-size: 1rem;
            font-weight: 800;
            color: var(--ink);
            margin-bottom: 0.25rem;
        }

        .panel-subtitle {
            color: var(--muted);
            font-size: 0.9rem;
            line-height: 1.5;
        }

        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.86);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 0.9rem 1rem;
            box-shadow: 0 12px 28px rgba(15, 23, 42, 0.05);
        }

        [data-testid="stMetricLabel"] {
            color: var(--muted);
            font-size: 0.84rem;
        }

        [data-testid="stMetricValue"] {
            color: var(--ink);
            font-weight: 800;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 18px;
            overflow: hidden;
            border: 1px solid var(--border);
        }

        .stMarkdown p {
            color: var(--ink);
        }

        hr {
            border-color: rgba(15, 23, 42, 0.10);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(kicker: str, title: str, subtitle: str, tags: list[str] | None = None) -> None:
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-kicker">{kicker}</div>
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
            <div class="tag-row">
                {''.join(f'<span class="tag">{tag}</span>' for tag in (tags or []))}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def panel(title: str, subtitle: str | None = None) -> None:
    st.markdown(
        f"""
        <div class="panel">
            <div class="panel-title">{title}</div>
            {f'<div class="panel-subtitle">{subtitle}</div>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_row(items: list[tuple[str, str]]) -> None:
    cols = st.columns(len(items))
    for col, (label, value) in zip(cols, items):
        col.metric(label, value)


def render_page_links(current: str | None = None) -> None:
    cols = st.columns(len(PAGE_LINKS))
    for col, (label, target, icon) in zip(cols, PAGE_LINKS):
        if current == target:
            col.markdown(f"**{icon} {label}**")
        else:
            col.page_link(target, label=label, icon=icon)
