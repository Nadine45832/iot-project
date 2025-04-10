import json
from flask import Flask, Response, jsonify, send_from_directory, stream_with_context
from queue import Queue
from threading import Lock
import uuid

from group_2_subscriber import Assignment4Subscriber

MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "comp216_assignment4"

app = Flask(__name__, static_folder="static")


@app.route("/sources", methods=["GET"])
def get_sources():
    with open("sources.json", "r") as f:
        sources = json.load(f) or []
        return jsonify(
            [
                {"name": s["name"], "topic": s["name"].lower().replace(" ", "_")}
                for s in sources
            ]
        )


topics = {}
topics_lock = Lock()


def subscribe(topic):
    q = Queue()

    with topics_lock:
        if topic not in topics:
            queues = []
            subscriber = Assignment4Subscriber(queues, f"{uuid.uuid4()}")
            topics[topic] = {"client": subscriber, "queues": queues}
            subscriber.subscribe(topic)

    queues = topics[topic]["queues"]
    queues.append(q)

    print(f"{topic} with queue: {len(queues)}")

    try:
        while True:
            message = q.get()
            yield f"data: {message}\n\n"
    except GeneratorExit:
        queues.remove(q)

        if len(queues) == 0:
            topics[topic]["client"].stop()
            topics.pop(topic)


# Server Side Events subscribtion
@app.route("/events/<topic>", methods=["GET"])
def get_events(topic):
    return Response(
        stream_with_context(subscribe(topic)),
        headers={"Content-Type": "text/event-stream"},
    )


@app.route("/", methods=["GET"])
def index():
    return send_from_directory("static", "index.html")


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8081)
