import streamlit as st

pages = {
    'HOME': [
        st.Page('./pages/page01.py', title='👜 기내반입 가능 물품 판별'),
        st.Page('./pages/page01_sub.py', title='💡 보조배터리 기내반입 판별'),
    ],
    '운송제한물품 안내': [
        st.Page('./pages/page02.py', title='🔋리튬배터리'),
        st.Page('./pages/page03.py', title='💣항공기 반입금지 물품'),
        st.Page('./pages/page04.py', title='💊제한적 기내 반입 물품'),
        st.Page('./pages/page05.py', title='🥂위탁 수하물 제한 물품'),
    ],
    'test2': [
        st.Page('./pages/page06.py', title='📷test 03'),
        st.Page('./pages/page07.py', title='⚖️test 04'),
    ],
}

pg = st.navigation(pages)
pg.run()
