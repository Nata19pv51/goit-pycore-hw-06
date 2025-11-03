from collections import UserDict
import re


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
        
    def phone_validation(self, phone):
        pattern = r'\d{10}'
        match = re.fullmatch(pattern, phone)
        if match:
            return True
        return False


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        try:        
            p = Phone(phone)         
            self.phones.append(p)
        except(ValueError):
            return False
        return True

    def remove_phone(self, phone):
        for one_phone in self.phones:
            if one_phone == phone:
                self.phones.remove(one_phone)
                return "The phone was removed"
            return "The phone doesn't exist"

    def edit_phone(self, old_phone, new_phone):
        o_phone = Phone(old_phone)
        n_phone = Phone(new_phone)

        for phone in self.phones:
            if phone.value == o_phone.value:
                phone.value = n_phone.value
                return True
        return False

    def find_phone(self, phone):
        phone_obj = Phone(phone)

        for p in self.phones:
            if p.value == phone_obj.value:
                return p
            
        return None

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
            print("!!!!!!!!!!!!!!!!!!!!!!!")
            return True
        
        print("********************")
        return False


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

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

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")


    for name, record in book.data.items():
        print(record)