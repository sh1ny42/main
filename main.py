import json
from abc import ABC, abstractmethod

class FileWork:
    DATA_FILE = "data.json"

    def __init__(self):
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.DATA_FILE, "r") as file:
                file_content = file.read().strip()
                if file_content:
                    return json.loads(file_content)
                else:
                    return {"apartments": [], "residents": []}
        except (FileNotFoundError, json.JSONDecodeError):

            self.create_empty_file()
            return {"apartments": [], "residents": []}

    def save_data(self, data):
        with open(self.DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def create_empty_file(self):
        with open(self.DATA_FILE, "w") as f:
            json.dump({"apartments": [], "residents": []}, f, indent=4)



class ResidentalComplex:
    def __init__(self):
        self.apartments_list = []
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

    def show_residents(self):
        if self.resident_list:
            for resident in self.resident_list:
                print(resident)
        else:
            print("Список жильцов пуст!")

    def show_apartments(self):
        if self.apartments_list:
            for apartment in self.apartments_list:
                print(apartment)
        else:
            print("Список квартир пуст!")

    def concrete_apartment(self):
        choice = int(input("Напишите номер квартиры, чью информацию хотите узнать: "))
        apartment = next((apt for apt in self.apartments_list if apt["number"] == choice), None)
        if apartment:
            print(apartment)
        else:
            print("Данной квартиры не существует!")

    def concrete_floor(self):
        choice = int(input("Напишите этаж квартиры, чьи информации хотите узнать: "))
        apartments_on_floor = [apt for apt in self.apartments_list if apt["floor"] == choice]
        if apartments_on_floor:
            for apt in apartments_on_floor:
                print(apt)
        else:
            print("Квартир на этаже не существует!")

    def one_type_apartment(self):
        choice = int(input("Напишите количество комнат квартир, чьи информации хотите узнать: "))
        apartments_with_rooms = [apt for apt in self.apartments_list if apt["rooms"] == choice]
        if apartments_with_rooms:
            for apt in apartments_with_rooms:
                print(apt)
        else:
            print("Квартир с таким количеством комнат не существует!")


class Resident:

    @staticmethod
    def add_resident(residental_complex):
        resident_name = input("Добавьте жильца: ").lower()
        if resident_name not in residental_complex.resident_list:
            residental_complex.resident_list.append(resident_name)
            print("Жилец добавлен.")
            residental_complex.save_data()
        else:
            print("Такой жилец уже есть.")

    @staticmethod
    def delete_resident(residental_complex):
        resident_name = input("Впишите жильца, которого хотите удалить: ").lower()
        if resident_name in residental_complex.resident_list:
            residental_complex.resident_list.remove(resident_name)
            print("Жилец удалён.")
            residental_complex.save_data()
        else:
            print("Такого жильца не существует.")

    @staticmethod
    def pin_resident(residental_complex):
        resident_name = input("Напишите жильца, которого хотите закрепить за квартирой: ").lower()
        apartment_number = int(input("Напишите номер квартиры, к которой хотите закрепить жильца: "))
        if resident_name in residental_complex.resident_list and any(
                apt["number"] == apartment_number for apt in residental_complex.apartments_list):
            residental_complex.pinned_dict[resident_name] = apartment_number
            print("Жилец закреплён")
            residental_complex.save_data()
        else:
            print("Такого жильца или квартиры не существует.")

    @staticmethod
    def unpin_resident(residental_complex):
        resident_name = input("Напишите жильца, которого хотите открепить от квартиры: ").lower()
        apartment_number = int(input("Напишите номер квартиры, от которой хотите открепить жильца: "))
        if resident_name in residental_complex.pinned_dict and residental_complex.pinned_dict[
            resident_name] == apartment_number:
            del residental_complex.pinned_dict[resident_name]
            print("Жилец откреплён.")
            residental_complex.save_data()
        else:
            print("Такого жильца или квартиры не существует.")


class Apartment:

    @staticmethod
    def add_apartment(residental_complex):
        number = int(input("Номер квартиры: "))
        size = int(input("Размер вашей квартиры в м2: "))
        rooms = int(input("Количество комнат в вашей квартире: "))
        floor = int(input("На каком этаже находится ваша квартира: "))
        residents = int(input("Количество жильцов в вашей квартире: "))

        apartment = {
            "number": number,
            "size": size,
            "rooms": rooms,
            "floor": floor,
            "residents": residents,
        }

        print(f"""Вы добавили квартиру:
        Номер квартиры: {apartment["number"]}
        Размер: {apartment["size"]}
        Количество комнат: {apartment["rooms"]}
        Этаж квартиры: {apartment["floor"]}
        Количество жильцов: {apartment["residents"]}
        """)

        if apartment not in residental_complex.apartments_list:
            residental_complex.apartments_list.append(apartment)
            print("Квартира добавлена.")
            residental_complex.save_data()
        else:
            print("Такая квартира уже существует.")

    @staticmethod
    def remove_apartment(residental_complex):
        number = int(input("Какую квартиру вы хотите удалить?(по номеру): "))
        apartment = next((apt for apt in residental_complex.apartments_list if apt["number"] == number), None)

        if apartment:
            choice = input("Вы точно хотите удалить квартиру? y/n: ")
            if choice == "y":
                residental_complex.apartments_list.remove(apartment)
                print("Квартира удалена.")
                residental_complex.save_data()
            elif choice == "n":
                print("Действие отменено.")
            else:
                print("Введите допустимое значение!")
        else:
            print("Такой квартиры не существует.")


class Menu(ABC):
    def create_menu(self):
        while True:
            try:
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
                    print("Работа завершена!")
                    break
                else:
                    print("Неверный выбор, попробуйте снова.")
            except ValueError:
                print("Ввод должен быть числом. Попробуйте снова.")


class ResidentMenu(Menu):
    def create_menu(self):
        residental_complex = ResidentalComplex()
        while True:
            try:
                choice = int(input(""" 
                Выберите опцию:
                1. Добавление жильцов
                2. Удаление жильцов
                3. Закрепить жильца
                4. Открепить жильца
                5. Выход в меню
                """))
                if choice == 1:
                    Resident.add_resident(residental_complex)
                    # ResidentMenu().create_menu()
                elif choice == 2:
                    Resident.delete_resident(residental_complex)
                    # ResidentMenu().create_menu()
                elif choice == 3:
                    Resident.pin_resident(residental_complex)
                    # ResidentMenu().create_menu()
                elif choice == 4:
                    Resident.unpin_resident(residental_complex)
                    # ResidentMenu().create_menu()
                elif choice == 5:
                    # Menu().create_menu()
                    break
                else:
                    print("Неверный выбор, попробуйте снова.")
            except ValueError:
                print("Ввод должен быть числом. Попробуйте снова.")


class ApartmentMenu(Menu):
    def create_menu(self):
        residental_complex = ResidentalComplex()
        while True:
            try:
                choice = int(input(""" 
                Выберите опцию:
                1. Добавление квартир
                2. Удаление квартир
                3. Выход в меню
                """))
                if choice == 1:
                    Apartment.add_apartment(residental_complex)
                    # ApartmentMenu().create_menu()
                elif choice == 2:
                    Apartment.remove_apartment(residental_complex)
                    # ApartmentMenu().create_menu()
                elif choice == 3:
                    # Menu().create_menu()
                    break
                else:
                    print("Неверный выбор, попробуйте снова.")
            except ValueError:
                print("Ввод должен быть числом. Попробуйте снова.")


class InfoMenu(Menu):
    def create_menu(self):
        while True:
            try:
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
                    ResidentalComplex().concrete_apartment()
                elif choice == 4:
                    ResidentalComplex().concrete_floor()
                elif choice == 5:
                    ResidentalComplex().one_type_apartment()
                elif choice == 6:
                    break
                else:
                    print("Неверный выбор, попробуйте снова.")
            except ValueError:
                print("Ввод должен быть числом. Попробуйте снова.")

menu1 = Menu()
menu1.create_menu()