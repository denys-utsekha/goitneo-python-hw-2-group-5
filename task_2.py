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
            print("Such a phone already exists")
        except PhoneNotExistError:
            print("There is no such phone.")
        except RecordAlreadyExistError:
            print("A record with this name already exists.")
        except RecordNotExistError:
            print("No such record found.")
        except KeyError:
            print("Nothing was found for this key.")

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
        if len(phone) != 10:
            raise ValueError("The phone must be 10 character.")
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
