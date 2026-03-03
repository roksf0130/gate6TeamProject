import streamlit as st

if "langpack" not in st.session_state:
    st.session_state["langpack"] = 0


def update_sidebar():
    selected = st.session_state.my_pills
    if selected == "한국어":
        st.session_state["langpack"] = 0
    else:
        st.session_state["langpack"] = 1


pages = {
    "HOME": [
        st.Page(
            "./pages/page01.py",
            title=(
                "👜 기내반입 가능 물품 판별"
                if st.session_state["langpack"] == 0
                else "👜 Determining what items can be carried on board"
            ),
        ),
        st.Page(
            "./pages/page01_sub.py",
            title=(
                "💡 보조배터리 기내반입 판별"
                if st.session_state["langpack"] == 0
                else "💡 Determination of carry-on status of auxiliary batteries"
            ),
        ),
    ],
    (
        "운송제한물품 안내"
        if st.session_state["langpack"] == 0
        else "Restricted items information"
    ): [
        st.Page(
            "./pages/page02.py",
            title=(
                "🔋 리튬배터리"
                if st.session_state["langpack"] == 0
                else "🔋 Lithium battery"
            ),
        ),
        st.Page(
            "./pages/page03.py",
            title=(
                "💣 항공기 반입금지 물품"
                if st.session_state["langpack"] == 0
                else "💣 Restricted carry-on items"
            ),
        ),
        st.Page(
            "./pages/page04.py",
            title=(
                "💊 제한적 기내 반입 물품"
                if st.session_state["langpack"] == 0
                else "💊 Restricted items"
            ),
        ),
        st.Page(
            "./pages/page05.py",
            title=(
                "🥂 위탁 수하물 제한 물품"
                if st.session_state["langpack"] == 0
                else "🥂 Restricted checked items"
            ),
        ),
    ],
    "ResNet50 테스트": [
        st.Page("./pages/page06.py", title="ResNet50 테스트"),
    ],
    "오류 신고 / 제보하기" if st.session_state["langpack"] == 0 else "Contact us": [
        st.Page(
            "./pages/page07.py",
            title=(
                "😍 오류신고 / 제보하기"
                if st.session_state["langpack"] == 0
                else "😍 Contact us"
            ),
        ),
    ],
}

with st.sidebar:
    # pills 위젯
    lang = st.pills(
        "언어 / LANGUAGE",
        ["한국어", "ENGLISH"],
        key="my_pills",
        on_change=update_sidebar,
    )

pg = st.navigation(pages)
pg.run()
