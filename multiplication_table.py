"""Программа проверяет знание таблицы умножения."""

import random
import re
import time

PROGRAM_NAME = "Таблица умножения"
MAX_MISTAKES_NUMBER = 3  # максимальное количество ошибок в примере
MAX_CASE_TIME = 5  # максимальное количество времени на пример
TIME_PENALTY_COEFFICIENT = 5  # градиент штрафа по времени

def examples_number_define():
    while True:
        answer = input("\nВведите количество примеров [5–81]: ")
        if re.fullmatch(r"\d+", answer):
            examples_number = int(answer)
            if examples_number < 5 or examples_number > 81:
                print("Введите целое число от 5 до 81")
                continue
            return examples_number
        else:
            print("Необходимо ввести целое число!")

def create_cases():
    cases = []  # набор примеров
    for i in range(9):
        for j in range(9):
            cases.append((i+1, j+1))

    random.shuffle(cases)
    del cases[examples_number:]

    print("Сгенерирован следующий набор:")
    for number, case in enumerate(cases):
        print("{:2}: {} × {}".format(number+1, *case))

    return cases

def penalty_calculation():
    mistakes_penalty = total_mistakes / examples_number * 100

    max_time_penalty = MAX_CASE_TIME * TIME_PENALTY_COEFFICIENT
    if mistakes_penalty > 100 - max_time_penalty:
        mistakes_penalty = 100 - max_time_penalty

    time_penalty = TIME_PENALTY_COEFFICIENT * average_case_time

    return mistakes_penalty, time_penalty

def grade_calculation():
    score = 100 - mistakes_penalty - time_penalty

    if 80 < score <= 100:
        return score, "отлично"
    elif 60 < score <= 80:
        return score, "хорошо"
    elif 40 < score <= 60:
        return score, "удовлетворительно"
    elif score <= 40:
        return score, "неудовлетворительно"

def testing():
    total_mistakes = 0  # количество неправильных ответов
    testing_start_time = time.time()

    cases_times = []

    for number, case in enumerate(cases):

        current_time = time.time()
        print(f"\nПример № {number+1} (осталось {examples_number-number-1}):")
        first_multiplier, second_multiplier = case
        multiplication = first_multiplier * second_multiplier
        answer = 0
        mistakes = 0

        while mistakes < MAX_MISTAKES_NUMBER:
            answer = input(f"{first_multiplier} × {second_multiplier} = ")

            if re.fullmatch(r"\d{1,2}", answer):
                if int(answer) == multiplication:
                    print("Верно!")
                    break
                else:
                    mistakes += 1
                    total_mistakes += 1
                    if mistakes < MAX_MISTAKES_NUMBER:
                        print("Ошибка! Введите другой вариант ответа.")
                    else:
                        print("Превышено максимальное количество ошибок в примере.")
            else:
                print("Введите целое число (не более двух цифр).")
                answer = 0

        case_time = time.time() - current_time
        if case_time < MAX_CASE_TIME:
            cases_times.append(case_time)
            print(f"Δt = {case_time:.1f}")
        else:
            cases_times.append(MAX_CASE_TIME)
            print(f"Δt > {MAX_CASE_TIME}")

    average_case_time = sum(cases_times) / examples_number
    testing_finish_time = time.time()
    test_time = testing_finish_time - testing_start_time

    return total_mistakes, test_time, average_case_time

def results_print():
    print("\nРезультаты теста".upper())
    print(f"Примеров: {examples_number}")
    print(f"Ошибок: {total_mistakes}")
    print(f"Штраф по ошибкам в баллах: {mistakes_penalty:.1f}")
    print(f"Общее время: {test_time:.1f}")
    print(f"Среднее время на пример: {average_case_time:.1f}")
    print(f"Штраф по времени в баллах: {time_penalty:.1f}")
    print(f"Баллы: {score:.1f}")
    print(f"Оценка: {grade}")

if __name__ == '__main__':
    print(f"\nПрограмма '{PROGRAM_NAME.upper()}'")
    examples_number = examples_number_define()
    cases = create_cases()
    total_mistakes, test_time, average_case_time = testing()
    mistakes_penalty, time_penalty = penalty_calculation()
    score, grade = grade_calculation()
    results_print()
