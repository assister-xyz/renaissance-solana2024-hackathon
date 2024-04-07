import streamlit as st
import pandas as pd
from pymongo import MongoClient
from config import STACK_EXCHANGE_API_KEY, API_BASE_URL, MONGODB_URI, MONGODB_NAME
from bs4 import BeautifulSoup
import threading
import requests

client = MongoClient(MONGODB_URI)
db = client[MONGODB_NAME]
user_collection = db["users"]
question_collection = db["questions"]
answer_collection = db["answers"]  

def calculate_assisterr_rating(row):
    assister_rating = row["answer_count"] + row["question_count"] + row["up_vote_count"] - row["down_vote_count"]
    return assister_rating

def export_to_excel():
    top_100_users_by_answers = list(user_collection.find().sort("answer_count", -1).limit(100))
    df_top_100_answers = pd.DataFrame(top_100_users_by_answers, columns=["user_id", "link", "display_name", "answer_count"])

    top_100_users_by_assiterr_rating = list(user_collection.find().sort("answer_count", -1).limit(100))
    df_top_100_users_by_assisterr_rating = pd.DataFrame(top_100_users_by_assiterr_rating, columns=["user_id", "link", "display_name",
                                                                          "answer_count", "question_count", "up_vote_count", "down_vote_count"])

    top_100_users_by_upvotes = list(user_collection.find().sort("up_vote_count", -1).limit(100))
    df_top_100_upvotes = pd.DataFrame(top_100_users_by_upvotes, columns=["user_id", "link", "display_name", "up_vote_count"])

    top_100_users_by_downvotes = list(user_collection.find().sort("down_vote_count", -1).limit(100))
    df_top_100_downvotes = pd.DataFrame(top_100_users_by_downvotes, columns=["user_id", "link", "display_name", "down_vote_count"])

    top_100_users_who_asked_questions = list(user_collection.find({"question_count": {"$gt": 0}}).sort("question_count", -1).limit(100))
    df_top_100_questions = pd.DataFrame(top_100_users_who_asked_questions, columns=["user_id", "link", "display_name", "question_count"])

    users_who_asked_questions = list(user_collection.find({"question_count": {"$gt": 0}}))
    df_who_asked_questions = pd.DataFrame(users_who_asked_questions, columns=["user_id", "link", "display_name", "question_count", "up_vote_count"])

    users_who_responded_questions = list(user_collection.find({"answer_count": {"$gt": 0}}))
    df_who_responded_questions = pd.DataFrame(users_who_responded_questions, columns=["user_id", "link", "display_name", "answer_count", "up_vote_count"])

    cols_to_use = df_who_responded_questions.columns.difference(df_who_asked_questions.columns)

    intersection_df = pd.merge(df_who_asked_questions, df_who_responded_questions[cols_to_use], left_index=True, right_index=True, how='outer')
    intersection_df = intersection_df.reindex(columns=["user_id", "link", "display_name", "answer_count", "question_count", "up_vote_count"])
    intersection_df.fillna(0, inplace=True)

    top_100_by_reputation_change_year = list(user_collection.find().sort("reputation_change_year", -1).limit(100))
    df_top_100_by_reputation_change_year = pd.DataFrame(top_100_by_reputation_change_year, columns=["user_id", "link", "display_name", "reputation_change_year"])

    top_100_by_reputation_change_quarter = list(user_collection.find().sort("reputation_change_quarter", -1).limit(100))
    df_top_100_by_reputation_change_quarter = pd.DataFrame(top_100_by_reputation_change_quarter, columns=["user_id", "link", "display_name", "reputation_change_quarter"])

    top_100_by_reputation_change_month = list(user_collection.find().sort("reputation_change_month", -1).limit(100))
    df_top_100_by_reputation_change_month = pd.DataFrame(top_100_by_reputation_change_month, columns=["user_id", "link", "display_name", "reputation_change_month"])

    top_100_by_reputation_change_week = list(user_collection.find().sort("reputation_change_week", -1).limit(100))
    df_top_100_by_reputation_change_week = pd.DataFrame(top_100_by_reputation_change_week, columns=["user_id", "link", "display_name", "reputation_change_week"])

    top_100_by_reputation_change_day = list(user_collection.find().sort("reputation_change_day", -1).limit(100))
    df_top_100_by_reputation_change_day = pd.DataFrame(top_100_by_reputation_change_day, columns=["user_id", "link", "display_name", "reputation_change_day"])

    top_100_by_view_count = list(user_collection.find().sort("view_count", -1).limit(100))
    df_top_100_by_view_count = pd.DataFrame(top_100_by_view_count, columns=["user_id", "link", "display_name", "view_count"])

    top_100_by_badges = list(user_collection.find().sort("badge_counts", -1).limit(100))
    df_top_100_by_badges = pd.DataFrame(top_100_by_badges, columns=["user_id", "link", "display_name", "badge_counts"])

    excel_writer = pd.ExcelWriter("user_stats.xlsx")

    df_top_100_answers.to_excel(excel_writer, sheet_name="Top 100 Users by Answer Count", index=False)
    # df_highest_acceptance_rate.to_excel(excel_writer, sheet_name="Authors with Highest Acceptance Rate", index=False)
    intersection_df.to_excel(excel_writer, sheet_name="Top 100 Users by Answers&Questions Intersection", index=False)

    df_top_100_upvotes.to_excel(excel_writer, sheet_name="Top 100 Users by Received Upvotes", index=False)
    df_top_100_downvotes.to_excel(excel_writer, sheet_name="Top 100 Users by Received Downvotes", index=False)
    df_top_100_questions.to_excel(excel_writer, sheet_name="Top 100 Users Who Asked Questions", index=False)
    df_who_asked_questions.to_excel(excel_writer, sheet_name="List of People Who Ever Asked Question", index=False)
    df_who_responded_questions.to_excel(excel_writer, sheet_name="List of People Who Ever Responded for Question", index=False)
    df_top_100_by_reputation_change_year.to_excel(excel_writer, sheet_name="Top 100 Users by Reputation Change Year", index=False)
    df_top_100_by_reputation_change_quarter.to_excel(excel_writer, sheet_name="Top 100 Users by Reputation Change Quarter", index=False)
    df_top_100_by_reputation_change_month.to_excel(excel_writer, sheet_name="Top 100 Users by Reputation Change Month", index=False)
    df_top_100_by_reputation_change_week.to_excel(excel_writer, sheet_name="Top 100 Users by Reputation Change Week", index=False)
    df_top_100_by_reputation_change_day.to_excel(excel_writer, sheet_name="Top 100 Users by Reputation Change Day", index=False)
    df_top_100_by_view_count.to_excel(excel_writer, sheet_name="Top 100 Users by View Count", index=False)
    df_top_100_by_badges.to_excel(excel_writer, sheet_name="Top 100 Users by Badges", index=False)
    df_top_100_users_by_assisterr_rating.to_excel(excel_writer, sheet_name="Top 100 Users by Assisterr Rating", index=False)
    excel_writer.close()

    st.success("Excel file 'user_stats.xlsx' generated successfully.")





