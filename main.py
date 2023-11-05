from _collections_abc import Iterator
import re
from itertools import islice
from collections import UserDict
from datetime import date, timedelta


class Field():
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    ...


class Birthday(Field):
    def __init__(self, bd: str):
        self.__birthday = None
        self.birthday = bd

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, bd):
        if re.match(r"[0-9]{4}\-[0-9]{2}\-[0-9]{2}", bd):
            bd_date = list(map(int, bd.split("-")))
            birthday = date(*bd_date)
            self.__birthday = birthday
        else:
            raise ValueError("Wrong date format. Use YYYY-MM-DD")


class Phone(Field):
    def __init__(self, phone: str):
        self.__phone = None
        self.phone = phone

    @property
    def phone(self):
        return self.__phone
    
    @phone.setter
    def phone(self, phone: str):
        if re.match(r"[0-9]{10}", phone):
            self.__phone = phone
        else:
            raise ValueError("Wrong phone format. It must contains 10 digits")


class Record:
    def __init__(self, name, phone: str = None, birthday_date: str = None):
        self.name = Name(name)
        self.phones: list(Phone) = []
        self.birthday = None
        if phone:
            self.phones.append(Phone(phone))
        if birthday_date:
            self.birthday = Birthday(birthday_date)

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))
        return f"Added phone {phone} to contact {self.name}"

    def add_birthday(self, bd_date: str):
        self.birthday = Birthday(bd_date)

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
            return f"Removed phone {phone} from contact {self.name}."
        else:
            raise ValueError

    def edit_phone(self, phone: str, new_phone: str) -> str:
        edit_check = False
        for i in range(len(self.phones)):
            if self.phones[i].value == phone:
                edit_check = True
                self.phones[i] = Phone(new_phone)
                return f"Changed phone {phone} for contact {self.name} to {new_phone}"
        if not edit_check:
            raise ValueError

    def days_to_birthday(self) -> timedelta or str:
        if self.birthday:
            now_date = date.today()
            future_bd = self.birthday.birthday
            future_bd = future_bd.replace(year=now_date.year)
            if future_bd.month > now_date.month:
                return future_bd - now_date
            else:
                future_bd = future_bd.replace(year=future_bd.year+1)
                return future_bd - now_date
        else:
            return f"No birthday set"

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        return "Contact name: {}, birthday: {}, phones: {}".format(
            self.name,
            self.birthday,
            phones
        )


class AddressBook(UserDict):
    def __init__(self, data=None):
        super().__init__(data)
        self.counter = 0

    def add_record(self, rec: Record):
        if rec.name.value not in self.data.keys():
            self.data[rec.name.value] = rec
        else:
            raise ValueError

    def find(self, name: str):
        if name in self.data.keys():
            return self.data.get(name)
        else:
            return None

    def delete(self, name: str):
        if name in self.data.keys():
            return self.data.pop(name)

    def iterator(self, quantity: int):
        values = list(map(str, islice(self.data.values(), None)))
        while self.counter < len(values):
            yield values[self.counter:self.counter+quantity]
            self.counter += quantity


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
    bill_record = Record("Bill", "7234592343")
    dow_record = Record("Dow")
    book.add_record(bill_record)
    book.add_record(dow_record)
    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    for b in book.iterator(4):
        print(b)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    print(john)
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Додавання днів народження і вивід днів до нього
    john.add_birthday("1993-12-01")
    print(john.days_to_birthday())
    jane_record.add_birthday("2004-09-11")
    print(jane_record.days_to_birthday())
    print(dow_record.days_to_birthday())

    # Видалення запису Jane
    book.delete("Jane")
