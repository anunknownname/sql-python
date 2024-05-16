import sqlite3
from datetime import timedelta, datetime, date
#Function creations
with sqlite3.connect("sql-python/Develop_a_database_assessment_folder/database.db") as database:
    db = database.cursor()
    def search():
        while True:
            try:
                condition = input("What would you like to sort the books by: Author, Genre, Size, Title, or just everything(all)? \n Enter 'Exit' to exit ")
                if condition.lower() == 'exit':
                    break
                if condition.lower() != "all":
                    desired_outcome = input("Input the specific thing you are searching for. Eg: Fantasy, The Hobbit, 345 pages. ")
                if condition.lower() == "size":
                    q = (f"SELECT * FROM book_information WHERE size >= {desired_outcome.lower()} ORDER BY size DESC")
                elif condition.lower() == "all":
                    q = ("SELECT * FROM book_information ORDER BY id DESC")
                elif condition.lower() == 'author':
                    q = (f"SELECT * FROM book_information, author WHERE author.name == '{desired_outcome.lower()}' ORDER BY title DESC")
                else:
                    q = (f'SELECT * FROM book_information WHERE {condition.lower()} == "{desired_outcome.lower()}" ORDER BY title DESC')
                db.execute(q)
                results = db.fetchall()
                if results:
                    print("Here are your results: ")
                    for i in results:
                        print(i)
                else:
                    print("There were no results")
            except:
                print("That was an invalid answer you gave. Please input on of the specified sorting conditions.")
    def book_user_search():
        while True:
            try:
                librarian_choice = input("Enter whether you would like to search for a user, or a book: (user/book) ")
                if librarian_choice.lower() == "user":
                    user_name = input("Enter the name of the user you would like to search for: ")
                    db.execute(f"SELECT * FROM user WHERE user_name == '{user_name}';")
                    results = db.fetchall()
                    if results:
                        print("This person has this information")
                        for i in results:
                            print(i)
                    else:
                        print("That person doesn't seem to have a book out at the moment")
                elif librarian_choice.lower() == "book":
                    book_name = input("Enter the name of the book you would like to search for: ")
                    db.execute(f'SELECT * FROM user WHERE user.current_book == "{book_name.lower()}";')
                    results = db.fetchall()
                    if results:
                        print("This book is currently kept by this person: ")
                        for i in results:
                            print(i)
                    else:
                        print("That book does seem to be taken out by anyone at the moment! Have another look on the shelves!")

            except:
                print("Invalid Input, try again!")
    def overdue():
        print("Here are the people that have a book overdue!")
        db.execute(f"SELECT borrowed_date, user_name FROM user;")
        results = db.fetchall()
        today = datetime.now()
        overdue_margin = today - \
                            timedelta(days = 14)
        overdue_margin = str(overdue_margin).split()
        overdue_margin = overdue_margin[0].split("-")
        thenbefore = date(int(overdue_margin[0]), int(overdue_margin[1]), int(overdue_margin[2]))
        for i in results:
            then = str(i[0])
            then = then.split("-")
            borrowed_date = date(int(then[0]), int(then[1]), int(then[2]))
            delta = thenbefore - borrowed_date
            delta = str(delta).split(",")
            if borrowed_date < thenbefore:
                print(str(i[1]) + " has a book over due " + str(delta[0]))
    def book_out():
        print("The following people have a book out!")
        db.execute("SELECT user_name FROM user WHERE current_book IS NOT NULL")
        results = db.fetchall()
        for i in results:
            print(i[0], "has a book out!")
    def check_out()
    def check_for_check_out():
        name = input("Enter the name to check out a book under!")
        db.execute(f"SELECT user_name FROM user WHERE current_book IS NULL AND user_name == '{name}'")
        
        results = db.fetchall()
        if results:
            check_out()
        
        else:
            db.execute(f"SELECT user_name FROM user WHERE user_name == '{name}'")
            results = db.fetchall()
            if results:
                check_out()
            else:
                print("Looks like you already have a book out, or you misspelled your name\n Return your current book to be able to check a new one out.")
    

        
        
        



def user():
    print("You entered the user portal!")
    while True:
        user_choice = input("Please enter the number for the search function you would like to use!\n 1. Go back to login\n 2. Search for specific condition\n 3. Check out a book from the library!\n ")
        if user_choice == "1":
            break
        if user_choice == "2":
            search()
        if user_choice == "3":
            check_for_check_out()
def librarian():
    print("You entered the librarian portal!")
    while True:
        librarian_choice = input("Please enter the number for the function you would like to do!\n 1. Go back to login\n 2. Search for the user of a specific book\n 3. Search for all users who have a book overdue\n 4. See who has a book out\n")
        if librarian_choice == "1":
            break
        if librarian_choice == "2":
            book_user_search()
        if librarian_choice == "3":
            overdue()
        if librarian_choice == "4":
            book_out()

#User interface
while True:
    user_type = input("This is the user/librarian login!\n If you are looking to find or checkout books, type in 'user'.\n Otherwise, type in librarian! \n Enter 'Exit' to exit ")
    if user_type.lower() == "exit":
        break
    elif user_type.lower() == "user":
        user()
    elif user_type.lower() == "librarian":
        librarian()
    else:
        print("Invalid Input, try again")

