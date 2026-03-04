import requests
import time
from pathlib import Path
from usermodules import extract_battery_spec
import streamlit as st


def azure_cv_ocr():
    # Azure Computer Vision API 를 이용한 OCR
    wattage = 0
    return_type = 0

    # load_dotenv()

    BASE_DIR = Path(__file__).resolve().parent
    image_path = BASE_DIR.parent / "uploads" / "fixed_temp_image.jpg"

    # 기본 설정
    try:
        endpoint = st.secrets["AZURE_CV_OCR_ENDPOINT"]
        key = st.secrets["AZURE_CV_OCR_KEY"]
        url = endpoint.rstrip("/") + "/vision/v3.2/read/analyze"
    except KeyError as e:
        st.error(f"Missing configuration: {e}")
        return 0, 0

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/octet-stream",
    }

    try:
        with open(image_path, "rb") as f:
            ocr_image_data = f.read()

        # Azure Computer Vision API 호출
        response = requests.post(url, headers=headers, data=ocr_image_data, timeout=30)
        response.raise_for_status()
        operation_url = response.headers["Operation-Location"]

        # 응답 대기 (최대 횟수를 10으로 제한)
        max_attempts = 10
        for _ in range(max_attempts):
            result_resp = requests.get(
                operation_url, headers={"Ocp-Apim-Subscription-Key": key}, timeout=10
            )
            result_resp.raise_for_status()
            result_json = result_resp.json()

            if result_json["status"] == "succeeded":
                break
            elif result_json["status"] == "failed":
                st.error("OCR operation failed on Azure side.")
                return 0, 0

            time.sleep(1)

        else:
            st.error("OCR 타임아웃 발생")
            return 0, 0

        # OCR 결과에서 텍스트 추출
        full_text = ""
        for page in result_json.get("analyzeResult", {}).get("readResults", []):
            for line in page.get("lines", []):
                full_text += line.get("text", "") + " "

    except Exception as e:
        st.error(f"OCR 요청 실패: {e}")
        return 0, 0

    # 텍스트 클리닝
    specs = extract_battery_spec.extract_battery_spec(full_text)

    wh = specs.get("Wh")
    mah = specs.get("mAh")
    v = specs.get("V")

    # 판별 로직 (return_value : 0 문자인식 실패, 1 기내반입 가능(5개), 2 기내반입 가능(2개 카운터방문 필요), 3 불가)
    # 전력량이 표시되어 있을 때는 전력량으로 결과 리턴
    if wh:
        # 전력량을 바로 찾았을 때
        try:
            wattage = float(wh)
        except ValueError:
            return 0, 0
    elif mah and v:
        # 전력량이 표시되어 있지 않을 때는 전류와 전압으로 전력량 계산
        try:
            # 전력량은 전류 * 전압으로 계산
            wattage = (float(mah) / 1000.0) * float(v)
        except ValueError:
            return 0, 0
    else:
        # 인식을 제대로 못했을 경우에는 0을 리턴
        return 0, 0

    # 기내반입여부 리턴
    if wattage <= 100:
        return_type = 1  # 반입 가능
    elif wattage <= 160:
        return_type = 2  # 제한적 기내반입 가능
    else:
        return_type = 3  # 반입 불가

    return wattage, return_type
