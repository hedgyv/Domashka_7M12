# Завдання
# У цьому домашньому завданні ми:

# Додамо поле для дня народження Birthday. Це поле не обов'язкове, але може бути тільки одне.
# Додамо функціонал роботи з Birthday у клас Record, а саме функцію days_to_birthday, яка повертає кількість днів до наступного дня народження.
# Додамо функціонал перевірки на правильність наведених значень для полів Phone, Birthday.
# Додамо пагінацію (посторінковий висновок) для AddressBook для ситуацій, коли книга дуже велика і треба показати вміст частинами, а не все одразу. Реалізуємо це через створення ітератора за записами.
# Критерії прийому:
# AddressBook реалізує метод iterator, який повертає генератор за записами AddressBook і за одну ітерацію повертає уявлення для N записів.
# Клас Record приймає ще один додатковий (опціональний) аргумент класу Birthday
# Клас Record реалізує метод days_to_birthday, який повертає кількість днів до 
#наступного дня народження контакту, якщо день народження заданий. (новая ф-ия карирования?)
# setter та getter логіку для атрибутів value спадкоємців Field. ЭТО+
# Перевірку на коректність веденого номера телефону setter для value класу Phone. ЭТО+
# Перевірку на коректність веденого дня народження setter для value класу Birthday. сопоставить как в Phone(Field)

from collections import UserDict
from datetime import datetime
import pickle


#C:\Users\Yaroslav\OneDrive\Рабочий стол\SavedAddrBook

class AddressBook(UserDict):

    def add_record(self, record):
        
        self.data[record.name.value] = record
        print(f'checking {record.name.value}')
        print(f'checking {self.data[record.name.value]}')
        # print(len(self.data))
        
    # def __next__(self):
    #     if len(self.data) > 1:   
    #         self.current_value += 1        
    #         return self.current_value
    #     raise StopIteration 

    def iterator(self, counts):
        count = 0
        result = ""
        for name in self.data:
            if count < int(counts):
                count += 1
                result += str(self.data[name]) + "\n"
        return result
    
    def find(self, record, name):
        #print(len(self.data))
        if record.name.value == name:
            print(len(self.data))
            return self.data[record.name.value]  

    def delete(self, record):
        pass

   

class AddressBookSavedOnDisk:
    def __init__(self, filename: str, adr_book: AddressBook = None):
        self.filename = filename
        self.adr_book = adr_book
        if adr_book is None:
            adr_book = []
        
        
    def save_to_file(self):
        
        with open(self.filename, "wb") as fh:
            # print(type(self))
            #print(self.adr_book.data.values())
            # print(self)
            # print(self.adr_book)
            for record in self.adr_book.data.values():
                pickle.dump(record, fh)

            
    def read_from_file(self, adr_book):
        with open(self.filename, "rb") as fh:

            while True:
                try:
                    unpacked = pickle.load(fh)
                    print(unpacked)
                    adr_book.add_record(unpacked)
                except EOFError:
                    break
           
class CustomIterator:
    def __iter__(self):
        return AddressBook()

class Record:
    def __init__(self, name, birthday=None):
        self.name = name
        self.phones = []
        
    def add_phone(self, phone):
        self.phones.append(phone.number)
        

    def edit_phone(self, phone_old, phone_new): 
        index = self.phones.index(phone_old)
        self.phones[index] = phone_new
    

    def remove_phone(self, phone):
        self.phones.remove(phone)
    
    def find_phone(self, name, phone):
        pass
        #13task

    def days_to_birthday(self, birthday):
        current_date = datetime.now()
        next_birthday_year = current_date.year
        if current_date.month > int(birthday.month):
            next_birthday_year += 1
        next_birthday = datetime(year=next_birthday_year, month=int(birthday.month), day=int(birthday.day))
        days_left = (next_birthday - current_date).days
        return days_left
    
    #12
    def search_info(self, info):
        if (info in str(self.name) or
            any(info in str(phone) for phone in self.phones) or
            (info in str(self.birthday))):
            return True
        else:
            return False
    
    def __str__(self):
        return f"Name: {self.name.value}, Phones: {', '.join(str(phone) for phone in self.phones)}"


