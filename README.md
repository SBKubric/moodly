# Moodly
Курсовой проект LearnPython 15.
Проект проводит эмоцианальный анализ по заданному слову среди новостей и комментариев на reddit.com.
 - Анализ производится с помощью VADER Sentiment Analysis ([страница](https://pypi.org/project/vaderSentiment/)).
  - Для работы с reddit испольщуется пакет praw ([страница](https://pypi.org/project/praw/)).
   - Результаты демонстрируются с помощью сайта на Flask.
    - Запуск анализы происходит с помощью Celery.

Весь проект был портирован в Docker, в 4 контейнера (MariaDB, Redis, Celery и Flask). 

## Инструкция для запуска
  - Установить Docker и Docker-compose
  - Перейти в папку `moodly/docker`
  - Создать контейнеры
 ```shell
 sudo docker-compose build
 ```
  - Запустить контейнеры
```shell
sudo docker-compose up
```
  - Запуск контейнеров в режиме демона
```shell
sudo docker-compose up -d
```
  - Остановка контейнеров
```shell
sudo docker-compose down
```

## Инструкция по запуску (без Docker)
  - Перейти в папку `moodly/docker/flask`
  - Установить виртуальное окружение и активировать
```shell
python -m venv venv
venv\Scripts\activate
```
  - Установить зависимости
```shell
pip install -r requirements.txt
```
  - Создать или скопировать файл с настройками сервера
 ```shell
webapp\config.py
```
  - Создать и предварительно заполнить базу данных
```shell
python create_db.py
python create_first_data.py
```
  - Запуск web-приложения
```shell
run.bat
```