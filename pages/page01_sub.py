import streamlit as st
import time
import os
from PIL import Image
from usermodules import azure_cv_ocr, fileread
from usermodules.i18n import get_text
from usermodules.ui_components import (
    show_progress_bar,
    handle_image_removal,
    session_change,
)

# 세션 초기화
if "processed" not in st.session_state:
    st.session_state.processed = False


@st.dialog(title=get_text("modal_title"), width="medium")
def show_modal():
    lang_path = "kor" if st.session_state["langpack"] == 0 else "eng"

    """ 배터리 용량 계산법 Modal 창 """
    texts = [
        f"{lang_path}/battery_text02.txt",
        f"{lang_path}/battery_text03.txt",
        f"{lang_path}/battery_text04.txt",
    ]

    for t in texts:
        content = fileread.fileread(t, "r")
        if content:
            st.markdown(content, unsafe_allow_html=True)
            st.write("")

    if st.button(get_text("modal_close")):
        st.rerun()


def battery_analyze():
    """배터리 스펙 분석을 위한 함수"""
    st.write(get_text("ai_analysis_header"))

    # progress bar 생성
    show_progress_bar()

    # OCR 함수 호출
    wattage, return_type = azure_cv_ocr.azure_cv_ocr()

    # 사진 분석에 실패한 경우는 실패 메세지 출력하고 종료
    if return_type == 0:
        st.error(get_text("analysis_failed_battery"))
    # 사진 분석에 성공한 경우
    else:
        # 측정된 결과 출력
        st.info(f"{get_text('measured_power')} : {wattage:.2f}Wh")

        # 기내 탑승 가능 수량 출력
        if return_type == 1:
            st.info(get_text("battery_ok_5"))
        elif return_type == 2:
            st.info(get_text("battery_ok_2"))
        else:
            st.error(get_text("battery_no"))


# 페이지 설정
st.set_page_config(
    get_text("page01_sub_title"),
    layout="centered",
)
st.title(
    body=get_text("page01_sub_title"),
    width="stretch",
    text_alignment="center",
    anchor=False,
)

# info 출력
st.info(get_text("carry_on_info"))

st.markdown("---")

# 파일 업로드 영역
uploaded_file = st.file_uploader(
    label=get_text("uploader_label_battery"),
    type=["jpg", "jpeg", "png", "bmp"],
    on_change=session_change,
)

if uploaded_file is not None:
    # 두 개로 영역 분할
    col1, col2 = st.columns(spec=2, width="stretch")

    with col1:
        if st.button(
            label=get_text("btn_start_analysis"),
            width="stretch",
            on_click=session_change,
        ):
            if os.path.exists("uploads/fixed_temp_image.jpg"):
                with col2:
                    battery_analyze()

                # 분석 완료 후 업로드된 사진은 삭제
                handle_image_removal("uploads/fixed_temp_image.jpg")

        with Image.open(uploaded_file) as image:
            st.image(
                image=image,
                caption=get_text("image_caption"),
                width="stretch",
            )

            # 판별을 위한 임시 파일 저장
            if not st.session_state.processed:
                image.convert("RGB").save("uploads/fixed_temp_image.jpg", "JPEG")

st.markdown("---")
if st.button(
    get_text("btn_battery_calc"),
    width="stretch",
    on_click=session_change,
):
    show_modal()
