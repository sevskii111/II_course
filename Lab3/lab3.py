from abc import ABC
from datetime import datetime

class Virus(ABC):
    def __init__(self, name, year, os, vtype):
        self.__name = name
        self.os = os
        self.year = year
        self.vtype = vtype

    @property
    def name(self):
        return self.__name

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, year):
        OS_YEARS = {
            "Windows": 1985,
            "OSX": 2001,
            "Linux": 1991
        }
        first_year = OS_YEARS[self.os]
        curr_year = datetime.now().year
        if year < first_year or year > curr_year:
            raise ValueError(
                f"Year must be in range {first_year}<=year<={curr_year}")
        self.__year = year

    @property
    def os(self):
        return self.__os

    @os.setter
    def os(self, os):
        OS = ['Windows', 'Linux', 'OSX']
        if os not in OS:
            raise ValueError(f"Only viruses for {', '.join(OS)} are supported")
        self.__os = os

    @property
    def vtype(self):
        return self.__vtype

    @vtype.setter
    def vtype(self, vtype):
        self.__vtype = vtype

    def deserialize(virus_str):
        str_parts = virus_str.split(',')
        if str_parts[0] == 'L':
            return LocalVirus(str_parts[1], int(str_parts[2]), str_parts[3], str_parts[4], bool(str_parts[5]), bool(str_parts[6]))
        else:
            return RemoteVirus(str_parts[1], int(str_parts[2]), str_parts[3], str_parts[4], str_parts[5])

def serialize_bool(b):
    return '1' if b else ""

class LocalVirus(Virus):
    def __str__(self):
        return 'L,' + ','.join([self.name, str(self.year), self.os, self.vtype, serialize_bool(self.is_attached), serialize_bool(self.easy_detect)])

    def __init__(self, name, year, OS, vtype, is_attached, easy_detect):
        super().__init__(name, year, OS, vtype)
        self.is_attached = is_attached
        self.easy_detect = easy_detect

    @property
    def is_attached(self):
        return self.__is_attached

    @is_attached.setter
    def is_attached(self, is_attached):
        self.__is_attached = is_attached

    @property
    def easy_detect(self):
        return self.__easy_detect

    @easy_detect.setter
    def easy_detect(self, easy_detect):
        self.__easy_detect = easy_detect

class RemoteVirus(Virus):
    def __str__(self):
        return 'R,' + ','.join([self.name, str(self.year), self.os, self.vtype, self.attack_vector])

    def __init__(self, name, year, OS, vtype, attack_vector):
        super().__init__(name, year, OS, vtype)
        self.attack_vector = attack_vector

    @property
    def attack_vector(self):
        return self.__attack_vector

    @attack_vector.setter
    def attack_vector(self, attack_vector):
        ATTACK_VECTORS = ['Network', 'Web']
        if attack_vector not in ATTACK_VECTORS:
            raise ValueError(
                f"Only {', '.join(ATTACK_VECTORS)} attack vectors are supported")
        self.__attack_vector = attack_vector

def parse_db():
    db = []
    with open('db.txt') as db_file:
        for line in db_file.readlines():
            if len(line) > 0:
                db.append(Virus.deserialize(line.strip("\r\n ")))
    return db

def save_db():
    with open('db.txt', 'w') as db_file:
        db_file.write('\n'.join(map(str, db)))

def add_entry(e):
    if find_entry(e.name) is None:
        db.append(e)
        save_db()
    else:
        raise ValueError(f"Entry with same name is in DB already")

def find_entry(name):
    for e in db:
        if e.name == name:
            return e
    return None

def remove_entry(name):
    e = find_entry(name)
    if e is not None:
        db.remove(e)
        save_db()
    else:
        raise ValueError(f"Entry with this name not found in DB")

db = parse_db()

while True:
    command = None
    while command not in ['find', 'add', 'remove']:
        command = input("Please select action(find, add, remove): ")
    if command == 'find':
        e = find_entry(input('name: '))
        if e is not None:
            print(f"year: {e.year}\nOS: {e.os}\nvirus_type: {e.vtype}")
            if isinstance(e, LocalVirus):
                print(
                    f"is_attached: {e.is_attached}\neasy_detect: {e.easy_detect}")
            else:
                print(f"attack_vector: {e.attack_vector}")
        else:
            print(f"Entry with this name not found in DB")
    elif command == 'add':
        vclass = None
        while vclass not in ['local', 'remote']:
            vclass = input("virus_type(local, remote): ").lower()
        name = input('name: ')
        year = input('year: ')
        OS = input('OS: ')
        vtype = input('virus type: ')
        if vclass == 'local':
            is_attached = input('is_attached(y/n): ') == 'y'
            easy_detect = input('easy_detect(y/n): ') == 'y'
            try:
                add_entry(LocalVirus(name, int(year), OS,
                                     vtype, is_attached, easy_detect))
            except ValueError as e:
                print(e)
        else:
            attack_vector = input('attack vector: ')
            try:
                add_entry(RemoteVirus(name, int(year),
                                      OS, vtype, attack_vector))
            except ValueError as e:
                print(e)
    else:
        try:
            remove_entry(input('name: '))
        except ValueError as e:
            print(e)

