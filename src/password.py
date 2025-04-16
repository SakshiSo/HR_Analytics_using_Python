import pymysql
import bcrypt

# Connect to your database
conn = pymysql.connect(host="localhost", user="root", password="Daql@749#kdp6", database="hr_analytics")
cursor = conn.cursor()

# Fetch all users and update passwords
cursor.execute("SELECT email, password FROM users")  # Assuming the 'password' field is plain text
users = cursor.fetchall()

for email, plain_password in users:
    hashed_password = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    
    # Update database with hashed password
    cursor.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_password, email))
    print(f"Updated password for: {email}")

conn.commit()
cursor.close()
conn.close()
print("All passwords have been hashed and updated in the database.")
