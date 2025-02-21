FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PYTHONPATH=/app/src

CMD ["sh", "-c", "python /app/src/postgres_login.py && streamlit run /app/src/streamlit_run.py"]