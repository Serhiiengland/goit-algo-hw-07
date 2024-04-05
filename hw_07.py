from collections import UserDict
from datetime import datetime

def input_error(func): #декоратор для обробки помилок у функціях
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return str(e)
    return wrapper

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field): #перевизначення конструктора для перевірки валідності номеру телефону
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be a 10-digit number.")
        super().__init__(value)

class Birthday(Field): #для зберігання дати народження
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name) #встановлюємо ім*я контакту
        self.phones = []  #створюєм порожній список телефонів
        self.birthday = None

    def add_phone(self, phone):#додаємо телефон до списку
        self.phones.append(Phone(phone))

    def remove_phone(self, phone): #видаляєм номера телефону зі списку ном.
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone): #редагування, замінюємо старий номер на новиц
        for i, phone in enumerate(self.phones):
            if str(phone) == old_phone:
                self.phones[i] = Phone(new_phone)

    def find_phone(self, phone): #шукаємо телефон за знчанням
        for p in self.phones:
            if str(p) == phone:
                return p

    def add_birthday(self, birthday):   #додаємо дати народження
        self.birthday = Birthday(birthday)

    def __str__(self): #перевизначення методу для рядкового представлення об*єку
        phones_str = '; '.join(str(p) for p in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name}, phones: {phones_str}{birthday_str}"

class AddressBook(UserDict): #клас адресної книги
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):   #отримання списку майбутніх днів народження
        today = datetime.now()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y")
                if today.month == birthday_date.month and today.day <= birthday_date.day <= today.day + 7:
                    upcoming_birthdays.append(f"{record.name}'s birthday on {birthday_date.strftime('%d.%m.%Y')}")
        return upcoming_birthdays

@input_error
def add_contact(args, book: AddressBook): #додавання контакту з можливістю декількох номерів телефонів
    name, *phones = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    for phone in phones:
        record.add_phone(phone)
    return message

@input_error 
def change_phone(args, book): #зміна номера телефона
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return f"Phone number updated for {name}."
    return "Contact not found."

@input_error
def show_phone(args, book): #виведення номерів телефонів контакту
    name = args[0]
    record = book.find(name)
    if record:
        return f"{name}'s phone numbers: {', '.join(str(p) for p in record.phones)}."
    return "Contact not found."

@input_error
def show_all(book): #виводемо всіх контактів
    if book:
        return "\n".join(str(record) for record in book.values())
    return "Address book is empty."

@input_error
def add_birthday(args, book): #додаємо дати народження
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}."
    return "Contact not found."

@input_error
def show_birthday(args, book): #виводимо дати народження контакт
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday: {record.birthday}."
    return "Birthday not found."

@input_error
def birthdays(args, book): #виводемо майбутні дні народження
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join(upcoming_birthdays)
    return "No upcoming birthdays."

def main(): # головна функція програми
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = user_input.split()

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_phone(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
