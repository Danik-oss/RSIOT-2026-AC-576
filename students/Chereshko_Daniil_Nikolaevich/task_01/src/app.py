import logging
import os
import signal
from flask import Flask, jsonify, request
from redis import Redis
from werkzeug.serving import make_server

STU_ID = os.getenv("STU_ID", "220250")
STU_GROUP = os.getenv("STU_GROUP", "AS-576")
STU_VARIANT = os.getenv("STU_VARIANT", "23")
APP_PORT = int(os.getenv("APP_PORT", "9043"))
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_KEY_PREFIX = os.getenv("REDIS_KEY_PREFIX", "stu:220250:v23")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.before_request
def log_request():
    logger.info("HTTP %s %s from %s", request.method, request.path, request.remote_addr)

@app.route("/live")
def live():
    healthy = False
    try:
        healthy = redis_client.ping()
    except Exception as exc:
        logger.warning("Redis health check failed: %s", exc)
    return (
        jsonify(status="ok", redis=healthy, variant=STU_VARIANT),
        200,
    ) if healthy else (jsonify(status="degraded", redis=healthy, variant=STU_VARIANT), 503)

@app.route("/cache/<key>", methods=["GET"])
def cache_get(key):
    value = redis_client.get(f"{REDIS_KEY_PREFIX}:{key}")
    return jsonify(key=key, value=value), 200

@app.route("/cache/<key>", methods=["POST"])
def cache_set(key):
    payload = request.get_json(silent=True) or {}
    value = payload.get("value", "")
    redis_client.set(f"{REDIS_KEY_PREFIX}:{key}", value)
    return jsonify(key=key, value=value), 201

@app.route("/")
def index():
    return jsonify(
        message="RSIOT Flask app for variant 23",
        student_id=STU_ID,
        student_group=STU_GROUP,
        variant=STU_VARIANT,
    )


def create_app_server() -> make_server:
    server = make_server("0.0.0.0", APP_PORT, app)
    return server


if __name__ == "__main__":
    logger.info(
        "Starting RSIOT app: student=%s group=%s variant=%s port=%s",
        STU_ID,
        STU_GROUP,
        STU_VARIANT,
        APP_PORT,
    )
    server = create_app_server()

    def stop_server(signum, frame):
        logger.info("SIGTERM received, shutting down gracefully")
        server.shutdown()

    signal.signal(signal.SIGTERM, stop_server)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received, shutting down")
    logger.info("Application stopped")
