FROM python:3.10-alpine

WORKDIR /app
COPY requirements.txt /app
RUN apk add ffmpeg curl py3-lxml \
    && pip install -r requirements.txt \
    && addgroup -S python \
    && adduser -S python -G python \
    && chmod -R 777 /app

USER python
COPY --chown=python:python . /app

ARG COMMIT_HASH="none"
ARG COMMIT_TAG="none"
ARG PORT=5000
ENV PORT=$PORT
ENV COMMIT_HASH=$COMMIT_HASH
ENV COMMIT_TAG=$COMMIT_TAG
LABEL commit-hash=$COMMIT_HASH
LABEL commit-tag=$COMMIT_TAG

HEALTHCHECK  --interval=60s --retries=3 \
    CMD curl --fail http://localhost:$PORT/health || kill 1

# ENTRYPOINT [ "gunicorn", "-w 8","-b 0.0.0.0:$PORT" ,"app:app" ]
CMD gunicorn -w 16 -b 0.0.0.0:$PORT app:app
