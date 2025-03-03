import json
from abc import ABC, abstractmethod

class FileWork:
    DATA_FILE = "data.json"

    def __init__(self):
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.DATA_FILE, "r") as file:
                # Проверяем, что файл не пуст
                file_content = file.read().strip()
                if file_content:
                    return json.loads(file_content)  # Загружаем данные из JSON
                else:
                    return {"apartments": [], "residents": []}  # Если файл пуст, возвращаем пустые данные
        except (FileNotFoundError, json.JSONDecodeError):
            # Если файл не найден или ошибка в JSON, создаем новый пустой файл
            self.create_empty_file()
            return {"apartments": [], "residents": []}

    def save_data(self, data):
        with open(self.DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def create_empty_file(self):
        """Создаем пустой JSON файл, если его нет или он поврежден."""
        with open(self.DATA_FILE, "w") as f:
            json.dump({"apartments": [], "residents": []}, f, indent=4)


class ResidentalComplex:
    def __init__(self):
        self.apartments_list = []  # Список для квартир
        self.resident_list = []  # Список для жильцов
        self.pinned_dict = {}  # Словарь для закрепленных жильцов
        self.load_data()

    def load_data(self):
        data = FileWork().load_data()  # Загружаем данные из файла
        self.apartments_list = data.get("apartments", [])
        self.resident_list = data.get("residents", [])

    def save_data(self):
        data = {"apartments": self.apartments_list,
                "residents": self.resident_list}  # Сохраняем данные обо всех объектах
        FileWork().save_data(data)

    def show_residents(self):
        if self.resident_list:
            for resident in self.resident_list:
                print(resident)
        else:
            return "Список жильцов пуст!"  # Если список жильцов пуст, выводим сообщение

    def show_apartments(self):
        if self.apartments_list:
            for apartment in self.apartments_list:
                print(apartment)
        else:
            return "Список квартир пуст!"  # Если список квартир пуст, выводим сообщение

    def show_concrete_apartment(self):
        choice = int(input("Напишите номер квартиры, чью информацию хотите узнать: "))
        apartment = next((apt for apt in self.apartments_list if apt["number"] == choice), None)
        if apartment:
            print(apartment)
        else:
            return "Данной квартиры не существует!"  # Если квартира не найдена, выводим сообщение

    def show_concrete_floor(self):
        choice = int(input("Напишите этаж квартиры, чьи информации хотите узнать: "))
        apartments_on_floor = [apt for apt in self.apartments_list if apt["floor"] == choice]
        if apartments_on_floor:
            for apt in apartments_on_floor:
                print(apt)
        else:
            return "Квартир на этаже не существует!"  # Если квартир на данном этаже нет, выводим сообщение

    def show_apartments_by_rooms(self):
        choice = int(input("Напишите количество комнат квартир, чьи информации хотите узнать: "))
        apartments_with_rooms = [apt for apt in self.apartments_list if apt["rooms"] == choice]
        if apartments_with_rooms:
            for apt in apartments_with_rooms:
                print(apt)
        else:
            return "Квартир с таким количеством комнат не существует!"  # Если квартир с таким количеством комнат нет


class Resident:

    @staticmethod
    def add_resident():
        resident_name = input("Добавьте жильца: ").lower()
        if resident_name not in ResidentalComplex().resident_list:
            ResidentalComplex().resident_list.append(resident_name)
            ResidentalComplex().save_data()  # Сохраняем изменения
        else:
            return "Такой жилец уже есть."  # Если жилец уже есть, выводим сообщение

    @staticmethod
    def delete_resident():
        resident_name = input("Впишите жильца которого хотите удалить: ").lower()
        if resident_name in ResidentalComplex().resident_list:
            ResidentalComplex().resident_list.remove(resident_name)
            ResidentalComplex().save_data()  # Сохраняем изменения
        else:
            return "Такого жильца не существует."  # Если жилец не найден, выводим сообщение

    @staticmethod
    def pin_resident():
        resident_name = input("Напишите жильца, которого хотите закрепить за квартирой: ").lower()
        apartment_number = int(input("Напишите номер квартиры к которой хотите закрепить жильца: "))
        if resident_name in ResidentalComplex().resident_list and any(
                apt["number"] == apartment_number for apt in ResidentalComplex().apartments_list):
            ResidentalComplex().pinned_dict[resident_name] = apartment_number
            ResidentalComplex().save_data()  # Сохраняем закрепление
        else:
            return "Такого жильца или квартиры не существует."  # Если жилец или квартира не найдены, выводим сообщение

    @staticmethod
    def unpin_resident():
        resident_name = input("Напишите жильца, которого хотите открепить от квартиры: ").lower()
        apartment_number = int(input("Напишите номер квартиры от которой хотите открепить жильца: "))
        if resident_name in ResidentalComplex().pinned_dict and ResidentalComplex().pinned_dict[
            resident_name] == apartment_number:
            del ResidentalComplex().pinned_dict[resident_name]
            ResidentalComplex().save_data()  # Сохраняем изменения
        else:
            return "Такого жильца или квартиры не существует."  # Если жилец или квартира не закреплены, выводим сообщение


class Apartment:

    @staticmethod
    def add_apartment():
        number = int(input("Номер квартиры: "))
        size = int(input("Размер вашей квартиры в м2: "))
        rooms = int(input("Количество комнат в вашей квартире: "))
        floor = int(input("На каком этаже находится ваша квартира: "))
        residents = int(input("Количество жильцов в вашей квартире: "))
        apartment = {"number": number, "size": size, "rooms": rooms, "floor": floor, "residents": residents}

        if not any(apt["number"] == number for apt in ResidentalComplex().apartments_list):
            ResidentalComplex().apartments_list.append(apartment)
            ResidentalComplex().save_data()  # Сохраняем изменения
            print(f"Вы добавили квартиру:\n{apartment}")
        else:
            return "Такая квартира уже существует."  # Если квартира уже существует, выводим сообщение

    @staticmethod
    def remove_apartment():
        number = int(input("Какую квартиру вы хотите удалить?(по номеру): "))
        apartment = next((apt for apt in ResidentalComplex().apartments_list if apt["number"] == number), None)
        if apartment:
            choice = input("Вы точно хотите удалить квартиру? y/n: ")
            if choice == "y":
                ResidentalComplex().apartments_list.remove(apartment)
                ResidentalComplex().save_data()  # Сохраняем изменения
            elif choice == "n":
                return "Действие отменено."  # Если действие отменено
            else:
                return "Введите допустимое значение!"  # Неверный ввод
        else:
            return "Такой квартиры не существует."  # Если квартира не найдена, выводим сообщение


class Menu(ABC):

    def create_menu(self):
        choice = int(input("""
        Выберите опцию:
        1. Редактирование жильцов
        2. Редактирование квартир
        3. Отображение информации
        4. Завершить работу
        """))
        if choice == 1:
            ResidentMenu().create_menu()
        elif choice == 2:
            ApartmentMenu().create_menu()
        elif choice == 3:
            InfoMenu().create_menu()
        elif choice == 4:
            print("Работа завершена!")  # Завершаем работу
            return
        else:
            print("Неверный выбор.")  # Неверный выбор
            self.create_menu()


class ResidentMenu(Menu):

    def create_menu(self):
        choice = int(input("""
        Выберите опцию:
        1. Добавление жильцов
        2. Удаление жильцов
        3. Закрепить жильца
        4. Открепить жильца
        5. Выход в меню
        """))
        if choice == 1:
            Resident.add_resident()
        elif choice == 2:
            Resident.delete_resident()
        elif choice == 3:
            Resident.pin_resident()
        elif choice == 4:
            Resident.unpin_resident()
        elif choice == 5:
            Menu().create_menu()  # Возврат в главное меню
        else:
            print("Неверный выбор.")  # Неверный выбор
            self.create_menu()


class ApartmentMenu(Menu):

    def create_menu(self):
        choice = int(input("""
        Выберите опцию:
        1. Добавление квартир
        2. Удаление квартир
        3. Выход в меню
        """))
        if choice == 1:
            Apartment.add_apartment()
        elif choice == 2:
            Apartment.remove_apartment()
        elif choice == 3:
            Menu().create_menu()  # Возврат в главное меню
        else:
            print("Неверный выбор.")  # Неверный выбор
            self.create_menu()


class InfoMenu(Menu):

    def create_menu(self):
        choice = int(input("""
        Выберите опцию:
        1. Показать список жильцов
        2. Показать список квартир
        3. Поиск квартиры по номеру
        4. Поиск квартир по этажу
        5. Поиск квартир по количеству комнат
        6. Выход в меню
        """))
        if choice == 1:
            ResidentalComplex().show_residents()
        elif choice == 2:
            ResidentalComplex().show_apartments()
        elif choice == 3:
            ResidentalComplex().show_concrete_apartment()
        elif choice == 4:
            ResidentalComplex().show_concrete_floor()
        elif choice == 5:
            ResidentalComplex().show_apartments_by_rooms()
        elif choice == 6:
            Menu().create_menu()  # Возврат в главное меню
        else:
            print("Неверный выбор.")  # Неверный выбор
            self.create_menu()


menu1 = Menu()
menu1.create_menu()  # Запуск главного меню