class Field:
    def __init__(self, value = None):
        self._value = value
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, new_value):
        if self.is_valid(new_value):
            self._value = new_value
        else:
            raise ValueError("Invalid field value")
    def is_valid(self, value):
        return bool(value.strip())

class Name(Field):

    def __init__(self, value):
        self.value = value
        #print(self.value)

    def is_valid(self, value):
        return value is not None and value.isalpha() and value.strip()
    
    def __str__(self):
        return self.value

class Phone(Field):
    def __init__(self, number):
        self.number = number
        
    def is_valid(self, value):
        return value is not None and len(value) == 10
    
    def __str__(self):
        return self.number
    
class Birthday(Field):
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    def is_valid(self, value):
        return bool(datetime.strptime(value, '%d.%m.%Y'))
    
    def __str__(self):
        return ".".join((self.day, self.month, self.year))
# новая функция карирования с командой др, которая вызывает функцию записи дня рождения и та в свою очередь 
#вызывает days_to_birthday в классе Record?


#phone_book = {} #We use adr_book instance of AdressBook class instead

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Error: Contact not found."
        except ValueError:
            return "Error: Invalid input. Please enter name and phone number."
        except IndexError:
            return "Error: You don't have any contacts yet."
    return inner

    
@input_error
def add_contact(adr_book, name, phone):
    name_u = Name(name)
    phone_u = Phone(phone)
    

    if name_u.is_valid(name) and phone_u.is_valid(phone):
        if name in adr_book.data:
            existing_record = adr_book.data[name]
            existing_record.add_phone(phone_u)
        else:
            record = Record(name_u)
            
            record.add_phone(phone_u)
            adr_book.add_record(record)
            
            
            print(adr_book.data[name])
    
        return f"Contact {name} with phone {phone} has been added."
    raise ValueError

def search_information(adr_book, inform):
    res = "Contacts:\n"
    for name in adr_book.data:
        ex_record  = adr_book.data[name]
        if ex_record.search_info(inform):
            res += str(ex_record) + '\n'
    return res


def save_on_disc(adr_book):

    
    text_file = 'C://Users/Yaroslav/OneDrive/Рабочий стол/SavedAddrBook/data_written.bin'
    
    adr_book_to_save = AddressBookSavedOnDisk(text_file, adr_book)
    adr_book_to_save.save_to_file()
    # read = adr_book_to_save.read_from_file()
    # return read


def read_from_disc(adr_book):

    text_file = 'C://Users/Yaroslav/OneDrive/Рабочий стол/SavedAddrBook/data_written.bin'
    adr_book_to_save = AddressBookSavedOnDisk(text_file)
    print(adr_book_to_save.read_from_file(adr_book))




@input_error
def find_contact(adr_book, name):

    name_u = Name(name)
    if name not in adr_book.data:
        raise KeyError
    #existing_record = adr_book.data[name]
    record = Record(name_u)
    existing_record = adr_book.find(record, name)
    phone_numbers = ', '.join(str(phone) for phone in existing_record.phones)
    result = f"Phone numbers for {name}: {phone_numbers}"
    return result


@input_error
def change_contact(adr_book, name, phone_old, phone_new ):
    phone_u_new = Phone(phone_new)
    if name not in adr_book.data:
        raise KeyError
    existing_record = adr_book.data[name]
    if phone_u_new.is_valid(phone_new):
        for num in existing_record.phones:
            if str(num) == phone_old:
                existing_record.edit_phone(num, phone_u_new)
                return f"Phone number for {name} has been changed to {phone_new}."
    raise ValueError
        
@input_error
def delete_contact(adr_book, name, phone):
    if name not in adr_book.data:
        raise KeyError
    existing_record = adr_book.data[name]
    for num in existing_record.phones:
        if str(num) == phone:
            existing_record.remove_phone(num)
            return f"Phone number {phone} has been deleted from {name}."

@input_error
def show_contacts(adr_book):
    result = "Contacts:\n"
    for record in adr_book.data.values():
        result += str(record) + "\n"
        
    return result




