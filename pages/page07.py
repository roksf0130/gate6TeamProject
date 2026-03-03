import streamlit as st

# 페이지 설정

st.set_page_config(
    page_title=(
        "오류신고 / 제보하기" if st.session_state["langpack"] == 0 else "Contact us"
    ),
    page_icon="✈️",
    layout="centered",
)
st.title(
    body=(
        "😍 오류신고 / 제보하기"
        if st.session_state["langpack"] == 0
        else "😍 Contact us"
    ),
    width="stretch",
    text_alignment="center",
)


st.subheader(
    "📬 오류 또는 문제점을 제보해주세요."
    if st.session_state["langpack"] == 0
    else "Please report any errors or issues."
)
with st.form("email_form"):
    u_email = st.text_input(
        "작성자의 이메일 주소" if st.session_state["langpack"] == 0 else "Email address"
    )
    u_msg = st.text_area("내용" if st.session_state["langpack"] == 0 else "Content")
    uploaded_file = st.file_uploader(
        label=(
            "사진 첨부 (선택사항)"
            if st.session_state["langpack"] == 0
            else "Upload File (Optional)"
        ),
        type=["jpg", "jpeg", "png", "bmp"],
    )
    if st.session_state["langpack"] == 0:
        submitted = st.form_submit_button("보내기")
    elif st.session_state["langpack"] == 1:
        submitted = st.form_submit_button("Send")

    if submitted:
        if u_email and u_msg:
            with st.spinner(
                "메일을 보내는 중..."
                if st.session_state["langpack"] == 0
                else "Sending email..."
            ):
                st.success(
                    "관리자에게 메일이 성공적으로 전송되었습니다!"
                    if st.session_state["langpack"] == 0
                    else "Your email has been successfully sent to the administrator!"
                )
        else:
            st.warning(
                "이메일과 내용을 모두 입력해주세요."
                if st.session_state["langpack"] == 0
                else "Please enter both your email address and content."
            )
