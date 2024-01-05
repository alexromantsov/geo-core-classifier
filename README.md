# GeoCoreClassifier

**GeoCoreClassifier** - это приложение на Python, предназначено для геологов, работающих с керном. "GeoCoreClassifier" использует передовые алгоритмы машинного обучения для анализа и классификации текстовых описаний керна, предоставленных геологами.

## Установка


1. Установите Python версии 3.9 или выше.
2. Клонируйте репозиторий GeoCoreClassifier
3. Перейдите в папку проекта:
```bash
cd geo-core-classifier
```

4. Установите необходимые зависимости:
```bash
pip install -r requirements.txt
```

## Запуск сервера
```bash
python manage.py runserver
```



### Создание requirements.txt

```bash
pip freeze > requirements.txt
```

### Выполнения миграций 
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
### Создание суперпользователя (superuser)
```bash
python manage.py createsuperuser
```

### Сгенерировать тестовые описания керна
```bash
python manage.py generate_core_descriptions
```

## Сборка образа Docker 
```bash
docker build -t romanrsov/geo-core-classifier:latest .
```

### Загрузка образа Docker
```
docker pull romanrsov/geo-core-classifier:latest
```

### Запуск контейнера
```
docker run -d -p 8008:8000 --name geo-core-classifier romanrsov/geo-core-classifier:latest
```