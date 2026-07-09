from __future__ import annotations

import streamlit as st

import pandas as pd

from crime_shared import DATASETS, hero, human_count, inject_theme, load_csv, metric_row, panel, render_page_links


st.set_page_config(page_title="범죄 데이터 분석", page_icon="📊", layout="wide")
inject_theme()


def dataset_stats(df: pd.DataFrame) -> dict[str, str]:
    return {
        "행 수": human_count(len(df)),
        "열 수": human_count(len(df.columns)),
        "결측치": human_count(int(df.isna().sum().sum())),
    }


def render_home() -> None:
    hero(
        "Crime Data Overview",
        "범죄 데이터를 한 화면에서 정리하고 탐색하는 대시보드",
        "시간대, 지역, 장소, 뉴스보도 데이터를 같은 기준으로 비교하도록 설계했습니다. "
        "핵심 통계와 원본 데이터 미리보기를 빠르게 확인할 수 있습니다.",
        ["CSV 4종", "cp949", "Streamlit", "지역·장소·시간 분석"],
    )

    st.markdown("### 빠른 이동")
    render_page_links(current="appy.py")

    panel("페이지 구성", "왼쪽 사이드바에서 분석할 데이터셋을 고릅니다.")

    loaded = []
    for item in DATASETS:
        if item["file"].exists():
            try:
                df = load_csv(item["file"])
                loaded.append((item, df))
            except Exception:
                pass

    metric_row(
        [
            ("데이터 파일", str(len(DATASETS))),
            ("불러온 파일", str(len(loaded))),
            ("총 행 수", human_count(sum(len(df) for _, df in loaded))),
            ("총 열 수", human_count(sum(len(df.columns) for _, df in loaded))),
        ]
    )

    st.markdown("### 데이터셋 개요")
    overview_rows = []
    for item in DATASETS:
        if item["file"].exists():
            try:
                df = load_csv(item["file"])
                overview_rows.append(
                    {
                        "구분": item["title"],
                        "파일명": item["file"].name,
                        "행 수": len(df),
                        "열 수": len(df.columns),
                        "설명": item["description"],
                    }
                )
            except Exception as exc:
                overview_rows.append(
                    {
                        "구분": item["title"],
                        "파일명": item["file"].name,
                        "행 수": "-",
                        "열 수": "-",
                        "설명": f"불러오기 실패: {exc}",
                    }
                )
        else:
            overview_rows.append(
                {
                    "구분": item["title"],
                    "파일명": item["file"].name,
                    "행 수": "-",
                    "열 수": "-",
                    "설명": "파일이 존재하지 않습니다.",
                }
            )
    st.dataframe(pd.DataFrame(overview_rows), use_container_width=True, hide_index=True)

    st.markdown("### 빠른 안내")
    left, right = st.columns([1.1, 0.9])
    with left:
        st.markdown(
            """
            - `홈`: 전체 데이터 상태와 구조를 요약합니다.
            - `뉴스보도`: 기사 메타데이터의 분포를 확인합니다.
            - `지역별 통계`: 시도 단위 범죄 발생을 비교합니다.
            - `장소별 통계`: 장소 유형별 범죄 발생을 확인합니다.
            - `시간대/요일`: 시간 흐름과 요일 패턴을 봅니다.
            """
        )
    with right:
        st.info("모든 페이지는 `data/` 폴더와 `cp949` 인코딩을 공통으로 사용합니다.")


def render_dataset(item: dict[str, str]) -> None:
    hero(
        "Dataset Detail",
        item["title"],
        item["description"],
        ["원본 미리보기", "기본 통계", item["file"].name],
    )

    if not item["file"].exists():
        st.error(f"파일을 찾을 수 없습니다: {item['file'].name}")
        return

    try:
        df = load_csv(item["file"])
    except Exception as exc:
        st.error(f"CSV를 불러오지 못했습니다: {exc}")
        return

    stats = dataset_stats(df)
    metric_row(
        [
            ("행 수", stats["행 수"]),
            ("열 수", stats["열 수"]),
            ("결측치", stats["결측치"]),
        ]
    )

    st.markdown("### 요약 정보")
    left, right = st.columns([1.15, 0.85])
    with left:
        st.markdown(
            f"""
            <div class="panel">
                <div class="panel-title">파일 정보</div>
                <div class="panel-subtitle">
                    파일명: <strong>{item["file"].name}</strong><br/>
                    데이터 설명: {item["description"]}<br/>
                    컬럼 수: {len(df.columns)}개<br/>
                    행 수: {len(df):,}행
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("#### 컬럼 목록")
        st.write(", ".join(map(str, df.columns)))

    with right:
        st.markdown(
            f"""
            <div class="panel">
                <div class="panel-title">분석 메모</div>
                <div class="panel-subtitle">
                    이 데이터셋은 {item["title"]} 분석에 사용됩니다.<br/>
                    결측치와 컬럼 구조를 먼저 확인한 뒤, 아래 미리보기에서 실제 값을 점검하세요.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### 데이터 미리보기")
    preview_tab1, preview_tab2 = st.tabs(["상위 행", "결측치"])
    with preview_tab1:
        st.dataframe(df.head(20), use_container_width=True, hide_index=True)
    with preview_tab2:
        missing = df.isna().sum().reset_index()
        missing.columns = ["컬럼", "결측치"]
        st.dataframe(missing, use_container_width=True, hide_index=True)


def main() -> None:
    options = ["홈"] + [item["title"] for item in DATASETS]
    choice = st.sidebar.selectbox("페이지 선택", options)
    st.sidebar.markdown("### 빠른 이동")
    render_page_links(current="appy.py")
    st.sidebar.markdown("### 데이터 파일")
    for item in DATASETS:
        st.sidebar.write(f"- {item['file'].name}")

    st.sidebar.markdown("### 사용 팁")
    st.sidebar.caption("홈에서 전체 구조를 확인한 뒤, 필요한 데이터셋을 개별적으로 열어 보세요.")

    if choice == "홈":
        render_home()
        return

    selected = next(item for item in DATASETS if item["title"] == choice)
    render_dataset(selected)


if __name__ == "__main__":
    main()
