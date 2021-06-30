FROM python:3.9

RUN mkdir -p /parser/

WORKDIR /parser/

COPY . /parser/

RUN pip install psycopg2 requests bs4 loguru psycopg2

CMD ["python3", "main_class.py"]
