import time
import streamlit as st
from PIL import Image
from usermodules import azure_cv_classify

def classify_analyze():
    st.write('💻 AI 분석 결과')

    # 진행바 생성
    progress_text = 'AI가 이미지를 분석 중입니다. 잠시만 기다려 주세요...'
    progress_bar = st.progress(0, text=progress_text)

    # 진행바 애니메이션
    for percent_complete in range(100):
        time.sleep(0.01) # 진행바가 올라가는 속도 조절
        progress_bar.progress(percent_complete + 1, text=progress_text)

    # 함수 호출
    classify_result, probability, return_type = azure_cv_classify.azure_cv_classify()

    # 분석 완료 후 바 제거
    progress_bar.empty()
    st.success('✅ 분석이 완료되었습니다!')

    # 결과 출력
    if return_type == 0:
        st.error('❌ 사진 분석에 실패했습니다.')
    elif return_type == 1:
        if classify_result == '반입 가능한 물품':
            st.info(f'<{classify_result}> 으로 확인됩니다. 신뢰도는 {round(probability * 100, 2)}% 입니다.')
        else:
            st.error(f'<{classify_result}> 으로 확인됩니다. 신뢰도는 {round(probability * 100, 2)}% 입니다.')
            st.error(f'이 물품은 기내반입이 불가합니다.')


# 페이지 설정
st.set_page_config(page_title='기내반입 가능 물품 판별', page_icon='✈️', layout='centered')
st.title(body='이거 :blue[기내반입] 되나? 🤔', width='stretch', text_alignment='center')
st.markdown('---')

uploaded_file = st.file_uploader(label='물품 사진을 촬영 또는 업로드해주세요', type=['jpg','jpeg','png','bmp'])

if uploaded_file is not None:
    # 두 개로 영역 분할
    col1, col2 = st.columns(spec=2, width='stretch')

    with col1:
        if st.button(label='분석시작', width='stretch'):
            st.session_state.processed = True
            with col2:
                classify_analyze()

        image = Image.open(uploaded_file)
        st.image(image=image, caption='판별대상물품', width='stretch')
        image = image.convert('RGB') # MPO 정보를 버리고 일반 RGB로 변환
        image.save('./uploads/fixed_classify_image.jpg', 'JPEG')
    # with col2:
    #     st.write('💻 AI 분석 결과')

    #     # 진행바 생성
    #     progress_text = 'AI가 이미지를 분석 중입니다. 잠시만 기다려 주세요...'
    #     progress_bar = st.progress(0, text=progress_text)

    #     # 진행바 애니메이션
    #     for percent_complete in range(100):
    #         time.sleep(0.01) # 진행바가 올라가는 속도 조절
    #         progress_bar.progress(percent_complete + 1, text=progress_text)

    #     # 함수 호출
    #     classify_result, probability, return_type = azure_cv_classify.azure_cv_classify()

    #     # 분석 완료 후 바 제거
    #     progress_bar.empty()
    #     st.success('✅ 분석이 완료되었습니다!')

    #     # 결과 출력
    #     if return_type == 0:
    #         st.error('❌ 사진 분석에 실패했습니다.')
    #     elif return_type == 1:
    #         if classify_result == '반입 가능한 물품':
    #             st.info(f'<{classify_result}> 으로 확인됩니다. 신뢰도는 {round(probability * 100, 2)}% 입니다.')
    #         else:
    #             st.error(f'<{classify_result}> 으로 확인됩니다. 신뢰도는 {round(probability * 100, 2)}% 입니다.')
    #             st.error(f'이 물품은 기내반입이 불가합니다.')

# st.markdown('---')

# if st.button('🔄 다시 검사하기'):
#     st.rerun()
