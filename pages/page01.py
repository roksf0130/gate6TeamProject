import time
import streamlit as st
from PIL import Image

# 페이지 설정
st.set_page_config(page_title='기내반입 가능 물품 판별', page_icon='✈️', layout='centered')
st.title(body='이거 :blue[기내반입] 되나? 🤔', width='stretch', text_alignment='center')
st.markdown('---')

uploaded_file = st.file_uploader(label='물품 사진을 촬영 또는 업로드해주세요', type=['jpg','jpeg','png','bmp'])

if uploaded_file is not None:
    # 두 개로 영역 분할
    col1, col2 = st.columns(spec=2, width='stretch')

    with col1:
        image = Image.open(uploaded_file)
        st.image(image=image, caption='판별대상물품', width='stretch')
    with col2:
        st.write('💻 AI 분석 결과')

        # 분석중인 것 처럼 보이도록 연출
        progress_text = 'AI가 이미지를 분석 중입니다. 잠시만 기다려 주세요...'
        progress_bar = st.progress(0, text=progress_text)

        # Progress Bar 애니메이션
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1, text=progress_text)

        # 분석 완료 후 Progress Bar 제거
        progress_bar.empty()
        st.success('✅ 분석이 완료되었습니다!')

# st.markdown('---')

# if st.button('🔄 다시 검사하기'):
#     st.rerun()
