import sqlite3
import re

conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (id TEXT, password TEXT)''')
conn.commit()


def is_input_valid(input_string):
    # If the sanitized input is the same as the original input, all characters are valid
    return re.sub(r'[^a-zA-Z0-9 =/\+\*]', '', input_string) == input_string


def register():

    try:
        while True:
            id = input("Enter a id: ")
            password = input("Enter a password: ")

            if not is_input_valid(id) or not is_input_valid(password) or id.isalpha():
                print("Invalid characters in username(Int) or password.")
            elif len(password) < 8:
                print("Password to short must be at least 8 characters.")
            else:        
                cursor.execute(f"SELECT * FROM users WHERE id = {id}")
                existing_user = cursor.fetchone()

                if not existing_user:
                    cursor.execute(f"INSERT INTO users VALUES ({id}, {hash(password)})")
                    conn.commit()
                    print("Registration successful. You can now log in.")
                    break
                else:
                    print("User already exists")
    except:
        print("Error User Input")
        
def login():

    
    count = 0
    try:
        while count < 6:
            id = input("Enter your id: ")
            password = input("Enter your password: ")

            if not is_input_valid(id) or not is_input_valid(password):
                print("Invalid characters in username(Int) or password.")
            else:
                cursor.execute(f"SELECT * FROM users WHERE id = {id} AND password = {hash(password)}")
                user = cursor.fetchone()

                if user:
                    print(user)
                    break

                print("Invalid id or password. Please try again.")
                count += 1
    except:
        print("Error User Input")

    if count == 6:
        exit(0)
        
    

while True:
    
    print("\nOptions:")
    print("1. Register")
    print("2. Login")
    print("3. Quit")
    choice = input("Enter the number of your choice: ")

    if choice == "1":
        register()
    elif choice == "2":
        login()
    elif choice == "3":
        break
    else:
        print("Invalid choice. Please select 1, 2 or 3")

conn.close()