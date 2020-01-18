# moodly
LP 15 team project

## Инструкция для началы работы
  - Установить виртуальное окружение и активировать
```bat
python -m venv venv
venv\Scripts\activate
```
  - Установить зависимости
```bat
pip install -r requirements.txt
```
  - Создать или скопировать файл с настройками сервера
 ```bat
 webapp\config.py
 ```
  - Создать и предварительно заполнить базу данных
```bat
create_db.bat
python create_first_data.py
```
  - Запуск web-приложения
```bat
run.bat
```
