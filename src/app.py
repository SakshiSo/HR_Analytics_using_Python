import streamlit as st
import pymysql
import bcrypt
from config import app_config
import data
import tab_capacity
import tab_summary
import tab_attrition
import tab_prediction
import utils
import filters

# Ensure session state initialization
if "user" not in st.session_state:
    st.session_state["user"] = None

# Ensure set_page_config is called first
st.set_page_config(page_title="HR Analytics Dashboard", page_icon="📊", layout="wide")

# Connect to MySQL database and fetch user details
def get_user_from_db(email):
    """Fetch user details (hashed password, role) from the database."""
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Daql@749#kdp6',
        db='hr_analytics',
    )
    try:
        with connection.cursor() as cursor:
            sql = "SELECT password, role FROM users WHERE email = %s"
            cursor.execute(sql, (email,))
            result = cursor.fetchone()
            return result  # Returns (hashed_password, role)
    finally:
        connection.close()

# Create a new user in the database with role employee
def create_employee_user(email, password):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Daql@749#kdp6',
        db='hr_analytics',
    )
    try:
        with connection.cursor() as cursor:
            hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            sql = "INSERT INTO users (email, password, role) VALUES (%s, %s, %s)"
            cursor.execute(sql, (email, hashed_pw, "employee"))
        connection.commit()
    finally:
        connection.close()

# HR/Admin/Employee Login
if st.session_state["user"] is None:
    st.title("Login to HR Analytics Dashboard")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user_data = get_user_from_db(email)
        if user_data:
            stored_password, role = user_data
            if bcrypt.checkpw(password.encode("utf-8"), stored_password.encode("utf-8")):
                st.session_state["user"] = {"email": email, "role": role}
                st.success(f"Logged in as {role.capitalize()} - {email}")
                st.rerun()  # Refresh the page
            else:
                st.error("Invalid password.")
        else:
            # Automatically create new employee user
            create_employee_user(email, password)
            st.success("New employee account created and logged in.")
            st.session_state["user"] = {"email": email, "role": "employee"}
            st.rerun()
            
# If user is logged in, show the dashboard
if st.session_state["user"]:
    role = st.session_state["user"]["role"]
    email = st.session_state["user"]["email"]
    st.sidebar.write(f"Welcome, {st.session_state['user']['email']}")
    
    if role == "HR":
        st.title("HR Analytics Dashboard")

        utils.setup_app(app_config)

       # Load fresh data on every visit (optional: controlled by refresh button)
        if "df_hr" not in st.session_state:
            st.session_state["df_hr"] = data.load_transform()

        if st.button("🔄 Refresh Data"):
            st.session_state["df_hr"] = data.load_transform()
            st.success("Data refreshed!")

        df_hr = st.session_state["df_hr"]   

        df_hr = filters.apply(df_hr)

        # df_hr = data.load_transform()
        # df_hr = filters.apply(df_hr)
        exec_summary, capacity_analysis, attrition_analysis, prediction_analysis = utils.create_tabs([
            "EXECUTIVE SUMMARY 📝", "CAPACITY ANALYSIS 🚀", "ATTRITION ANALYSIS 🏃‍♂️", "PREDICTION ANALYSIS 🔮"
        ])
        with exec_summary:
            # st.write(f"Total records in HR Data: {len(df_hr)}")

            tab_summary.render(df_hr)
        with capacity_analysis:
            tab_capacity.render(df_hr)       
        with attrition_analysis:
            tab_attrition.render(df_hr)
        with prediction_analysis:
            tab_prediction.render()
    
    elif role == "admin":
        import admin_dashboard
        admin_dashboard.render_admin_dashboard()
    
    elif role == "employee":
        from employee_dashboard import render_employee_dashboard
        render_employee_dashboard()
    
    if st.sidebar.button("Logout"):
        st.session_state["user"] = None
        st.rerun()
