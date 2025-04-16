import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pymysql

# Database connection setup
def fetch_data():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="Daql@749#kdp6",
        database="hr_analytics"
    )
    query = """
        SELECT e.EmployeeID, e.EmployeeName, e.Gender, e.Age,
               d.BusinessTravel, d.DailyRate, d.Department, d.DistanceFromHome,
               d.Education, d.EducationField, d.EnvironmentSatisfaction, d.HourlyRate,
               d.JobInvolvement, d.JobLevel, d.JobRole, d.JobSatisfaction, d.MonthlyIncome,
               d.MonthlyRate, d.NumCompaniesWorked, d.OverTime, d.PercentSalaryHike,
               d.PerformanceRating, d.TotalWorkingYears, d.YearsAtCompany, d.YearsInCurrentRole,
               d.YearsSinceLastPromotion, d.YearsWithCurrentManager
        FROM employee_details e
        JOIN employee_dashboard d ON e.EmployeeID = d.EmployeeID
    """
    df = pd.read_sql(query, connection)
    connection.close()
    return df

# Preprocess the data
def preprocess_data(df):
    df = df.copy()
    categorical_cols = ["BusinessTravel", "Department", "EducationField", "JobRole", "OverTime"]
    le = LabelEncoder()
    for col in categorical_cols:
        df[col] = le.fit_transform(df[col])
    return df

# Train dummy model using IBM sample dataset format
def train_dummy_model():
    # For demonstration, we'll simulate a model using random forest
    # Normally you would train this on a real dataset with known attrition labels
    from sklearn.datasets import make_classification
    X, y = make_classification(n_samples=500, n_features=10, random_state=42)
    model = RandomForestClassifier()
    model.fit(X, y)
    return model

# Score new data
def predict_attrition(df, model):
    sample_features = df.select_dtypes(include=['int64', 'float64']).iloc[:, :10]  # simulate features
    df['AttritionScore'] = model.predict_proba(sample_features)[:, 1]
    df['AttritionRisk'] = df['AttritionScore'].apply(lambda x: 'High' if x > 0.7 else 'Moderate' if x > 0.4 else 'Low')
    return df

def render():
    # st.title("🧠 Future Attrition Prediction")

    df = fetch_data()
    df_processed = preprocess_data(df)
    model = train_dummy_model()
    df_scored = predict_attrition(df_processed, model)

    st.subheader("Predicted Attrition Risk for Active Employees")
    st.dataframe(df_scored[[
        'EmployeeID', 'MonthlyIncome', 'JobRole', 'Department',
        'JobSatisfaction', 'OverTime', 'AttritionRisk', 'AttritionScore'
    ]], use_container_width=True)

    # Filter top high risk employees (e.g., top 10 by AttritionScore)
    top_risk_employees = df_scored.sort_values(by='AttritionScore', ascending=False).head(10)

    st.subheader("🔴 Top 10 High Attrition Risk Employees")
    st.dataframe(top_risk_employees[['EmployeeID', 'EmployeeName', 'Department', 'JobRole', 'MonthlyIncome', 'JobSatisfaction', 'AttritionScore', 'AttritionRisk']], use_container_width=True)

    # CSV download
    csv = top_risk_employees.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download High Risk Employees as CSV",
        data=csv,
        file_name='high_risk_employees.csv',
        mime='text/csv'
    )

    # Plots
    st.subheader("📊 Visual Insights")
    # Create columns
    col1, col2 = st.columns(2)

    # First plot in first column
    with col1:
        fig1 = px.histogram(
            df_scored,
            x='AttritionRisk',
            color='AttritionRisk',
            title="Attrition Risk Distribution",
            color_discrete_map={
                'High': '#EF553B',
                'Moderate': '#636EFA',
                'Low': '#00CC96'
            }
        )

        # Make bar thinner
        fig1.update_traces(marker_line_width=1, marker_line_color="black")

        # Add more spacing between bars (visually shrinks the bar width)
        fig1.update_layout(
            bargap=0.6,  # 0.1 to 1.0 for thinner bars
            xaxis_title='Attrition Risk',
            yaxis_title='Count'
        )

        st.plotly_chart(fig1, use_container_width=True)

    # Second plot in second column
    with col2:
        fig2 = px.scatter(
            df_scored, x='MonthlyIncome', y='AttritionScore', color='AttritionRisk',
            title='Attrition Score vs Monthly Income', trendline='ols'
        )
        st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.box(df_scored, x='Department', y='AttritionScore', color='Department',
                  title='Department-wise Attrition Score')
    st.plotly_chart(fig3, use_container_width=True)
