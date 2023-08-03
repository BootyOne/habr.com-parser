FROM python:3.11

COPY Pipfile* /app/

WORKDIR /app
RUN pip install pipenv
RUN pipenv install

COPY . /app

CMD ["pipenv", "run", "python", "src/main.py"]