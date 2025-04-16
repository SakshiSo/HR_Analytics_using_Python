import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pymysql
import seaborn as sns

# Function to connect to MySQL and fetch data
def fetch_data(query):
    conn = pymysql.connect(
        host="localhost",
        user="root",  
        password="Daql@749#kdp6",  
        database="hr_analytics"
    )
    df = pd.read_sql(query, conn)

    # Query to fetch employees who have left
    query = """
    SELECT LastWorkingDay 
    FROM employees 
    WHERE LastWorkingDay IS NOT NULL
    """
    df = pd.read_sql(query, conn)

    # Convert LastWorkingDay to datetime format
    df['LastWorkingDay'] = pd.to_datetime(df['LastWorkingDay'])

    # Group by month and count occurrences
    df_monthly = df.resample('M', on='LastWorkingDay').size().reset_index(name='Employee Exits')

    # Plotting
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_monthly, x='LastWorkingDay', y='Employee Exits', marker='o', color='red')

    plt.title("Employee Exit Trends Over Time")
    plt.xlabel("Date")
    plt.ylabel("Number of Employees Exiting")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

# Close the connection
# conn.close()

    conn.close()
    return df




# 1. Attrition by Gender
def plot_attrition_by_gender(df):
    attrition_df = df[df["Attrition"] == "Yes"].groupby("Gender").size().reset_index(name="EmployeesWhoLeft")

    # Plot Graph
    plt.figure(figsize=(8, 5))
    sns.barplot(x='Gender', y='EmployeesWhoLeft', data=attrition_df, palette='pastel')
    plt.title('Attrition by Gender')
    plt.xlabel('Gender')
    plt.ylabel('Employees Who Left')
    st.pyplot(plt)

# 📌 2. Attrition by Department
def plot_attrition_by_department(df):
    attrition_df = df[df["Attrition"] == "Yes"].groupby("Department").size().reset_index(name="EmployeesWhoLeft")

    # Plot Graph
    plt.figure(figsize=(10, 5))
    sns.barplot(x='Department', y='EmployeesWhoLeft', data=attrition_df, palette='coolwarm')
    plt.xticks(rotation=45)
    plt.title('Attrition by Department')
    plt.xlabel('Department')
    plt.ylabel('Employees Who Left')
    st.pyplot(plt)

# 📌 3. Monthly Attrition Trend
def plot_monthly_attrition(df):
    df["AttritionMonth"] = df["LastWorkingDay"].dt.to_period("M")
    attrition_df = df[df["Attrition"] == "Yes"].groupby("AttritionMonth").size().reset_index(name="EmployeesWhoLeft")

    # Plot Line Chart
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=attrition_df["AttritionMonth"].astype(str), y=attrition_df["EmployeesWhoLeft"], marker="o", palette='coolwarm')
    plt.title('Monthly Attrition Trend')
    plt.xlabel('Month')
    plt.ylabel('Employees Who Left')
    st.pyplot(plt)

    