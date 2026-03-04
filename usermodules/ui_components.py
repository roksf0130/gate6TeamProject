import streamlit as st
import time
import os
from usermodules.i18n import get_text


def show_progress_bar():
    """displays a localized progress bar for AI analysis."""
    progress_text = get_text("analyzing_msg")
    progress_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        progress_bar.progress(percent_complete + 1, text=progress_text)

    progress_bar.empty()
    st.success(get_text("analysis_complete"))


def handle_image_removal(file_path):
    """Removes the temporary image and updates session state."""
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            st.session_state.processed = True
            st.toast(get_text("privacy_toast"))
        except Exception as e:
            st.error(f"Error deleting file: {e}")


def session_change():
    """프로세스 처리여부를 변경하는 함수"""
    st.session_state.processed = not st.session_state.get("processed", False)


def apply_custom_css():
    """Applies font size and structural styling."""
    font_size = st.session_state.get("font_size", "16px")
    st.markdown(
        f"""
        <style>
        html, body, [class*="css"] {{
            font-size: {font_size};
        }}
        .stButton>button {{
            width: 100%;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
