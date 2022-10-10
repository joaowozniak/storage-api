FROM python:3.8

WORKDIR /code

COPY ./src /code/src
COPY ./requirements.txt /code

RUN pip install --no-cache-dir -r /code/requirements.txt

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]