import streamlit as st
from streamlit_pages.crawling_page import crawling_page
from streamlit_pages.reward_database_page import reward_database_page
from streamlit_pages.vectorization_page import vectorization_page
from streamlit_pages.eda_page import eda_page
def main():
    st.set_page_config(
        page_title="Data Admin Page",
        page_icon="brain",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={}
    )
    st.markdown(
        r"""
        <style>
        .stDeployButton {
                visibility: hidden;
            }
        </style>
        """, unsafe_allow_html=True
    )
    st.session_state.setdefault("fetched_qa", None)
    st.session_state.setdefault("df_qa", None)
    st.session_state.setdefault("df_qa_with_vectors", None)

    pages = ["Crawling", "Vectorization", "Reward Database Manager", "EDA"] #"RAG Database Manager" removed
    page = st.sidebar.radio("Select Page", pages)

    if page == "Crawling":
        crawling_page()
    elif page == "Vectorization":
        vectorization_page()
    elif page == "Reward Database Manager":
        reward_database_page()
    elif page == "EDA":
        eda_page()
        

if __name__ == "__main__":
    main()
