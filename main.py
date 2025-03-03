"""Создать приложение «Домовой менеджмент». Основная задача проекта — предоставить пользователю возможность хранить информацию о жильцах дома.

Интерфейс приложения должен предоставлять такие возможности:
· Добавление жильцов дома +
· Удаление жильцов дома +
· Добавление квартир (обязательно наличие возможности добавлять информации об этаже) +
· Удаление квартир +
· Закрепление жильцов за квартирой +
· Открепление жильцов от квартиры +
· Сохранение информации в файл +
· Загрузка информации из файла +
· Создание отчётов по таким параметрам:
    · Отображение полного списка жильцов +
    · Отображение полного списка квартир +
    · Отображение информации о конкретной квартире +
    · Отображение информации о квартирах на конкретном этаже +
    · Отображение информации о квартирах одного типа (например, отобразить все однокомнатные квартиры) +

Создание меню
Тест багов
Улучшить работу с исключениями
Доработать приложение

Правильное использование паттернов проектирования, принципов SOLID, механизмов тестирования при реализации задания позволит получить более высокую оценку."""

import json
from abc import ABC, abstractmethod

class FileWork:
    DATA_FILE = "data.json"

    def __init__(self):
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.DATA_FILE, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"apartments": [], "residents": []}

    def save_data(self, data):
        with open(self.DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)



class ResidentalComplex:
    def __init__(self):
        # self.apartments_amount = apartments_amount
        # self.floor_number = floor_number
        self.apartments_list = []
        # self.resident_amount = resident_amount
        self.resident_list = []
        self.pinned_dict = {}
        self.load_data()

    def load_data(self):
        data = FileWork().load_data()
        self.apartments_list = data.get("apartments", [])
        self.resident_list = data.get("residents", [])

    def save_data(self):
        data = {"apartments": self.apartments_list, "residents": self.resident_list}
        FileWork().save_data(data)

    def resident_list(self):
        if self.resident_list:
            for resident in self.resident_list:
                print(resident)
        else:
            return "Список жильцов пуст!"

    def apartments_list(self):
        if self.apartments_list:
            for apartment in self.apartments_list:
                print(apartment)
        else:
            return "Список квартир пуст!"

    def concrete_apartment(self):
        choice = int(input("Напишите номер квартиры, чью информацию хотите узнать: "))
        if choice in self.apartments_list():
            print(Apartment().number)
        else:
            return "Данной квартиры не существует!"

    def concrete_floor(self):
        choice = int(input("Напишите этаж квартиры, чьи информации хотите узнать: "))
        key_to_find = 'floor'
        try:
            for Apartment().number in self.apartments_list():
                for d in enumerate(Apartment().number):
                    if key_to_find in d:
                        print(f"Информация об этаже {choice}: {d}")
        except KeyError:
            return "Квартир на этаже не существует!"

    def one_type_apartment(self):
        choice = int(input("Напишите количество комнат квартир, чьи информации хотите узнать: "))
        key_to_find = 'rooms'
        try:
            for Apartment().number in self.apartments_list():
                for d in enumerate(Apartment().number):
                    if key_to_find in d:
                        for key in d:
                            if choice == key:
                                print(f"Информация об квартирах одного типа: {d}")
        except KeyError:
            return "Квартир на этаже не существует!"


class Resident:

    def add_resident(self):
        self.resident = input("Добавьте жильца: ")
        if self.resident not in ResidentalComplex().resident_list:
            ResidentalComplex().resident_list.append(self.resident.lower())
            FileWork().save_data(ResidentalComplex().resident_list)
        else:
            return "Такой жилец уже есть."


    def delete_resident(self):
        self.resident = input("Впишите жильца которого хотите удалить: ").lower()
        if self.resident in ResidentalComplex().resident_list:
            ResidentalComplex().resident_list.remove(self.resident)
            FileWork().save_data(ResidentalComplex().resident_list)
        else:
            return "Такого жильца не существует."

    def pin_resident(self):
        self.resident = input("Напишите жильца, которого хотите закрепить за квартирой: ")
        Apartment().self_number = input("Напишите номер квартиры к которой хотите закрепить жильца: ")
        if self.resident in ResidentalComplex().resident_list and Apartment().self_number in ResidentalComplex().apartments_list:
            self.pinned_dict = {self.resident: Apartment().self_number}
        else:
            return "Такого жильца или квартиры не существует."

    def unpin_resident(self):
        self.resident = input("Напишите жильца, которого хотите открепить от квартиры: ")
        Apartment().self_number = input("Напишите номер квартиры от которой хотите открепить жильца: ")
        if self.resident in ResidentalComplex().resident_list and Apartment().self_number in ResidentalComplex().apartments_list:
            self.pinned_dict.pop(self.resident)
        else:
            return "Такого жильца или квартиры не существует."




