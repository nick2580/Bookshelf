import mysql.connector as mysql
import questionary
import requests
import json

# First Create a Database by running the database.sql file.
# IF you have edited the database name in database.sql, kindly edit the same name here i.e. main.py

db = mysql.connect(host='localhost', port='3306', user='root', password='12345678', database='bookshelf_2')

command_handler = db.cursor(buffered=True)

banner = (r'''
.______     ______     ______    __  ___      _______. __    __   _______  __       _______ 
|   _  \   /  __  \   /  __  \  |  |/  /     /       ||  |  |  | |   ____||  |     |   ____|
|  |_)  | |  |  |  | |  |  |  | |  '  /     |   (----`|  |__|  | |  |__   |  |     |  |__   
|   _  <  |  |  |  | |  |  |  | |    <       \   \    |   __   | |   __|  |  |     |   __|  
|  |_)  | |  `--'  | |  `--'  | |  .  \  .----)   |   |  |  |  | |  |____ |  `----.|  |     
|______/   \______/   \______/  |__|\__\ |_______/    |__|  |__| |_______||_______||__|     
 ''')

logo = ('''
   ____________________________________________________
  |____________________________________________________|
  | __     __   ____   ___ ||  ____    ____     _  __  |
  ||  |__ |--|_| || |_|   |||_|**|*|__|+|+||___| ||  | |
  ||==|^^||--| |=||=| |=*=||| |~~|~|  |=|=|| | |~||==| |
  ||  |##||  | | || | |JRO|||-|  | |==|+|+||-|-|~||__| |
  ||__|__||__|_|_||_|_|___|||_|__|_|__|_|_||_|_|_||__|_|
  ||_______________________||__________________________|
  | _____________________  ||      __   __  _  __    _ |
  ||=|=|=|=|=|=|=|=|=|=|=| __..\/ |  |_|  ||#||==|  / /|
  || | | | | | | | | | | |/\ \  \\|++|=|  || ||==| / / |
  ||_|_|_|_|_|_|_|_|_|_|_/_/\_.___\__|_|__||_||__|/_/__|
  |____________________ /\~()/()~//\ __________________|
  | __   __    _  _     \_  (_ .  _/ _      _     _____|
  ||~~|_|..|__| || |_ _   \ //\\ /  |=|_  /) |___| | | |
  ||--|+|^^|==|1||2| | |__/\ __ /\__| |(\/((\ +|+|=|=|=|
  ||__|_|__|__|_||_|_| /  \ \  / /  \_|_\___/|_|_|_|_|_|
  |_________________ _/    \/\/\/    \_ /   /__________|
  | _____   _   __  |/      \../      \/   /   __   ___|
  ||_____|_| |_|##|_||   |   \/ __\       /=|_|++|_|-|||
  ||______||=|#|--| |\   \   o     \_____/  |~|  | | |||
  ||______||_|_|__|_|_\   \  o     | |_|_|__|_|__|_|_|||
  |_________ __________\___\_______|____________ ______|
  |__    _  /    ________     ______           /| _ _ _|
  |\ \  |=|/   //    /| //   /  /  / |        / ||%|%|%|
  | \/\ |*/  .//____// //   /__/__/ (_)      /  ||=|=|=|
__|  \/\|/   /(____|/ //                    /  /||~|~|~|__
  |___\_/   /________//   ________         /  / ||_|_|_|
  |___ /   (|________/   |\_______\       /  /| |______|
      /                  \|________)     /  / | |

''')


print(banner)
print(logo)

