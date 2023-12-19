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
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте файлы проекта в контейнер
COPY . /app

# Expose the port the app will run on
EXPOSE 8000

# Создайте скрипт для запуска Django команд и сервера
RUN echo "#!/bin/sh" > /app/run.sh
RUN echo "python3 manage.py collectstatic --noinput" >> /app/run.sh
RUN echo "python3 manage.py makemigrations" >> /app/run.sh
RUN echo "python3 manage.py migrate" >> /app/run.sh
RUN echo "python3 manage.py runserver 0.0.0.0:8000" >> /app/run.sh
RUN echo "chmod 777 /app/static" >> /app/run.sh
RUN echo "chmod 777 /app/media" >> /app/run.sh
RUN chmod +x /app/run.sh

# Определите команду для запуска скрипта
CMD ["/app/run.sh"]
