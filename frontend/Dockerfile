FROM node:18-alpine as build

ARG BACKEND="https://reddvid-api.henrikgerdes.me"
ENV BACKEND_URL=$BACKEND
ENV NODE_OPTIONS=--openssl-legacy-provider

WORKDIR /build
COPY . /build

RUN npm install
RUN npm run generate


FROM nginx:1.23
ARG COMMIT_HASH="none"
ARG COMMIT_TAG="none"
ENV COMMIT_HASH=$COMMIT_HASH
ENV COMMIT_TAG=$COMMIT_TAG
LABEL commit-hash=$COMMIT_HASH
LABEL commit-tag=$COMMIT_TAG


COPY --from=build /build/dist /usr/share/nginx/html/
