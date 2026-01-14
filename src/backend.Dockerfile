FROM python:3.13.11-alpine3.23

WORKDIR /code

COPY ../requirements.txt /code/requirements.txt

COPY ../.env /code/.env

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src/backend /code/app

CMD ["fastapi", "run", "app/api_server.py", "--port", "80"]