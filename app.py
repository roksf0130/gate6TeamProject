import streamlit as st
from usermodules.i18n import get_text
from usermodules.ui_components import apply_custom_css

# 언어 및 폰트 사이즈 세션 초기화
if "langpack" not in st.session_state:
    st.session_state["langpack"] = 0

if "font_size" not in st.session_state:
    st.session_state["font_size"] = "16px"


# 언어 설정을 위한 콜백함수
def update_sidebar():
    selected = st.session_state.my_pills
    if selected == "한국어":
        st.session_state["langpack"] = 0
    else:
        st.session_state["langpack"] = 1


pages = {
    get_text("nav_home"): [
        st.Page("./pages/page01.py", title=get_text("page01_title")),
        st.Page("./pages/page01_sub.py", title=get_text("page01_sub_title")),
    ],
    get_text("nav_restricted"): [
        st.Page("./pages/page02.py", title=get_text("page02_title")),
        st.Page("./pages/page03.py", title=get_text("page03_title")),
        st.Page("./pages/page04.py", title=get_text("page04_title")),
        st.Page("./pages/page05.py", title=get_text("page05_title")),
    ],
    get_text("nav_contact"): [
        st.Page("./pages/page07.py", title=get_text("page07_title")),
    ],
    get_text("nav_admin"): [
        st.Page("./pages/page08.py", title=get_text("page08_title")),
    ],
}

with st.sidebar:
    # pills 위젯
    st.pills(
        "언어 / LANGUAGE",
        ["한국어", "ENGLISH"],
        key="my_pills",
        on_change=update_sidebar,
        default="한국어",
    )
    # 글자 크기 조절
    size_option = st.pills(
        "글자 크기 / FONT SIZE",
        ["보통(NORMAL)", "크게(BIG)"],
        key="font_selector",
        default="보통(NORMAL)",
    )

    # 글자 크기 조정
    if size_option == "보통(NORMAL)":
        st.session_state["font_size"] = "16px"
    else:
        st.session_state["font_size"] = "22px"

    # CSS 적용
    apply_custom_css()

pg = st.navigation(pages)
pg.run()
