import streamlit as st
import requests
import json
import os
from streamlit_pages.chat_page import chat_page
from streamlit_pages.leaderboard_page import leaderboard_page
def main():
    st.session_state.setdefault("current_page", "chat_page")
    st.set_page_config(
        page_title="Assisterr Chat",
        page_icon="",
        layout="wide",
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
    if st.session_state.current_page == "chat_page":
        chat_page()
    elif st.session_state.current_page == "leaderboard_page":
        leaderboard_page()

if __name__ == "__main__":
    main()
