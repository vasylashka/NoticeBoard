FROM python:3.10-slim

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv

RUN pipenv install --deploy --ignore-pipfile

COPY . /app

EXPOSE 80

ENV NAME World

CMD ["python", "app.py"]