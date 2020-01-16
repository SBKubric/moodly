# moodly
LP 15 team project

## Инструкция для началы работы
  - Установить виртуальное окружение и активировать
`python -m venv venv`
`venv\Scripts\activate`
  - Установить зависимости
`pip install -r requirements.txt`
  - Создать или скопировать файл с настройками сервера
 `webapp\config.py`
  - Создать и предварительно заполнить базу данных
`python create_db.py`
`python create_first_data.py`
  - Запуск web-приложения
`run.bat`