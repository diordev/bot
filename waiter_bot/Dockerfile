# Установите базовый образ Python
FROM python:3.11

# Установите рабочую директорию в контейнере
WORKDIR /app

# Установите переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Скопируйте только файл requirements.txt
COPY requirements.txt /app/

# Установите зависимости проекта
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Скопируйте файлы проекта в контейнер
COPY . /app

# Создайте скрипт для запуска Django команд и сервера
RUN echo "#!/bin/sh" > /app/run.sh
RUN echo "python3 app.py" >> /app/run.sh
RUN chmod +x /app/run.sh

# Определите команду для запуска скрипта
CMD ["/app/run.sh"]
