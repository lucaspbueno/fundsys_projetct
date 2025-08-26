FROM python:3.13.3

WORKDIR /projeto-fundsys

COPY main.py .
COPY logging_config.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./projeto-fundsys/src

CMD ["fastapi", "dev"]