def process_body(body):
    soup = BeautifulSoup(body, 'html.parser')
    for code_tag in soup.find_all('code'):
        code_tag.replace_with(f"```{code_tag.text}```")
    for li_tag in soup.find_all('li'):
        li_tag.replace_with(f"- {li_tag.text}")
    return soup.get_text(separator='\n')


def initialize_db():
    st.write("Initializing MongoDB Collections...")
    user_collection.drop()
    question_collection.drop()
    answer_collection.drop() 
    st.success("Collections dropped.")

def get_questions_data(max_questions=None):
    params = {
        "order": "desc",
        "sort": "creation",
        "site": "solana.stackexchange",
        "pagesize": 100,
        "filter": "withbody",
        "key": STACK_EXCHANGE_API_KEY
    }

    st.write("Fetching Questions Data from Stack Exchange API...")
    
    all_questions = []
    page = 1
    total_questions_fetched = 0
    try:
        while (not max_questions or total_questions_fetched < max_questions):
            params["page"] = page
            response = requests.get(API_BASE_URL + "/questions", params=params)
            if response.status_code == 200 and len(response.json()["items"]) != 0:
                questions_data = response.json()["items"]
                for question in questions_data:
                    question["body"] = process_body(question["body"])
                question_collection.insert_many(questions_data)
                total_questions_fetched += len(questions_data)
                all_questions.extend(questions_data)
                st.session_state.remaining_quota = response.json()["quota_remaining"]

                page += 1
            else:
                print("Error fetching questions:", response.status_code)
                print("Response:", response.text)
                break
    except Exception as e:
        print("Exception while fetching questions:", str(e))
    
    return all_questions[:max_questions] if max_questions else all_questions


def fetch_answers(question_id, answer_collection):
    params = {
        "order": "desc",
        "sort": "votes",
        "site": "solana.stackexchange",
        "filter": "withbody",
        "key": STACK_EXCHANGE_API_KEY
    }
    try:
        response = requests.get(API_BASE_URL + f"/questions/{question_id}/answers", params=params)
        if response.status_code == 200:
            answers_data = response.json()["items"]
            
            for answer in answers_data:
                answer["body"] = process_body(answer["body"])
            
            answer_collection.insert_many(answers_data)
        else:
            print("Error fetching answers for question:", question_id)
            print("Response:", response.text)
    except Exception as e:
        print("Exception while fetching answers for question", question_id, ":", str(e))

