import sqlite3
from datetime import timedelta, datetime, date #Modules needed to format TIME values from sqLite
import textwrap # Modulde for formatting paragraphs so words aren't cut of the serial monitor
import random
#Function creations
with sqlite3.connect("sql-python/Develop_a_database_assessment_folder/database.db") as database:
    db = database.cursor()
    def search():
        while True:
            try:
                inv = False
                condition = input("What would you like to sort the library by (genre, author, size, title)? \n Enter 'Exit' to exit ") #Finding what to search the library by
                if condition.lower() == 'exit':
                    break
                if condition.lower() == 'genre': #Sorting by genre
                    desired_genre = input("Input the genre you would like to sort by:\n (Fantasy, Supernatural, Mystery, Adventure, Romance) ")
                    q = (f"SELECT * FROM book_information WHERE genre == '{desired_genre.lower()}' ORDER BY title DESC")
                elif condition.lower() == "size": #Sorting by size
                    desired_size = input("Input the minimum length of the book: ")
                    q = (f"SELECT * FROM book_information WHERE size >= {desired_size} ORDER BY size ASC")
                elif condition.lower() == 'title': #Sorting by book title
                    desired_title = input("Input the name of a book you would like to search for: ")
                    q = f"SELECT * FROM book_information WHERE title == '{desired_title}'"
                elif condition.lower() == "all": #Searching all books
                    q = ("SELECT * FROM book_information ORDER BY id DESC")
                elif condition.lower() == 'author': #Sorting by author
                    desired_author = input("Input the name of an author you would like to search for: ")
                    q = f"SELECT book_information.id, title, size, book_availability_status, blurb, genre FROM book_information JOIN author ON book_information.author_id = author.id WHERE author.name == '{desired_author}'"
                else:
                    print("Invalid Input, try again")
                    inv = True
                    results = ''
                if inv == False: #Executing the query ONLY if new data has been inputted. This means it won't run if there was prior invalid input
                    db.execute(q)
                    results = db.fetchall()
                if results: #Formatting the text results nicely using textwrap module
                    print("Here are your results: ")
                    for i in results: 
                        print(f"""Book Id: {i[0]}
                            Book Title: {i[1]}
                            Book page length: {i[2]}
                            Book Availability: {i[3]}
                            Book Genre: {i[5]} \n
Book Blurb: {textwrap.fill(i[4], 110)} \n """)

                else:
                    print("There were no results")
                    inv = False
            except:
                print("That was an invalid answer you gave. Please input on of the specified sorting conditions.")
    def book_user_search():
        while True:
            try:
                librarian_choice = input("Would you like to find the information of a specific person, or see the information of a person using a specific book? (user/book)\nEnter 'Exit' to exit: ") #Getting input on whether to search for a person or a book
                if librarian_choice.lower() == "user":
                    user_name = input("Enter the name of the user you would like to search for: ")
                    db.execute(f"SELECT * FROM user WHERE user_name == '{user_name}';")
                    results = db.fetchall() #Executing Query
                    if results: #Formatting Query
                        print("This person has this information")
                        for i in results:
                            print(f""" User ID: {i[0]}
                                       User name: {i[1]}
                                       Current Book: {i[2]}
                                       Borrowed Since: {(i[3])[0:10]} \n""")
                    else:
                        print("That person doesn't seem to have a book out at the moment")
                elif librarian_choice.lower() == "book":
                    book_name = input("Enter the name of the book you would like to search for: ")
                    db.execute(f'SELECT * FROM user WHERE user.current_book == "{book_name}";') #Executing Query
                    results = db.fetchall()
                    if results: #Formatting Query
                        print("This book is currently kept by this person: ")
                        for i in results:
                            print(f""" User ID: {i[0]}
                                       User name: {i[1]}
                                       Current Book: {i[2]} 
                                       Borrowed Since: {(i[3])[0:10]} \n""")
                    else:
                        print("That book does seem to be taken out by anyone at the moment! Have another look on the shelves!")
                else:
                    break

            except:
                print("Invalid Input, try again!")
    def overdue():
        print("Here are the people that have a book overdue!")
        db.execute(f"SELECT borrowed_date, user_name FROM user;") #Getting the DATE value of when a user got a book out
        results = db.fetchall()
        today = datetime.now()
        overdue_margin = today - \
                            timedelta(days = 14) # Using the timedelta function to subtract 14 days from a the current time
        overdue_margin = str(overdue_margin).split()
        overdue_margin = overdue_margin[0].split("-") # Formatting the data to use in a date function
        thenbefore = date(int(overdue_margin[0]), int(overdue_margin[1]), int(overdue_margin[2])) #Executing date function. Shows when the threshold for a having a book overdue is
        for i in results:
            then = str(i[0])
            then = then.split("-")
            borrowed_date = date(int(then[0]), int(then[1]), int((then[2])[0:2])) #Getting the DATE value of when a user got a book out
            delta = thenbefore - borrowed_date #Finding the differential between the overdue threshold and when the user got a book out. Tells the programme how overdue a specific book is
            delta = str(delta).split(",") #Formatting results
            if borrowed_date < thenbefore:
                print(str(i[1]) + " has a book over due " + str(delta[0])) #Printing results
    def book_out():
        print("The following people have a book out!")
        db.execute("SELECT user_name FROM user WHERE current_book IS NOT NULL") #Executing query to find all users that have a current_book value of NOT NULL
        results = db.fetchall()
        for i in results:
            print(i[0], "has a book out!")
    def new_user():
        new_name = input("Enter your name: ")
        pin = random.randint(10000, 99999)
        db.execute(f"INSERT INTO user (user_name, user_pin) VALUES ('{new_name}', {pin})") #Inserting the new users name into the database
        database.commit()
        print(f"Your library pin is {pin}, please remember this number!")
        user_pin(new_name)
        check_out(new_name) # Passing in user name to next function

    def check_out(user_name):
        book_name = input("Enter the name of the book you would like to check out: ") #Getting input
        db.execute(f"SELECT title FROM book_information WHERE title == '{book_name}' AND book_availability_status == 'Available'") #Using a query to check whether a book exists by seeing if it has data when searched using an SQL query
        results = db.fetchall()
        if results:
            db.execute(f"SELECT id FROM user WHERE user_name == '{user_name}'") #Finding the id of a user whos name has been passed into the function
            results = db.fetchall()
            user_id = results[0][0]
            db.execute(f"UPDATE user SET current_book = '{book_name}', borrowed_date = '{datetime.now()}' WHERE user_name == '{user_name}'") #Checking out the book using an UPDATE query
            db.execute(f"UPDATE book_information SET book_availability_status = 'Unavailable', current_user_id = '{user_id}' WHERE title == '{book_name}'")#Updating the books data to match the new user
            database.commit()
            print(f"You checked out {book_name}!")
        else:
            print("That book either doesn't exist, or it isn't available right now. Check your spelling.")
            db.execute(f"DELETE FROM user WHERE user_name == '{user_name}'")
            database.commit()
    def check_for_check_out(name):
        db.execute(f"SELECT user_name FROM user WHERE current_book IS NULL AND user_name == '{name}'") #Checking to see if the user is in the database and does not have a book out
        results = db.fetchall()
        if results:
            check_out(name) # Passing in the name of the user to the check out function so the program doesn't have to ask twice
        else:
            db.execute(f"SELECT user_name FROM user WHERE user_name == '{name}'") #Searching to see whether the user is in the databse. If they are, because of the prior query, we know that they have a book out, else, they must not be in the database at all
            results = db.fetchall()
            if not results:
                new_user()
            else:
                print("Looks like you already have a book out, or you misspelled your name\n Return your current book to be able to check a new one out.")
    def return_book(name):
        db.execute(f"SELECT current_book FROM user WHERE user_name == '{name}'")
        results = db.fetchall() #Getting data
        if name == "new_person":
            new_user()
        if results:
            db.execute(f"SELECT current_book FROM user WHERE user_name == '{name}'")
            results = db.fetchall()
            db.execute(f"UPDATE book_information SET book_availability_status = 'Available', current_user_id = NULL WHERE title == '{results[0][0]}';") #Updating the information of the book so that it is available
            db.execute(f"UPDATE user SET borrowed_date = NULL, current_book = NULL WHERE user_name == '{name}'")
            database.commit()
            print(f"{results[0][0]} has been successfully returned. Have a great day! :)")
        else:
            print("You don't seem to have a book out right now. Did you misspell your name?")

    def new_book():
        print("This is where you input new books into the library!") #Getting data
        book_name = input("What is the new book's Title? ")
        book_author = input("What is the new book's Author? ")
        book_genre = input("What is the new book's main genre? ")
        book_length = input("What is the new book's length in pages? ")
        book_blurb = input("Enter the new book's blurb")
        
        db.execute(f"INSERT INTO book_information (title, size, blurb, genre) VALUES ('{book_name}', '{book_length}', '{book_blurb}', '{book_genre}')") #Inserting the new book into the database
        database.commit()
        db.execute(f"SELECT id FROM author WHERE name == '{book_author}'")
        results = db.fetchall()
        author_id = results[0]
        db.execute(f"INSERT INTO author (name) VALUES ('{book_author}')") #Updating the author table
        database.commit()
        db.execute(f"INSERT INTO book_information (author_id) VALUES ('{author_id}')") 
    def print_all():
        print("Here is a list of every book in the library: ")
        db.execute("SELECT * FROM book_information ORDER BY id DESC")
        results = db.fetchall()
        for i in results: #Printing all books with nice formatting using textwrap module
                        print(f"""Book Id: {i[0]}
                            Book Title: {i[1]}
                            Book page length: {i[2]}
                            Book Availability: {i[3]}
                            Book Genre: {i[5]} \n
Book Blurb: {textwrap.fill(i[4], 110)} \n """)
    def user_pin(name):
        db.execute(f"SELECT user_pin FROM user WHERE user_name == '{name}'")
        results = db.fetchall()
        pin = int(input(f"Please enter your library pin, {name} "))
        while results[0][0] != pin:
            print("That is not your pin, try again")
            pin = int(input(f"Please enter your library pin, {name} "))
        print(f"You have been successfully logged in as {name}!")
