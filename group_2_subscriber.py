from typing import Any
import paho.mqtt.client as mqtt

MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "comp216_assignment4"


class Assignment4Subscriber:
    def __init__(self, queues, client_id):
        self.client = mqtt.Client(
            client_id=client_id, callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )
        self.client.on_message = self.on_message
        self.queues = queues

    def on_message(
        self, client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage
    ) -> None:
        """Handles incoming MQTT messages."""
        try:
            payload: str = msg.payload.decode("utf-8")
            print(payload)
            for queue in self.queues:
                queue.put(payload)
        except Exception as e:
            print(f"Error in {self.__class__.__name__}.on_message: {e}")

    def subscribe(self, topic) -> None:
        try:
            print(f"Subscribed to {topic}")
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
            self.client.subscribe(f"{MQTT_TOPIC}/{topic}")
            self.client.loop_start()
        except Exception as e:
            print(f"Error in {self.__class__.__name__}.subscribe: {e}")

    def stop(self):
        print("Stopped")
        self.client.loop_stop()
        self.client.disconnect()
