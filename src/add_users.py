# New user (HR/Admin/Emp) to hash their password
# import pymysql
# import bcrypt

# # MySQL Connection
# conn = pymysql.connect(host="localhost", user="root", password="Daql@749#kdp6", database="hr_analytics")
# cursor = conn.cursor()

# # Fetch all users with plain-text passwords (assuming plain text passwords don't start with '$2b$', the bcrypt prefix)
# cursor.execute("SELECT email, password FROM users WHERE password NOT LIKE '$2b$%'")
# users = cursor.fetchall()

# if users:
#     for email, plain_password in users:
#         # Hash the plain-text password
#         hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

#         # Update the database with the hashed password
#         cursor.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_password, email))

#     conn.commit()
#     print(f"Updated {len(users)} user(s) with hashed passwords.")
# else:
#     print("No plain-text passwords found.")

# cursor.close()
# conn.close()


# To add all employees in user table, who dont have their password , Lets set their default password "Pass@123"
# import pymysql
# import bcrypt

# # Connect to the MySQL database
# conn = pymysql.connect(
#     host="localhost",
#     user="root",
#     password="Daql@749#kdp6",
#     database="hr_analytics"
# )
# cursor = conn.cursor()

# # Set the default password and hash it
# default_password = "welcome123"
# hashed_password = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt())

# # Step 1: Get all emails from employee_details not already in user table
# query = """
# SELECT Email FROM employee_details
# WHERE Email NOT IN (SELECT email FROM user)
# """
# cursor.execute(query)
# new_employees = cursor.fetchall()

# # Step 2: Insert into user table
# insert_query = "INSERT INTO user (email, password, role) VALUES (%s, %s, %s)"
# for emp in new_employees:
#     email = emp[0]
#     cursor.execute(insert_query, (email, hashed_password, 'employee'))

# # Commit the changes
# conn.commit()

# print(f"✅ {cursor.rowcount} new employee accounts created in 'user' table.")

# # Close the connection
# cursor.close()
# conn.close()

# import pymysql
# import bcrypt

# # MySQL connection
# connection = pymysql.connect(
#     host='localhost',
#     user='root',
#     password='Daql@749#kdp6',
#     database='hr_analytics',
#     cursorclass=pymysql.cursors.DictCursor
# )

# # The new password you want to set for all employees
# new_password = "Pass@123"  # Replace with your desired password
# hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

# try:
#     with connection.cursor() as cursor:
#         update_query = """
#         UPDATE users 
#         SET password = %s 
#         WHERE role = 'employee'
#         """
#         cursor.execute(update_query, (hashed_password,))
#     connection.commit()
#     print("All employee passwords updated successfully.")
# finally:
#     connection.close()
