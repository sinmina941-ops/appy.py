from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parent
DATA_ROOT = ROOT / "data"

DATASETS = [
    {
        "key": "news",
        "title": "한국언론진흥재단 뉴스빅데이터 메타데이터 - 범죄보도",
        "file": DATA_ROOT / "한국언론진흥재단_뉴스빅데이터_메타데이터_범죄보도_20231231.csv",
        "description": "범죄 보도 기사 메타데이터를 기반으로 뉴스 관점의 흐름을 확인하는 자료입니다.",
    },
    {
        "key": "region",
        "title": "경찰청 범죄 발생 지역별 통계",
        "file": DATA_ROOT / "경찰청_범죄 발생 지역별 통계_20241231.csv",
        "description": "시도/지역 단위로 범죄 발생 분포를 비교하는 자료입니다.",
    },
    {
        "key": "place",
        "title": "경찰청 범죄 발생 장소별 통계",
        "file": DATA_ROOT / "경찰청_범죄 발생 장소별 통계_20241231.csv",
        "description": "범죄가 발생한 장소 유형을 기준으로 패턴을 확인하는 자료입니다.",
    },
    {
        "key": "time",
        "title": "경찰청 범죄 발생 시간대 및 요일",
        "file": DATA_ROOT / "경찰청_범죄 발생 시간대 및 요일_20191231.csv",
        "description": "시간대와 요일에 따른 범죄 발생 추이를 확인하는 자료입니다.",
    },
]


st.set_page_config(
    page_title="범죄 데이터 분석",
    page_icon="📊",
    layout="wide",
)


@st.cache_data(show_spinner=False)
def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(Path(path), encoding="cp949")


def human_count(value: int) -> str:
    return f"{value:,}"


def dataset_stats(df: pd.DataFrame) -> dict[str, str]:
    return {
        "행 수": human_count(len(df)),
        "열 수": human_count(len(df.columns)),
        "결측치": human_count(int(df.isna().sum().sum())),
    }


def render_home() -> None:
    st.title("홈")
    st.write("범죄 관련 4개 CSV를 하나의 Streamlit 앱에서 요약해서 볼 수 있도록 정리했습니다.")

    st.markdown(
        """
        ## 페이지 목록

        왼쪽 사이드바에서 데이터를 선택하세요.

        1. **홈** - 전체 개요와 빠른 통계
        2. **뉴스보도** - 범죄 관련 뉴스 메타데이터 요약
        3. **지역별 통계** - 지역 단위 범죄 분포
        4. **장소별 통계** - 장소 유형별 범죄 분포
        5. **시간대/요일** - 시간 패턴 분석
        """
    )

    loaded = []
    for item in DATASETS:
        if item["file"].exists():
            try:
                df = load_csv(str(item["file"]))
                loaded.append((item, df))
            except Exception:
                pass

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("데이터 파일", str(len(DATASETS)))
    col2.metric("불러온 파일", str(len(loaded)))
    col3.metric("총 행 수", human_count(sum(len(df) for _, df in loaded)))
    col4.metric("총 열 수", human_count(sum(len(df.columns) for _, df in loaded)))

    st.subheader("데이터셋 개요")
    overview_rows = []
    for item in DATASETS:
        if item["file"].exists():
            try:
                df = load_csv(str(item["file"]))
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


def render_dataset(item: dict[str, str]) -> None:
    st.title(item["title"])
    st.write(item["description"])

    if not item["file"].exists():
        st.error(f"파일을 찾을 수 없습니다: {item['file'].name}")
        return

    try:
        df = load_csv(str(item["file"]))
    except Exception as exc:
        st.error(f"CSV를 불러오지 못했습니다: {exc}")
        return

    stats = dataset_stats(df)
    c1, c2, c3 = st.columns(3)
    c1.metric("행 수", stats["행 수"])
    c2.metric("열 수", stats["열 수"])
    c3.metric("결측치", stats["결측치"])

    st.subheader("컬럼 목록")
    st.write(", ".join(map(str, df.columns)))

    st.subheader("데이터 미리보기")
    st.dataframe(df.head(20), use_container_width=True, hide_index=True)

    st.subheader("기본 요약")
    summary_col1, summary_col2 = st.columns(2)
    with summary_col1:
        st.write("상위 5개 행")
        st.dataframe(df.head(5), use_container_width=True, hide_index=True)
    with summary_col2:
        st.write("결측치 개수")
        missing = df.isna().sum().reset_index()
        missing.columns = ["컬럼", "결측치"]
        st.dataframe(missing, use_container_width=True, hide_index=True)


def main() -> None:
    options = ["홈"] + [item["title"] for item in DATASETS]
    choice = st.sidebar.selectbox("페이지 선택", options)

    st.sidebar.markdown("### 데이터 파일")
    for item in DATASETS:
        st.sidebar.write(f"- {item['file'].name}")

    if choice == "홈":
        render_home()
        return

    selected = next(item for item in DATASETS if item["title"] == choice)
    render_dataset(selected)


if __name__ == "__main__":
    main()
