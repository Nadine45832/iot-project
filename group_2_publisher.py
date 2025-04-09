import json
import random
import time
import paho.mqtt.client as mqtt

from group_2_util import Assignment4Util


MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "comp216_assignment4"


class Assignment4Publisher:
    def __init__(self):
        pass

    def publish(self):
        try:
            client_id = "nadzeya_published_23145"
            client = mqtt.Client(
                mqtt.CallbackAPIVersion.VERSION2,
                client_id=client_id,
            )
            client.connect(MQTT_BROKER, MQTT_PORT)

            data = Assignment4Util.create_data()
            payload = json.dumps(data)
            client.publish(MQTT_TOPIC, payload)
            print("Sending Data:")
            Assignment4Util.print_data(data)

            client.disconnect()
        except Exception as e:
            print(f"Error in {self.__class__.__name__}.publish: {e}")


if __name__ == "__main__":
    _publisher = Assignment4Publisher()
    while True:
        if random.random() > 0.2:
            _publisher.publish()
        time.sleep(1)
