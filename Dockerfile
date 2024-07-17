FROM python:3.12.4-alpine3.20

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

CMD ["flask", "--app", "main.py", "run", "--host", "0.0.0.0"]