class Apartment:
    # def __init__(self, number, size, rooms, floor, residents):
    #     self.size = size
    #     self.rooms = rooms
    #     self.floor = floor
    #     self.residents = residents
    #     self.number = number

    def add_apartment(self):
        self.number = int(input("Номер квартиры: "))
        self.size = int(input("Размер вашей квартиры в м2: "))
        self.rooms = int(input("Количество комнат в вашей квартире: "))
        self.floor = int(input("На каком этаже находится ваша квартира: "))
        self.residents = int(input("Количество жильцов в вашей квартире: "))
        self.number = {
            "size":self.size,
            "rooms":self.rooms,
            "floor":self.floor,
            "residents":self.residents,
        }
        print(f"""Вы добавили квартиру:
        Номер квартиры: {self.number}
        Размер: {self.size}
        Количество комнат: {self.rooms}
        Этаж квартиры: {self.floor}
        Количество жильцов: {self.residents}"""
        )
        if self.number not in ResidentalComplex().apartments_list:
            ResidentalComplex().apartments_list.append(self.number)
            FileWork().save_data(ResidentalComplex().apartments_list)
        else:
            return "Такая квартира уже существует."

    def remove_apartment(self):
        self.number = int(input("Какую квартиру вы хотите удалить?(по номеру): "))
        if self.number in ResidentalComplex().apartments_list:
            choice = input("Вы точно хотите удалить квартиру? y/n: ")
            if choice == "y":
                ResidentalComplex().apartments_list.remove(self.number)
                FileWork().save_data(ResidentalComplex().resident_list)
            if choice == "n":
                return "Действие отменено."
            else:
                return "Введите допустимое значение!"
        else:
            return "Такой квартиры не существует."

class Menu(ABC):
    def create_menu(self):
        choice = int(input("""
        Выберите опцию
        1. Редактирование жильцов
        2. Редактирование квартир
        3. Отображение информации
        4. Завершить работу
        """))
        if choice == 1:
            ResidentMenu().create_menu()
        if choice == 2:
            ApartmentMenu().create_menu()
        if choice == 3:
            InfoMenu().create_menu()
        if choice == 4:
            print("Работа завершена!")
            # second_choice = int(input("""
            # Выберите опцию
            # 1. Добавление жильцов
            # 2. Удаление жильцов
            # 3. Закрепить жильца
            # 4. Открепить жильца
            # 5. Выход
            # """))

class ResidentMenu(Menu):
    def create_menu(self):
        choice = int(input("""
        Выберите опцию
        1. Добавление жильцов
        2. Удаление жильцов
        3. Закрепить жильца
        4. Открепить жильца
        5. Выход в меню
        """))
        if choice == 1:
            Resident().add_resident()
            ResidentMenu().create_menu()
        if choice == 2:
            Resident().delete_resident()
            ResidentMenu().create_menu()
        if choice == 3:
            Resident().pin_resident()
            ResidentMenu().create_menu()
        if choice == 4:
            Resident().unpin_resident()
            ResidentMenu().create_menu()
        if choice == 5:
            Menu().create_menu()

class ApartmentMenu(Menu):
    def create_menu(self):
        choice = int(input("""
        Выберите опцию
        1. Добавление квартир
        2. Удаление квартир
        3. Выход в меню
        """))
        if choice == 1:
            Apartment().add_apartment()
            ApartmentMenu().create_menu()
        if choice == 2:
            Apartment().remove_apartment()
            ApartmentMenu().create_menu()
        if choice == 3:
            Menu().create_menu()

class InfoMenu(Menu):
    def create_menu(self):
        choice = int(input("""
        Выберите опцию
        1. Показать список жильцов
        2. Показать список квартир
        3. Поиск квартиры по номеру
        4. Поиск квартир по этажу
        5. Поиск квартир по количеству комнат
        6. Выход в меню
        """))
        if choice == 1:
            ResidentalComplex().resident_list()
            InfoMenu().create_menu()
        if choice == 2:
            ResidentalComplex().apartments_list()
            InfoMenu().create_menu()
        if choice == 3:
            ResidentalComplex().concrete_apartment()
            InfoMenu().create_menu()
        if choice == 4:
            ResidentalComplex().concrete_floor()
            InfoMenu().create_menu()
        if choice == 5:
            ResidentalComplex().one_type_apartment()
            InfoMenu().create_menu()
        if choice == 6:
            Menu().create_menu()

menu1 = Menu()
menu1.create_menu()