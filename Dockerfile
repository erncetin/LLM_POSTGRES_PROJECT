FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["sh", "-c", "python /app/src/deneme.py && python /app/src/postgres_login.py"]
