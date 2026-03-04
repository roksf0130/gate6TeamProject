import os
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta, timezone
from pathlib import Path

# import matplotlib.pyplot as plt

# 터미널: pip install streamlit-autorefresh
from streamlit_autorefresh import st_autorefresh

# LOG_PATH = "predict.csv"
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_PATH = BASE_DIR / "predict.csv"

st.set_page_config(page_title="모니터링", page_icon="⚠️", layout="centered")
st.title(
    body="서비스 모니터링",
    width="stretch",
    text_alignment="center",
)

refresh_count = st_autorefresh(interval=5000, key="monitor_refresh")
st.caption(f"🔄 자동 갱신: 5초마다 / 갱신 횟수: {refresh_count}")

KST = timezone(timedelta(hours=9))

EXPECTED_COLS = [
    "ts",
    "client_id",
    "filename",
    "pred_label",
    "pred_prob",
    "decision",
    "latency_ms",
    "error",
]


def load_logs():
    if not os.path.exists(LOG_PATH):
        return pd.DataFrame(columns=EXPECTED_COLS)

    df = pd.read_csv(LOG_PATH)

    for c in EXPECTED_COLS:
        if c not in df.columns:
            df[c] = None

    if "ts" in df.columns:
        df["ts"] = pd.to_datetime(df["ts"], errors="coerce", utc=True).dt.tz_convert(
            KST
        )

    if "pred_prob" in df.columns:
        df["pred_prob"] = pd.to_numeric(df["pred_prob"], errors="coerce")
    if "latency_ms" in df.columns:
        df["latency_ms"] = pd.to_numeric(df["latency_ms"], errors="coerce")

    return df


df = load_logs()

# 사이드바
st.sidebar.markdown("---")
st.sidebar.write("필터")
window_hours = st.sidebar.slider("조회 기간(시간)", 1, 168, 24)
cutoff = datetime.now(KST) - timedelta(hours=window_hours)

dfw = df.copy()
if not dfw.empty and "ts" in dfw.columns:
    dfw = dfw[dfw["ts"] >= cutoff]

now_kst = datetime.now(KST)
st.sidebar.caption(f"기준 시각(KST): {now_kst.strftime('%Y-%m-%d %H:%M:%S')}")

if not dfw.empty and "ts" in dfw.columns and dfw["ts"].notna().any():
    last_log_ts = dfw["ts"].max()
else:
    last_log_ts = None

one_min_ago = now_kst - timedelta(minutes=1)
if not dfw.empty and "ts" in dfw.columns:
    new_1m = int((dfw["ts"] >= one_min_ago).sum())
else:
    new_1m = 0

col1, col2, col3, col4 = st.columns(4)

total = len(dfw)

if total and "error" in dfw.columns:
    errors = int((dfw["error"].fillna("") != "").sum())
else:
    errors = 0

err_rate = (errors / total * 100) if total else 0.0
avg_conf = (
    float(dfw["pred_prob"].dropna().mean())
    if total and "pred_prob" in dfw.columns
    else 0.0
)
avg_lat = (
    float(dfw["latency_ms"].dropna().mean())
    if total and "latency_ms" in dfw.columns
    else 0.0
)

col1.metric("요청 수", f"{total}", f"+{new_1m} (최근 1분)")
col2.metric("에러 수", f"{errors}", f"{err_rate:.1f}%")
col3.metric(
    "마지막 로그(KST)",
    last_log_ts.strftime("%m-%d %H:%M:%S") if last_log_ts is not None else "-",
)
col4.metric("평균 Confidence", f"{avg_conf:.3f}")

st.divider()

# 차트
left, right = st.columns(2)

with left:
    st.subheader("클래스 분포")
    if total and "pred_label" in dfw.columns:
        class_counts = (
            dfw["pred_label"]
            .fillna("(unknown)")
            .replace("", "(unknown)")
            .value_counts()
        )
        st.bar_chart(class_counts)
    else:
        st.info("표시할 로그가 없습니다.")

with right:
    st.subheader("반입 가능/불가 비율")
    if total and "decision" in dfw.columns:
        decision_counts = (
            dfw["decision"].fillna("(unknown)").replace("", "(unknown)").value_counts()
        )
        st.bar_chart(decision_counts)
    else:
        st.info("표시할 로그가 없습니다.")

st.divider()

# 시간대별 그래프
st.subheader("시간대별 요청량")
if total and "ts" in dfw.columns:
    tmp = dfw.dropna(subset=["ts"]).copy()
    tmp["bucket"] = tmp["ts"].dt.floor("10min")
    traffic = tmp.groupby("bucket").size()
    st.line_chart(traffic)
else:
    st.info("표시할 로그가 없습니다.")

st.divider()

# 최근 요청 목록
st.subheader("최근 요청 로그")
show_n = st.slider("표시 개수", 10, 200, 50)

if total:
    show_cols = [
        "ts",
        "filename",
        "pred_label",
        "pred_prob",
        "decision",
        "latency_ms",
        "error",
    ]
    show_cols = [c for c in show_cols if c in dfw.columns]
    st.dataframe(
        dfw.sort_values("ts", ascending=False)[show_cols].head(show_n), width="stretch"
    )
else:
    st.info("표시할 로그가 없습니다.")

# 새로고침/초기화
st.sidebar.divider()
if st.sidebar.button("새로고침"):
    st.rerun()

if st.sidebar.button("로그 초기화(주의)"):
    if os.path.exists(LOG_PATH):
        os.remove(LOG_PATH)
    st.rerun()
