from flask import Flask
import os
import redis

app = Flask(__name__)

board_name = os.environ.get("BOARD_NAME", "Campus Notice Board")
redis_host = os.environ.get("REDIS_HOST", "redis")
version = os.environ.get("APP_VERSION", "1.0")

r = redis.Redis(host=redis_host, port=6379, decode_responses=True)


@app.route("/")
def count_view():
    count = r.incr("views")

    return f"""
    <h1>{board_name}</h1>
    <p>Views: {count}</p>
    <p>Version: {version}</p>
    """


@app.route("/health")
def health():
    try:
        r.ping()
        return "healthy", 200
    except Exception:
        return "unhealthy", 503


app.run(host="0.0.0.0", port=5000)