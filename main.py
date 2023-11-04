from collections import UserDict


class Field():
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    ...


class Phone(Field):
    def __init__(self, value: str):
        if all([len(value) == 10, value.isdecimal()]):
            super().__init__(value)
        else:
            raise ValueError


class Record:
    def __init__(self, name, phone=None):
        self.name = Name(name)
        self.phones: list(Phone) = []
        if phone:
            self.phones.append(Phone(phone))

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))
        return f"Added phone {phone} to contact {self.name}"

    def find_phone(self, phone: str):
        result = None
        for p in self.phones:
            if phone == p.value:
                result = p
        return result

    def remove_phone(self, phone: str):
        search = self.find_phone(phone)
        if search in self.phones:
            self.phones.remove(search)
        else:
            raise ValueError

    def edit_phone(self, phone: str, new_phone: str):
        edit_check = False
        for i in range(len(self.phones)):
            if self.phones[i].value == phone:
                edit_check = True
                self.phones[i] = Phone(new_phone)
        if not edit_check:
            raise ValueError

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):

    def add_record(self, rec: Record):
        if rec.name.value not in self.data.keys():
            self.data[rec.name.value] = rec
        else:
            raise ValueError

    def find(self, name: str):
        if name in self.data.keys():
            return self.data[name]
        else:
            return None

    def delete(self, name: str):
        if name in self.data.keys():
            return self.data.pop(name)


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
    print(john)
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
