import streamlit as st
from usermodules import fileread

# 스타일 읽어와서 페이지에 적용
style = fileread.fileread('style.txt', 'r')
st.markdown(style, unsafe_allow_html=True)

# 페이지 설정
st.set_page_config(page_title='항공기 반입금지 물품', layout='centered')
st.title(body='항공기 반입금지 물품💣', width='stretch', text_alignment='center')
st.info('아래 품목은 휴대 수하물로 기내 반입하거나 위탁 수하물로 운송하는 것이 금지되어 있습니다. (휴대 :red[X], 위탁 :red[X])')

option_map = {
    0: '발화성/인화성 물질',
    1: '고압가스 용기',
    2: '무기 및 폭발물 종류',
    3: '기타 위험 물질',
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
    st.markdown(fileread.fileread('prohibited_items_text01.txt', 'r'), unsafe_allow_html=True)
elif selection == 1:
    st.markdown(fileread.fileread('prohibited_items_text02.txt', 'r'), unsafe_allow_html=True)
elif selection == 2:
    st.markdown(fileread.fileread('prohibited_items_text03.txt', 'r'), unsafe_allow_html=True)
elif selection == 3:
    st.markdown(fileread.fileread('prohibited_items_text04.txt', 'r'), unsafe_allow_html=True)
