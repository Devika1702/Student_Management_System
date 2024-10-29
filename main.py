import mysql.connector
from mysql.connector import Error
from datetime import datetime

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root", 
            password="Password@01",  
            database="studentmanagementsystem"  
        )
        if connection.is_connected():
            print("Connected to the database")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

conn = create_connection()
cursor = conn.cursor()

def register():
    print("\n--- Registration ---")
    email = input("Enter email: ")
    username = input("Enter username: ")
    # special case
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        print("Username already exists. Try a different one.\n")
        return

    password = input("Enter password: ")
    confirm_password = input("Confirm password: ")
    # Check if passwords match
    if password != confirm_password:
        print("Passwords do not match. Please try again.\n")
        return

    cursor.execute("INSERT INTO users (email, username, password) VALUES (%s, %s, %s)", (email, username, password))
    conn.commit()
    print(f"\nStudent {username} registered successfully!\n")

# Function to login a student
def login():
    print("\n--- Login ---")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Check if the username and password match
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    result = cursor.fetchone()

    if result:
        print(f"\nLogin successful! Welcome, {username}!\n")
        return True
    else:
        print("\nInvalid username or password. Please try again.\n")
        return False

# Function to add a student
def add_student():
    firstname = input("Enter student's first name: ")
    lastname = input("Enter student's last name: ")
    address = input("Enter student's address: ")
    dob_input = input("Enter student's date of birth (YYYY-MM-DD): ")
    
    # special case - Check date format
    try:
        dob = datetime.strptime(dob_input, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.\n")
        return
    
    gender = input("Enter student's gender (Male/Female/Other): ")
    if gender not in ('Male', 'Female', 'Other'):
        print("Invalid gender. Please enter 'Male', 'Female', or 'Other'.\n")
        return

    grade = input("Enter student's grade: ")
    contact_number = input("Enter student's 10-digit contact number: ")

    #special case
    if not (contact_number.isdigit() and len(contact_number) == 10):
        print("Invalid contact number. It must be a 10-digit number.\n")
        return

    cursor.execute("INSERT INTO students (firstname, lastname, address, dob, gender, grade, contact_number) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (firstname, lastname, address, dob, gender, grade, contact_number))
    conn.commit()
    print(f"\nStudent {firstname} {lastname} added successfully!\n")

def delete_student():
    name = input("Enter the first name of the student to delete: ")
    cursor.execute("DELETE FROM students WHERE firstname = %s", (name,))
    conn.commit()
    print(f"\nStudent {name} deleted successfully!\n")

def view_all_students():
    cursor.execute("SELECT * FROM students")
    results = cursor.fetchall()

    if len(results) == 0:
        print("\nNo students in the system.\n")
    else:
        print("\nStudent List:")
        for student in results:
            print(f"ID: {student[0]}, Name: {student[1]} {student[2]}, Address: {student[3]}, DOB: {student[4]}, Gender: {student[5]}, Grade: {student[6]}, Contact Number: {student[7]}")
        print()

def view_student():
    name = input("Enter the first name of the student to view: ")
    cursor.execute("SELECT * FROM students WHERE firstname = %s", (name,))
    result = cursor.fetchone()

    if result:
        print(f"\nName: {result[1]} {result[2]}, Address: {result[3]}, DOB: {result[4]}, Gender: {result[5]}, Grade: {result[6]}, Contact Number: {result[7]}\n")
    else:
        print("\nStudent not found.\n")

def edit_student():
    name = input("Enter the first name of the student to edit: ")
    cursor.execute("SELECT * FROM students WHERE firstname = %s", (name,))
    result = cursor.fetchone()

    if result:
        print("\nStudent found.")
        new_firstname = input("Enter new first name: ")
        new_lastname = input("Enter new last name: ")
        new_address = input("Enter new address: ")
        
        new_dob_input = input("Enter new date of birth (YYYY-MM-DD): ")
        try:
            new_dob = datetime.strptime(new_dob_input, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.\n")
            return

        new_gender = input("Enter new gender (Male/Female/Other): ")
        if new_gender not in ('Male', 'Female', 'Other'):
            print("Invalid gender.\n")
            return

        new_grade = input("Enter new grade: ")
        new_contact_number = input("Enter new 10-digit contact number: ")

        if not (new_contact_number.isdigit() and len(new_contact_number) == 10):
            print("Invalid contact number.\n")
            return

        cursor.execute("UPDATE students SET firstname = %s, lastname = %s, address = %s, dob = %s, gender = %s, grade = %s, contact_number = %s WHERE firstname = %s",
                       (new_firstname, new_lastname, new_address, new_dob, new_gender, new_grade, new_contact_number, name))
        conn.commit()
        print("\nStudent updated successfully!\n")
    else:
        print("\nStudent not found.\n")

# Function to display the menu and perform CRUD operations
def student_menu():
    while True:
        print("\n--- Student Management Menu ---")
        print("1. Add Student")
        print("2. Delete Student")
        print("3. View All Students")
        print("4. View Specific Student")
        print("5. Edit Student")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            add_student()
        elif choice == '2':
            delete_student()
        elif choice == '3':
            view_all_students()
        elif choice == '4':
            view_student()
        elif choice == '5':
            edit_student()
        elif choice == '6':
            print("Exiting the program...")
            cursor.close()
            conn.close()
            break
        else:
            print("Invalid choice. Please try again.\n")

def main():
    while True:
        print("\n--- Welcome to the Student Management System ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            register()
        elif choice == '2':
            if login():
                student_menu() 
        elif choice == '3':
            print("Exiting the program...")
            cursor.close()
            conn.close()  
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()
