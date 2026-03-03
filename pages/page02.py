import streamlit as st
from usermodules import fileread

# 스타일 읽어와서 페이지에 적용
style = fileread.fileread("style.txt", "r")
st.markdown(style, unsafe_allow_html=True)

# 페이지 설정
st.set_page_config(
    page_title="리튬배터리" if st.session_state["langpack"] == 0 else "Lithium battery",
    layout="centered",
)
st.title(
    body="리튬배터리🔋" if st.session_state["langpack"] == 0 else "Lithium battery🔋",
    width="stretch",
    text_alignment="center",
)
st.info(
    "국제항공 운송협회 위험물 규정(IATA Dangerous Goods Regulations)에 의거하여 규정이 적용됩니다."
    if st.session_state["langpack"] == 0
    else "Rules apply in accordance with the IATA Dangerous Goods Regulations."
)

if st.session_state["langpack"] == 0:
    option_map = {
        0: "보조/여분 리튬배터리",
        1: "보조배터리 용량 계산법",
        2: "리튬 배터리 장착 전자기기",
        3: "전동 휠체어",
        4: "스마트 가방",
    }
    selection = st.pills(
        "세부 항목을 선택하세요.",
        options=option_map.keys(),
        format_func=lambda option: option_map[option],
        selection_mode="single",
        default=0,
    )
elif st.session_state["langpack"] == 1:
    option_map = {
        0: "Spare/extra lithium batteries",
        1: "How to calculate the capacity of spare batteries",
        2: "Lithium battery-powerd electronic devices",
        3: "Electric wheelchairs",
        4: "Smart luggage",
    }
    selection = st.pills(
        "Select",
        options=option_map.keys(),
        format_func=lambda option: option_map[option],
        selection_mode="single",
        default=0,
    )


st.markdown("---")
if st.session_state["langpack"] == 0:
    if selection == 0:
        st.markdown(
            fileread.fileread("kor/battery_text01.txt", "r"), unsafe_allow_html=True
        )
    elif selection == 1:
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
    elif selection == 2:
        st.markdown(
            fileread.fileread("kor/battery_text05.txt", "r"), unsafe_allow_html=True
        )
    elif selection == 3:
        st.markdown(
            fileread.fileread("kor/battery_text06.txt", "r"), unsafe_allow_html=True
        )
        st.write("")
        st.markdown(
            fileread.fileread("kor/battery_text07.txt", "r"), unsafe_allow_html=True
        )
        st.write(
            "❗ 전동 휠체어는 사이즈 및 배터리 타입에 따라 운송 가능 여부 및 처리 절차가 달라질 수 있으니 자세한 사항은 항공사로 문의해 주시기 바랍니다."
        )
    elif selection == 4:
        st.markdown(
            fileread.fileread("kor/battery_text08.txt", "r"), unsafe_allow_html=True
        )
elif st.session_state["langpack"] == 1:
    if selection == 0:
        st.markdown(
            fileread.fileread("eng/battery_text01.txt", "r"), unsafe_allow_html=True
        )
    elif selection == 1:
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
    elif selection == 2:
        st.markdown(
            fileread.fileread("eng/battery_text05.txt", "r"), unsafe_allow_html=True
        )
    elif selection == 3:
        st.markdown(
            fileread.fileread("eng/battery_text06.txt", "r"), unsafe_allow_html=True
        )
        st.write("")
        st.markdown(
            fileread.fileread("eng/battery_text07.txt", "r"), unsafe_allow_html=True
        )
        st.write(
            "❗ The handling procedure and whether transportation is allowed for an electric wheelchair depend on the wheelchair’s size and battery type, so please contact the Service Center for more details."
        )
    elif selection == 4:
        st.markdown(
            fileread.fileread("eng/battery_text08.txt", "r"), unsafe_allow_html=True
        )