def user():
    print("You entered the user portal!")
    name = input("Enter the name to log in as, or if you want to continue into the library, enter 'continue': ")
    if name == 'continue':
        name = "new_person"
    else:
        user_pin(name)
    while True:
        try:      
            user_choice = int(input("Please enter the number for the search function you would like to use!\n 1. Go back to login\n 2. Sort the library books \n 3. Check out a book from the library!\n 4. Return a book to the library\n ")) #Getting user choice for specific function
            if user_choice == 1:
                break
            list_of_lists[1][user_choice - 2](name) #Calling the function that corresponds to the number the user entered
        except:
            print("Invalid Input")
def librarian():
    print("You entered the librarian portal!")
    while True:
        try:      
            librarian_choice = int(input("Please enter the number for the function you would like to do!\n 1. Go back to login\n 2. Search for the user of a specific book\n 3. Search for all users who have a book overdue\n 4. See who has a book out\n 5. Enter a new book into the library\n")) #Getting user choice
            if librarian_choice == 1:
                break
            list_of_lists[0][librarian_choice - 2]() # Calling specified funciton
            
        except:
            print("Invalid Input")
def UI():
    while True:
        try:
            user_type = int(input("This is the user/librarian login!\n Enter 1 to access the user portal.\n Otherwise, enter 2 to access the librarian portal! \n Enter 3 to see all books in the library, \n Finally, enter 4 to close the application! ")) #Getting input
            if user_type == 4:
                break
            list_of_lists[2][user_type - 1]() #Calling specified function
        except:
            print("Invalid Input")

list_of_lists = [[book_user_search, overdue, book_out, new_book], [search, check_for_check_out, return_book], [user, librarian, print_all]] #Creation of the list of all the functions for the UI, user, and librarian portal. Must be below all other functions as otherwise it doesn't work.
UI() #Calling the UI function and essentially starting the application