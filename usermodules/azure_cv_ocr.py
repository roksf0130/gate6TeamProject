import requests
import time
import os
from dotenv import load_dotenv
from pathlib import Path
from usermodules import extract_battery_spec

def azure_cv_ocr():
    wattage = 0
    return_type = 0

    load_dotenv()

    BASE_DIR = Path(__file__).resolve().parent
    image_path = BASE_DIR.parent / "uploads" / "fixed_temp_image.jpg"

    # 기본 설정
    azure_cv_endpoint = os.getenv("AZURE_CV_ENDPOINT")
    azure_cv_key = os.getenv("AZURE_CV_KEY")
    azure_cv_url = azure_cv_endpoint + "vision/v3.2/read/analyze"

    azure_cv_headers = {
        "Ocp-Apim-Subscription-Key": azure_cv_key,
        "Content-Type": "application/octet-stream"
    }

    with open(image_path, "rb") as f:
        ocr_image = f.read()

    # Azure CV를 이용한 OCR 시작
    azure_cv_response = requests.post(azure_cv_url, headers=azure_cv_headers, data=ocr_image)
    operation_url = azure_cv_response.headers["Operation-Location"]

    # Azure에서 응답이 올때까지 대기
    while True:
        result = requests.get(operation_url, headers={"Ocp-Apim-Subscription-Key": azure_cv_key})
        result_json = result.json()

        if result_json["status"] == "succeeded":
            break

        time.sleep(1)

    # OCR 인식 결과에서 텍스트 추출
    full_text = ""
    for page in result_json["analyzeResult"]["readResults"]:
        for line in page["lines"]:
            full_text += line["text"] + " "

    # 텍스트 클리닝
    cleaned_text = extract_battery_spec.extract_battery_spec(full_text)

    wh_pattern = cleaned_text.get('Wh')
    mah_pattern = cleaned_text.get('mAh')
    v_pattern = cleaned_text.get('V')

    # 판별 로직 (return_value : 0 문자인식 실패, 1 기내반입 가능(5개), 2 기내반입 가능(2개 카운터방문 필요), 3 불가)
    # 전력량이 표시되어 있을 때는 전력량으로 결과 리턴
    if wh_pattern:
        # 숫자만 추출
        wattage = float(wh_pattern)

        if wattage <= 100:
            return_type = 1
        elif wattage <= 160:
            return_type = 2
        else:
            return_type = 3
    # 전력량이 표시되어 있지 않을 때는 전류와 전압으로 전력량 계산
    elif mah_pattern and v_pattern:
        floatValue_mAh = float(mah_pattern)
        floatValue_V = float(v_pattern)
        wattage = (floatValue_mAh / 1000) * floatValue_V    # 전력량은 전류 * 전압으로 계산

        if wattage <= 100:
            return_type = 1
        elif wattage <= 160:
            return_type = 2
        else:
            return_type = 3
    # 인식을 제대로 못했을 경우에는 0을 리턴
    else:
        return_type = 0

    return wattage, return_type
