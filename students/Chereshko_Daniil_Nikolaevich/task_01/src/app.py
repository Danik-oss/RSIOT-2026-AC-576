import logging
import os
import signal
from flask import Flask, jsonify, request
from werkzeug.serving import make_server

STU_ID = os.getenv("STU_ID", "220250")
STU_GROUP = os.getenv("STU_GROUP", "AS-576")
STU_VARIANT = os.getenv("STU_VARIANT", "26")
APP_PORT = int(os.getenv("APP_PORT", "9032"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.before_request
def log_request():
    logger.info("HTTP %s %s from %s", request.method, request.path, request.remote_addr)

@app.route("/health")
def health():
    return jsonify(status="ok", variant=STU_VARIANT), 200

@app.route("/ready")
def ready():
    return jsonify(status="ready", variant=STU_VARIANT), 200

@app.route("/")
def index():
    return jsonify(
        message="RSIOT Flask app for variant 26",
        student_id=STU_ID,
        student_group=STU_GROUP,
        variant=STU_VARIANT,
    )


def create_app_server() -> make_server:
    server = make_server("0.0.0.0", APP_PORT, app)
    return server


if __name__ == "__main__":
    logger.info("Starting RSIOT app: student=%s group=%s variant=%s port=%s", STU_ID, STU_GROUP, STU_VARIANT, APP_PORT)
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
