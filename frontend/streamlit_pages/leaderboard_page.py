import streamlit as st
import requests
from config import BACKEND_URL
def fetch_users():
    response = requests.get(f"{BACKEND_URL}/api/users")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data")
        return []

def create_leaderboard_table(users, sorting_key, title):
    st.markdown(
        """
        <style>
        .gold {
            background-color: gold;
            font-weight: bold;
            font-size: larger;
        }
        
        .silver {
            background-color: silver;
            font-weight: bold;
            font-size: larger;
        }
        
        .bronze {
            background-color: #cd7f32; /* Bronze color */
            font-weight: bold;
            font-size: larger;
        }
        .center-text {
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True
    )

    table = f"<h3>{title}</h3><table style='width: 100%;'><tr><th style='width: 5%;'>Rank</th><th>User</th><th>Value</th></tr>"
    for i, user in enumerate(users, start=1):
        medal = ""
        if i == 1:
            medal = "🥇"
            row_class = "gold"
            row_style = "font-weight: bold; font-size: xx-large;"  # Larger size for 1st place
        elif i == 2:
            medal = "🥈"
            row_class = "silver"
            row_style = "font-weight: bold; font-size: x-large;"   # Larger size for 2nd place
        elif i == 3:
            medal = "🥉"
            row_class = "bronze"
            row_style = "font-weight: bold; font-size: x-large;"   # Larger size for 3rd place
        else:
            medal = ""
            row_class = ""
            row_style = ""
        
        table += f"""<tr>
        <td class='center-text {row_class}' style='width: 5%; {row_style}'>{medal if i <= 3 else i}</td>
        <td><a href='{user['link']}' target='_blank'><img src='{user['profile_image']}' style='width: 50px; height: 50px; border-radius: 50%;'></a> {user['display_name']}</td>
        <td class='center-text' style='width: 5%;'>{user[sorting_key]}</td>
        </tr>"""

    table += "</table>"
    st.markdown(table, unsafe_allow_html=True)



def leaderboard_page():
    users = fetch_users()

    

    st.header("Leaderboards")

    leaderboard_categories = {
        "Reputation Changes": {
            "Reputation Overall": "reputation",
            "Reputation Change Year": "reputation_change_year",
            #"Reputation Change Quarter": "reputation_change_quarter",
            "Reputation Change Month": "reputation_change_month",
            "Reputation Change Week": "reputation_change_week",
            "Reputation Change Day": "reputation_change_day"
        },
        "Votes & Views": {
            "Upvotes": "up_vote_count",
            "Downvotes d☠️": "down_vote_count",
            "View Count": "view_count"
        },
        "Questions & Answers": {
            "Questions Asked Count": "question_count",
            "Questions Answered Count": "answer_count"
        }
        
    }

    with st.sidebar:
        selected_tab = st.radio("Select Leaderboard Category", list(leaderboard_categories.keys()))
        if st.button("Back to chat", use_container_width=True):
            st.session_state.current_page = "chat_page"
            st.rerun()
    if selected_tab in leaderboard_categories:
        st.subheader(f"{selected_tab} Leaderboards")
        category = leaderboard_categories[selected_tab]
        tabs = st.tabs(category.keys())
        for index, (title, sorting_key) in enumerate(category.items()):
            with tabs[index]:
                top_users = sorted(users, key=lambda x: x.get(sorting_key, 0), reverse=True)[:100]
                create_leaderboard_table(top_users,sorting_key, f"Top 100 Users by {title}")

