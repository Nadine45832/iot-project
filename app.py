import json
from typing import Any
from flask import Flask, jsonify
import paho.mqtt.client as mqtt
from group_2_util import Assignment4Util

MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "comp216_assignment4"


# MQTT Message Handler
def on_message(
    client: mqtt.Client,
    userdata: Any,
    msg: mqtt.MQTTMessage,
) -> None:
    try:
        payload: str = msg.payload.decode("utf-8")
        data: dict[str, Any] = json.loads(payload)
        print("📥 Received Data:")
        Assignment4Util.print_data(data)
    except Exception as e:
        print(f"❌ Error in on_message: {e}")


# MQTT Connection Handler
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"[MQTT] Connected with result code {rc}")
    if rc == 0:
        print("[MQTT] Connection successful ✅")
        client.subscribe(MQTT_TOPIC)
        print(f"[MQTT] Subscribed to topic: {MQTT_TOPIC}")
    else:
        print("[MQTT] Connection failed ❌")


def create_subscriber():
    client_id = "nadzeya_subscriber_23145"  # Unique ID for subscriber
    mqtt_client = mqtt.Client(
        client_id=client_id,
        protocol=mqtt.MQTTv311,
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    )

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    # Connect to broker
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    mqtt_client.subscribe(MQTT_TOPIC)

    # Start the MQTT loop in a background thread
    mqtt_client.loop_start()


# Flask App Setup
def create_app():
    app = Flask(__name__)

    @app.route("/", methods=["GET"])
    def root():
        return jsonify({"message": "MQTT Flask app is running and subscribed!"})

    return app


# Run Flask App (for development)
if __name__ == "__main__":
    app = create_app()
    create_subscriber()
    app.run(debug=True)
