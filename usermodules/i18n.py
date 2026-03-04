import streamlit as st

# UI 문자열 dict
# 0: Korean (langpack=0)
# 1: English (langpack=1)

STRINGS = {
    "sidebar_language": ["언어", "LANGUAGE"],
    "sidebar_font_size": ["글자 크기", "FONT SIZE"],
    "font_normal": ["보통", "NORMAL"],
    "font_big": ["크게", "BIG"],
    "nav_home": ["HOME", "HOME"],
    "nav_restricted": ["운송제한물품 안내", "Restricted Items"],
    "nav_contact": ["오류 신고 / 제보하기", "Contact Us"],
    "nav_admin": ["ADMIN", "ADMIN"],
    "page01_title": ["👜 기내반입 가능 물품 판별", "👜 Carry-on Item Identification"],
    "page01_sub_title": [
        "💡 보조배터리 기내반입 판별",
        "💡 Power Bank Carry-on Identification",
    ],
    "page02_title": ["🔋 리튬배터리", "🔋 Lithium Battery"],
    "page03_title": ["💣 항공기 반입금지 물품", "💣 Prohibited Items"],
    "page04_title": ["💊 제한적 기내 반입 물품", "💊 Restricted Carry-on Items"],
    "page05_title": ["🥂 위탁 수하물 제한 물품", "🥂 Restricted Checked Items"],
    "page07_title": ["😍 오류신고 / 제보하기", "😍 Error Report / Tips"],
    "page08_title": ["⚠️ ADMIN", "⚠️ ADMIN"],
    "ai_analysis_header": ["💻 AI 분석 결과", "💻 AI Analysis Results"],
    "analyzing_msg": [
        "AI가 이미지를 분석 중입니다. 잠시만 기다려 주세요...",
        "AI is analyzing the image. Please wait...",
    ],
    "analysis_complete": ["✅ 분석이 완료되었습니다!", "✅ Analysis complete!"],
    "analysis_failed": ["❌ 사진 분석에 실패했습니다.", "❌ Photo analysis failed."],
    "analysis_failed_battery": [
        "❌ 사진 분석에 실패했습니다. 배터리 스펙부분을 확대한 선명한 사진을 업로드하면 인식률이 더욱 향상됩니다.",
        "❌ Photo analysis failed. For better results, upload a clear, zoomed-in photo of the battery specs.",
    ],
    "carry_on_info": [
        "본 서비스는 AI 분석 결과를 기반으로 한 참고 정보입니다. 항공사 및 국가별 보안 규정은 수시로 변경될 수 있으며, 실제 반입 가능 여부는 해당 항공사 및 공항 보안 당국의 판단을 따릅니다.",
        "This service provides reference information based on AI analysis. Security regulations vary by airline and country. Final decisions are made by airlines and airport security.",
    ],
    "uploader_label": [
        "물품 사진을 촬영 또는 업로드해주세요. 사진은 판별 후 즉시 삭제됩니다.",
        "Please take or upload a photo of the item. It will be deleted immediately after identification.",
    ],
    "uploader_label_battery": [
        "보조배터리의 상세 스펙 사진을 촬영 또는 업로드해주세요. 사진은 판별 후 즉시 삭제됩니다.",
        "Please upload a photo of the power bank specifications. It will be deleted immediately.",
    ],
    "btn_start_analysis": ["분석시작", "Start Analysis"],
    "btn_check_battery": [
        "보조배터리 기내반입 가능여부 확인",
        "Check Power Bank Carry-on Status",
    ],
    "restricted items": [
        "이 물품은 기내반입이 불가합니다.",
        "This item is not permitted carry-on.",
    ],
    "btn_battery_calc": ["배터리 용량 계산법", "Capacity Calculation Method"],
    "image_caption": ["판별대상물품", "Item for identification"],
    "privacy_toast": [
        "개인정보 보호를 위해 사진이 삭제되었습니다.",
        "Photo deleted for privacy protection.",
    ],
    "measured_power": ["측정된 전력량", "Measured Power"],
    "battery_ok_5": [
        "✈️ 1인 5개까지 기내 반입이 가능한 용량입니다.",
        "✈️ Up to 5 items per person allowed.",
    ],
    "battery_ok_2": [
        "✈️ 1인 2개까지 기내 반입이 가능하지만 승인을 위해 카운터 방문이 필요합니다.",
        "✈️ Up to 2 items allowed, but requires counter approval.",
    ],
    "battery_no": ["❌ 기내 반입 불가 용량입니다.", "❌ Carry-on not permitted."],
    "modal_title": ["배터리 용량 계산법 안내", "Battery Capacity Calculation"],
    "modal_close": ["닫기", "Close"],
    "honey_title": [
        "자기야!! 이거 :blue[기내반입] 되나? 🤔",
        "Honey! Can I bring this on board? 🤔",
    ],
}


def get_text(key):
    """
    Returns the localized string based on the current langpack in session_state.
    """
    lang = st.session_state.get("langpack", 0)
    return STRINGS.get(key, ["", ""])[lang]
