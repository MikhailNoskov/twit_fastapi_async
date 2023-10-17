FROM python:3.11

WORKDIR /app

COPY ./requirements.txt ./
RUN apt-get update && apt-get install -y python3-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .