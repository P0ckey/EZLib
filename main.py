import customtkinter
import sqlite3
from CTkListbox import *

connection = sqlite3.connect("library.db")

cursor = connection.cursor()

# cursor.execute("DROP TABLE users")
#
# sql_command = """CREATE TABLE users (
# id INTEGER PRIMARY KEY,
# username VARCHAR(20),
# password VARCHAR(30),
# admin BOOL,
# bbooks VARCHAR(10));"""
#
# cursor.execute(sql_command)
# connection.commit()
#
# cursor.execute("DROP TABLE books")
#
#
# sql_command = """CREATE TABLE books (
# id INTEGER PRIMARY KEY,
# name VARCHAR(50),
# author VARCHAR(40),
# buser INTEGER,
# isbn VARCHAR(13));"""
#
# cursor.execute(sql_command)
# connection.commit()
#
# cursor.execute("INSERT INTO users VALUES (0, 'admin', 'admin', TRUE, '1')")
# connection.commit()
# cursor.execute("INSERT INTO books VALUES (0, 'Atomic Habits', 'James Clear', -1, '9780735211292')")
# connection.commit()

bookmap = []
books = []
users = []

def GetBorrowedBooks(username):
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    result = cursor.fetchall()
    uid = result[0][0]
    # print(uid)
    result = getbooks()[0]
    bbooks = []
    for i in result:
        if i[3] == uid:
            bbooks.append(i[1])
    return bbooks



def getbooks():
    cursor.execute("SELECT * FROM books")
    bookmap = cursor.fetchall()
    books=[]
    for i in bookmap:
        books.append(i[1])
    return bookmap, books

def getusers():
    cursor.execute("SELECT * FROM users")
    usermap = cursor.fetchall()
    print(usermap
          )
    users=[]
    for i in usermap:
        users.append(i[1])
    return usermap, users
class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.geometry("900x500")
        self.title("EZLib Login")
        self.minsize(400,300)



        # ██╗░░░░░░█████╗░░██████╗░██╗███╗░░██╗
        # ██║░░░░░██╔══██╗██╔════╝░██║████╗░██║
        # ██║░░░░░██║░░██║██║░░██╗░██║██╔██╗██║
        # ██║░░░░░██║░░██║██║░░╚██╗██║██║╚████║
        # ███████╗╚█████╔╝╚██████╔╝██║██║░╚███║
        # ╚══════╝░╚════╝░░╚═════╝░╚═╝╚═╝░░╚══╝

        def button_click():
            global username
            username = UsernameEntry.get()
            password = PasswordEntry.get()
            result = cursor.execute("SELECT * FROM users")
            print(result)
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            connection.commit()
            result = cursor.fetchall()
            global userid
            for i in getusers()[0]:
                if i[1] == username:
                    userid = i[0]
            if result and result[0][3] == True:
                print("success")
                app.withdraw()
                toplevel = AdminPanel(self)
            elif result:
                app.withdraw()
                toplevel = ClientPanel(self)
            return


        # page widgets
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.button = customtkinter.CTkButton(self, command=button_click, text="Login")
        TitleLabel = customtkinter.CTkLabel(self, text="EZLib Login", fg_color="transparent", font=customtkinter.CTkFont(size=35))
        TitleLabel.grid(row=0, column=0, padx=10, pady=(50, 25), columnspan=2)
        UsernameLabel = customtkinter.CTkLabel(self, text="Username: ", fg_color="transparent")
        UsernameLabel.grid(row=1, column=0, padx=10, pady=(20,5), sticky="e")
        UsernameEntry = customtkinter.CTkEntry(self, placeholder_text="username")
        UsernameEntry.grid(row=1, column=1, padx=10, pady=(20,5), sticky="w")
        PasswordLabel = customtkinter.CTkLabel(self, text="Password: ", fg_color="transparent")
        PasswordLabel.grid(row=2, column=0, padx=10, pady=(5,10), sticky="e")
        PasswordEntry = customtkinter.CTkEntry(self, placeholder_text="password")
        PasswordEntry.grid(row=2, column=1, padx=10, pady=(5,10), sticky="w")
        self.button.grid(row=3, column=0, padx=20, pady=10, columnspan=2)




