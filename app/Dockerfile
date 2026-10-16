# Purpose: one source tree, three images (1.0.0, 1.1.0, 1.2.0-broken) via build args.
FROM python:3.12-alpine
ARG APP_VERSION=1.0.0
ARG STUDENT_ID=unknown
ARG BROKEN=false
ENV APP_VERSION=$APP_VERSION STUDENT_ID=$STUDENT_ID BROKEN=$BROKEN
RUN adduser -D -u 10001 appuser
WORKDIR /app
COPY app.py .
USER 10001
EXPOSE 8080
CMD ["python", "-u", "app.py"]