FROM python:3.9.13-alpine

# Установите рабочую директорию внутри контейнера
WORKDIR /usr/src/app

# Копируйте файлы requirements.txt в рабочую директорию
COPY requirements.txt ./

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируйте остальные файлы проекта в рабочую директорию
COPY . .

# Определите команду для запуска сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