def user_session():
    while 1:
        print('')
        print('Welcome to User Profile')
        print('')
        print('1. Add Book from Google Books')
        print('2. Add Book')
        print('3. View all Books')
        print('4. Update Book')
        print('5. Delete Book')
        print('6. Logout')
        print('7. Delete Your Account Data')
        print('')

        # CRUD OPERATION STARTS FROM HERE
        user_option = input(str("Option: "))
        print('')

        # CREATE BY GOOGLE BOOKS
        if user_option == '1':
            print('')
            print('GOOGLE BOOKS')
            print('')
            user_search_query = input(str('Enter name of book to search (Ex Harry Potter): '))
            searchBook(user_search_query)

        # CREATE
        if user_option == '2':
            print('')
            print('Add New Book')
            print('')
            book_title = input(str('Enter Book Title: '))
            book_author = input(str('Enter Author: '))
            book_category = input(str('Enter Book Category: '))
            query_value = (book_title, book_author, book_category,userId)
            command_handler.execute("INSERT INTO books(title,author,category,user_id) VALUES(%s,%s,%s,%s)", query_value)
            db.commit()
            print(book_title + ' has been added to DB')
        # READ
        elif user_option == '3':
            print('')
            print('View All Books')
            print('')
            query_value = userId
            sql = f"SELECT DISTINCT book_id, title, author, category from books WHERE user_id={query_value}"
            command_handler.execute(sql)
            books = command_handler.fetchall()
            for book in books:
                # print("Book: ", book)
                book_obj = book
                print('')
                print("BookId: ", book_obj[0])
                print("Title: ", book_obj[1])
                print("Author: ", book_obj[2])
                print("Category: ", book_obj[3])
                print('')
        # UPDATE
        elif user_option == '4':
            print('')
            print('Update Book')
            print('')
            query_value = userId
            sql = f"SELECT DISTINCT book_id, title, author, category from books WHERE user_id={query_value}"
            command_handler.execute(sql)
            books = command_handler.fetchall()
            for book in books:
                book_obj = book
                print('')
                print("BookId: ", book_obj[0])
                print("Title: ", book_obj[1])
                print("Author: ", book_obj[2])
                print("Category: ", book_obj[3])
                print('')
            user_book_id = input('Enter BookId to update: ')
            print('')
            print("1. Book Title")
            print("2. Book Author")
            print("3. Book Category")
            print('')
            book_update_option = input('What you want to update? : ')
            print('')
            if book_update_option == '1':
                updated_title = input(str('Enter new title: '))
                # if you get ERROR 1094 (HY000): Unknown thread id: XXX,
                # then follow https://stackoverflow.com/questions/2766785 fixing-lock-wait-timeout-exceeded-try-restarting-transaction-for-a-stuck-my/10315184
                sql = f"UPDATE books SET title='{updated_title}' WHERE book_id={user_book_id};"
                command_handler.execute(sql)
                db.commit()
                print('')
                print(f"New Book Title is {updated_title}")
            elif book_update_option == '2':
                updated_author = input(str('Enter new author: '))
                sql = f"UPDATE books SET author='{updated_author}' WHERE book_id={user_book_id};"
                command_handler.execute(sql)
                db.commit()
                print('')
                print(f"New Book Author is {updated_author}")
            elif book_update_option == '3':
                updated_category = input(str("Enter new category: "))
                sql = f"UPDATE books SET category='{updated_category}' WHERE book_id={user_book_id};"
                command_handler.execute(sql)
                db.commit()
                print('')
                print(f"New Book category is {updated_category}")
            else:
                print('Invalid Input')
        # DELETE
        elif user_option == '5':
            print('')
            print('Delete Book')
            print('')
            query_value = userId
            sql = f"SELECT DISTINCT book_id, title, author, category from books WHERE user_id={query_value}"
            command_handler.execute(sql)
            books = command_handler.fetchall()
            for book in books:
                book_obj = book
                print('')
                print("BookId: ", book_obj[0])
                print("Title: ", book_obj[1])
                print("Author: ", book_obj[2])
                print("Category: ", book_obj[3])
                print('')
            user_book_id = input('Enter BookId to delete book: ')
            print('')
            user_decision = input(str('ARE YOU SURE YOU WANT TO DELETE THIS BOOK  y/n: '))
            if user_decision == 'y' or user_decision == 'Y':
                sql = f"DELETE FROM books WHERE book_id={user_book_id};"
                command_handler.execute(sql)
                db.commit()
                print('')
                print("Book Deleted Successfully")
            elif user_decision == 'n' or user_decision == 'N':
                return
        # Logout
        elif  user_option == '6':
            print("Logout successful")
            return
        # Delete All Operations
        elif  user_option == '7':
            print('')
            print('Delete My Account')
            print('')
            print('')
            user_decision = input(str('ARE YOU SURE YOU WANT TO DELETE YOUR ACCOUNT DATA  yes/no: '))
            if user_decision == 'yes':
                check_account_sql = f"SELECT * from books WHERE user_id={userId};"
                command_handler.execute(check_account_sql)
                doesUserExist = command_handler.fetchall()
                for x in doesUserExist:
                    if x:
                        sql_book = f"DELETE from books WHERE user_id={userId};"
                        command_handler.execute(sql_book)
                        db.commit()
                        print('')
                        print("All Books Deleted from your account")
                    else: 
                        print('No Books were found linked with your account')
                sql_user = f"DELETE FROM user WHERE user_id={userId};"
                command_handler.execute(sql_user)
                db.commit()
                print('')
                print("Account Data Deleted Successfully")
                print('')
                return
            elif user_decision == 'no':
                return


