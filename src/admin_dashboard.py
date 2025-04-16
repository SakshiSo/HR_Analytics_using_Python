import streamlit as st
import pymysql
import bcrypt

def sync_employees_to_user_table(connection):
    try:
        with connection.cursor() as cursor:
            default_password = "Pass@123"
            hashed_password = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt())

            # Get emails from employee_details (normalized)
            cursor.execute("SELECT DISTINCT TRIM(LOWER(Email)) AS email FROM employee_details WHERE Email IS NOT NULL")
            employee_emails = cursor.fetchall()

            insert_query = "INSERT IGNORE INTO users (email, password, role) VALUES (%s, %s, %s)"
            count = 0

            for emp in employee_emails:
                email = emp['email']
                cursor.execute(insert_query, (email, hashed_password, 'employee'))
                count += cursor.rowcount  # only if inserted

            connection.commit()
            st.success(f"✅ {count} new employees synced to user table.")

    except Exception as e:
        st.error(f"❌ Error syncing users: {str(e)}")

 

def render_admin_dashboard():
    st.title("Admin Dashboard")   

    # MySQL connection
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Daql@749#kdp6',
        db='hr_analytics',
        cursorclass=pymysql.cursors.DictCursor
    )

    # 🔄 Sync employees to user table button
    if st.button("🔄 Sync Employees to User Table"):
        sync_employees_to_user_table(connection)

    with connection.cursor() as cursor:
        cursor.execute("SELECT EmployeeID, EmployeeName FROM employee_details ORDER BY EmployeeID")
        employees = cursor.fetchall()

    employee_options = {f"{emp['EmployeeID']} - {emp['EmployeeName']}": emp["EmployeeID"] for emp in employees}
    selected_emp = st.selectbox("Select an employee to edit", list(employee_options.keys()))

    emp_id = employee_options[selected_emp]

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM employee_dashboard WHERE EmployeeID = %s", (emp_id,))
        work_data = cursor.fetchone()

        cursor.execute("SELECT LastWorkingDay FROM employee_details WHERE EmployeeID = %s", (emp_id,))
        detail_data = cursor.fetchone()

    st.subheader(f"Edit Work Details for {selected_emp}")

    # Dropdowns for selection
    business_travel = st.selectbox(
        "Business Travel", 
        ["Travel_Rarely", "Travel_Frequently", "Non-Travel"], 
        index=["Travel_Rarely", "Travel_Frequently", "Non-Travel"].index(work_data["BusinessTravel"]) if work_data and work_data.get("BusinessTravel") else 0
    )

    department = st.selectbox(
        "Department", 
        ["HR", "IT", "Research & Development", "Sales", "Finance"], 
        index=["HR", "IT", "Research & Development", "Sales", "Finance"].index(work_data["Department"]) if work_data and work_data.get("Department") else 0
    )

    job_involvement = st.slider("Job Involvement", 1, 4, value=work_data["JobInvolvement"] if work_data else 3)
    job_level = st.selectbox("Job Level", [1, 2, 3, 4, 5], index=(work_data["JobLevel"] - 1) if work_data and work_data["JobLevel"] is not None else 0)

    job_roles = [
        "HR", "HR Manager", "HR Specialist", "Manager", "Software Engineer", "Data Scientist", 
        "Financial Analyst", "Investment Analyst", "Sales Manager", "Sales Executive", 
        "Sales Representative", "Research Director", "Research Scientist", "Healthcare Representative", 
        "Developer", "Network Engineer"
    ]

    job_role = st.selectbox(
        "Job Role", job_roles, 
        index=job_roles.index(work_data["JobRole"]) if work_data and work_data.get("JobRole") in job_roles else 0
    )

    monthly_income = st.number_input("Monthly Income", min_value=1000, value=work_data["MonthlyIncome"] if work_data else 30000)

    overtime = st.selectbox("OverTime", ["Yes", "No"], index=0 if (work_data and work_data.get("OverTime") == "Yes") else 1)

    performance_options = [1, 2, 3, 4]
    selected_rating = work_data.get("PerformanceRating", 3) if work_data else 3
    selected_rating = selected_rating if selected_rating in performance_options else 3
    performance_rating = st.selectbox("Performance Rating", performance_options, index=performance_options.index(selected_rating))

    # Last Working Day
    last_working_day = st.date_input(
        "Last Working Day (leave empty if still working)", 
        value=detail_data["LastWorkingDay"] if detail_data and detail_data.get("LastWorkingDay") else None
    )

    if st.button("Save Changes"):
        with connection.cursor() as cursor:
            # Update work details
            cursor.execute("""
                UPDATE employee_dashboard SET
                    BusinessTravel=%s,
                    Department=%s,
                    JobInvolvement=%s,
                    JobLevel=%s,
                    JobRole=%s,
                    MonthlyIncome=%s,
                    OverTime=%s,
                    PerformanceRating=%s
                WHERE EmployeeID=%s
            """, (
                business_travel,
                department,
                job_involvement,
                job_level,
                job_role,
                monthly_income,
                overtime,
                performance_rating,
                emp_id
            ))

            # Update Last Working Day
            cursor.execute("""
                UPDATE employee_details SET
                    LastWorkingDay=%s
                WHERE EmployeeID=%s
            """, (last_working_day, emp_id))

            connection.commit()
            st.success("Employee work details updated successfully!")
