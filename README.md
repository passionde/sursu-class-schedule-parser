# Расписание Сургутского Государственного Университета (СурГУ)

Этот проект представляет собой парсер расписания для Сургутского Государственного Университета. С помощью данного скрипта вы можете создавать файлы Excel (.xlsx) и базу данных SQLite (.db) на основе расписания, предоставленного на [официальном сайте СурГУ](https://www.surgu.ru/ucheba/raspisanie/ochnaya-forma-obucheniya).

## Установка зависимостей

Для установки всех необходимых зависимостей выполните следующую команду:

```bash
pip install -r requirements.txt
```

## Получение файла Excel

Чтобы создать файл Excel с расписанием, выполните следующую команду:

```bash
python scripts/get_xlsx_file.py
```

Этот скрипт соберет расписание из PDF-файлов, которые должны быть предварительно скачаны с [официального сайта СурГУ](https://www.surgu.ru/ucheba/raspisanie/ochnaya-forma-obucheniya) и помещены в папку `schedules`. Затем он создаст файл `schedule.xlsx` в директории `files`, содержащий расписание в формате Excel.

## Выгрузка в базу данных SQLite

Для загрузки данных из PDF-расписания в базу данных SQLite выполните следующую команду:

```bash
python scripts/upload_to_db.py
```

Этот скрипт соберет расписание из PDF-файлов, которые должны быть предварительно скачаны с [официального сайта СурГУ](https://www.surgu.ru/ucheba/raspisanie/ochnaya-forma-obucheniya) и помещены в папку `schedules`, а затем загрузит данные в базу данных SQLite `schedule.db` в директории `files`.

## Примечание

Убедитесь, что перед запуском скрипта все PDF-файлы с расписанием скачаны и находятся в папке `schedules`.

## Зависимости

Все зависимости проекта указаны в файле `requirements.txt`. Установите их, как указано выше, чтобы гарантировать корректное выполнение скриптов.