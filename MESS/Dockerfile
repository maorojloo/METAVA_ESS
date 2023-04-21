FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /django

COPY requirements.txt /django/
RUN pip install -r requirements.txt

COPY . /django/

EXPOSE 8000 











