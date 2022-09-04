# syntax=docker/dockerfile:1
FROM python:3.10.6-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 8080
CMD [ "waitress-serve", "--port=8080" , "--call", "main:get_app"]