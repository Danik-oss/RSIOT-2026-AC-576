FROM python:3.12-alpine AS builder
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    python -m pip install --prefix=/install -r requirements.txt

FROM python:3.12-alpine
COPY --from=builder /install /usr/local
COPY app.py .
COPY requirements.txt .
RUN adduser -u 10001 -D appuser
USER appuser
WORKDIR /app

EXPOSE 9032
LABEL org.bstu.student.fullname="Черешко Даниил Николаевич"
LABEL org.bstu.student.id="220250"
LABEL org.bstu.group="AS-576"
LABEL org.bstu.variant="26"
LABEL org.bstu.course="RSIOT"

USER appuser
ENV STU_ID=220250 \
    STU_GROUP=RSIOT-2026 \
    STU_VARIANT=26 \
    APP_PORT=9032

HEALTHCHECK --interval=15s --timeout=5s --retries=3 CMD curl -f http://localhost:9032/health || exit 1

ENTRYPOINT ["python", "app.py"]
