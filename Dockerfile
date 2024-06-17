# Используем официальный образ Python 3.10
FROM python:3.10-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем зависимости для выполнения команд
RUN apt-get update && apt-get install -y libpq-dev build-essential
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app
COPY . /app

RUN pip install flask
RUN pip install blinker
RUN pip install click
RUN pip install colorama
RUN pip install et-xmlfile
RUN pip install gunicorn
RUN pip install itsdangerous
RUN pip install Jinja2
RUN pip install MarkupSafe
RUN pip install mysql-connector-python
RUN pip install openpyxl
RUN pip install packaging
RUN pip install Werkzeug
RUN pip install flask-cors



# Копируем остальные файлы приложения
#COPY . .

# Открываем порт, на котором будет работать приложение
EXPOSE 5000

# Команда для запуска приложения
CMD ["python", "run.py"]
