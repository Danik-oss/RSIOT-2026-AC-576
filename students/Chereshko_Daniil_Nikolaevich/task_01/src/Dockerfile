FROM python:3.12-alpine AS builder
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    python -m pip install --prefix=/install -r requirements.txt

FROM python:3.12-alpine
RUN addgroup -S appgroup && adduser -S -u 65532 -G appgroup appuser
WORKDIR /app
COPY --from=builder /install /usr/local
COPY app.py .
COPY requirements.txt .

EXPOSE 9043
LABEL org.bstu.student.fullname="Черешко Даниил Николаевич"
LABEL org.bstu.student.id="220250"
LABEL org.bstu.group="AS-576"
LABEL org.bstu.variant="23"
LABEL org.bstu.course="RSIOT"

USER appuser
ENV STU_ID=220250 \
    STU_GROUP=AS-576 \
    STU_VARIANT=23 \
    APP_PORT=9043 \
    REDIS_HOST=redis \
    REDIS_PORT=6379 \
    REDIS_KEY_PREFIX=stu:220250:v23

HEALTHCHECK --interval=15s --timeout=5s --retries=3 CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:9043/live').getcode()==200 else 1)"

ENTRYPOINT ["python", "app.py"]
