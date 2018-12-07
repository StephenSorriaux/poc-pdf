FROM python:3.6-slim

ENV HOST="0.0.0.0"
ENV PORT="5000"

WORKDIR /usr/src

RUN apt-get update \
 && mkdir -p /usr/share/man/man1 \
 && apt-get install -y openjdk-8-jdk \
 && rm -rf /var/lib/apt/lists/*

COPY . ./

RUN pip install -r requirements.txt

CMD ["python", "app.py"]