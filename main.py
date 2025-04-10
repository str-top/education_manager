# цель: автоматизировать работу с данными студентов
import random
# действия:
# - отчисление при падении успеваемости

import threading
import time

students = {}
grades = []

def students_list():
    # имя, пол, курс, возраст, группа, текущий статус, форма обучения, должен ли денег
    students = {"Богдан": ["м", 8, 18, "python41", "учится", "очно", "должен денег"]}
    students["Игнат"] = ["м", 1, 58, "вторая", "учится", "очно", "должен денег"]
    students["Иван"] = ["м", 3, 8, "вторая", "учится", "очно", "не должен денег"]
    students["Агнесса"] = ["ж", 4, 5, "вторая", "учится", "очно", "не должен денег"]
    grades.append(["Богдан", "19:11", 5])
    grades.append(["Игнат", "19:11", 2])
    grades.append(["Богдан", "19:11", 4])
    grades.append(["Игнат", "19:11", 3])
    grades.append(["Иван", "19:11", 5])
    grades.append(["Агнесса", "19:11", 4])

lesson_time = 3
break_time = 1

current_status = ""
last_change_time = time.time()
last_deadline_check_time = time.time()

def just_for_fun():
    face = r"""
   _________
  /         \
 |  O     O  |
 |     ^     |
 |   \___/   |
 |           |
 |  \_____/  |
  \_________/
     |   |
     ----- 
    """
    print(face)


def add_student():
    while True:
        try:
            name = input('Введи имя нового студента: ')
            if name in students:
                print("такой студент уже есть. ")

            gender = input('Пол студента ("м", "ж"): ')
            if gender not in ['м', 'ж']:
                raise ValueError("Пол должен быть 'м' или 'ж'.")

            level = int(input('Введите курс студента: '))
            if level < 1:
                raise ValueError("курс должен быть положительным. ")

            age = int(input('Введите возраст студента: '))
            if age < 0:
                raise ValueError("возраст не может быть отрицательым")

            group = input('Введите группу студента: ')
            form = input('Введите форму обучения студента: ')
            status = input('Введите статус студента (обучается, отчислен или закончил обучение): ')
            dont_pay = input('Укажите, есть ли долг по оплате (да/нет): ')

            if dont_pay not in ['да', 'нет']:
                raise ValueError("Ответ должен быть 'да' или 'нет'.")

            students[name] = [gender, level, age, form, group, status, dont_pay]
            print(f'Студент {name} добавлен.')
            just_for_fun()
            break

        except Exception as e:
            print('Ошибка', e)

def del_student_2(name):
    global students
    students.pop(name)
    print(f"Студент {name} удален.")

def del_student(age=18, level=1):
    global students
    while True:
        if not students:
            print("Список студентов пуст. Невозможно удалить студента.")
            break
    if name in students:
        del_student_2(name)
    else:
        print('Такого студента не существует')


def new_grade():
    while True:
        student_name = input("Введите имя студента: ")
        if student_name in students:
            time_of_grade = input("Введите время получения оценки через двоеточие: ")  # 10:24
            grade_number = input("Введите оценку: ")  # 1 2 3 4 5

            # TODO

            grades.append([student_name, time_of_grade, grade_number])
            print(f"Оценка {grade_number} для студента {student_name} добавлена")
            break
        else:
            print(f"Студент с именем {student_name} не найден.")


def dont_pay():
    print("Должники: ")
    for student in students:
        if students[student][6] == "должен денег":
            print(student)

def student_data():
    global students
    name = input('Данные какого студента вывести? ')
    if name in students:
        new_name = name.upper()
        obr_name = new_name[::-2]
        print(f"Имя   пол   курс   возраст   группа    текущий статус   форма обучения  должен ли денег")
        print(obr_name, students[name][0], students[name][1], students[name][2], students[name][3], students[name][4],
              students[name][5], students[name][6])
    else:
        print('Такого студента не существует')


