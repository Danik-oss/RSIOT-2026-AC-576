import logging
import os
import signal
from flask import Flask, jsonify, request
from werkzeug.serving import make_server

STU_ID = os.getenv("STU_ID", "220250")
STU_GROUP = os.getenv("STU_GROUP", "AS-576")
STU_VARIANT = os.getenv("STU_VARIANT", "23")
APP_PORT = int(os.getenv("APP_PORT", "9043"))
APP_NAME = os.getenv("APP_NAME", "RSIOT App 23")
APP_ENV = os.getenv("APP_ENV", "production")
API_KEY = os.getenv("API_KEY", "not-set")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.before_request
def log_request():
    logger.info("HTTP %s %s from %s", request.method, request.path, request.remote_addr)

@app.route("/live")
def live():
    return jsonify(status="ok", variant=STU_VARIANT), 200

@app.route("/ready")
def ready():
    ready_state = bool(API_KEY != "not-set")
    if not ready_state:
        logger.warning("Readiness check failed: API_KEY not provided")
    return (
        jsonify(status="ready", api_key_present=ready_state, variant=STU_VARIANT),
        200 if ready_state else 503,
    )

@app.route("/config")
def config_info():
    return jsonify(
        app_name=APP_NAME,
        app_env=APP_ENV,
        student_id=STU_ID,
        student_group=STU_GROUP,
        variant=STU_VARIANT,
    )

@app.route("/")
def index():
    return jsonify(
        message="RSIOT Flask app variant 23",
        student_id=STU_ID,
        student_group=STU_GROUP,
        variant=STU_VARIANT,
    )


def create_app_server() -> make_server:
    server = make_server("0.0.0.0", APP_PORT, app)
    return server


if __name__ == "__main__":
    logger.info(
        "Starting RSIOT app: student=%s group=%s variant=%s port=%s env=%s",
        STU_ID,
        STU_GROUP,
        STU_VARIANT,
        APP_PORT,
        APP_ENV,
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
