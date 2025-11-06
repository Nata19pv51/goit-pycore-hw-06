from collections import UserDict
import re


def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res
        except ValueError:
            print("Wrong phone format")
        
    return wrapper


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if self.phone_validation(value):
            super().__init__(value)
        else:
            raise ValueError
        
    def phone_validation(self, phone: str):
        match = re.fullmatch(r'\d{10}', phone)
        if match:
            return True
        return False


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    @error_handler
    def add_phone(self, phone):      
        p = Phone(phone)         
        self.phones.append(p)
        return self.phones
    
    def check_phone_entry(self, phone):
        for index, p in enumerate(self.phones):
            if p.value == phone:
                return index
        return -1
    
    def find_phone(self, phone):
        index = self.check_phone_entry(phone)
        if index >= 0:
            return self.phones[index]
    
    def remove_phone(self, phone):
        index = self.check_phone_entry(phone)
        if index >= 0:
            self.phones.remove(self.phones[index])
            return True

    @error_handler
    def edit_phone(self, old_phone, new_phone):
        index = self.check_phone_entry(old_phone)
        if index >= 0:
            new_phone_obj = Phone(new_phone)
            self.phones[index] = new_phone_obj
            return self.phones

    def __str__(self):
        return f"Contact name: {self.name.value} \
            phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        # Find this name and return record of this contact:
        if name in self.data:
            return self.data[name]
        return None

    def delete(self, name):
        
        if name in self.data:
            self.data.pop(name)
            return self.data

        return None


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    booll = john_record.add_phone("5555555555")
    john_record.add_phone("3333333333")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555
    
    john.remove_phone("3333333333")

    print(john) 
    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")

    for name, record in book.data.items():
        print(record)