def show_groups():
    group = input("Введите название группы: ")
    print(f"Студенты группы {group}: ")
    for student in students:
        if students[student][3] == group:
            print(student)


def top_students():
    # 1) берем данные из списка оценок
    students_grades = {}

    # 2) соотносим оценки к студентам
    for grade in grades:
        if grade[0] in students_grades:
            students_grades[grade[0]].append(grade[2])
        else:
            students_grades[grade[0]] = [grade[2]]

    # 3) высчитываем средний балл
    avg_grades = {}
    for student_grades in students_grades:
        avg_grades[student_grades] = sum(students_grades[student_grades]) / len(students_grades[student_grades])

    # 4) сортируем по убыванию
    sorted_dict = dict(sorted(avg_grades.items(), key=lambda x: x[1], reverse=True))

    # 5) выводим первых трех студентов
    top_students = list(sorted_dict.items())[:3]
    for top_student in top_students:
        print(top_student[0])


def learning_state():
    global current_status
    global last_change_time
    if current_status == "":
        current_status = "study"
        last_change_time = int(time.time())
        print ("Пара началась, всем срочно в класс!!! Кто опоздает будет отсчислен")
    # смена статуса при истечении времени
    # TODO: не производить смену статуса в неучебное время суток
    if int(time.time()) > last_change_time + lesson_time:
        current_status = "break"
        last_change_time = int(time.time())
        print("Ура, перерыв! Идем пить кофе")
        # TODO: выставлять каждому студенту оценку за пару случайным образом
    elif current_status == "break":
        if int(time.time()) > last_change_time + break_time:
            current_status = "study"
            last_change_time = int(time.time())
            print("Пара началась, всем срочно в класс!!! Кто опоздает будет отсчислен")

def check_deadlines():
    global students
    global grades
    global last_deadline_check_time
    if int(time.time()) > last_deadline_check_time + lesson_time * 4 + break_time * 3:
        # каждую пятую пару проверяем
        last_deadline_check_time = time.time()
        for student in students:
            # каждому студента добавить по оценке, каждому пятому выставляем 1
            grade = random.choice([1,1,4,4,5])
            new_grade = [student, "12:12", grade]
            grades.append(new_grade)
            print(new_grade)

def check_avg_grades():
    # 1) пройтись по каждому студенту
    global students
    global grades
    students_copy = students.copy()
    for student in students_copy:
        my_grades = []
        for grade in grades:
            if grade[0] == student:
                my_grades.append(grade[2])
        # 2) подсчитать средний балл
        avg_grade = sum(my_grades) / len(my_grades)
        # 3) проверить есть ли условие для отчисления
        if avg_grade < 3:
            # 4) отчислить студента
            del_student_2(student)

def loop_task():
    while True:
        time.sleep(1)  # Simulate work

        learning_state()
        check_deadlines()
        check_avg_grades()
        # контрольные работы
        # праздничные дни


def user_input_task():
    while True:
        pass
        menu = """Список действий:
1) добавить студента
2) удалить студента
3) добавить оценку
4) вывести список неплательщиков
5) просмотр данных студента
6) просмотреть состав группы
7) топ 3 студента

Введите цифру действия: """

        selection = input(menu).strip()

        assert selection in ["1", "2", "3", "4", "5", "6", "7"], "Неверный номер действия"
        try:
            if selection == "1":
                add_student()
            elif selection == "2":
                del_student(age = 19, level = 2)
            elif selection == "3":
                new_grade()
            elif selection == "4":
                dont_pay()
            elif selection == "5":
                student_data()
            elif selection == "6":
                show_groups()
            elif selection == "7":
                top_students()

        except AssertionError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

        time.sleep(1)
        print("")

        # - просмотр данных студента
        # - вывести топ 3 студента


# Run loop in a separate thread
thread = threading.Thread(target=loop_task)
thread.start()

# Run user input in the main thread
user_input_task()
students_list()
