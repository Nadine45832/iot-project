import json
import threading
import time
from typing import Any
import paho.mqtt.client as mqtt

from group_2_publisher import Assignment4Publisher
from group_2_util import Assignment4Util


class Assignment4Subscriber:
    def __init__(self):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_message = self.on_message

    def on_message(
        self, client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage
    ) -> None:
        """Handles incoming MQTT messages."""
        try:
            payload: str = msg.payload.decode("utf-8")
            data: dict[str, Any] = json.loads(payload)
            print("Received Data:")
            Assignment4Util.print_data(data)
        except Exception as e:
            print(f"Error in {self.__class__.__name__}.on_message: {e}")

    def subscribe(self) -> None:
        try:
            self.client.connect("broker.hivemq.com", 1883, 60)
            self.client.subscribe("comp216_assignment4")
            print("Subscribed to topic: comp216_assignment4")
            self.client.loop_forever()
        except Exception as e:
            print(f"Error in {self.__class__.__name__}.subscribe: {e}")


if __name__ == "__main__":
    subscriber = Assignment4Subscriber()
    subscriber_thread = threading.Thread(
        target=subscriber.subscribe,
        daemon=True,
    )
    subscriber_thread.start()
    publisher = Assignment4Publisher()
    for _ in range(10):
        publisher.publish()
        time.sleep(1)
