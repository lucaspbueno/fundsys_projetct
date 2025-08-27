FROM python:3.13.3

WORKDIR /fundsys_project

COPY main.py .
COPY logging_config.py .
COPY poetry.lock .
COPY pyproject.toml .
COPY entrypoint.sh /fundsys_project/entrypoint.sh

RUN chmod +x /fundsys_project/entrypoint.sh

RUN pip install --no-cache-dir poetry && \
poetry config virtualenvs.create false && \
poetry install

COPY ./app ./fundsys_project/app

EXPOSE 8000

CMD ["fastapi", "dev"]