def searchBook(book):
    books =[]
    try:
        api_books_data = requests.get('https://www.googleapis.com/books/v1/volumes?q=' + book + '&printType=books')
        books_data = json.loads(api_books_data.content)
        # book_list = books_data['items']
        for book in books_data.get('items', []):
            book_title = book['volumeInfo']['title']
            book_author = book['volumeInfo']['authors']
            if 'categories' in book['volumeInfo']:
                book_category = book['volumeInfo']['categories']
            else:
                book_category = 'N/A'
            books.append(book_title + '^' + book_author[0] + '^' + book_category[0])
        print('')
        user_section = questionary.select("Select the book, which you want to add?", choices=books).ask()  
        selected_book = user_section.split('^')

        selected_book_title = selected_book[0]
        selected_book_author = selected_book[1]
        selected_book_category = selected_book[2]

        query_value = (selected_book_title, selected_book_author, selected_book_category, userId)
        command_handler.execute("INSERT INTO books(title,author,category,user_id) VALUES(%s,%s,%s,%s)", query_value)
        db.commit()
        print('')
        print(selected_book_title, ' was added to DB')
        print('')
    except requests.exceptions.ConnectionError:
        return print('Connection error check your internet connection')
    except KeyError:
        print("Don't panic this is a wierd bug I found in this, please try to search a different book or add manually. Sorry For Trouble")
        return


def create_account():
    # INSERT OPERATION
    print('')
    print('Create User Account')
    print('')
    print('')
    user_name = input(str('Enter your name: '))
    user_email = input(str('Enter your email: '))
    user_password = input(str('Enter password(max 8 char): '))
    query_value = (user_name, user_email, user_password)
    command_handler.execute("INSERT INTO user(name, email, password) VALUES(%s,%s,%s)", query_value)
    db.commit()
    print('')
    print(user_name + ' has been added to DB')
    main()
            
            
def checkUser(email, password):
    global userId
    query_value = (email, password)
    sql = "SELECT email, password, user_id from user WHERE email=%s AND password=%s"
    command_handler.execute(sql,query_value)
    data = command_handler.fetchall()
    for x in data:
        if email == x[0] and password == x[1]:
            userId = x[2]
            return True
        else:
            return False
      

def login():
    print('')
    print('User Login')
    print('')
    email = input(str('Email: '))
    password = input(str("Password: "))
    userStatus = checkUser(email, password)
    if userStatus == True:
        # print(userId)
        user_session()
    else:
        print("Incorrect details")

def main():
    print('')
    print("Welcome to BookShelf")
    print('')
    print("1. Login")
    print("2. Create Account")

    user_option = input(str("Option: "))

    if user_option == '1':
        login()
    elif user_option == '2':
        create_account()
    else:
        print('Invalid Option')

main()