import json
import paho.mqtt.client as mqtt

from assignment4_util import Assignment4Util


class Assignment4Publisher:
    def __init__(self):
        pass

    def publish(self):
        try:
            client = mqtt.Client()
            client.connect("localhost", 1883)

            data = Assignment4Util.create_data()
            payload = json.dumps(data)
            client.publish("comp216_assignment4", payload)
            print("Sending Data:")
            Assignment4Util.print_data(data)

            client.disconnect()
        except Exception as e:
            print(f"Error in {self.__class__.__name__}.publish: {e}")


if __name__ == "__main__":
    _publisher = Assignment4Publisher()
    _publisher.publish()
