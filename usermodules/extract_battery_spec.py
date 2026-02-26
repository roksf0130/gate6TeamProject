import re
from usermodules import heuristic_cleaning

def extract_battery_spec(text):
    # 텍스트 정제 (잘못 인식된 글자 수정)
    clean_text = heuristic_cleaning.heuristic_cleaning(text)

    # 1차 정제된 텍스트에서 불필요한 특수문자를 공백으로 변환
    clean_text = re.sub(r'[^\w\s.,]', ' ', clean_text)

    # 숫자와 단위를 쌍으로 추출 (예: 74Wh, 20000 mAh)
    # 패턴
    # /d+ : 숫자로 시작하며 숫자 1개 이상
    # [\d.,]* : 숫자 . , 가 0개 이상
    # \s? : 숫자와 단위 사이에 공백이 0개 또는 1개 존재
    # \s : 단위뒤에 공란이 1개 이상
    pattern = r'(\d+[\d.,]*)\s?(Wh|mAh|V)\s+'
    matches = re.findall(pattern, clean_text, re.IGNORECASE)

    results = {}
    for value, unit in matches:
        # 단위를 표준형으로 변환
        standard_unit = "Wh" if "w" in unit.lower() else ("mAh" if "m" in unit.lower() else "V")
        # 숫자 속 콤마 정리 (20,000 -> 20000)
        clean_value = value.replace(',', '')
        if results.get(standard_unit) == None:
            results[standard_unit] = clean_value

    return results
