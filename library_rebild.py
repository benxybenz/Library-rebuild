import json 

class Book:
    def __init__(self,book_id,title,author,status):
        self.book_id = book_id
        self.title = title 
        self.author = author
        self.status = status

    def display_book(self):
        print("=================================")
        print(f"Book id : {self.book_id}")
        print(f"Title : {self.title}")
        print(f"Author : {self.author}")
        print(f"Status : {self.status}")
        print("===============================")

   
        

class BorrowReccord:
    book_count = 0
    def __init__(self, list_of_all_books = None, my_books_list = None ):

        if list_of_all_books == None:
            self.list_of_all_books = []
        else:
            self.list_of_all_books = list_of_all_books

        if my_books_list == None:
            self.my_books_list = []
        else:
            self.my_books_list = my_books_list


    def from_python_to_json(self):
        temp_list = []
        for book in self.list_of_all_books:
            json_data = {"Book id": book.book_id,
                                 "Title" :book.title,
                                 "Author":book.author,
                                 "Status":book.status,
                    }
            temp_list.append(json_data)
        return temp_list
            
        
    def from_json_to_python(self,temp_list):
        new_list = []
        for book in temp_list:
            one_book = Book(book["Book id"],book["Title"],book["Author"],book["Status"])
            new_list.append(one_book)
        return new_list

    def unique_id_generator(self):
        new_count = self.book_count+1
        self.book_count = new_count
        return new_count
        
    

    def id_count_updater(self):
        pass 


    def id_validator(self,id):
        while True:
            try:
                clean_id = int(id)
                if  clean_id > 0  :
                    return int(id)
                elif clean_id < 0 :
                    id = input("Enter the id again = ")
            except ValueError:
                print("Invalid syntax ")
                id = input("Enter the id again = ")


    def title_duper_validator(self,title):
        while True:
            has_no_duplicate = True 
            for book in self.my_books_list:
                if book.title == title:
                    has_no_duplicate = False 
            if  has_no_duplicate:
                return title 
            elif not has_no_duplicate:
                print("Book has already been borrowed by you ")
                title = input("Enter the title again = ").capitalize().strip()
                title = self.title_validator(title)



    def title_validator(self,title):
        while True:
            clean_title = title.replace(" ","")
            if len(clean_title)>=6 and clean_title.isalpha() == True :
                return title
            else:
                print("Invalid title ")
                title = input("Enter title again = ").capitalize().strip()

    def author_validator(self,author):
        while True:
            clean_author = author.replace(" ","")
            if len(clean_author) >= 3 and clean_author.isalpha() == True:
                return author
            else:
                print("Invalid author name ")
                author = input("Enter the author name again = ").capitalize().strip()

    def borrow_a_book(self):
        id = self.unique_id_generator()
        title = input("Enter the title of the book you want to borrow = ").capitalize().strip()
        title = self.title_validator(title)
        title = self.title_duper_validator(title)
        author = input("Enter the author of the book you want to borrow = ").capitalize().strip()
        author = self.author_validator(author)
        status = "Burrowed"
        one_book = Book(id,title,author,status)
        self.list_of_all_books.append(one_book)
        self.my_books_list.append(one_book)
        one_book.display_book()
        print("Book has been sucesfully borrowed ")

        
    def my_books(self):
        if len(self.my_books_list) != 0:
            print("             MY BOOKS            ")
            for books in self.my_books_list:
                books.display_book()
        elif len(self.my_books_list) == 0 :
            print("No books have been borrowed by you ! ")

        
    def is_book_in_list_validator(self,id):
        while True:
            does_exist = False 
            for book in self.my_books_list:
                if book.book_id == id:
                    does_exist = True
            if does_exist:
                return id
            elif not does_exist:
                print("No id of such book has been found")
                id = input("Enter the id again = ")
                id = self.id_validator(id)

    def return_a_book(self):
        id = input("Enter the id of the book that you want to return = ")
        id = self.id_validator(id)
        id = self.is_book_in_list_validator(id)
        for book in self.my_books_list:
            if book.book_id == id:
                book.status = "Avilable"
                self.my_books_list.remove(book)
                print("Book has been sucesfully returned!")
                
        
    

#---------------- Front end -----------------#
manager = BorrowReccord()

menu_list = ["1) Borrow", "2) Return ","3) View my books ","4) Exit"]

def menu():
    print("===========  MENU =============")
    for menu in menu_list:
        print(menu)
    print("==============================")


def choice_identifier(choice):
    if choice in ["1","Borrow"]:
        manager.borrow_a_book()
    elif choice in ["2", "Return"]:
        manager.return_a_book()
    elif choice in ["3", "view"]:
        manager.my_books()


def choice_validator(choice):
    while True:
        if choice in ["1","2","3","4","Borrow","Return","View","Exit"]:
            return choice
        else:
            print("Choose the correct option !")
            choice = input("Enter your choice again = ").capitalize().strip()
    

def read_from_file():
    try:
        with open ("library.json","r") as f:
            data = json.load(f)
            book_object = manager.from_json_to_python(data)
            return book_object
    except FileNotFoundError:
        return "No such file was found "



def write_in_file():
    print("Write in file is being called")
    data = manager.from_python_to_json()
    print("Data to be written:", data)
    with open("library.json", "w") as f:
        json.dump(data, f)
    print("File writing completed")

read_from_file()
while True :
    menu()
    choice = input("Enter your choice = ").capitalize().strip()
    choice = choice_validator(choice)
    choice_identifier(choice)
    if choice =="4" or choice =="Exit":
        break 
write_in_file()
print("Thankyou have a great day ahead! ")
