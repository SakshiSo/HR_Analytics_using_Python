import pymysql
import pandas as pd

# Function to connect to MySQL and fetch data
def fetch_data(query):
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="Daql@749#kdp6",  # Replace with your MySQL password
            database="hr_analytics",
            cursorclass=pymysql.cursors.DictCursor    
        )
        cursor = conn.cursor()  # Use dictionary cursor
        cursor.execute(query)
        data = cursor.fetchall()  # Fetch data properly
        df = pd.DataFrame(data)   # Convert to DataFrame
        # cursor.close()
        # conn.close()
        
        # Ensure missing columns exist in DataFrame
        expected_columns = [
            "EmployeeID", "Gender", "Age", "MaritalStatus", "JoiningDate", "LastWorkingDay",
            "EducationField", "YearsAtCompany", "YearsSinceLastPromotion", "PerformanceRating", "TotalWorkingYears",
            "Department", "JobRole", "MonthlyIncome", "OverTime", "PercentSalaryHike", "YearsWithCurrentManager"
        ]

        for col in expected_columns:
            if col not in df.columns:
                df[col] = None  # Fill missing columns with NULL (avoids frontend errors)

        # WorkExperience = TotalWorkingYears
        df["WorkExperience"] = df["TotalWorkingYears"]
    
        return df

    except pymysql.err.OperationalError as e:
        print(f"❌ MySQL Operational Error: {e}")
    except pymysql.err.ProgrammingError as e:
        print(f"❌ MySQL Programming Error: {e}")
    except pymysql.MySQLError as e:
        print(f"❌ General MySQL Error: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# Updated function to load data from MySQL
def load_transform():
    query = """
    SELECT 
        e.EmployeeID, e.Gender, e.Age, e.MaritalStatus, e.JoiningDate, e.LastWorkingDay,
        d.EducationField, d.YearsAtCompany, d.YearsSinceLastPromotion, d.PerformanceRating, d.TotalWorkingYears,
        d.Department, d.JobRole, d.JobInvolvement, d.JobSatisfaction, d.MonthlyIncome, d.OverTime, d.PercentSalaryHike, d.YearsWithCurrentManager
    FROM employee_details e
    JOIN employee_dashboard d ON e.EmployeeID = d.EmployeeID;
    """
    df = fetch_data(query)

    if df.empty:
        print("No data found.")

    
    # Apply data transformations (if needed)
    df["JoiningDate"] = pd.to_datetime(df["JoiningDate"], errors="coerce")
    df["LastWorkingDay"] = pd.to_datetime(df["LastWorkingDay"], errors="coerce")

    # Calculate Attrition Status
    df["Attrition"] = df["LastWorkingDay"].apply(lambda x: "Yes" if pd.notna(x) else "No")

    # ✅ Ensure 'PctAtCompany' column exists
    if "YearsAtCompany" in df.columns and df["YearsAtCompany"].sum() > 0:
        df["PctAtCompany"] = (df["YearsAtCompany"] / df["YearsAtCompany"].sum()) * 100
        df["PctAtCompany"] = df["PctAtCompany"].round(2)  # ✅ Keep only 2 decimal places
    else:
        df["PctAtCompany"] = 0  # ✅ Default value if YearsAtCompany is missing

    # ✅ Ensure 'ToBePromoted' column exists
    if "YearsSinceLastPromotion" in df.columns and "PerformanceRating" in df.columns:
        df["ToBePromoted"] = df.apply(
            lambda row: "Yes" if row["YearsSinceLastPromotion"] > 3 and row["PerformanceRating"] >= 3 else "No", axis=1
        )
    else:
        df["ToBePromoted"] = "Unknown"  # ✅ Default value if columns are missing

    # ✅ Ensure 'ToBeRetrenched' column exists
    if "PerformanceRating" in df.columns and "YearsAtCompany" in df.columns:
        df["ToBeRetrenched"] = df.apply(
            lambda row: "Yes" if row["PerformanceRating"] <= 2 and row["YearsAtCompany"] > 10 else "No", axis=1
        )
    else:
        df["ToBeRetrenched"] = "Unknown"  # ✅ Default value if columns are missing

    # ✅ Debugging prints to confirm both columns exist
    print("✅ Columns in df:", df.columns.tolist())
    print("✅ PctAtCompany sample:", df["PctAtCompany"].head())
    print("✅ ToBePromoted sample:", df["ToBePromoted"].value_counts())
    print("✅ ToBeRetrenched column added. Sample values:", df["ToBeRetrenched"].value_counts())

    return df

def df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

# Function to return filter options
def get_filter_options(df, empty_filters=False):
    
    """Returns filter fields options to fill filter or clear filter fields"""
    valid_columns = df.columns

    filter_opt = {
        "Gender": df["Gender"].unique().tolist() if "Gender" in valid_columns else [],
        "Department": df["Department"].unique().tolist() if "Department" in valid_columns else [],
        "EducationField": df["EducationField"].unique().tolist() if "EducationField" in valid_columns else [],
        "JobRole": df["JobRole"].unique().tolist() if "JobRole" in valid_columns else [],
        "Age": [df["Age"].min(), df["Age"].max()] if "Age" in valid_columns else [0, 0],
        "YearsAtCompany": [df["YearsAtCompany"].min(), df["YearsAtCompany"].max()] if "YearsAtCompany" in valid_columns else [0, 0],
    }
    return filter_opt


def get_gender_count(df):
    """Returns total employees, male count, female count, and their percentages"""
    
    total_employees = len(df)
    male_count = len(df[df["Gender"] == "Male"])
    female_count = len(df[df["Gender"] == "Female"])

    male_pct = round((male_count / total_employees) * 100, 2) if total_employees > 0 else 0
    female_pct = round((female_count / total_employees) * 100, 2) if total_employees > 0 else 0

    return total_employees, male_count, female_count, male_pct, female_pct

def get_dept_stats_df(df):
    """Calculate various stats for each department and return results in a DataFrame"""
    
    required_cols = {
        "Department", "MonthlyIncome", "PercentSalaryHike",
        "TotalWorkingYears", "YearsAtCompany", "OverTime"
    }

    # Check for missing required columns
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        raise KeyError(f"Missing columns in dataset: {missing_cols}")

    # Calculate mean values for numeric columns (excluding TrainingTimesLastYear)
    df_dept = df.groupby("Department")[[
        "MonthlyIncome", "PercentSalaryHike",
        "TotalWorkingYears", "YearsAtCompany"
    ]].mean().round(2)

    # Calculate OverTime count per department
    df_ot = df[df["OverTime"] == "Yes"].groupby("Department")["OverTime"].count().to_frame()

    # Join department stats with OverTime counts
    df_dept_stat = df_dept.join(df_ot, how="left").reset_index()
    df_dept_stat["OverTime"] = df_dept_stat["OverTime"].fillna(0).astype(int)

    return df_dept_stat

 
def get_pct_at_cmp(df):
    """Returns percentage of employees grouped by years at company."""
    
    if "YearsAtCompany" not in df.columns:
        print("⚠ Warning: 'YearsAtCompany' column missing in DataFrame")
        return pd.DataFrame(columns=["YearsAtCompany", "Percentage"])  # Return empty DataFrame

    df_pct_at_cmp = df["YearsAtCompany"].value_counts(normalize=True).reset_index()
    df_pct_at_cmp.columns = ["YearsAtCompany", "Percentage"]
    
    # ✅ Convert Percentage to float to prevent formatting issues
    df_pct_at_cmp["Percentage"] = df_pct_at_cmp["Percentage"].astype(float).round(4)

    return df_pct_at_cmp


def get_promo_count(df):
    """Returns count of employees promoted vs not promoted and their percentages."""
    
    if "YearsSinceLastPromotion" not in df.columns:
        print("⚠ Warning: 'YearsSinceLastPromotion' column missing in DataFrame")
        return 0, 0, 0.0, 0.0  # Return default values

    promo_cnt = len(df[df["YearsSinceLastPromotion"] > 0])  # Employees who got a promotion
    not_promo_cnt = len(df[df["YearsSinceLastPromotion"] == 0])  # Employees with no promotion

    total_employees = promo_cnt + not_promo_cnt
    promo_pct = round((promo_cnt / total_employees) * 100, 2) if total_employees > 0 else 0
    no_promo_pct = round((not_promo_cnt / total_employees) * 100, 2) if total_employees > 0 else 0

    return promo_cnt, not_promo_cnt, promo_pct, no_promo_pct

def get_retrench_count(df):
    """Returns count of retrenched employees vs active employees and their percentages."""
    
    if "Attrition" not in df.columns:
        print("⚠ Warning: 'Attrition' column missing in DataFrame")
        return 0, 0, 0.0, 0.0  # Return default values

    retrench_cnt = len(df[df["Attrition"] == "Yes"])  # Employees who have left
    active_cnt = len(df[df["Attrition"] == "No"])  # Employees still working

    total_employees = retrench_cnt + active_cnt
    retrench_pct = round((retrench_cnt / total_employees) * 100, 2) if total_employees > 0 else 0
    active_pct = round((active_cnt / total_employees) * 100, 2) if total_employees > 0 else 0

    return retrench_cnt, active_cnt, retrench_pct, active_pct

def get_dept_promo_pct(df):
    """Returns department-wise percentage of employees who got promoted."""
    
    if "Department" not in df.columns or "YearsSinceLastPromotion" not in df.columns:
        print("⚠ Warning: 'Department' or 'YearsSinceLastPromotion' column missing in DataFrame")
        return pd.DataFrame(columns=["Department", "PromotionPercentage"])  # Return empty DataFrame if columns are missing

    # Count total employees per department
    df_dept_total = df.groupby("Department")["EmployeeID"].count().reset_index()
    df_dept_total.columns = ["Department", "TotalEmployees"]

    # Count employees who got a promotion (YearsSinceLastPromotion > 0)
    df_dept_promo = df[df["YearsSinceLastPromotion"] > 0].groupby("Department")["EmployeeID"].count().reset_index()
    df_dept_promo.columns = ["Department", "PromotedEmployees"]

    # Merge both DataFrames
    df_dept_promo = df_dept_total.merge(df_dept_promo, on="Department", how="left").fillna(0)

    # Calculate Promotion Percentage per department
    df_dept_promo["PromotionPercentage"] = (
        df_dept_promo["PromotedEmployees"] / df_dept_promo["TotalEmployees"]
    ) * 100

    df_dept_promo["PromotionPercentage"] = df_dept_promo["PromotionPercentage"].round(2)  # ✅ Round to 2 decimal places

    return df_dept_promo

def get_dept_retrench_pct(df):
    """Returns department-wise percentage of employees to be retrenched."""
    
    if "Department" not in df.columns or "ToBeRetrenched" not in df.columns:
        print("⚠ Warning: 'Department' or 'ToBeRetrenched' column missing in DataFrame")
        return pd.DataFrame(columns=["Department", "RetrenchPercentage"])  # ✅ Return empty DataFrame if columns are missing

    # Count total employees per department
    df_dept_total = df.groupby("Department")["EmployeeID"].count().reset_index()
    df_dept_total.columns = ["Department", "TotalEmployees"]

    # Count employees marked as "ToBeRetrenched"
    df_dept_retrench = df[df["ToBeRetrenched"] == "Yes"].groupby("Department")["EmployeeID"].count().reset_index()
    df_dept_retrench.columns = ["Department", "RetrenchedEmployees"]

    # Merge both DataFrames
    df_dept_retrench = df_dept_total.merge(df_dept_retrench, on="Department", how="left").fillna(0)

    # Calculate Retrenchment Percentage per department
    df_dept_retrench["RetrenchPercentage"] = (
        df_dept_retrench["RetrenchedEmployees"] / df_dept_retrench["TotalEmployees"]
    ) * 100

    df_dept_retrench["RetrenchPercentage"] = df_dept_retrench["RetrenchPercentage"].round(2)  # ✅ Round to 2 decimal places

    return df_dept_retrench

def get_attrition_stats(df):
    """Returns attrition statistics including department-wise and job role attrition."""
    
    if "Attrition" not in df.columns:
        print("⚠ Warning: 'Attrition' column missing in DataFrame")
        return {}  # ✅ Return empty dictionary if column is missing

    # Overall attrition rate
    total_employees = len(df)
    attrition_count = len(df[df["Attrition"] == "Yes"])
    attrition_rate = round((attrition_count / total_employees) * 100, 2) if total_employees > 0 else 0

    # Attrition stats by gender
    attrition_stats = {
        "CompanyWide": {
            "Total Attrition": attrition_count,
            "Attrition Rate": attrition_rate,
        },
        "Male": {
            "Total Attrition": len(df[(df["Gender"] == "Male") & (df["Attrition"] == "Yes")]),
            "Attrition Rate": round(
                (len(df[(df["Gender"] == "Male") & (df["Attrition"] == "Yes")]) / total_employees) * 100, 2
            ) if total_employees > 0 else 0,
        },
        "Female": {
            "Total Attrition": len(df[(df["Gender"] == "Female") & (df["Attrition"] == "Yes")]),
            "Attrition Rate": round(
                (len(df[(df["Gender"] == "Female") & (df["Attrition"] == "Yes")]) / total_employees) * 100, 2
            ) if total_employees > 0 else 0,
        },
        "Department": df[df["Attrition"] == "Yes"].groupby("Department")["EmployeeID"].count().to_dict(),
        "JobRole": df[df["Attrition"] == "Yes"].groupby("JobRole")["EmployeeID"].count().to_dict(),
        "WorkplaceProximity": df[df["Attrition"] == "Yes"].groupby("YearsWithCurrentManager")["EmployeeID"].count().to_dict(),
        "JobSatisfaction": df[df["Attrition"] == "Yes"].groupby("PerformanceRating")["EmployeeID"].count().to_dict(),
        "Ages": df[df["Attrition"] == "Yes"].groupby("Age")["EmployeeID"].count().to_dict(),
        "WorkExperience": df[df["Attrition"] == "Yes"].groupby("TotalWorkingYears")["EmployeeID"].count().to_dict(),
    }

    return attrition_stats


