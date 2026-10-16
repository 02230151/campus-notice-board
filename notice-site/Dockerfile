FROM python:3.12-alpine AS builder

WORKDIR /build

COPY notices.txt /input/notices.txt
COPY generate.py /build/generate.py

RUN mkdir -p /output && python /build/generate.py


FROM nginx:alpine

ARG VERSION=1.0

LABEL org.opencontainers.image.title="Campus Notice Board"
LABEL org.opencontainers.image.description="Campus student notice board"
LABEL org.opencontainers.image.version="${VERSION}"
LABEL org.opencontainers.image.authors="Tashi D Rinzin"

COPY --from=builder /output/index.html /usr/share/nginx/html/index.html