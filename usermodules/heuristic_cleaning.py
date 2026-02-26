import re

def heuristic_cleaning(text):
    # 흔한 오타 교정 (Case-insensitive)
    # vvH, VVh -> Wh / W/h -> Wh
    text = re.sub(r'(vv|VV|W/|W\s)h', 'Wh', text, flags=re.IGNORECASE)

    # mAh 오타 교정 (mAn, m4h 등)
    text = re.sub(r'mA(n|h|H|4)', 'mAh', text, flags=re.IGNORECASE)

    # 영문 O/o를 숫자 0으로 (단위 바로 앞인 경우)
    # text = re.sub(r'([OoD]+)(?=\s?(?:Wh|mAh|V))', '0', text, flags=re.IGNORECASE)
    text = re.sub(r'([OoDC]+)(?=\s?(?:Wh|mAh|V))', lambda m: '0' * len(m.group(1)), text, flags=re.IGNORECASE)

    return text
