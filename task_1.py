class ContactAlreadyExistError(Exception):
    pass


class ContactNotExistError(Exception):
    pass


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ContactAlreadyExistError:
            return "Contact with this name has already saved."
        except ContactNotExistError:
            return "This contact does not exist, please add it first."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter user name."

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, contacts):
    name, phone = args
    if name in contacts:
        raise ContactAlreadyExistError
    contacts.update({name: phone})
    return "Contact added."


@input_error
def change_contact(args, contacts):
    name, phone = args
    if not name in contacts:
        raise ContactNotExistError
    contacts.update({name: phone})
    return "Contact changed."


@input_error
def get_contact_phone(args, contacts):
    name = args[0]
    if not name in contacts:
        raise ContactNotExistError
    return contacts[name]


def get_all_contacts(contacts):
    result = ""
    for name in contacts:
        result += f"{name}: {contacts[name]}\n"
    return result[0:-1]


def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(get_contact_phone(args, contacts))
        elif command == "all":
            print(get_all_contacts(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
