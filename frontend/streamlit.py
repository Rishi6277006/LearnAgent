import frontend.streamlit as st
import requests
import pandas as pd

# Custom Styling for Dark Theme
st.markdown("""
<style>
/* General App Styling */
.stApp {
    background-color: #121212; /* Dark background */
    color: #ffffff; /* Default text color */
}
/* Headers */
h1 {
    color: #BB86FC; /* Light purple for titles */
    text-align: center;
}
h2 {
    color: #03DAC6; /* Teal for subheaders */
}
/* Buttons */
.stButton>button {
    background-color: #BB86FC; /* Purple buttons */
    color: white;
    border-radius: 5px;
    padding: 10px 20px;
    font-size: 16px;
    border: none;
}
/* Input Fields */
.stTextInput>div>div>input {
    background-color: #1E1E1E; /* Dark gray input fields */
    color: white;
    border-radius: 5px;
    padding: 10px;
    font-size: 16px;
    border: 1px solid #BB86FC; /* Purple border */
}
/* Sidebar */
.stSidebar {
    background-color: #1E1E1E; /* Dark gray sidebar */
}
/* DataFrames */
.stDataFrame {
    background-color: #1E1E1E; /* Dark gray table background */
    color: white;
}
/* Success/Error Messages */
.stSuccess {
    background-color: #1B5E20; /* Dark green for success messages */
    color: white;
    border-radius: 5px;
    padding: 10px;
}
.stError {
    background-color: #B71C1C; /* Dark red for error messages */
    color: white;
    border-radius: 5px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "user_registered" not in st.session_state:
    st.session_state.user_registered = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "register"
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# Registration Page
def register_user():
    st.subheader("Register a New User")
    with st.form("registration_form"):
        name = st.text_input("Name", placeholder="Enter your name")
        email = st.text_input("Email", placeholder="Enter your email")
        submitted = st.form_submit_button("Register")
        if submitted:
            if name.strip() and email.strip():
                try:
                    response = requests.post(
                        "http://127.0.0.1:8000/users/",
                        json={"name": name, "email": email}
                    )
                    response.raise_for_status()
                    user = response.json()
                    st.success(f"Welcome, {user['name']}! You are now registered.")
                    st.session_state.user_registered = True
                    st.session_state.user_id = user["id"]  # Store user ID
                    st.session_state.current_page = "login"  # Navigate to login page
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to register user: {str(e)}")
            else:
                st.warning("Please fill in all fields.")

# Login Page
def login_user():
    st.subheader("Login")
    email = st.text_input("Email", placeholder="Enter your email")
    if st.button("Login"):
        if email.strip():
            try:
                response = requests.get(f"http://127.0.0.1:8000/users/?email={email}")
                response.raise_for_status()
                user = response.json()
                st.success(f"Welcome back, {user['name']}!")
                st.session_state.user_id = user["id"]  # Store user ID
                st.session_state.current_page = "lesson"  # Navigate to lesson page
            except requests.exceptions.RequestException as e:
                st.error(f"Login failed: {str(e)}")
        else:
            st.warning("Please enter your email.")

def generate_lesson_page():
    st.subheader("Generate a Lesson")
    topic = st.text_input("Topic", placeholder="e.g., Python, Machine Learning, etc.")
    difficulty = st.selectbox("Select Difficulty", ["Beginner", "Intermediate", "Advanced"])
    preference = st.radio("Learning Preference", ["Theoretical", "Practical"])
    if st.button("Generate Lesson"):
        if topic.strip():
            with st.spinner("Generating lesson..."):
                try:
                    response = requests.get(
                        f"http://127.0.0.1:8000/lesson/?topic={topic}&level={difficulty}&preference={preference}&user_id={st.session_state.user_id}"
                    )
                    response.raise_for_status()
                    lesson = response.json()

                    # Debugging: Print the full response (REMOVE OR COMMENT OUT THIS LINE)
                    # st.write("Debugging: Full Response from Backend", lesson)

                    # Check if "content" exists and contains "lesson_content"
                    if "content" in lesson and "lesson_content" in lesson["content"]:
                        st.success("Lesson generated successfully!")
                        st.subheader(f"Lesson on {topic.capitalize()}")

                        # Render the lesson content as markdown
                        st.markdown(lesson["content"]["lesson_content"], unsafe_allow_html=False)
                    else:
                        st.error("Unexpected response format from backend. Missing 'lesson_content'.")
                        st.write("Full Response:", lesson)
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to generate lesson: {str(e)}")
        else:
            st.warning("Please enter a topic.")

# Leaderboard Page
def leaderboard_page():
    st.subheader("Leaderboard")
    try:
        response = requests.get("http://127.0.0.1:8000/users/")
        response.raise_for_status()
        users = response.json()
        # Sort users by total points
        sorted_users = sorted(users, key=lambda x: x["total_points"], reverse=True)
        leaderboard_data = {
            "Name": [user["name"] for user in sorted_users],
            "Total Points": [user["total_points"] for user in sorted_users]
        }
        df = pd.DataFrame(leaderboard_data)
        st.dataframe(df, use_container_width=True)
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch leaderboard: {str(e)}")

# Badges Page
def badges_page():
    st.subheader("Your Badges")
    badges = [
        "Completed 5 Lessons",
        "Scored 100 on a Quiz",
        "Earned 500 Points"
    ]
    for badge in badges:
        st.markdown(f"- 🏆 {badge}")

# Main App Logic
def main():
    st.title("LearnAgent: AI-Powered Learning Platform")
    # Navigation Based on Session State
    if st.session_state.current_page == "register":
        register_user()
    elif st.session_state.current_page == "login":
        login_user()
    elif st.session_state.current_page == "lesson":
        generate_lesson_page()
    elif st.session_state.current_page == "leaderboard":
        leaderboard_page()
    elif st.session_state.current_page == "badges":
        badges_page()
    
    # Sidebar Navigation
    if st.session_state.user_registered:
        menu = ["Generate Lesson", "Take a Quiz", "Leaderboard", "Badges"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Generate Lesson":
            st.session_state.current_page = "lesson"
        elif choice == "Take a Quiz":
            st.session_state.current_page = "quiz"
        elif choice == "Leaderboard":
            st.session_state.current_page = "leaderboard"
        elif choice == "Badges":
            st.session_state.current_page = "badges"

if __name__ == "__main__":
    main()