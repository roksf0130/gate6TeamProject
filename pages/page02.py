import streamlit as st
from usermodules import fileread

# 스타일 읽어와서 페이지에 적용
style = fileread.fileread('style.txt', 'r')
st.markdown(style, unsafe_allow_html=True)

# 페이지 설정
st.set_page_config(page_title='리튬배터리', layout='centered')
st.title(body='리튬배터리🔋', width='stretch', text_alignment='center')
st.info('국제항공 운송협회 위험물 규정(IATA Dangerous Goods Regulations)에 의거하여 규정이 적용됩니다.')

option_map = {
    0: '보조/여분 리튬배터리',
    1: '보조배터리 용량 계산법',
    2: '리튬 배터리 장착 전자기기',
    3: '전동 휠체어',
    4: '스마트 가방',
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
    st.markdown(fileread.fileread('battery_text01.txt', 'r'), unsafe_allow_html=True)
elif selection == 1:
    st.markdown(fileread.fileread('battery_text02.txt', 'r'), unsafe_allow_html=True)
    st.write('')
    st.markdown(fileread.fileread('battery_text03.txt', 'r'), unsafe_allow_html=True)
    st.write('')
    st.markdown(fileread.fileread('battery_text04.txt', 'r'), unsafe_allow_html=True)
elif selection == 2:
    st.markdown(fileread.fileread('battery_text05.txt', 'r'), unsafe_allow_html=True)
elif selection == 3:
    st.markdown(fileread.fileread('battery_text06.txt', 'r'), unsafe_allow_html=True)
    st.write('')
    st.markdown(fileread.fileread('battery_text07.txt', 'r'), unsafe_allow_html=True)
    st.write('❗ 전동 휠체어는 사이즈 및 배터리 타입에 따라 운송 가능 여부 및 처리 절차가 달라질 수 있으니 자세한 사항은 항공사로 문의해 주시기 바랍니다.')
elif selection == 4:
    st.markdown(fileread.fileread('battery_text08.txt', 'r'), unsafe_allow_html=True)
