import streamlit as st
import requests
import json
from config import BACKEND_URL, CONTRIBUTOR_URL


def streamlit_chat(prompt, openai_api_key):
    headers = {
        "Content-Type": "application/json",
        "OpenAI-API-Key": openai_api_key,
    }
    data = {"prompt": prompt}
    
    response = requests.post(BACKEND_URL+"/chat", headers=headers, data=json.dumps(data), stream=True)
    if response.status_code == 200:
        message_placeholder = st.empty() 
        full_text = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')  
                json_data = json.loads(decoded_line.replace('data: ', ''))
                full_text += json_data  
                current_text = message_placeholder.write(full_text)  
                st.session_state['last_message'] = json_data
    elif response.status_code == 401:
        st.error("Unauthorized, Invalid OpenAI key")


def chat_page():
    _, col2, _ = st.columns([0.27,0.46,0.27])
    with col2:
        st.title("Assisterr Chat (Solana Renaissance Hackathon)")
        prompt = st.text_input("Enter your question:")
        
        openai_api_key = st.text_input("Enter your OpenAI API Key:", type="password")
        
        col1, col2, col3 = st.columns([0.3,0.4,0.3])
        with col1:
            chat_button_clicked = st.button("Send", use_container_width=True)
        with col2:
            if st.button("Contribution Leaderboard", use_container_width=True):
                st.session_state.current_page = "leaderboard_page"
                st.rerun()
        with col3:
            st.link_button("Are You a contributor?", CONTRIBUTOR_URL, use_container_width=True)
        
        if chat_button_clicked:
            if not openai_api_key:
                st.error("OpenAI API Key is required.")
            else:
                streamlit_chat(prompt, openai_api_key)