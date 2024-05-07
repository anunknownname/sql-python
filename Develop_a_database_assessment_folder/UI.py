import sqlite3
#Function creations
with sqlite3.connect("sql-python/Develop_a_database_assessment_folder/database.db") as database:
    db = database.cursor()
    def search():
        condition = input("What would you like to sort the books by: Author, Genre, Size, or Title?")
        desired_outcome = input("Input the specific thing you are searching for. Eg: Fantasy, The Hobbit, 345")
        if condition.lower() == "size":
            q = (f"SELECT * FROM book_information WHERE book_size >= {desired_outcome.lower()} ORDER BY book_size DESC")
        else:
            q = (f'SELECT * FROM book_information WHERE {condition.lower()} ==  "{desired_outcome.lower()}" ORDER BY title DESC')
        print(q)
        db.execute(q)
        results = db.fetchall()
        for i in results:
            print(i)

#User interface

search()

