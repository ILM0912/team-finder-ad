FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD python manage.py migrate && \
    # можно убрать эту строчку если не нужны тестовые данные
    python manage.py loaddata db.json && \
    python manage.py collectstatic --noinput && \
    gunicorn team_finder.wsgi:application --bind 0.0.0.0:8000