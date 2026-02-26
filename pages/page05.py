import streamlit as st
from usermodules import fileread

# 스타일 읽어와서 페이지에 적용
style = fileread.fileread('style.txt', 'r')
st.markdown(style, unsafe_allow_html=True)

# 페이지 설정
st.set_page_config(page_title='위탁 수하물 제한 물품', layout='centered')
st.title(body='위탁 수하물 제한 물품🥂', width='stretch', text_alignment='center')
st.info('아래 품목은 수하물로 위탁할 수 없으므로, 직접 휴대해 주세요. (휴대 :blue[O], 위탁 :red[X])')

option_map = {
    0: '파손 또는 손상되기 쉬운 물품',
    1: '고가품 및 귀중품',
    2: '여객기로 운송 가능한 휴대용 전자기기의 보조/여분 배터리는 휴대만 가능',
    3: '라이터/전자담배',
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
    st.markdown(fileread.fileread('checked_baggage_text01.txt', 'r'), unsafe_allow_html=True)
elif selection == 1:
    st.markdown(fileread.fileread('checked_baggage_text02.txt', 'r'), unsafe_allow_html=True)
elif selection == 2:
    st.markdown(fileread.fileread('checked_baggage_text03.txt', 'r'), unsafe_allow_html=True)
elif selection == 3:
    st.markdown(fileread.fileread('checked_baggage_text04.txt', 'r'), unsafe_allow_html=True)
