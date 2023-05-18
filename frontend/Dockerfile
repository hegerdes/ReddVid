FROM node:18-alpine as build

ARG BACKEND="https://reddvid-api.henrikgerdes.me"
ENV BACKEND_URL=$BACKEND
ENV NODE_OPTIONS=--openssl-legacy-provider

WORKDIR /build
COPY package*.json /build/
RUN npm install

COPY . /build
RUN npm run generate


FROM nginx:1.24-alpine
ARG COMMIT_HASH="none"
ARG COMMIT_TAG="none"
ENV COMMIT_HASH=$COMMIT_HASH
ENV COMMIT_TAG=$COMMIT_TAG
LABEL commit-hash=$COMMIT_HASH
LABEL commit-tag=$COMMIT_TAG

HEALTHCHECK --interval=60s --retries=3 \
    CMD curl --fail http://localhost:80 || kill 1

COPY --from=build /build/dist /usr/share/nginx/html/
