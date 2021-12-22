FROM python:3.10-alpine

WORKDIR /app
COPY requirements.txt /app
RUN apk add ffmpeg curl\
    && pip install -r requirements.txt \
    && addgroup -S python \
    && adduser -S python -G python

USER python
COPY --chown=python:python . /app

HEALTHCHECK  --interval=60s --retries=3 \
    CMD curl --fail http://localhost:5000/health || kill 1

ENTRYPOINT [ "gunicorn", "-w 8","-b 0.0.0.0:5000" ,"app:app" ]