@input_error
def add_birthday(adr_book, name, birthday):
    the_name = Name(name)
    split_birthday_input = birthday.split('.')
    the_birthday = Birthday(year=split_birthday_input[2], month=split_birthday_input[1], day=split_birthday_input[0])
    data_now = datetime.now()
    if the_name.is_valid(name) and the_birthday.is_valid(birthday) and int(the_birthday.year) <= data_now.year :
        if name in adr_book.data:
            existing_record = adr_book.data[name]
            existing_record.birthday = (the_birthday)
        else:
            new_record = Record(the_name, birthday=the_birthday)
            adr_book.add_record(new_record)
        return f"Contact '{name}' with birthday '{birthday}' has been added."
    raise ValueError

@input_error
def days_left(adr_book, name):
    if name not in adr_book.data:
        raise KeyError
    existing_record = adr_book.data[name]
    the_birthday = existing_record.birthday
    if the_birthday is None:
        raise KeyError
    return existing_record.days_to_birthday(the_birthday)

@input_error
def l_iterator(adr_book, counts):
    if len(adr_book) < int(counts):
        raise ValueError
    print("Contacts:")
    return adr_book.iterator(counts)

   
def handle_requirement(req):
    split_command = ''
    for char in req:
        if char != ' ':
            split_command += char.lower()
        else:
            break
    return split_command

def split_req(req):
    return req.split()


def main():
    adr_book = AddressBook()
    #c = CustomIterator()
    
    

    def hello_func():
        print("How can I help you? \n")

    def add_func():
        if len(do_requirement_parts) < 3:
            print("Error: Tap an existed name and new phone")
        else:
            print(add_contact(adr_book, do_requirement_parts[1], do_requirement_parts[2]))
    
    def change_func():
        if len(do_requirement_parts) < 4:
            print("Error: Tap an existed name and new phone")
        else:
            print(change_contact(adr_book, do_requirement_parts[1], do_requirement_parts[2], do_requirement_parts[3]))

    def delete_func():
        if len(do_requirement_parts) < 3:
            print("Error: Tap an existed name and new phone")
        else:
            print(delete_contact(adr_book, do_requirement_parts[1], do_requirement_parts[2]))

    def phone_func():
        if len(do_requirement_parts) < 2:
            print("Error: Tap an existed name")
        else:
            print(find_contact(adr_book, do_requirement_parts[1]))
    
    def show_all_func():
        print(show_contacts(adr_book))
    
    def saving_func():
        print(save_on_disc(adr_book))
    
    def reader_func():
        print(read_from_disc(adr_book))

    def birth_func():
        print(add_birthday(adr_book, do_requirement_parts[1], do_requirement_parts[2]))

    def days_left_func():
        print(days_left(adr_book, do_requirement_parts[1]))

    def iterator_func():
        print(l_iterator(adr_book, do_requirement_parts[1]))
    
    def search_func():
        print(search_information(adr_book, do_requirement_parts[1]))


    while True:
        do_requirement = input(f'Write your command: ')

        do_requirement_parts = split_req(do_requirement)

        split_command = handle_requirement(do_requirement)
        
        all_commands = {
            'hello': hello_func,
            'add': add_func,
            'change': change_func,
            'delete': delete_func,
            'phone': phone_func,
            'show all': show_all_func,
            'birthday' : birth_func,
            'days_left': days_left_func,
            'iteration': iterator_func,
            'saveondisk' : saving_func,
            'readfromdisk' : reader_func,
            'searchinfo' : search_func,
            'good bye': lambda: print("Good bye!"),
            'close': lambda: print("Good bye!"),
            'exit': lambda: print("Good bye!"),
            
            
        }


        if do_requirement in all_commands:
            all_commands[do_requirement]()
            if do_requirement.lower() in ('good bye', 'close', 'exit'):
                break
        
        elif split_command in all_commands:
            all_commands[split_command]()


        else:
            print("Use command only: 'hello', 'add', 'change', 'phone', 'show all', 'good bye', 'close', or 'exit'")


if __name__ == '__main__':
    main()







    
        


