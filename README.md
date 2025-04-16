💼 HR Analytics Dashboard:

A data-driven web application to monitor and analyze employee performance, predict attrition risk, and provide HR insights using a role-based login system. Built using Streamlit, MySQL, and Python, this project enables HRs, Admins, and Employees to interact with data in real-time.

📌 Overview:

This HR Analytics system helps organizations keep track of employee performance and retention using interactive dashboards and predictive analytics. The system provides:
- Department-wise and demographic insights
- Attrition prediction for active employees
- Role-based access (HR, Admin, Employee)
- Real-time data updates through MySQL backend

🎯 Objective:

To build a comprehensive HR Analytics Dashboard that:
- Tracks key HR metrics such as attrition, performance rating, and promotions
- Allows employees to enter and update their information
- Enables admins to edit employee work-related details
- Predicts potential employee attrition using ML models
- Provides HRs with data insights for better decision-making

💡 Motivation:

Organizations today face major challenges in retaining top talent and identifying performance gaps. This project was inspired by the need to:
- Leverage data analytics for better HR management
- Digitize employee records and dashboards
- Create a system where employee information is accessible and manageable through a unified platform
- Enable predictive insights for proactive HR strategies

🧰 Technologies Used:

- Frontend: Streamlit
- Backend: Python (Pandas, Plotly, Seaborn, Matplotlib, bcrypt, streamlit_kpi)
- Database: MySQL (with pymysql connector)
- Authentication: Role-based login system (HR, Admin, Employee)

🗃️ Database Setup (MySQL):

The project uses a MySQL database named hr_analytics which contains three tables:
- user – Stores login credentials and user roles.
- employee_details – Stores personal employee information.
- employee_dashboard – Stores work-related details for analytics and predictions.

🔧 Steps to Setup MySQL:

Install MySQL Server if not already installed.
- Windows: https://dev.mysql.com/downloads/installer/

Login to MySQL CLI or GUI (like MySQL Workbench).

Create the database:
CREATE DATABASE hr_analytics;

Inside hr_analytics, create the following three tables:
- user
- employee_details
- employee_dashboard

🗂️ Database Schema
1. user Table: Stores user login information and roles.
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('HR', 'admin', 'employee') NOT NULL
);

2. employee_details Table: Stores basic personal information of employees.
CREATE TABLE employee_details (
    EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
    EmployeeName VARCHAR(100),
    ContactNumber VARCHAR(20),
    Email VARCHAR(100) UNIQUE,
    Address TEXT,
    Gender ENUM('Male', 'Female', 'Other'),
    Age INT,
    MaritalStatus ENUM('Single', 'Married', 'Divorced', 'Widowed'),
    JoiningDate DATE,
    LastWorkingDay DATE
);

3. employee_dashboard Table: Stores employee work-related details used for analytics and attrition prediction.
CREATE TABLE employee_dashboard (
    EmployeeID INT,
    BusinessTravel VARCHAR(50),
    DailyRate INT,
    Department VARCHAR(50),
    DistanceFromHome INT,
    Education INT,
    EducationField VARCHAR(50),
    HourlyRate INT,
    JobInvolvement INT,
    JobLevel INT,
    JobRole VARCHAR(50),
    JobSatsfaction INT,
    MonthlyIncome INT,
    MonthlyRate INT,
    NumCompaniesWorked INT,
    OverTime ENUM('Yes', 'No'),
    PercentSalaryHike INT,
    PerformanceRating INT,
    TotalWorkingYears INT,
    YearsAtCompany INT,
    YearsInCurrentRole INT,
    YearsSinceLastPromotion INT,
    YearsWithCurrentManager INT,
    PRIMARY KEY (EmployeeID),
    FOREIGN KEY (EmployeeID) REFERENCES employee_details(EmployeeID) ON DELETE CASCADE
);

✨ Features
🔐 Role-Based Login System:
- HR users can view analytics dashboards, employee attrition predictions, and department-wise metrics.
- Admin users can edit all employee work-related data using a centralized Admin Dashboard.
- Employees can sign up, log in, and update their personal information.

📊 Interactive Dashboards:
- Executive Summary with KPIs like attrition rate, promotion rate, and retrenchment.
- Department-wise analytics using charts and filters.
- Demographic insights based on gender, age, marital status, etc.

🧠 Attrition Prediction:
-  Predicts attrition probability for each active employee using job satisfaction, role, department, salary, overtime status, and more.
- Visual indicators to flag high-risk employees.

🧾 Real-Time Data Management:
- All updates to employee details or dashboards are instantly reflected in the database.
- Auto-generated EmployeeID for new employees.
- Smart form filling for both new entries and updating existing data.

🔄 Seamless Integration with MySQL:
- Centralized MySQL database (hr_analytics) for storing and fetching employee data.
- Dynamic fetching and transformation using Pandas + PyMySQL pipeline.

🖼️ Screenshots & Demo
![Login Page](https://github.com/SakshiSo/HR_Analytics_using_Python/blob/main/Images/Login.png)
![Admin Dashboard](https://github.com/SakshiSo/HR_Analytics_using_Python/blob/main/Images/Admin%20Dashboard.png)
![Employee Dashboard](https://github.com/SakshiSo/HR_Analytics_using_Python/blob/main/Images/Employee%20Dashboard.png)
![Summary Dashboard](https://github.com/SakshiSo/HR_Analytics_using_Python/blob/main/Images/Summary%20Dashboard.png)
![Attrition Prediction](https://github.com/SakshiSo/HR_Analytics_using_Python/blob/main/Images/Attrition%20Prediction.png)
![Top and Bottom Employee](https://github.com/SakshiSo/HR_Analytics_using_Python/blob/main/Images/Top%20and%20Bottom%20Employees.png)


How to Run Locally
Follow these steps to run the HR Analytics Dashboard on your local machine:

1. Clone the Repository
git clone https://github.com/your-username/hr-analytics-dashboard.git
cd hr-analytics-dashboard

2. Create Virtual Environment (Optional but Recommended)
python -m venv venv
venv\Scripts\activate        # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Setup MySQL
Create the database:

CREATE DATABASE hr_analytics;
Run the table creation scripts provided earlier to create:

user

employee_details

employee_dashboard

5. Update MySQL Credentials
In your db.py or config file, update the credentials:
connection = pymysql.connect(
    host='localhost',
    user='username', # your sql root username
    password='password', # your sql root password
    db='hr_analytics'
)

6. Run the App
streamlit run app.py
or
python.exe -m streamlit run app.py

✅ requirements.txt
List the essential libraries (already in your project, but summarize in the README too):
streamlit
pymysql
pandas
plotly
seaborn
matplotlib
bcrypt

pip install -r requirements.txt

🙋‍♀️ Author
**Sakshi Sonavane**  
Final Year Computer Engineering  
Mumbai University  

📄 License
This project is for educational purposes only. No commercial use is intended.

📬 Contact
For queries or contributions, feel free to reach out at:  
📧 sonavanesakshi2002@gmail.com  
📱 LinkedIn: [linkedin.com/in/sakshi-sonavane](https://www.linkedin.com/in/sakshi-sonavane/)