import json
import threading

from group_2_data_generator import DataGenerator
from group_2_publisher import Assignment4Publisher


def create_publisher(source):
    generator = DataGenerator(
        (source["min"], source["max"]),
        source["pattern"],
        1,
        source["mean"],
        source["std"],
    )
    publicher = Assignment4Publisher(source["name"], generator)
    publicher.start()


if __name__ == "__main__":
    threads = []
    with open("sources.json", "r") as f:
        sources = json.load(f)
        for source in sources:
            publisher_thread = threading.Thread(
                target=create_publisher,
                args=[source],
                daemon=True,
            )
            publisher_thread.start()
            threads.append(publisher_thread)

    for thread in threads:
        thread.join()
