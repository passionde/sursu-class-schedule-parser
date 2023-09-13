import os
import re

import pdfplumber
from pdfplumber.page import Page

DAYS_WEEK = [
    "ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ",
    "пн", "вт", "ср", "чт", "пт", "сб"
]


# Очистка строки
def row_cleaning(row):
    def remove_items(lst, items):
        return [item for item in lst if item not in items]

    row = remove_items(row, [None, ""])
    if len(row) == 1 and row[0] not in DAYS_WEEK:
        return None

    cleaned_row = []
    for cell in row:
        cell = cell.replace("\n", " ")
        cell = " ".join(cell.split())

        replacements = [("п/г ", "п/г"), ("/ /", "//"), ("// ", "//"), (" //", "//")]
        for old, new in replacements:
            cell = cell.replace(old, new)

        cleaned_row.append(cell)

    return cleaned_row


# Получение номера группы
def get_number(table, path, page_number):
    for row in table:
        for cell in row:
            if not cell:
                continue
            group = re.findall(r'\s\d{3}-\d{2}[а-яА-яAA-Za-z]?', cell)
            if group:
                return group[0][1:]

    # Если дошло до этой строки, то группа не найдена
    print("Не удалось определить группу:")
    print(f"\tФайл {path}")
    print(f"\tСтраница: {page_number}")
    return input("\tВведите номер группы >>> ").lower()


# Определение начала расписания
def get_start_index(table):
    for idx, row in enumerate(table):
        if "ПН" in row:
            return idx

    raise ValueError("Failed to determine the start of the schedule")


def parse_data(table):
    data = []
    day_week = ""

    for row in table[get_start_index(table):]:
        # Очистка строки
        row = row_cleaning(row)
        if not row:
            continue

        # Обновление дня недели
        for dw in DAYS_WEEK:
            if dw in row:
                row.remove(dw)
                day_week = dw.lower()
                break

        # Пропуск строк типа: ["1"] (появляются после row.remove(dw))
        if len(row) <= 1:
            continue

        lesson_number = row[0]

        for cell in row[1:]:
            subgroup = 0
            if "п/г" in cell:
                subgroup = int(cell[cell.find("п/г") + len("п/г")])

            parts = cell.split("//")

            if len(parts) == 1 and parts[0]:
                data.append(ScheduleItem(day_week, subgroup, 0, parts[0], lesson_number))
                continue

            if parts[0]:
                data.append(ScheduleItem(day_week, subgroup, 1, parts[0], lesson_number))
            if parts[1]:
                data.append(ScheduleItem(day_week, subgroup, 2, parts[1], lesson_number))

    return data


class ScheduleItem:
    def __init__(self, week_day, subgroup, type_week, lesson, lesson_number):
        self.week_day = week_day
        self.subgroup = subgroup
        self.type_week = type_week
        self.lesson = lesson
        self.lesson_number = lesson_number

    def to_sql(self):
        return [self.lesson_number, self.week_day, self.type_week, self.subgroup, self.lesson]


class ScheduleGroup:
    def __init__(self, page: Page, path: str):
        table = page.extract_table()
        self.number: int = get_number(table, path, page.page_number)
        self.data = parse_data(table)

    def to_sql(self) -> list[tuple]:
        result = []
        for j in self.data:
            result.append((self.number, *j.to_sql()))

        return result


if __name__ == "__main__":
    for filename in os.listdir("../schedules"):
        file = pdfplumber.open(f"schedules/{filename}")

        for p in file.pages:
            sch = ScheduleGroup(p, f"schedules/{filename}")
            for i in sch.to_sql():
                print(i)

