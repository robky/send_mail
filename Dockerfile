FROM python:2.7-slim
WORKDIR app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /app
RUN pip install -U pip
RUN pip install -r /app/requirements.txt --no-cache-dir
COPY . .
