import streamlit as st
import pymysql
import pandas as pd
from datetime import date

def render_employee_dashboard():
    st.title("Employee Dashboard")

    # Get email from session
    email = st.session_state["user"]["email"]

    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='Daql@749#kdp6',
            database='hr_analytics',
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conn.cursor()

        # Fetch existing details
        cursor.execute("SELECT * FROM employee_details WHERE Email = %s", (email,))
        detail = cursor.fetchone()

        cursor.execute("SELECT * FROM employee_dashboard WHERE EmployeeID = (SELECT EmployeeID FROM employee_details WHERE Email = %s)", (email,))
        dashboard = cursor.fetchone()

        # Auto-generate EmployeeID if new
        if not detail:
            cursor.execute("SELECT MAX(EmployeeID) as max_id FROM employee_details")
            max_id = cursor.fetchone()["max_id"] or 1000
            employee_id = max_id + 1
        else:
            employee_id = detail["EmployeeID"]

        # --- Personal Info ---
        st.subheader("Personal Information")
        name = st.text_input("Name", value=detail["EmployeeName"] if detail else "")
        contact = st.text_input("Contact Number", value=detail["ContactNumber"] if detail else "")
        address = st.text_input("Address", value=detail["Address"] if detail else "")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=0 if not detail else ["Male", "Female", "Other"].index(detail["Gender"]))
        age = st.number_input("Age", min_value=18, max_value=60, value=detail["Age"] if detail else 25)
        marital_status = st.selectbox("Marital Status", ["Single", "Married"], index=0 if not detail else ["Single", "Married"].index(detail["MaritalStatus"]))
        joining_date = st.date_input("Joining Date", value=detail["JoiningDate"] if detail else date.today())

        # --- Work Info ---
        st.subheader("Work Details")

        travel_options = ["Travel_Rarely", "Travel_Frequently", "Non-Travel"]
        business_travel = st.selectbox("Business Travel", travel_options,
            index=travel_options.index(dashboard["BusinessTravel"]) if dashboard and dashboard["BusinessTravel"] in travel_options else 0)

        daily_rate = st.number_input("Daily Rate", min_value=0, value=dashboard["DailyRate"] if dashboard else 100)

        department_options = ["Sales", "Research & Development", "Human Resources"]
        department = st.selectbox("Department", department_options,
            index=department_options.index(dashboard["Department"]) if dashboard and dashboard["Department"] in department_options else 0)

        distance_from_home = st.number_input("Distance From Home", min_value=0, value=dashboard["DistanceFromHome"] if dashboard else 5)

        education = st.selectbox("Education Level (1-Basic to 5-Doctorate)", [1, 2, 3, 4, 5],
            index=(dashboard["Education"] - 1) if dashboard and dashboard["Education"] is not None else 2)

        education_field_options = ["Life Sciences", "Medical", "Marketing", "Technical Degree", "Other"]
        education_field = st.selectbox("Education Field", education_field_options,
            index=education_field_options.index(dashboard["EducationField"]) if dashboard and dashboard["EducationField"] in education_field_options else 0)

        environment_satisfaction = st.selectbox("Environment Satisfaction (1-4)", [1, 2, 3, 4],
            index=(dashboard["EnvironmentSatisfaction"] - 1) if dashboard and dashboard["EnvironmentSatisfaction"] is not None else 2)

        job_role_options = ["Sales Executive", "Research Scientist", "Laboratory Technician", "Manufacturing Director",
                            "Healthcare Representative", "Manager", "Sales Representative", "Research Director", "Human Resources"]
        job_role = st.selectbox("Job Role", job_role_options,
            index=job_role_options.index(dashboard["JobRole"]) if dashboard and dashboard["JobRole"] in job_role_options else 0)

        job_satisfaction = st.slider("Job Satisfaction (1-4)", 1, 4, value=dashboard["JobSatisfaction"] if dashboard else 3)

        monthly_income = st.number_input("Monthly Income", min_value=1000, value=dashboard["MonthlyIncome"] if dashboard else 30000)
        monthly_rate = st.number_input("Monthly Rate", min_value=0, value=dashboard["MonthlyRate"] if dashboard else 20000)
        num_companies_worked = st.number_input("Number of Companies Worked", min_value=0, value=dashboard["NumCompaniesWorked"] if dashboard else 1)
        overtime = st.selectbox("OverTime", ["Yes", "No"], index=0 if dashboard and dashboard["OverTime"] == "Yes" else 1)
        total_working_years = st.number_input("Total Working Years", min_value=0, value=dashboard["TotalWorkingYears"] if dashboard else 5)
        years_at_company = st.number_input("Years at Company", min_value=0, value=dashboard["YearsAtCompany"] if dashboard else 3)
        years_in_current_role = st.number_input("Years in Current Role", min_value=0, value=dashboard["YearsInCurrentRole"] if dashboard else 2)
        years_since_last_promotion = st.number_input("Years Since Last Promotion", min_value=0, value=dashboard["YearsSinceLastPromotion"] if dashboard else 1)
        years_with_current_manager = st.number_input("Years with Current Manager", min_value=0, value=dashboard["YearsWithCurrentManager"] if dashboard else 2)

        # --- Submit Button ---
        if st.button("Save Details"):
            try:
                # Insert or update personal details
                cursor.execute("""
                    REPLACE INTO employee_details (
                        EmployeeID, EmployeeName, ContactNumber, Email,
                        Address, Gender, Age, MaritalStatus, JoiningDate
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (employee_id, name, contact, email, address, gender, age, marital_status, joining_date))

                # Insert or update work details
                cursor.execute("""
                    REPLACE INTO employee_dashboard (
                        EmployeeID, BusinessTravel, DailyRate, Department, DistanceFromHome,
                        Education, EducationField, EnvironmentSatisfaction, JobRole, JobSatisfaction,
                        MonthlyIncome, MonthlyRate, NumCompaniesWorked, OverTime, TotalWorkingYears,
                        YearsAtCompany, YearsInCurrentRole, YearsSinceLastPromotion, YearsWithCurrentManager
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    employee_id, business_travel, daily_rate, department, distance_from_home,
                    education, education_field, environment_satisfaction, job_role, job_satisfaction,
                    monthly_income, monthly_rate, num_companies_worked, overtime, total_working_years,
                    years_at_company, years_in_current_role, years_since_last_promotion, years_with_current_manager
                ))

                conn.commit()
                st.success("Details saved successfully!")

            except Exception as e:
                st.error(f"Error while saving: {e}")

    except Exception as e:
        st.error(f"Connection error: {e}")
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass
