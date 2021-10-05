import sys  # nopep8
sys.path.append('tables')  # nopep8

from project_config import *
from dbconnection import *
from people_table import *
from phones_table import *
from constants import *


class Main:

    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        DbTable.dbconn = self.connection
        return

    def db_init(self):
        PeopleTable().create()
        PhonesTable().create()
        return

    def db_insert_somethings(self):
        pt = PeopleTable()
        pht = PhonesTable()
        pt.insert_one(["Test", "Test", "Test"])
        pt.insert_one(["Test2", "Test2", "Test2"])
        pt.insert_one(["Test3", "Test3", "Test3"])
        pht.insert_one([1, "123"])
        pht.insert_one([2, "123"])
        pht.insert_one([3, "123"])

    def db_drop(self):
        pht = PhonesTable()
        pt = PeopleTable()
        pht.drop()
        pt.drop()
        return

    def show_main_menu(self):
        menu = main_menu
        print(menu)
        return

    def read_next_step(self):
        return input("=> ").strip()

    def after_main_menu(self, next_step):
        if next_step == "2":
            self.db_drop()
            self.db_init()
            self.db_insert_somethings()
            print("Таблицы созданы заново!")
            return "0"
        elif next_step != "1" and next_step != "9":
            print("Выбрано неверное число! Повторите ввод!")
            return "0"
        else:
            return next_step

    def show_people(self):
        self.person_id = -1
        menu = """Просмотр списка людей!
№\tФамилия\tИмя\tОтчество"""
        print(menu)
        lst = PeopleTable().all()
        for i in lst:
            print(str(i[0]) + "\t" + str(i[1]) +
                  "\t" + str(i[2]) + "\t" + str(i[3]))
        menu = people_menu
        print(menu)
        return

    def after_show_people(self, next_step):
        while True:
            if next_step == "4":
                next_step = self.delete_man_by_id()
            elif next_step == "6":
                next_step = self.show_add_phone()
            elif next_step == "7":
                next_step = self.delete_phone()
            elif next_step == "5":
                next_step = self.show_phones_by_people()
            elif next_step != "0" and next_step != "9" and next_step != "3":
                print("Выбрано неверное число! Повторите ввод!")
                return "1"
            else:
                return next_step

    def check_input(self, label, max_len, not_null, break_code=None):
        candidate = (input(f"Введите {str(label)} (1 - отмена): ").strip())
        if candidate == "1":
            return break_code
        while not_null and len(candidate.strip()) == 0 or len(candidate.strip()) > max_len:
            candidate = input(
                "Некорректный ввод (1 - отмена):").strip()
            if candidate == "1":
                return break_code
        return candidate

    def show_add_person(self):
        data = []
        surname = self.check_input('фамилию', 32, True)
        if (not surname):
            return
        data.append(surname)
        name = self.check_input('имя', 32, True)
        data.append(name)
        if (not name):
            return
        data.append(self.check_input('отчество', 32, False))

        PeopleTable().insert_one(data)
        return

    def delete_by_field(self, table, menu, field):
        while True:
            num = str(input(prompts["empty_line"]))
            while len(num.strip()) == 0:
                num = str(input(prompts["empty_line_error"]))
            if num == "0":
                return "1"
            obj = table().check_field_exist(field, num)
            if not obj:
                print(prompts["no_rows_error"])
            else:
                break
        success = table().delete_one_by_field(field, num)
        print("Запись была уничтожена!" if success else "Неверный ввод")
        print(menu)
        return self.read_next_step()

    def delete_man_by_id(self):
        return self.delete_by_field(PeopleTable, people_menu, 'id')

    def delete_phone(self):
        return self.delete_by_field(PhonesTable, phones_menu, 'phone')

    def show_add_phone(self):
        break_code = '6'
        phone = self.check_input('номер телефона', 12, True, break_code)
        if (phone == break_code):
            return break_code
        exist = PhonesTable().check_field_exist(
            ['person_id', 'phone'], [self.person_id, phone])
        print(phones_menu)
        if (exist):
            print("Нарушен Primary Key, запись не была вставлена")
            return self.read_next_step()
        PhonesTable().insert_one([self.person_id, phone])
        return self.read_next_step()

    def show_phones_by_people(self):
        if self.person_id == -1:
            while True:
                num = input(prompts["empty_line"])
                while len(num.strip()) == 0:
                    num = input(prompts["empty_line_error"])
                if num == "0":
                    return "1"
                person = PeopleTable().find_by_id(int(num))
                if not person:
                    print("Нет такого человека!")
                else:
                    self.person_id = int(person[0])
                    self.person_obj = person
                    break
        print("Выбран человек: " +
              self.person_obj[1] + " " + self.person_obj[2] + " " + self.person_obj[3])
        print("Телефоны:")
        lst = PhonesTable().all_by_person_id(self.person_id)
        for i in lst:
            print(i[1])
        print(phones_menu)
        return self.read_next_step()

        return self.read_next_step()

    def main_cycle(self):
        current_menu = "0"
        next_step = None
        while(current_menu != "9"):
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
            elif current_menu == "1":
                self.show_people()
                next_step = self.read_next_step()
                current_menu = self.after_show_people(next_step)
            elif current_menu == "2":
                self.show_main_menu()
            elif current_menu == "3":
                self.show_add_person()
                current_menu = "1"
        print("До свидания!")
        return


m = Main()
m.main_cycle()