# ░█████╗░██████╗░███╗░░░███╗██╗███╗░░██╗
# ██╔══██╗██╔══██╗████╗░████║██║████╗░██║
# ███████║██║░░██║██╔████╔██║██║██╔██╗██║
# ██╔══██║██║░░██║██║╚██╔╝██║██║██║╚████║
# ██║░░██║██████╔╝██║░╚═╝░██║██║██║░╚███║
# ╚═╝░░╚═╝╚═════╝░╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝
class AdminPanel(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("900x600")
        self.title("EZLib Admin")
        tabview = customtkinter.CTkTabview(master=self)
        tabview.pack(fill = 'both', expand = 1)
        tabview.add("books")
        tabview.add("users")
        tabview.set("books")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        books = getbooks()[1]
        selection=""
        self.minsize(600, 550)


        # ██████╗░░█████╗░░█████╗░██╗░░██╗░██████╗
        # ██╔══██╗██╔══██╗██╔══██╗██║░██╔╝██╔════╝
        # ██████╦╝██║░░██║██║░░██║█████═╝░╚█████╗░
        # ██╔══██╗██║░░██║██║░░██║██╔═██╗░░╚═══██╗
        # ██████╦╝╚█████╔╝╚█████╔╝██║░╚██╗██████╔╝
        # ╚═════╝░░╚════╝░░╚════╝░╚═╝░░╚═╝╚═════╝░

        def BookListSelect(choice):
            cursor.execute("SELECT * FROM books WHERE name = ?", (choice,))
            result=cursor.fetchall()
            BookNameResult.configure(text=result[0][1])
            AuthorNameResult.configure(text=result[0][2])
            print(result)
            if result[0][3] != -1:
                BorrowedResult.configure(text=result[0][3])
            else:
                BorrowedResult.configure(text="None")
            ISBNResult.configure(text=result[0][4])


        ###Left ListBox Element
        BookLabel = customtkinter.CTkLabel(text="Books", master=tabview.tab("books"))
        BookLabel.grid(row=0, column=0, padx=20)
        BookList = CTkListbox(command=BookListSelect, master=tabview.tab("books"))
        BookList.grid(row=1, column=0, rowspan=10, padx=20, sticky="w")
        for idx, i in enumerate(books):
            BookList.insert(idx, i)


        ###Book Info Display
        BookName = customtkinter.CTkLabel(text="Title: ", master=tabview.tab("books"))
        BookName.grid(row=1, column=1, padx=(25,10), sticky="e")
        BookNameResult = customtkinter.CTkLabel(text="", master=tabview.tab("books"))
        BookNameResult.grid(row=1, column=2, padx=(25,10), sticky="w")
        AuthorName = customtkinter.CTkLabel(text="Author: ", master=tabview.tab("books"))
        AuthorName.grid(row=2, column=1, padx=(25,10), sticky="e")
        AuthorNameResult = customtkinter.CTkLabel(text="", master=tabview.tab("books"))
        AuthorNameResult.grid(row=2, column=2, padx=(25,10), sticky="w")
        ISBN = customtkinter.CTkLabel(text="ISBN Number: ", master=tabview.tab("books"))
        ISBN.grid(row=3, column=1, padx=(25,10), sticky="e")
        ISBNResult = customtkinter.CTkLabel(text="", master=tabview.tab("books"))
        ISBNResult.grid(row=3, column=2, padx=(25,10), sticky="w")
        Borrowed = customtkinter.CTkLabel(text="Borrowed By: ", master=tabview.tab("books"))
        Borrowed.grid(row=4, column=1, padx=(25,10), sticky="e")
        BorrowedResult = customtkinter.CTkLabel(text="", master=tabview.tab("books"))
        BorrowedResult.grid(row=4, column=2, padx=(25, 10), sticky="w")

        ###Removing a book
        def RemoveBook():
            cursor.execute("DELETE FROM books WHERE name = ?", (BookList.get(),))
            connection.commit()
            books=getbooks()[1]
            BookNameResult.configure(text="")
            AuthorNameResult.configure(text="")
            ISBNResult.configure(text="")
            BorrowedResult.configure(text="")
            BookList.delete("all")
            for idx, i in enumerate(books):
                BookList.insert(idx, i)

        RemoveButton = customtkinter.CTkButton(master=tabview.tab("books"), text="Remove Selected Book", command=RemoveBook, fg_color="red")
        RemoveButton.grid(row=11, column=0,padx=10, pady=10)


        def AddBook():
            if ISBNInput.get() == '' or AuthorInput.get() == '' or BookNameInput == '':
                AddBookError.configure(text="Fields Cannot Be Empty")
                return
            AddBookError.configure(text="")
            if len(ISBNInput.get()) != 13:
                AddBookError.configure(text="Incorrect ISBN Format")
                return
            cursor.execute("SELECT * FROM books WHERE name = ?", (BookNameInput.get(),))
            result=cursor.fetchall()
            if result:
                AddBookError.configure(text="Book Already Exists")
                return
            cursor.execute("SELECT max(id) FROM books")
            maximum = cursor.fetchall()
            try:
                maximum[0][0]/1
                max=maximum[0][0]
            except:
                max = -1
            print(maximum)
            cursor.execute("INSERT INTO books VALUES (?, ?, ?, -1, ?)", (max+1, BookNameInput.get(), AuthorInput.get(), ISBNInput.get()))
            connection.commit()
            books=getbooks()[1]
            for idx, i in enumerate(books):
                BookList.insert(idx, i)

        AddBookLabel = customtkinter.CTkLabel(text="Add Book", master=tabview.tab("books"))
        AddBookLabel.grid(row=11, column=2)
        BookNameInputLabel = customtkinter.CTkLabel(text="Book Name: ", master=tabview.tab("books"))
        BookNameInputLabel.grid(row=12, column=1, sticky="e")
        BookNameInput = customtkinter.CTkEntry(master=tabview.tab("books"), placeholder_text="book name")
        BookNameInput.grid(row=12, column=2)
        AuthorInputLabel = customtkinter.CTkLabel(text="Author: ", master=tabview.tab("books"))
        AuthorInputLabel.grid(row=13, column=1, sticky="e")
        AuthorInput = customtkinter.CTkEntry(master=tabview.tab("books"), placeholder_text="author")
        AuthorInput.grid(row=13, column=2)
        ISBNInputLabel = customtkinter.CTkLabel(text="ISBN: ", master=tabview.tab("books"))
        ISBNInputLabel.grid(row=14, column=1, sticky="e")
        ISBNInput = customtkinter.CTkEntry(master=tabview.tab("books"), placeholder_text="isbn")
        ISBNInput.grid(row=14, column=2)
        AddBookButton = customtkinter.CTkButton(master=tabview.tab("books"), text="Add Book", command=AddBook)
        AddBookButton.grid(row=15, column=2, sticky="e")
        AddBookError = customtkinter.CTkLabel(master=tabview.tab("books"), text="", text_color="red")
        AddBookError.grid(row=16, column=2, sticky="w")




        # ██╗░░░██╗░██████╗███████╗██████╗░░██████╗
        # ██║░░░██║██╔════╝██╔════╝██╔══██╗██╔════╝
        # ██║░░░██║╚█████╗░█████╗░░██████╔╝╚█████╗░
        # ██║░░░██║░╚═══██╗██╔══╝░░██╔══██╗░╚═══██╗
        # ╚██████╔╝██████╔╝███████╗██║░░██║██████╔╝
        # ░╚═════╝░╚═════╝░╚══════╝╚═╝░░╚═╝╚═════╝░

        users = getusers()[1]

        def UserListSelect(choice):
            UserNameResult.configure(text=choice)
            # BorrowResult
            if len(GetBorrowedBooks(choice))>0:
                BorrowResult.configure(text=", ".join(GetBorrowedBooks(choice)))
            else:
                BorrowedResult.configure(text="None")
            cursor.execute("SELECT admin FROM users WHERE username = ?", (choice,))
            result = cursor.fetchall()
            if result[0][0] == True:
                AdminResult.configure(text="Yes")
            else:
                AdminResult.configure(text="No")

        ###Left ListBox Element
        UserLabel = customtkinter.CTkLabel(text="Users", master=tabview.tab("users"))
        UserLabel.grid(row=0, column=0, padx=20)
        UserList = CTkListbox(command=UserListSelect, master=tabview.tab("users"))
        UserList.grid(row=1, column=0, rowspan=10, padx=20, sticky="w")
        for idx, i in enumerate(users):
            UserList.insert(idx, i)

        ###User Info Display
        UserName = customtkinter.CTkLabel(text="Username: ", master=tabview.tab("users"))
        UserName.grid(row=1, column=1, padx=(25, 10), sticky="e")
        UserNameResult = customtkinter.CTkLabel(text="", master=tabview.tab("users"))
        UserNameResult.grid(row=1, column=2, padx=(25, 10), sticky="w")
        Borrow = customtkinter.CTkLabel(text="Borrowed Books: ", master=tabview.tab("users"))
        Borrow.grid(row=2, column=1, padx=(25, 10), sticky="e")
        BorrowResult = customtkinter.CTkLabel(text="", master=tabview.tab("users"))
        BorrowResult.grid(row=2, column=2, padx=(25, 10), sticky="w")
        Admin = customtkinter.CTkLabel(text="Is Admin: ", master=tabview.tab("users"))
        Admin.grid(row=3, column=1, padx=(25, 10), sticky="e")
        AdminResult = customtkinter.CTkLabel(text="", master=tabview.tab("users"))
        AdminResult.grid(row=3, column=2, padx=(25, 10), sticky="w")

        def ResetPassword():
            ResetPasswordError.configure(text="")
            if ResetPasswordInput.get() != ResetConfirmPasswordInput.get():
                ResetPasswordError.configure(text="Passwords don't match")
                return
            elif ResetConfirmPasswordInput.get() == '' or ResetPasswordInput.get() == '':
                ResetPasswordError.configure(text="Passwords can't be empty")
                return
            elif not UserList.get():
                ResetPasswordError.configure(text="Please select a user")
                return
            cursor.execute("UPDATE users SET password = ? WHERE username = ?", (ResetPasswordInput.get(), UserList.get()))
            connection.commit()


        ResetLabel = customtkinter.CTkLabel(text="Reset Password", master=tabview.tab("users"))
        ResetLabel.grid(row=4, column=1, padx=10, pady=10)
        ResetPasswordInputLabel = customtkinter.CTkLabel(text="New Password: ", master=tabview.tab("users"))
        ResetPasswordInputLabel.grid(row=5, column=1, sticky="e")
        ResetPasswordInput = customtkinter.CTkEntry(master=tabview.tab("users"), placeholder_text="password")
        ResetPasswordInput.grid(row=5, column=2)
        ResetConfirmPasswordInputLabel = customtkinter.CTkLabel(text="Confirm Password: ", master=tabview.tab("users"))
        ResetConfirmPasswordInputLabel.grid(row=6, column=1, sticky="e")
        ResetConfirmPasswordInput = customtkinter.CTkEntry(master=tabview.tab("users"), placeholder_text="password")
        ResetConfirmPasswordInput.grid(row=6, column=2)
        ResetPassowrdButton = customtkinter.CTkButton(master=tabview.tab("users"), text="Reset Password", command=ResetPassword)
        ResetPassowrdButton.grid(row=7, column=2, sticky="e")
        ResetPasswordError = customtkinter.CTkLabel(master=tabview.tab("users"), text="", text_color="red")
        ResetPasswordError.grid(row=8, column=2, sticky="w")


        ###Removing a user
        def RemoveUser():
            cursor.execute("DELETE FROM users WHERE username = ?", (UserList.get(),))
            connection.commit()
            users = getusers()[1]
            UserNameResult.configure(text="")
            BorrowedResult.configure(text="")
            UserList.delete("all")
            for idx, i in enumerate(users):
                UserList.insert(idx, i)

        RemoveButton = customtkinter.CTkButton(master=tabview.tab("users"), text="Remove Selected User",
                                               command=RemoveUser, fg_color="red")
        RemoveButton.grid(row=11, column=0, padx=10, pady=10)

        def AddUser():
            if UserNameInput.get() == '' or PasswordInput.get() == '' or ConfirmPasswordInput == '':
                AddUserError.configure(text="Fields Cannot Be Empty")
                return
            AddUserError.configure(text="")
            if ConfirmPasswordInput.get() != PasswordInput.get():
                AddUserError.configure(text="Passwords Don't Match")
                return
            cursor.execute("SELECT * FROM users WHERE username = ?", (UserNameInput.get(),))
            result = cursor.fetchall()
            if result:
                AddUserError.configure(text="User Already Exists")
                return
            cursor.execute("SELECT max(id) FROM users")
            maximum = cursor.fetchall()
            try:
                if maximum[0][0]>=0:
                    max = maximum[0][0]
                else:
                    max = -1
            except:
                max = -1
            print(maximum)
            if IsAdmin.get() == 1:
                cursor.execute("INSERT INTO users VALUES (?, ?, ?, TRUE, '')",
                               (max + 1, UserNameInput.get(), PasswordInput.get()))
            else:
                cursor.execute("INSERT INTO users VALUES (?, ?, ?, FALSE, '')",
                               (max + 1, UserNameInput.get(), PasswordInput.get()))
            connection.commit()
            users = getusers()[1]
            for idx, i in enumerate(users):
                UserList.insert(idx, i)

        AddUserLabel = customtkinter.CTkLabel(text="Add User", master=tabview.tab("users"))
        AddUserLabel.grid(row=11, column=2)
        UserNameInputLabel = customtkinter.CTkLabel(text="Username: ", master=tabview.tab("users"))
        UserNameInputLabel.grid(row=12, column=1, sticky="e")
        UserNameInput = customtkinter.CTkEntry(master=tabview.tab("users"), placeholder_text="username")
        UserNameInput.grid(row=12, column=2)
        PasswordInputLabel = customtkinter.CTkLabel(text="Password: ", master=tabview.tab("users"))
        PasswordInputLabel.grid(row=13, column=1, sticky="e")
        PasswordInput = customtkinter.CTkEntry(master=tabview.tab("users"), placeholder_text="password")
        PasswordInput.grid(row=13, column=2)
        ConfirmPasswordInputLabel = customtkinter.CTkLabel(text="Confirm Password: ", master=tabview.tab("users"))
        ConfirmPasswordInputLabel.grid(row=14, column=1, sticky="e")
        ConfirmPasswordInput = customtkinter.CTkEntry(master=tabview.tab("users"), placeholder_text="password")
        ConfirmPasswordInput.grid(row=14, column=2)
        IsAdmin = customtkinter.CTkCheckBox(master=tabview.tab("users"), text="Admin")
        IsAdmin.grid(row=15, column=2)
        AddUserButton = customtkinter.CTkButton(master=tabview.tab("users"), text="Add User", command=AddUser)
        AddUserButton.grid(row=16, column=2, sticky="e")
        AddUserError = customtkinter.CTkLabel(master=tabview.tab("users"), text="", text_color="red")
        AddUserError.grid(row=17, column=2, sticky="w")





# ░█████╗░██╗░░░░░██╗███████╗███╗░░██╗████████╗
# ██╔══██╗██║░░░░░██║██╔════╝████╗░██║╚══██╔══╝
# ██║░░╚═╝██║░░░░░██║█████╗░░██╔██╗██║░░░██║░░░
# ██║░░██╗██║░░░░░██║██╔══╝░░██║╚████║░░░██║░░░
# ╚█████╔╝███████╗██║███████╗██║░╚███║░░░██║░░░
# ░╚════╝░╚══════╝╚═╝╚══════╝╚═╝░░╚══╝░░░╚═╝░░░

class ClientPanel(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("900x500")
        self.title("EZLib Client")
        def Refresh():
            for idx, i in enumerate(GetBorrowedBooks(username)):
                BorrowList.insert(idx, i)
        tabview = customtkinter.CTkTabview(master=self, command=Refresh)
        tabview.pack(fill = 'both', expand = 1)
        tabview.add("browse")
        tabview.add("manage")
        tabview.set("browse")
        books = getbooks()[1]



        # ██████╗░██████╗░░█████╗░░██╗░░░░░░░██╗░██████╗███████╗
        # ██╔══██╗██╔══██╗██╔══██╗░██║░░██╗░░██║██╔════╝██╔════╝
        # ██████╦╝██████╔╝██║░░██║░╚██╗████╗██╔╝╚█████╗░█████╗░░
        # ██╔══██╗██╔══██╗██║░░██║░░████╔═████║░░╚═══██╗██╔══╝░░
        # ██████╦╝██║░░██║╚█████╔╝░░╚██╔╝░╚██╔╝░██████╔╝███████╗
        # ╚═════╝░╚═╝░░╚═╝░╚════╝░░░░╚═╝░░░╚═╝░░╚═════╝░╚══════╝


        def BorrowBook():
            #update the book data
            cursor.execute("UPDATE books SET buser = ? WHERE name = ?", (userid, BookList.get()))
            connection.commit()
            cursor.execute("SELECT * FROM books WHERE name = ?", (BookList.get(),))
            result = cursor.fetchall()
            print(result)
            print(result[0][3])
            if result[0][3] == -1:
                AvailabilityResult.configure(text="Available")
                BorrowButton.grid(row=5, column=1, padx=10, pady=10, sticky="w")
                ReturnButton.grid_forget()
            elif result[0][3] == userid:
                AvailabilityResult.configure(text="Borrowed By Me")
                ReturnButton.grid(row=5, column=1, padx=10, pady=10, sticky="w")
                BorrowButton.grid_forget()
            else:
                AvailabilityResult.configure(text="Unavailable")
                BorrowButton.grid_forget()
                ReturnButton.grid_forget()


        def ReturnBook():
            #update the book data
            cursor.execute("UPDATE books SET buser = ? WHERE name = ?", (-1, BookList.get()))
            connection.commit()
            cursor.execute("SELECT * FROM books WHERE name = ?", (BookList.get(),))
            result = cursor.fetchall()
            print(userid)
            if result[0][3] == -1:
                AvailabilityResult.configure(text="Available")
                BorrowButton.grid(row=5, column=1, padx=10, pady=10, sticky="w")
                ReturnButton.grid_forget()
            elif result[0][3] == userid:
                AvailabilityResult.configure(text="Borrowed By Me")
                ReturnButton.grid(row=5, column=1, padx=10, pady=10, sticky="w")
                BorrowButton.grid_forget()
            else:
                AvailabilityResult.configure(text="Unavailable")
                BorrowButton.grid_forget()
                ReturnButton.grid_forget()

        def BookListSelect(choice):
            cursor.execute("SELECT * FROM books WHERE name = ?", (choice,))
            result=cursor.fetchall()
            BookNameResult.configure(text=result[0][1])
            AuthorNameResult.configure(text=result[0][2])
            ISBNResult.configure(text=result[0][4])
            cursor.execute("SELECT * FROM books WHERE name = ?", (choice,))
            result = cursor.fetchall()
            if result[0][3] == -1:
                AvailabilityResult.configure(text="Available")
                BorrowButton.grid(row=5, column=1, padx=10, pady=10, sticky="w")
                ReturnButton.grid_forget()
            elif result[0][3] == userid:
                AvailabilityResult.configure(text="Borrowed By Me")
                ReturnButton.grid(row=5, column=1, padx=10, pady=10, sticky="w")
                BorrowButton.grid_forget()
            else:
                AvailabilityResult.configure(text="Unavailable")
                BorrowButton.grid_forget()
                ReturnButton.grid_forget()


        ###Left ListBox Element
        BookLabel = customtkinter.CTkLabel(text="Books", master=tabview.tab("browse"))
        BookLabel.grid(row=0, column=0, padx=20)
        BookList = CTkListbox(command=BookListSelect, master=tabview.tab("browse"))
        BookList.grid(row=1, column=0, rowspan=10, padx=20, sticky="w")
        for idx, i in enumerate(books):
            BookList.insert(idx, i)


        ###Book Info Display
        BookName = customtkinter.CTkLabel(text="Title: ", master=tabview.tab("browse"))
        BookName.grid(row=1, column=1, padx=(25,10), sticky="e")
        BookNameResult = customtkinter.CTkLabel(text="", master=tabview.tab("browse"))
        BookNameResult.grid(row=1, column=2, padx=(25,10), sticky="w")
        AuthorName = customtkinter.CTkLabel(text="Author: ", master=tabview.tab("browse"))
        AuthorName.grid(row=2, column=1, padx=(25,10), sticky="e")
        AuthorNameResult = customtkinter.CTkLabel(text="", master=tabview.tab("browse"))
        AuthorNameResult.grid(row=2, column=2, padx=(25,10), sticky="w")
        ISBN = customtkinter.CTkLabel(text="ISBN Number: ", master=tabview.tab("browse"))
        ISBN.grid(row=3, column=1, padx=(25,10), sticky="e")
        ISBNResult = customtkinter.CTkLabel(text="", master=tabview.tab("browse"))
        ISBNResult.grid(row=3, column=2, padx=(25,10), sticky="w")
        Availability = customtkinter.CTkLabel(text="Availability: ", master=tabview.tab("browse"))
        Availability.grid(row=4, column=1, padx=(25,10), sticky="e")
        AvailabilityResult = customtkinter.CTkLabel(text="", master=tabview.tab("browse"))
        AvailabilityResult.grid(row=4, column=2, padx=(25, 10), sticky="w")
        BorrowButton = customtkinter.CTkButton(master=tabview.tab("browse"), command=BorrowBook, width=100, height=35, state="standard", corner_radius=16, text="Borrow", fg_color="green")
        # BorrowButton.grid(row=5, column=1, padx=10, pady=10, sticky="w")
        ReturnButton = customtkinter.CTkButton(master=tabview.tab("browse"), command=ReturnBook, width=100, height=35, state="standard", corner_radius=16, text="Return", fg_color="red")
        # ReturnButton.grid(row=5, column=1, padx=10, pady=10, sticky="w")


        # ███╗░░░███╗░█████╗░███╗░░██╗░█████╗░░██████╗░███████╗
        # ████╗░████║██╔══██╗████╗░██║██╔══██╗██╔════╝░██╔════╝
        # ██╔████╔██║███████║██╔██╗██║███████║██║░░██╗░█████╗░░
        # ██║╚██╔╝██║██╔══██║██║╚████║██╔══██║██║░░╚██╗██╔══╝░░
        # ██║░╚═╝░██║██║░░██║██║░╚███║██║░░██║╚██████╔╝███████╗
        # ╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝░╚═════╝░╚══════╝


        def BorrowListSelect(choice):
            cursor.execute("SELECT * FROM books WHERE name = ?", (choice,))
            result=cursor.fetchall()
            BorrowBookNameResult.configure(text=result[0][1])
            BorrowAuthorNameResult.configure(text=result[0][2])
            BorrowISBNResult.configure(text=result[0][4])


        ###Left ListBox Element
        BorrowLabel = customtkinter.CTkLabel(text="Books", master=tabview.tab("manage"))
        BorrowLabel.grid(row=0, column=0, padx=20)
        BorrowList = CTkListbox(command=BorrowListSelect, master=tabview.tab("manage"))
        BorrowList.grid(row=1, column=0, rowspan=10, padx=20, sticky="w")
        for idx, i in enumerate(GetBorrowedBooks(username)):
            BorrowList.insert(idx, i)

        BorrowBookName = customtkinter.CTkLabel(text="Title: ", master=tabview.tab("manage"))
        BorrowBookName.grid(row=1, column=1, padx=(25, 10), sticky="e")
        BorrowBookNameResult = customtkinter.CTkLabel(text="", master=tabview.tab("manage"))
        BorrowBookNameResult.grid(row=1, column=2, padx=(25, 10), sticky="w")
        BorrowAuthorName = customtkinter.CTkLabel(text="Author: ", master=tabview.tab("manage"))
        BorrowAuthorName.grid(row=2, column=1, padx=(25, 10), sticky="e")
        BorrowAuthorNameResult = customtkinter.CTkLabel(text="", master=tabview.tab("manage"))
        BorrowAuthorNameResult.grid(row=2, column=2, padx=(25, 10), sticky="w")
        BorrowISBN = customtkinter.CTkLabel(text="ISBN Number: ", master=tabview.tab("manage"))
        BorrowISBN.grid(row=3, column=1, padx=(25, 10), sticky="e")
        BorrowISBNResult = customtkinter.CTkLabel(text="", master=tabview.tab("manage"))
        BorrowISBNResult.grid(row=3, column=2, padx=(25, 10), sticky="w")

        def ReturnBorrow():
            cursor.execute("UPDATE books SET buser = ? WHERE name = ?", (-1, BorrowList.get()))
            connection.commit()
            BookNameResult.configure(text="")
            AuthorNameResult.configure(text="")
            ISBNResult.configure(text="")
            BorrowList.delete("all")
            for idx, i in enumerate(GetBorrowedBooks(username)):
                BorrowList.insert(idx, i)


        ReturnBut = customtkinter.CTkButton(master=tabview.tab("manage"), command=ReturnBorrow, width=100, height=35, state="standard", corner_radius=16, text="Return", fg_color="red")
        ReturnBut.grid(row=4, column=2, padx=(25, 10), sticky="w")



app = App()
app.mainloop()

connection.close()