import sqlite3
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
                    db.execute(f"SELECT * FROM user WHERE user_name == {user_name}")
                    results = db.fetchall()
                    if results:
                        print("This person has this information")
                        for i in results:
                            print(i)
                    else:
                        print("That person doesn't seem to have a book out at the moment")
                elif librarian_choice.lower() == "book"


            except:
def user():
    print("You entered the user portal!")
    while True:
        user_choice = input("Please enter the number for the search function you would like to use!\n 1. Go back to login\n 2. Search for specific condition\n")
        if user_choice == "1":
            break
        if user_choice == "2":
            search()
def librarian():
    print("You entered the librarian portal!")
    while True:
        librarian_choice = input("Please enter the number for the function you would like to do!\n 1. Go back to login\n 2. Search for the user of a specific book\n")
        if librarian_choice == "1":
            break
        if librarian_choice == "2":

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

