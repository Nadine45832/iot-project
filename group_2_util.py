import json
import time
import random
from dataclasses import dataclass, asdict, field

from group_2_data_generator import DataGenerator


@dataclass
class HealthData:
    id: int = field(default_factory=lambda: Assignment4Util.get_next_id())
    user: str = field(default_factory=lambda: f"User_{random.randint(1, 100)}")
    time: str = field(default_factory=lambda: time.asctime())
    temperature: int = field(
        default_factory=lambda: int(
            DataGenerator(
                data_range=(-10, 40), pattern="sine", mean=15, std_dev=5
            ).value
        )
    )
    humidity: int = field(
        default_factory=lambda: int(
            DataGenerator(
                data_range=(20, 100), pattern="random", mean=60, std_dev=10
            ).value
        )
    )
    pressure: int = field(
        default_factory=lambda: int(
            DataGenerator(
                data_range=(980, 1050),
                pattern="gaussian",
                mean=1015,
                std_dev=5,
            ).value
        )
    )
    air_quality_index: float = field(
        default_factory=lambda: round(
            DataGenerator(
                data_range=(0, 200), pattern="random", mean=50, std_dev=20
            ).value,
            2,
        )
    )
    condition: str = field(
        default_factory=lambda: random.choice(
            [
                "Sunny",
                "Cloudy",
                "Rainy",
                "Partly Cloudy",
                "Thunderstorm",
                "Snowy",
            ]
        )
    )
    wind: dict = field(
        default_factory=lambda: {
            "speed": int(
                DataGenerator(
                    data_range=(0, 50), pattern="random", mean=20, std_dev=10
                ).value
            ),
            "direction": str(
                random.choice(["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
            ),
        }
    )
    location: str = field(
        default_factory=lambda: random.choice(
            ["Toronto", "Vancouver", "Ottawa", "Calgary"]
        )
    )


# Utility module
class Assignment4Util:
    def __init__(self):
        pass

    start_id = 111

    @staticmethod
    def get_next_id() -> int:
        Assignment4Util.start_id += 1
        return Assignment4Util.start_id

    @staticmethod
    def create_data() -> dict:
        """Generates structured health data."""
        return asdict(HealthData())

    @staticmethod
    def print_data(data: dict) -> None:
        """Prints structured data in a readable format."""
        print(json.dumps(data, indent=4))


class DataSources:
    def __init__(self):
        self.sources = []
        self.data_generators = {}

    def load(self, config_file="sources.json"):
        with open(config_file, "r") as f:
            self.sources = json.load(f)
            for source in self.sources:
                dg = DataGenerator(
                    (source["min"], source["max"]),
                    source["pattern"],
                    1,
                    source["mean"],
                    source["std"],
                )
                self.data_generators[source["name"]] = dg

            return self.data_generators


if __name__ == "__main__":
    _data = Assignment4Util.create_data()
    Assignment4Util.print_data(_data)

    ds = DataSources()
    sources = ds.load()

    for name, generator in sources.items():
        print(f"Values for {name}: ")
        for _ in range(0, 10):
            print(generator.value)
