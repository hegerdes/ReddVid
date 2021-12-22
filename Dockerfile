FROM python:3.10-alpine

WORKDIR /app
COPY requirements.txt /app
RUN apk add ffmpeg curl\
    && pip install -r requirements.txt \
    && addgroup -S python \
    && adduser -S python -G python \
    && chmod -R 777 /app

USER python
COPY --chown=python:python . /app

HEALTHCHECK  --interval=60s --retries=3 \
    CMD curl --fail http://localhost/health || kill 1

# ENTRYPOINT [ "gunicorn", "-w 8","-b 0.0.0.0:5000" ,"app:app" ]
CMD [ "gunicorn", "-w 2","-b 0.0.0.0:80" ,"app:app" ]
