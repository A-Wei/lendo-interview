FROM python:3.9-slim

RUN apt-get update && apt-get install -y curl python-dev gcc make
RUN pip3 install poetry==1.1.*

COPY poetry.lock pyproject.toml /

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-dev

COPY . /

ENTRYPOINT ["python3", "jobs.py"]
