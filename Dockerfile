FROM python:3.13.3

WORKDIR /app

COPY main.py .
COPY logging_config.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./app/src

CMD ["fastapi", "dev"]