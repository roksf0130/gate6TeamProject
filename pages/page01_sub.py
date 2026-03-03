import streamlit as st
import time
import os
from PIL import Image
from usermodules import azure_cv_ocr, fileread

if "processed" not in st.session_state:
    st.session_state.processed = False


def session_change():
    if st.session_state.processed == True:
        st.session_state.processed = False
    else:
        st.session_state.processed = True


@st.dialog(title="배터리 용량 계산법 안내", width="medium")
def show_modal():
    if st.session_state["langpack"] == 0:
        st.markdown(
            fileread.fileread("kor/battery_text02.txt", "r"), unsafe_allow_html=True
        )
        st.write("")
        st.markdown(
            fileread.fileread("kor/battery_text03.txt", "r"), unsafe_allow_html=True
        )
        st.write("")
        st.markdown(
            fileread.fileread("kor/battery_text04.txt", "r"), unsafe_allow_html=True
        )
        if st.button("닫기"):
            st.rerun()
    elif st.session_state["langpack"] == 1:
        st.markdown(
            fileread.fileread("eng/battery_text02.txt", "r"), unsafe_allow_html=True
        )
        st.write("")
        st.markdown(
            fileread.fileread("eng/battery_text03.txt", "r"), unsafe_allow_html=True
        )
        st.write("")
        st.markdown(
            fileread.fileread("eng/battery_text04.txt", "r"), unsafe_allow_html=True
        )
        if st.button("Close"):
            st.rerun()


# 재실행되는 streamlit 작동원리때문에 분석로직을 별도 함수로 생성
def battery_analyze():
    st.write(
        "💻 AI 분석 결과"
        if st.session_state["langpack"] == 0
        else "💻 AI analysis results"
    )

    # 진행바 생성
    progress_text = (
        "AI가 이미지를 분석 중입니다. 잠시만 기다려 주세요..."
        if st.session_state["langpack"] == 0
        else "AI is analyzing the image. Please wait."
    )
    progress_bar = st.progress(0, text=progress_text)

    # 진행바 애니메이션
    for percent_complete in range(100):
        time.sleep(0.01)  # 진행바가 올라가는 속도 조절
        progress_bar.progress(percent_complete + 1, text=progress_text)

    # 함수 호출
    # wattage, return_type = battery_ocr.battery_ocr(cv2_image)
    wattage, return_type = azure_cv_ocr.azure_cv_ocr()

    # 분석 완료 후 바 제거
    progress_bar.empty()
    st.success(
        "✅ 분석이 완료되었습니다!"
        if st.session_state["langpack"] == 0
        else "✅ Analysis is complete!"
    )

    # 결과 출력
    if return_type == 0:
        if st.session_state["langpack"] == 0:
            st.error(
                "❌ 사진 분석에 실패했습니다. 배터리 스펙부분을 확대한 선명한 사진을 업로드하면 인식률이 더욱 향상됩니다."
            )
        elif st.session_state["langpack"] == 1:
            st.error(
                "❌ Photo analysis failed. Recognition rates will improve if you upload a clear photo with a zoomed-in view of the battery specifications."
            )
    elif return_type == 1:
        if st.session_state["langpack"] == 0:
            st.info(f"측정된 전력량 : {wattage:.2f}Wh")
            st.info("✈️  1인 5개까지 기내 반입이 가능한 용량입니다.")
        elif st.session_state["langpack"] == 1:
            st.info(f"Measured power : {wattage:.2f}Wh")
            st.info("✈️  This is the maximum carry-on capacity of 5 per person.")
    elif return_type == 2:
        if st.session_state["langpack"] == 0:
            st.info(f"측정된 전력량 : {wattage:.2f}Wh")
            st.info(
                "✈️  1인 2개까지 기내 반입이 가능하지만 승인을 위해 카운터 방문이 필요합니다."
            )
        elif st.session_state["langpack"] == 1:
            st.info(f"Measured power : {wattage:.2f}Wh")
            st.info(
                "✈️  Up to two items per person are allowed on board, but a visit to the counter is required for approval."
            )
    else:
        if st.session_state["langpack"] == 0:
            st.error(f"측정된 전력량 : {wattage:.2f}Wh")
            st.error(f"❌ 기내 반입 불가 용량입니다.")
        elif st.session_state["langpack"] == 1:
            st.error(f"Measured power : {wattage:.2f}Wh")
            st.error(f"❌ Restricted Item.")


# 페이지 설정
st.set_page_config(
    page_title=(
        "보조배터리 기내반입 판별"
        if st.session_state["langpack"] == 0
        else "Determination of carry-on status of auxiliary batteries"
    ),
    page_icon="✈️",
    layout="centered",
)
st.title(
    body=(
        "보조배터리 기내반입 판별 🤔"
        if st.session_state["langpack"] == 0
        else "Determination of carry-on status of auxiliary batteries 🤔"
    ),
    width="stretch",
    text_alignment="center",
)

if st.session_state["langpack"] == 0:
    st.info(
        """
            본 서비스는 AI 분석 결과를 기반으로 한 참고 정보입니다.
            항공사 및 국가별 보안 규정은 수시로 변경될 수 있으며, 실제 반입 가능 여부는 해당 항공사 및 공항 보안 당국의 판단을 따릅니다.
            본 서비스는 이용 결과로 발생하는 문제에 대해 책임을 지지 않습니다.
            """
    )
elif st.session_state["langpack"] == 1:
    st.info(
        """
            This service is provided as reference information based on AI analysis results.
            Airline and country security regulations are subject to change at any time, and actual carry-on permits are determined by the relevant airline and airport security authorities.
            This service is not responsible for any issues arising from its use.
            """
    )

st.markdown("---")

uploaded_file = st.file_uploader(
    label=(
        "보조배터리의 상세 스펙 사진을 촬영 또는 업로드해주세요. 사진은 판별 후 즉시 삭제됩니다."
        if st.session_state["langpack"] == 0
        else "Please take or upload a photo of the auxiliary battery's detailed specifications. The photo will be deleted immediately after verification."
    ),
    type=["jpg", "jpeg", "png", "bmp"],
    on_change=session_change(),
)

if uploaded_file is not None:
    # 두 개로 영역 분할
    col1, col2 = st.columns(spec=2, width="stretch")

    with col1:
        if st.button(
            label="분석시작" if st.session_state["langpack"] == 0 else "Start analysis",
            width="stretch",
            on_click=session_change(),
        ):
            if os.path.exists("uploads/fixed_temp_image.jpg"):
                try:
                    with col2:
                        battery_analyze()
                    os.remove("uploads/fixed_temp_image.jpg")
                    # 처리 완료 상태로 변경 (Rerun 시 재저장 방지)
                    st.session_state.processed = True
                    st.toast("개인정보 보호를 위해 사진이 삭제되었습니다.")
                except Exception as e:
                    st.error(f"오류 발생: {e}")
        with Image.open(uploaded_file) as image:
            st.image(
                image=image,
                caption=(
                    "판별대상물품"
                    if st.session_state["langpack"] == 0
                    else "Items subject to determination"
                ),
                width="stretch",
            )
            image = image.convert("RGB")  # MPO 정보를 버리고 일반 RGB로 변환

            if uploaded_file and not st.session_state.processed:
                image.save("./uploads/fixed_temp_image.jpg", "JPEG")

st.markdown("---")
if st.button(
    (
        "배터리 용량 계산법"
        if st.session_state["langpack"] == 0
        else "How to calculate the capacity of spare batteries"
    ),
    on_click=session_change(),
):
    show_modal()
