import getpass
import mysql.connector
import random
import os
import platform

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Harkeerat@098",
    database="quizMySql"
)

cur = db.cursor()

def clearScreen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def saveUser(username, pwd):
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cur.execute(query, (username, pwd))
    db.commit()
    print("Registration successful! Welcome aboard!\n")

def register():
    clearScreen()
    username = input("Enter a username: ")
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    if user:
        print("Oh no! That username is already taken. Please try a different one.\n")
        return
    pwd = getpass.getpass("Enter a password: ")
    saveUser(username, pwd)

def loadUser(username):
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    return cur.fetchone()

def login():
    clearScreen()
    username = input("Enter your username: ")
    user = loadUser(username)
    if not user:
        print("Hmm, I couldn't find that username. Are you sure you registered?\n")
        return None
    pwd = getpass.getpass("Enter your password: ")
    if user[1] == pwd:
        print("Login successful! Great to see you again!\n")
        return username
    else:
        print("Incorrect password! Please try again.\n")
        return None

def loadQuiz(sub):
    query = "SELECT * FROM quizzes WHERE subject = %s"
    cur.execute(query, (sub,))
    return cur.fetchall()

def takeQuiz(username, sub):
    quizzes = loadQuiz(sub)
    random.shuffle(quizzes)
    selectedQs = quizzes[:5]
    score = 0

    for q in selectedQs:
        print(f"\n{q[2]}\n\na) {q[3]}\nb) {q[4]}\nc) {q[5]}\nd) {q[6]}\n")
        while True:
            ans = input("Enter your answer (a, b, c, d): ")
            if ans in ['a', 'b', 'c', 'd']:
                break
            else:
                print("Invalid input. Please enter one of the options: a, b, c, d.\n")
        if ans == q[7]:
            score += 1

    print(f"\nNice job, {username}! You scored {score} out of 5\n")
    saveResult(username, sub, score, 5)

def saveResult(username, sub, score, total):
    query = "INSERT INTO results (username, subject, score, total) VALUES (%s, %s, %s, %s)"
    cur.execute(query, (username, sub, score, total))
    db.commit()

def viewResults(username):
    query = "SELECT * FROM results WHERE username = %s"
    cur.execute(query, (username,))
    results = cur.fetchall()
    if results:
        print(f"Here are your results, {username}:\n")
        for res in results:
            print(f"Subject: {res[2]}, Score: {res[3]}/{res[4]}\n")
    else:
        print("No results found. Looks like you haven't taken any quizzes yet.\n")

def main():
    subjects = {
        "1": "Python",
        "2": "C++",
        "3": "Java"
    }

    loggedInUser = None
    while True:
        if not loggedInUser:
            print("1. Register\n2. Login\n3. Exit\n")
            choice = input("Enter your choice: ")

            if choice == '1':
                register()
            elif choice == '2':
                loggedInUser = login()
                if loggedInUser:
                    clearScreen()
                    print(f"Welcome, {loggedInUser}!\n")
            elif choice == '3':
                print("Exiting... Hope to see you again!\n")
                break
            else:
                clearScreen()
                print("Invalid choice. Please try again.\n")
        else:
            print("1. Take Quiz\n2. View Results\n3. Logout\n")
            subChoice = input("Enter your choice: ")
            if subChoice == '1':
                clearScreen()
                print("Choose a subject for the quiz:\n")
                for key, sub in subjects.items():
                    print(f"{key}. {sub}")
                subChoice = input("\nEnter your choice: ")

                if subChoice in subjects:
                    clearScreen()
                    takeQuiz(loggedInUser, subjects[subChoice])
                else:
                    clearScreen()
                    print("Invalid choice. Please try again.\n")
            elif subChoice == '2':
                clearScreen()
                viewResults(loggedInUser)
            elif subChoice == '3':
                print("Logging out... See you next time!\n")
                loggedInUser = None
                clearScreen()
            else:
                clearScreen()
                print("Invalid choice. Please try again.\n")

main()
