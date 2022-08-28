import mysql.connector as mysql

db = mysql.connect(host="localhost",user="root",password="",database="hr_hero")
command_handler = db.cursor(buffered=True)

def manager_session():
    while 1:
        print("")
        print("Manager Menu")
        print("1. Add new employee")
        print("2. Delete existing employee")
        print("3. Mark employee attendance")
        print("4. View register")
        print("5. Logout")
    
        user_option = input(str("Option : "))
        if user_option == "1":
            print("")
            print("Register New Employee")
            username = input(str("Employee username : "))
            password = input(str("Employee password : "))
            query_vals = (username,password)
            command_handler.execute("INSERT INTO users (username,password,privilege) VALUES (%s,%s,'employee')",query_vals)
            db.commit()
            print(username + " has been registered as a employee")
        
        elif user_option == "2":
            print("")
            print("Delete Existing Employee Account")
            username = input(str("Employee username : "))
            query_vals = (username,"employee")
            command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s ",query_vals)
            db.commit()
            if command_handler.rowcount < 1:
                print("User not found")
            else:
                print(username + " has been deleted")
        
        elif user_option == "3":
            print("")
            print("Mark employee attendance")
            command_handler.execute("SELECT username FROM users WHERE privilege = 'employee'")
            records = command_handler.fetchall()
            date    = input(str("Date : DD/MM/YYYY : "))
            for record in records:
                record = str(record).replace("'","")
                record = str(record).replace(",","")
                record = str(record).replace("(","")
                record = str(record).replace(")","")
                #Present | Absent | Late
                status = input(str("Status for " + str(record) + "P/A/L : "))
                query_vals = (str(record),date,status)
                command_handler.execute("INSERT INTO attendance (username, date, status) VALUES(%s,%s,%s)",query_vals)
                db.commit()
                print(record + " Marked as " + status)
        elif user_option == "4":
            print("")
            print("Viewing all employee attendance")
            command_handler.execute("SELECT username, date, status FROM attendance")
            records = command_handler.fetchall()
            print("Displaying all Attendance")
            for record in records:
                print(record)
        elif user_option == "5":
            break
        else:
            print("No valid option was selected")

def employee_session(username):
    while 1:
        print("")
        print("Employee's Menu")
        print("")
        print("1. View Attendance")
        print("2. Download Attendance")
        print("3. Apply for leave")
        print("4. Logout")

        user_option = input(str("Option : "))
        if user_option == "1":
            print("Displaying attendance")
            username = (str(username),)
            command_handler.execute("SELECT date, username, status FROM attendance WHERE username = %s",username)
            records = command_handler.fetchall()
            for record in records:
                print(record)
        elif user_option == "2":
            print("Downloading Attendance")
            username = (str(username),)
            command_handler.execute("SELECT date, username, status FROM attendance WHERE username = %s",username)
            records = command_handler.fetchall()
            for record in records:
                with open("C:/Users/A R MOHON/Desktop/attendance.txt", "w") as f:
                    f.write(str(records)+"\n")
                f.close()
            print("All records saved")
        elif user_option == "4":
            break
        else:
            print("No valid option was selected")


def admin_session():
    while 1:
        print("")
        print("Admin Menu")
        print("1. Register new Manager")
        print("2. Delete Existing Manager")
        print("3. Logout")

        user_option = input(str("Option : "))
        if user_option == "1":
            print("")
            print("Register New Manager")
            username = input(str("Manager username : "))
            password = input(str("Manager password : "))
            query_vals = (username,password)
            command_handler.execute("INSERT INTO users (username,password,privilege) VALUES (%s,%s,'manager')",query_vals)
            db.commit()
            print(username + " has been registered as a manager")
    
        elif user_option == "2":
            print("")
            print("Delete Existing Manager Account")
            username = input(str("Manager username : "))
            query_vals = (username,"manager")
            command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s ",query_vals)
            db.commit()
            if command_handler.rowcount < 1:
                print("User not found")
            else:
                print(username + " has been deleted")

        elif user_option == "3":
            break
        else:
            print("No valid option selected")

def auth_employee():
    print("")
    print("Employee's Login")
    print("")
    username = input(str("Username : "))
    password = input(str("Password : "))
    query_vals = (username, password, "employee")
    command_handler.execute("SELECT username FROM users WHERE username = %s AND password = %s AND privilege = %s",query_vals)
    if command_handler.rowcount <= 0:
        print("Invalid login details")
    else:
        employee_session(username)

def auth_manager():
    print("")
    print("Manager's Login")
    print("")
    username = input(str("Username : "))
    password = input(str("Password : "))
    query_vals = (username, password)
    command_handler.execute("SELECT * FROM users WHERE username = %s AND password = %s AND privilege = 'manager'",query_vals)
    if command_handler.rowcount <= 0:
        print("Login not recognized")
    else:
        manager_session()

def auth_admin():
    print("")
    print("Admin Login")
    print("")
    username = input(str("Username : "))
    password = input(str("Password : "))
    if username == "admin":
        if password == "admin":
            admin_session()
        else:
            print("Incorrect password !")
    else:
        print("Login details not recognised") 

def main():
    while 1:
        print("Welcome to HR HERO system")
        print("")
        print("1. Login as employee")
        print("2. Login as manager")
        print("3. Login as admin")

        user_option = input(str("Option : "))
        if user_option == "1":
            auth_employee()
        elif user_option == "2":
            auth_manager()
        elif user_option == "3":
            auth_admin()
        else:
            print("No valid option was selected")

main()
