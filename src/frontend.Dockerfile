FROM python:3.13.11-alpine3.23

WORKDIR /code

COPY ../requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src/frontend/publish /code/publish

CMD ["fastapi", "run", "publish/react_server.py", "--port", "80"]