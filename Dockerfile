FROM python:3.8-slim

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD requirements.txt /
RUN pip install --no-cache-dir  -r requirements.txt && apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

COPY . src
WORKDIR /src

RUN mkdir -p media

ENTRYPOINT ["python", "server.py"]