def get_answers_for_questions(questions):
    st.write("Fetching Answers for Questions...")
    
    threads = []
    for question in questions:
        question_id = question["question_id"]
        answer_count = question["answer_count"]
        if answer_count > 0:
            thread = threading.Thread(target=fetch_answers, args=(question_id, answer_collection))
            threads.append(thread)
            thread.start()
    
    for thread in threads:
        thread.join()


def get_users_data(max_users=None):
    params = {
        "order": "desc",
        "sort": "reputation",
        "site": "solana.stackexchange",
        "pagesize": 100,
        "filter": "!*Mg4PjfXdyMcuyW.",
        "key": STACK_EXCHANGE_API_KEY
    }

    st.write("Fetching Users Data from Stack Exchange API...")
    
    all_users = []
    page = 1
    total_users_fetched = 0
    try:
        while (not max_users or total_users_fetched < max_users):
            params["page"] = page
            response = requests.get(API_BASE_URL + "/users", params=params)
            if response.status_code == 200 and len(response.json()["items"]) != 0:
                users_data = response.json()["items"]
                users_data = [user for user in users_data if user['user_id'] != -1]
                user_collection.insert_many(users_data)
                total_users_fetched += len(users_data)
                all_users.extend(users_data)
                st.session_state.remaining_quota = response.json()["quota_remaining"]
                print(page)

                page += 1
            else:
                print("Error fetching questions:", response.status_code)
                print("Response:", response.text)
                break
    except Exception as e:
        print("Exception while fetching questions:", str(e))
    
    return all_users[:max_users] if max_users else all_users

def reward_database_page():
    # if st.button("Initialize MongoDB Collections"):
    #     initialize_db()

    if st.button("Get Users Data and Insert into MongoDB"):
        users_data = get_users_data(max_users=10000)
        if users_data:
            st.success("Users data inserted into MongoDB.")
        else:
            st.warning("No Users Data Found")

    if st.button("Get Question Data and Insert into MongoDB"):
        question_data = get_questions_data(max_questions=10000)
        if question_data:
            st.success("Questions data inserted into MongoDB.")
        else:
            st.warning("No Questions Data Found")
    
    if st.button("Get Answers Data and Insert into MongoDB"):
        get_answers_for_questions(question_collection.find())
        st.success("Answers data inserted into MongoDB.")

    col1, col2 = st.columns(2)
    with col2:
        user_count_display = st.number_input("Enter Count of Users to Display (default is 100)", min_value=1, value=100)

    with col1:
        if st.button("Fetch Users Data"):
            users_data = list(user_collection.find().limit(user_count_display))
            if users_data:
                st.markdown(f"### Users Data {len(users_data)}")
                for user in users_data:
                    st.markdown(f"- **Name:** {user['display_name']}, **Reputation:** {user['reputation']}")
                    with st.expander(f"Full data of {user['display_name']}"):
                        st.json(user)

            else:
                st.warning("No Users Data Found")
    
    col1, col2 = st.columns(2)
    with col2:
        question_count_display = st.number_input("Enter Count of Questions to Display (default is 100)", min_value=1, value=100)

    with col1:
        if st.button("Fetch Questions Data"):
            questions_data = list(question_collection.find().limit(question_count_display))
            if questions_data:
                st.markdown(f"### Questions Data {len(questions_data)}")
                for question in questions_data:
                    st.markdown(f"- **Title:** {question['title']}, **Score:** {question['score']}")
                    with st.expander(f"Full data of Question ID = {question['question_id']}"):
                        st.json(question)

            else:
                st.warning("No Questions Data Found")

    col1, col2 = st.columns(2)
    with col2:
        answer_count_display = st.number_input("Enter Count of Answer to Display (default is 100)", min_value=1, value=100)

    with col1:
        if st.button("Fetch Answer Data"):
            answer_data = list(answer_collection.find().limit(answer_count_display))
            if answer_data:
                st.markdown(f"### Answers Data {len(answer_data)}")
                for answer in answer_data:
                    st.markdown(f"- **Answer ID:** {answer['answer_id']}, **Score:** {answer['score']}")
                    with st.expander(f"Full data of Answer ID = {answer['answer_id']}"):
                        st.json(answer)

            else:
                st.warning("No Answers Data Found")


    if st.button("Export Data to Excel"):
        st.write("Exporting data to Excel...")
        excel_file_path = export_to_excel()
        st.success(f"Data exported to Excel file: {excel_file_path}")

    if "remaining_quota" not in st.session_state:
        st.session_state.remaining_quota = None
    
    if st.session_state.remaining_quota is not None:
        st.markdown(f"### Remaining API Quota: {st.session_state.remaining_quota}")
    
    pass

