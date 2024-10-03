import json
from datetime import datetime

MINIMUM_AGE = 20
FIRST_PASSPORT_CHANGE_AGE = 20
SECOND_PASSPORT_CHANGE_AGE = 45
ACCEPTABLE_DEBT = 0
ACCEPTABLE_DAYS_ON_OVERDUE = 60
ACCEPTABLE_DAYS_ON_OVERDUE_NET = 15
ACCEPTABLE_DAYS_ON_OVERDUE_COUNT = 2
ACCEPTABLE_DAYS_ON_OVERDUE_CREDIT = 30
ACCEPTABLE_DEBT_CREDIT = 30


def stopcheck(user_data: str) -> bool:
    """
       Проверяет, соответствует ли пользователь установленным критериям (возраст, паспортные данные, кредитная история).
       Возвращает True, если все проверки пройдены, иначе False.
    """
    # открываем json файл
    with open(user_data, "r", encoding="UTF-8") as json_file:
        user_attributes = json.load(json_file)
    # преобразование строк с датами рождения и выдачи паспорта в объекты datetime, для дальнейшей работы
    birthDate = datetime.strptime(user_attributes["birthDate"], '%Y-%m-%dT%H:%M:%S.%fZ')
    passportIssued = datetime.strptime(user_attributes["passport"]["issuedAt"], '%Y-%m-%dT%H:%M:%S.%fZ')

    # текущая дата
    now = datetime.now()

    # проверка на валидность внесённых данных
    if now.year < birthDate.year or now.year < passportIssued.year:
        return False

    # проверка на минимальный возраст
    if (now.year - birthDate.year < MINIMUM_AGE) or \
            (now.year - birthDate.year == MINIMUM_AGE and (now.month, now.day) < (birthDate.month, birthDate.day)):
        return False

    # проверка на валидность паспорта при достижении 20 лет
    if (now.year - birthDate.year > FIRST_PASSPORT_CHANGE_AGE) or \
            ((now.year - birthDate.year == FIRST_PASSPORT_CHANGE_AGE) and
             (now.month, now.day) >= (birthDate.month, birthDate.day)):
        if passportIssued.year < birthDate.year + FIRST_PASSPORT_CHANGE_AGE or \
            (passportIssued.year == birthDate.year + FIRST_PASSPORT_CHANGE_AGE and
                (passportIssued.month, passportIssued.day) < (birthDate.month, birthDate.day)):
            return False

    # проверка на валидность паспорта при достижении 45 лет
    if (now.year - birthDate.year > SECOND_PASSPORT_CHANGE_AGE) or \
            ((now.year - birthDate.year == SECOND_PASSPORT_CHANGE_AGE) and
             (now.month, now.day) >= (birthDate.month, birthDate.day)):
        if passportIssued.year < birthDate.year + SECOND_PASSPORT_CHANGE_AGE or \
            (passportIssued.year == birthDate.year + SECOND_PASSPORT_CHANGE_AGE and
                (passportIssued.month, passportIssued.day) < (birthDate.month, birthDate.day)):
            return False

    # проверки по кредитным условиям
    overdue_count = 0 # счётчик задолженностей
    for credit_issue in user_attributes["creditHistory"]:
        if not credit_issue["type"] == "Кредитная карта":

            if credit_issue["numberOfDaysOnOverdue"] > ACCEPTABLE_DAYS_ON_OVERDUE_NET:
                overdue_count += 1
            if credit_issue["currentOverdueDebt"] > ACCEPTABLE_DEBT:
                return False
            if credit_issue["numberOfDaysOnOverdue"] > ACCEPTABLE_DAYS_ON_OVERDUE:
                return False
            if overdue_count > ACCEPTABLE_DAYS_ON_OVERDUE_COUNT:
                return False

        elif credit_issue["type"] == "Кредитная карта":

            if credit_issue["currentOverdueDebt"] > ACCEPTABLE_DEBT_CREDIT:
                return False
            if credit_issue["numberOfDaysOnOverdue"] > ACCEPTABLE_DAYS_ON_OVERDUE_CREDIT:
                return False

    return True


def main():
    # вывод результата и выбор .json файла, который проверяем
    print(f"main result {stopcheck("data.json")}")


if __name__ == "__main__":
    main()
