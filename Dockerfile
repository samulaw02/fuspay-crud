FROM python:3.8-alpine

WORKDIR /app

COPY . .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["sh", "./start.sh"]

EXPOSE 4000