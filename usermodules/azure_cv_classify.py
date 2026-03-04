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

    if "client_id" not in st.session_state:
        st.session_state.client_id = f"session-{int(time.time())}"

    classify_result = ""
    probability = 0
    return_type = 0

    BASE_DIR = Path(__file__).resolve().parent
    image_path = BASE_DIR.parent / "uploads" / "fixed_classify_image.jpg"
    LOG_PATH = BASE_DIR.parent / "predict.csv"

    azure_cv_endpoint = st.secrets["AZURE_CV_CLASSIFY_ENDPOINT"]
    azure_cv_key = st.secrets["AZURE_CV_CLASSIFY_KEY"]
    azure_cv_url = (
        azure_cv_endpoint
        + "customvision/v3.0/Prediction/0c07f4c5-7f9b-4c1b-9b21-3c7f0dfd2538/classify/iterations/test_9/image"
    )

    azure_cv_headers = {
        "Prediction-Key": azure_cv_key,
        "Content-Type": "application/octet-stream",
    }

    with open(image_path, "rb") as f:
        classify_image = f.read()
    # 바이트 데이터를 PIL 이미지 객체로 변환
    img = Image.open(io.BytesIO(classify_image))
    img = img.convert("RGB")

    # 목표 사이즈 설정
    target_size = (224, 224)

    # 원본 사진의 비율 유지하며 리사이즈하고 나머지를 검정색으로 채우기.
    preprocessed_img = ImageOps.pad(img, target_size, color=(0, 0, 0))

    # 애저CV를 이용한 물품판별을 위해 전처리된 이미지를 다시 바이트 형태로 변환
    buffer = io.BytesIO()
    preprocessed_img.save(buffer, format="JPEG")
    classify_image = buffer.getvalue()

    start = time.time()

    # Azure CV를 이용한 OCR 시작
    classify_cv_response = requests.post(
        azure_cv_url, headers=azure_cv_headers, data=classify_image
    )
    classify_cv_response.raise_for_status()
    raw = classify_cv_response.json()

    pred_label, pred_prob = parse_top1(raw)
    error_msg = ""
    decision = ""
    if pred_prob is None:
        error_msg = "no_predictions"
        decision = "ERROR"
    else:
        decision = decision_rule(pred_label, pred_prob, threshold=0.75)

    latency_ms = int((time.time() - start) * 1000)

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
            "error": error_msg,
        },
    )

    # 응답코드 확인
    if classify_cv_response.status_code != 200:
        # 정상응답을 받지 못한 경우 return 처리
        classify_result = ""
        probability = 0
        return_type = 0
    else:
        result_json = classify_cv_response.json()

        # 예측 결과 정렬
        predictions = sorted(
            result_json["predictions"], key=lambda x: x["probability"], reverse=True
        )
        # 정렬 후 가장 확률이 높은 아이템 가져오기
        top_item = predictions[0]

        classify_result = top_item["tagName"]
        probability = top_item["probability"]
        return_type = 1

    return classify_result, probability, return_type
