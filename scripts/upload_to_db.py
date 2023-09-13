import os
import sqlite3

import pdfplumber

from parser import ScheduleGroup

PATH_SCHEDULES = "schedules"

if __name__ == "__main__":
    con = sqlite3.connect("files/schedule.db")
    cursor = con.cursor()

    cursor.execute("""CREATE TABLE schedule
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                    group_number varchar(7),
                    lesson_number int,
                    day_week varchar(2) check ( day_week IN ('пн', 'вт', 'ср', 'чт', 'пт', 'сб') ),
                    type_week int check ( type_week IN (0, 1, 2) ),
                    subgroup_number int check ( subgroup_number >= 0 AND subgroup_number <= 3),
                    info TEXT)""")

    rows = []
    for filename in os.listdir(PATH_SCHEDULES):
        file = pdfplumber.open(f"{PATH_SCHEDULES}/{filename}")
        for p in file.pages:
            sch = ScheduleGroup(p, f"{PATH_SCHEDULES}/{filename}")
            for i in sch.to_sql():
                rows.append(i)

    cursor.executemany("""INSERT INTO schedule 
    (group_number, lesson_number, day_week, type_week, subgroup_number, info)
    VALUES (?, ?, ?, ?, ?, ?)""", rows)

    con.commit()
