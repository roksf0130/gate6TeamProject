import requests
import time
from pathlib import Path
import streamlit as st
from PIL import Image, ImageOps
import io
from usermodules.cv_logging import (
    parse_top1,
    decision_rule,
    append_log,
    now_utc_iso_no_microseconds,
)


def azure_cv_classify():
    # Azure Custom Vision API 를 이용한 이미지 분류

    if "client_id" not in st.session_state:
        st.session_state.client_id = f"session-{int(time.time())}"

    classify_result = ""
    probability = 0
    return_type = 0

    # PATH 및 각종 설정
    BASE_DIR = Path(__file__).resolve().parent
    image_path = BASE_DIR.parent / "uploads" / "fixed_classify_image.jpg"
    LOG_PATH = BASE_DIR.parent / "predict.csv"

    try:
        endpoint = st.secrets["AZURE_CV_CLASSIFY_ENDPOINT"]
        key = st.secrets["AZURE_CV_CLASSIFY_KEY"]
        url = (
            endpoint.rstrip("/")
            + "/customvision/v3.0/Prediction/0c07f4c5-7f9b-4c1b-9b21-3c7f0dfd2538/classify/iterations/test_9/image"
        )
    except KeyError as e:
        st.error(f"Azure 기본 설정 오류: {e}")
        return "", 0, 0

    headers = {
        "Prediction-Key": key,
        "Content-Type": "application/octet-stream",
    }

    # 이미지 처리
    # Image Preprocessing
    try:
        with open(image_path, "rb") as f:
            raw_image_data = f.read()

        img = Image.open(io.BytesIO(raw_image_data)).convert("RGB")

        # 원본 사진의 비율 유지하며 리사이즈하고 나머지를 검정색으로 채우기.
        target_size = (224, 224)
        preprocessed_img = ImageOps.pad(img, target_size, color=(0, 0, 0))

        # 애저CV를 이용한 물품판별을 위해 전처리된 이미지를 다시 바이트 형태로 변환
        buffer = io.BytesIO()
        preprocessed_img.save(buffer, format="JPEG")
        processed_image_bytes = buffer.getvalue()
    except Exception as e:
        st.error(f"이미지 처리 오류: {e}")
        return "", 0, 0

    # Azure API 호출
    start_time = time.time()

    try:
        response = requests.post(
            url, headers=headers, data=processed_image_bytes, timeout=30
        )
        response.raise_for_status()
        result_json = response.json()
    except Exception as e:
        latency_ms = int((time.time() - start_time) * 1000)
        append_log(
            LOG_PATH,
            {
                "ts": now_utc_iso_no_microseconds(),
                "client_id": st.session_state.client_id,
                "filename": "fixed_classify_image.jpg",
                "pred_label": "",
                "pred_prob": "",
                "decision": "ERROR",
                "latency_ms": latency_ms,
                "error": str(e),
            },
        )
        return "", 0, 0

    latency_ms = int((time.time() - start_time) * 1000)
    pred_label, pred_prob = parse_top1(result_json)

    decision = (
        decision_rule(pred_label, pred_prob, threshold=0.75) if pred_prob else "ERROR"
    )

    # 모니터링을 위한 로깅
    append_log(
        LOG_PATH,
        {
            "ts": now_utc_iso_no_microseconds(),
            "client_id": st.session_state.client_id,
            "filename": "fixed_classify_image.jpg",
            "pred_label": pred_label,
            "pred_prob": pred_prob if pred_prob is not None else "",
            "decision": decision,
            "latency_ms": latency_ms,
            "error": "",
        },
    )

    if pred_label:
        classify_result = pred_label
        probability = pred_prob
        return_type = 1

    return classify_result, probability, return_type
