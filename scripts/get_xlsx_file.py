import os

import openpyxl
import pdfplumber

from parser import ScheduleGroup

PATH_SCHEDULES = "schedules"

if __name__ == "__main__":
    data = []
    for filename in os.listdir(PATH_SCHEDULES):
        file = pdfplumber.open(f"{PATH_SCHEDULES}/{filename}")

        for p in file.pages:
            sch = ScheduleGroup(p, f"{PATH_SCHEDULES}/{filename}")
            for i in sch.to_sql():
                data.append(i)

        workbook = openpyxl.Workbook()
        sheet = workbook.active

        for row_index, row_data in enumerate(data, start=1):
            for column_index, cell_value in enumerate(row_data, start=1):
                sheet.cell(row=row_index, column=column_index, value=cell_value)

        workbook.save('files/schedule.xlsx')