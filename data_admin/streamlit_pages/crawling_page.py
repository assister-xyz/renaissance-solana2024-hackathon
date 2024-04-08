import streamlit as st
from utils.data_fetching import fetch_questions_and_answers
from utils.data_proccessing import process_body
from utils.dataframe import create_dataframe_from_qa, save_dataframe_to_csv
from config import CSV_OUTPUT_DIRECTORY

def display_fetched_questions():
    if st.session_state.fetched_qa:
        st.write(f"Total Questions: {len(st.session_state.fetched_qa)}")
        with st.expander("Questions"):
            for i, question in enumerate(st.session_state.fetched_qa):
                st.write("Question:", process_body(question['body']))
                try:
                    if question["accepted_answer"]:
                        st.write("Answer:",(question["accepted_answer"])["body"])
                    else:
                        st.write("Answer:",(question["accepted_answer"]))
                    st.write("---")
                except Exception as e:
                    print(question)
                    break


def crawling_page():
    col1, col2 = st.columns([0.3, 0.7])
    with col1:
        st.header("Question Crawling")
        csv_filename = st.text_input("Enter csv filename (e.g solana-program):", "solana")
        max_question = st.number_input("Max Questions:", min_value = 1, step=1, value=100)
        if st.button("Fetch Questions and Answers"):
            st.session_state.fetched_qa = fetch_questions_and_answers(max_question)
        if st.button("Create and Display DataFrame"):
            st.session_state.df_qa = create_dataframe_from_qa(st.session_state.fetched_qa)
        if st.button("Save to CSV"):
            if st.session_state.df_qa is not None:
                save_dataframe_to_csv(st.session_state.df_qa, csv_filename, CSV_OUTPUT_DIRECTORY)
            else:
                st.write("Please fetch questions and create DataFrame first.")
    
    with col2:
        tab1, tab2 = st.tabs(["Q&A", "Dataframe"])
        with tab1:
            st.subheader(f"Questions and Answers from solana.stackexchange.com")
            display_fetched_questions()
        with tab2:
            st.subheader("CSV Data")
            st.dataframe(st.session_state.df_qa)