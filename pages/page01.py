import time
import os
import streamlit as st
from PIL import Image
from usermodules import azure_cv_classify

if 'processed' not in st.session_state:
    st.session_state.processed = False

def session_change():
    if st.session_state.processed == True:
        st.session_state.processed = False
    else:
        st.session_state.processed = True

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
            if classify_result == '보조배터리':
                st.error('보조배터리 기내반입 가능여부를 확인해주시기 바랍니다.')
            else :
                st.error(f'이 물품은 기내반입이 불가합니다.')

# 페이지 설정
st.set_page_config(page_title='기내반입 가능 물품 판별', page_icon='✈️', layout='centered')
st.title(body='자기야!! 이거 :blue[기내반입] 되나? 🤔', width='stretch', text_alignment='center')
st.info('''
        본 서비스는 AI 분석 결과를 기반으로 한 참고 정보입니다.
        항공사 및 국가별 보안 규정은 수시로 변경될 수 있으며, 실제 반입 가능 여부는 해당 항공사 및 공항 보안 당국의 판단을 따릅니다.
        본 서비스는 이용 결과로 발생하는 문제에 대해 책임을 지지 않습니다.
        ''')
st.markdown('---')

uploaded_file = st.file_uploader(label='물품 사진을 촬영 또는 업로드해주세요. 사진은 판별 후 즉시 삭제됩니다.', type=['jpg','jpeg','png','bmp'], on_change=session_change())

if uploaded_file is not None:
    # 두 개로 영역 분할
    col1, col2 = st.columns(spec=2, width='stretch')

    with col1:
        if st.button(label='분석시작', width='stretch', on_click=session_change()):
            if os.path.exists('uploads/fixed_classify_image.jpg'):
                try:
                    with col2:
                        classify_analyze()
                    os.remove('uploads/fixed_classify_image.jpg')
                    # 처리 완료 상태로 변경 (Rerun 시 재저장 방지)
                    st.session_state.processed = True
                    st.toast('개인정보 보호를 위해 사진이 삭제되었습니다.')
                except Exception as e:
                    st.error(f"오류 발생: {e}")
        with Image.open(uploaded_file) as image:
            st.image(image=image, caption='판별대상물품', width='stretch')
            image = image.convert('RGB') # MPO 정보를 버리고 일반 RGB로 변환

            if uploaded_file and not st.session_state.processed:
                image.save('./uploads/fixed_classify_image.jpg', 'JPEG')

if st.button('보조배터리 기내반입 가능여부 확인', on_click=session_change()):
    st.switch_page('pages/page01_sub.py')
