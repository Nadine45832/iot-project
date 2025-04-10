import json
import random
import time
import paho.mqtt.client as mqtt
import uuid

from group_2_util import Assignment4Util
from group_2_data_generator import DataGenerator


MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "comp216_assignment4"


class Assignment4Publisher:
    def __init__(self, name: str, generator: DataGenerator):
        self.name = name
        self.generator = generator
        self.topic = f"{MQTT_TOPIC}/{self.name.lower().replace(' ', '_')}"

    def start(self):
        try:
            client_id = f"{uuid.uuid4()}"
            client = mqtt.Client(
                mqtt.CallbackAPIVersion.VERSION2,
                client_id=client_id,
            )
            client.connect(MQTT_BROKER, MQTT_PORT)
            while True:
                if random.random() > 0.01:
                    data = {
                        "name": self.name,
                        "value": self.generator.value,
                        "timestamp": time.time(),
                    }
                    payload = json.dumps(data)
                    client.publish(self.topic, payload)
                    print(f"Sending Data: {self.topic}")
                    Assignment4Util.print_data(data)
                time.sleep(1)
        except Exception as e:
            print(f"Error in {self.__class__.__name__}.publish: {e}")
