FROM python:3.9-slim-buster

# Ustawienie katalogu roboczego
WORKDIR /WysokiPoziom

# Kopiowanie plików z aplikacji do katalogu roboczego
COPY . /WysokiPoziom

# Instalacja wymaganych pakietów
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Ustawienie zmiennych środowiskowych
ENV DJANGO_SETTINGS_MODULE=myproject.settings
ENV PYTHONPATH /WysokiPoziom
# ENV DJANGO_SECRET_KEY=mysecretkey

# Migracja bazy danych
RUN python manage.py makemigrations
RUN python manage.py migrate

# Ustawienie komendy startowej
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]