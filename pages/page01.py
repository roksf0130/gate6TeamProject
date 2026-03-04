import time
import os
import streamlit as st
from PIL import Image
from usermodules import azure_cv_classify
from deep_translator import GoogleTranslator
from usermodules.i18n import get_text
from usermodules.ui_components import (
    show_progress_bar,
    handle_image_removal,
    session_change,
)

# 세션 초기화
if "processed" not in st.session_state:
    st.session_state.processed = False


# 콜백함수
def session_change():
    if st.session_state.processed == True:
        st.session_state.processed = False
    else:
        st.session_state.processed = True


def classify_analyze():
    """
    업로드된 사진을 AI 모델을 이용하여 분석하고 결과를 화면에 출력하는 함수
    기내반입가능여부를 판단하며, 보조배터리인 경우는 추가 안내 문구 출력
    """
    st.write(get_text("ai_analysis_header"))

    # progress bar 생성
    show_progress_bar()

    # 함수 호출
    classify_result, probability, return_type = azure_cv_classify.azure_cv_classify()

    # 사진 분석에 실패한 경우는 실패 메세지 출력하고 종료
    if return_type == 0:
        st.error(get_text("analysis_failed"))
        return

    korText = f"<{classify_result}> 으로 확인됩니다. 신뢰도는 {round(probability * 100, 2)}% 입니다."

    # 고정되지 않은 문자열은 GoogleTranslator 를 활용하여 번역
    if st.session_state["langpack"] == 1:
        display_text = GoogleTranslator(source="auto", target="en").translate(korText)
    else:
        display_text = korText

    # 반입 가능한 물품 또는 보조배터리인 경우 메세지 출력
    if classify_result == "반입 가능한 물품":
        st.info(display_text)
    else:
        st.error(display_text)
        if classify_result == "보조배터리":
            st.error(get_text("btn_check_battery"))
        else:
            st.error(get_text("restricted items"))


# 페이지 설정
st.set_page_config(
    page_title=get_text("page01_title"),
    layout="centered",
)
st.title(
    body=get_text("honey_title"), width="stretch", text_alignment="center", anchor=False
)

# info 출력
st.info(get_text("carry_on_info"))

st.markdown("---")

# 파일 업로드 영역
uploaded_file = st.file_uploader(
    label=get_text("uploader_label"),
    type=["jpg", "jpeg", "png", "bmp"],
    on_change=session_change,
)

# 업로드가 완료된 이후 프로세스
if uploaded_file is not None:
    # 두 개로 영역 분할
    col1, col2 = st.columns(spec=2, width="stretch")

    with col1:
        if st.button(
            label=get_text("btn_start_analysis"),
            width="stretch",
            on_click=session_change,
        ):
            if os.path.exists("uploads/fixed_classify_image.jpg"):
                with col2:
                    classify_analyze()

                # 분석 완료 후 업로드된 사진은 삭제
                handle_image_removal("uploads/fixed_classify_image.jpg")
        with Image.open(uploaded_file) as image:
            st.image(
                image=image,
                caption=get_text("image_caption"),
                width="stretch",
            )
            image = image.convert("RGB")  # MPO 정보를 버리고 일반 RGB로 변환

            # 판별을 위한 임시 파일 저장
            if not st.session_state.processed:
                image.convert("RGB").save("uploads/fixed_classify_image.jpg", "JPEG")

if st.button(
    get_text("btn_check_battery"),
    on_click=session_change(),
):
    st.switch_page("pages/page01_sub.py")
