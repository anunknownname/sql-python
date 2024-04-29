import sqlite3 
 
def all(value):
    print(value)
    db = sqlite3.connect("task3.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM fighter ORDER BY {value} DESC;")
    results = cursor.fetchall()
    print("name                          speed   max_g  climb  range   payload")
    for planes in results:
        print(f"{planes[1]:<30}{planes[2]:<8}{planes[3]:<7}{planes[4]:<7}{planes[5]:<8}{planes[6]:<7}")
    db.close() 
def print_all():
    db = sqlite3.connect("task3.db")
    cursor = db.cursor()
    sql = "SELECT * FROM fighter;"
    cursor.execute(sql)
    results = cursor.fetchall()
    print("name                          speed   max_g  climb  range   payload")
    for planes in results:
        print(f"{planes[1]:<30}{planes[2]:<8}{planes[3]:<7}{planes[4]:<7}{planes[5]:<8}{planes[6]:<7}")
    db.close()
while True:
    user_input = input(
        """
What would you like to do?
1. Print all aircraft
2. Print all aircraft sorted by max gravity.
3. Print all aircraft sorted by climbrate.
4. Print all aircraft sorted by range.
5. Print all aircraft sorted by payload.
Enter Exit to exit""")
    if user_input == "1":
        print_all()
    elif user_input == "2":
        all("max_g")
    elif user_input == "3":
        all("climb_rate")
    elif user_input == "4":
        all("range")
    elif user_input == "5":
        all("payload")
    elif user_input.lower() == "exit":
        break

    else:
        print("Invalid answer.")
