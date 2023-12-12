from collections import UserDict


class PhoneAlreadyExistError(Exception):
    pass


class RecordAlreadyExistError(Exception):
    pass


class RecordNotExistError(Exception):
    pass


class PhoneNotExistError(Exception):
    pass


def handle_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PhoneAlreadyExistError:
            print("Такий телефон уже є в списку")
        except RecordAlreadyExistError:
            print("Запис з таким іменем вже створенний.")
        except RecordNotExistError:
            print("Такого запису не знайденно.")
        except PhoneNotExistError:
            print("Такого телефону немає в списку.")
        except KeyError:
            return "По такому ключу нічого не знайдено"

    return inner


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(self.validate(name))

    def validate(self, name):
        if len(name) < 2:
            raise ValueError("The name must be longer than 1 character.")
        return name


class Phone(Field):
    def __init__(self, phone):
        super().__init__(self.validate(phone))

    def validate(self, phone):
        if len(phone) < 10:
            raise ValueError("The phone must be longer than 10 character.")
        return phone


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    @handle_error
    def add_phone(self, phone):
        if self.find_phone(phone):
            raise PhoneAlreadyExistError
        self.phones.append(Phone(phone))

    @handle_error
    def remove_phone(self, phone):
        if not self.find_phone(phone):
            raise PhoneNotExistError
        self.phones = list(
            filter(lambda current_phone: current_phone.value != phone, self.phones)
        )

    @handle_error
    def edit_phone(self, old_phone, new_phone):
        if not self.find_phone(old_phone):
            raise PhoneNotExistError
        self.phones = list(
            map(
                lambda current_phone: current_phone
                if current_phone.value != old_phone
                else Phone(new_phone),
                self.phones,
            )
        )

    def find_phone(self, search_phone):
        result = list(filter(lambda phone: phone.value == search_phone, self.phones))
        return result[0] if len(result) else None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    @handle_error
    def add_record(self, record):
        if record.name.value in self.data:
            raise RecordAlreadyExistError
        self.data[record.name.value] = record

    @handle_error
    def find(self, name):
        return self.data[name]

    @handle_error
    def delete(self, name):
        del self.data[name]


# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
john_record.edit_phone("5555555555123", "123123123123123")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(f"record - {record}")

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")
print(john)

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")

# Видалення запису Jane
book.delete("Jane")
