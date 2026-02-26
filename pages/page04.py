import streamlit as st
from usermodules import fileread

# 스타일 읽어와서 페이지에 적용
style = fileread.fileread('style.txt', 'r')
st.markdown(style, unsafe_allow_html=True)

# 페이지 설정
st.set_page_config(page_title='제한적 기내 반입 물품', layout='centered')
st.title(body='제한적 기내 반입 물품💊', width='stretch', text_alignment='center')
st.info('아래 품목은 기내로 소량 반입할 수 있습니다. (휴대 :orange[△], 위탁 :blue[O])')

option_map = {
    0: '액체류 (국제선 출발, 환승에 한함)',
    1: '의약품',
    2: 'MacBook 배터리 리콜 대상',
    3: '기타',
}
selection = st.pills(
    '세부 항목을 선택하세요.',
    options=option_map.keys(),
    format_func=lambda option: option_map[option],
    selection_mode='single',
    default=0,
)

st.markdown('---')

if selection == 0:
    st.markdown(fileread.fileread('restrictions_allowed_text01.txt', 'r'), unsafe_allow_html=True)
elif selection == 1:
    st.markdown(fileread.fileread('restrictions_allowed_text02.txt', 'r'), unsafe_allow_html=True)
elif selection == 2:
    st.markdown(fileread.fileread('restrictions_allowed_text03.txt', 'r'), unsafe_allow_html=True)
elif selection == 3:
    st.markdown(fileread.fileread('restrictions_allowed_text04.txt', 'r'), unsafe_allow_html=True)
