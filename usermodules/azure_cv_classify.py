import requests
import time
from pathlib import Path
from usermodules import extract_battery_spec
import streamlit as st

def azure_cv_classify():
    classify_result = ''
    probability = 0
    return_type = 0

    BASE_DIR = Path(__file__).resolve().parent
    image_path = BASE_DIR.parent / 'uploads' / 'fixed_classify_image.jpg'

    azure_cv_endpoint = st.secrets['AZURE_CV_CLASSIFY_ENDPOINT']
    azure_cv_key = st.secrets['AZURE_CV_CLASSIFY_KEY']
    azure_cv_url = azure_cv_endpoint + 'customvision/v3.0/Prediction/0c07f4c5-7f9b-4c1b-9b21-3c7f0dfd2538/classify/iterations/test_9/image'

    azure_cv_headers = {
        'Prediction-Key': azure_cv_key,
        'Content-Type': 'application/octet-stream'
    }

    with open(image_path, 'rb') as f:
        classify_image = f.read()

    # Azure CV를 이용한 OCR 시작
    classify_cv_response = requests.post(azure_cv_url, headers=azure_cv_headers, data=classify_image)

    # 응답코드 확인
    if classify_cv_response.status_code != 200:
        # 정상응답을 받지 못한 경우 return 처리
        classify_result = ''
        probability = 0
        return_type = 0
    else:
        result_json = classify_cv_response.json()

        # 예측 결과 정렬
        predictions = sorted(
            result_json['predictions'],
            key = lambda x : x['probability'],
            reverse=True
        )
        # 정렬 후 가장 확률이 높은 아이템 가져오기
        top_item = predictions[0]

        classify_result = top_item['tagName']
        probability = top_item['probability']
        return_type = 1

    return classify_result, probability, return_type
