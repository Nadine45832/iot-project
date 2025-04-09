import threading

from group_2_publisher import Assignment4Publisher
from group_2_subscriber import Assignment4Subscriber
import time


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
