import streamlit as st
import time
from PIL import Image
from usermodules import azure_cv_ocr, fileread

@st.dialog(title="배터리 용량 계산법 안내", width='medium')
def show_modal():
    st.markdown(fileread.fileread('battery_text02.txt', 'r'), unsafe_allow_html=True)
    st.write('')
    st.markdown(fileread.fileread('battery_text03.txt', 'r'), unsafe_allow_html=True)
    st.write('')
    st.markdown(fileread.fileread('battery_text04.txt', 'r'), unsafe_allow_html=True)
    if st.button("닫기"):
        st.rerun()

# 재실행되는 streamlit 작동원리때문에 분석로직을 별도 함수로 생성
def battery_analyze():
    st.write('💻 AI 분석 결과')

    # 진행바 생성
    progress_text = 'AI가 이미지를 분석 중입니다. 잠시만 기다려 주세요...'
    progress_bar = st.progress(0, text=progress_text)

    # 진행바 애니메이션
    for percent_complete in range(100):
        time.sleep(0.01) # 진행바가 올라가는 속도 조절
        progress_bar.progress(percent_complete + 1, text=progress_text)

    # 함수 호출
    # wattage, return_type = battery_ocr.battery_ocr(cv2_image)
    wattage, return_type = azure_cv_ocr.azure_cv_ocr()

    # 분석 완료 후 바 제거
    progress_bar.empty()
    st.success('✅ 분석이 완료되었습니다!')

    # 결과 출력
    if return_type == 0:
        st.error('❌ 사진 분석에 실패했습니다. 배터리 스펙부분을 확대한 선명한 사진을 업로드하면 인식률이 더욱 향상됩니다.')
    elif return_type == 1:
        st.info(f'측정된 전력량 : {wattage:.2f}Wh')
        st.info('✈️  1인 5개까지 기내 반입이 가능한 용량입니다.')
    elif return_type == 2:
        st.info(f'측정된 전력량 : {wattage:.2f}Wh')
        st.info('✈️  1인 2개까지 기내 반입이 가능하지만 승인을 위해 카운터 방문이 필요합니다.')
    else:
        st.error(f'측정된 전력량 : {wattage:.2f}Wh')
        st.error(f'❌ 기내 반입 불가 용량입니다.')

# 페이지 설정
st.set_page_config(page_title='보조배터리 기내반입 판별', page_icon='✈️', layout='centered')
st.title(body='보조배터리 기내반입 판별 🤔', width='stretch', text_alignment='center')
st.markdown('---')

uploaded_file = st.file_uploader(label='보조배터리의 상세 스펙 사진을 촬영 또는 업로드해주세요', type=['jpg','jpeg','png','bmp'])

if uploaded_file is not None:
    # 두 개로 영역 분할
    col1, col2 = st.columns(spec=2, width='stretch')

    with col1:
        if st.button(label='분석시작', width='stretch'):
            st.session_state.processed = True
            with col2:
                battery_analyze()

        image = Image.open(uploaded_file)
        st.image(image, caption='판별대상물품', width='stretch')
        image = image.convert('RGB') # MPO 정보를 버리고 일반 RGB로 변환
        image.save('./uploads/fixed_temp_image.jpg', 'JPEG')

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
    #     # wattage, return_type = battery_ocr.battery_ocr(cv2_image)
    #     wattage, return_type = azure_cv_ocr.azure_cv_ocr()

    #     # 분석 완료 후 바 제거
    #     progress_bar.empty()
    #     st.success('✅ 분석이 완료되었습니다!')

    #     # 결과 출력
    #     if return_type == 0:
    #         st.error('❌ 사진 분석에 실패했습니다. 배터리 스펙부분을 확대한 선명한 사진을 업로드하면 인식률이 더욱 향상됩니다.')
    #     elif return_type == 1:
    #         st.info(f'측정된 전력량 : {wattage:.2f}Wh')
    #         st.info('✈️  1인 5개까지 기내 반입이 가능한 용량입니다.')
    #     elif return_type == 2:
    #         st.info(f'측정된 전력량 : {wattage:.2f}Wh')
    #         st.info('✈️  1인 2개까지 기내 반입이 가능하지만 승인을 위해 카운터 방문이 필요합니다.')
    #     else:
    #         st.error(f'측정된 전력량 : {wattage:.2f}Wh')
    #         st.error(f'❌ 기내 반입 불가 용량입니다.')

st.markdown('---')
if st.button('배터리 용량 계산법'):
    show_modal()

# if st.button('🔄 다시 검사하기'):
#     st.rerun()
