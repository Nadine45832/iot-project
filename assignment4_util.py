import json
import time
import random
from dataclasses import dataclass, asdict, field


# Utility module
@dataclass
class HealthData:
    id: int = field(default_factory=lambda: Assignment4Util.get_next_id())
    patient: str = field(default_factory=lambda: f"Patient_{random.randint(1, 100)}")
    time: str = field(default_factory=lambda: time.asctime())
    heart_rate: int = field(default_factory=lambda: int(random.gauss(80, 1)))
    respiratory_rate: int = field(default_factory=lambda: int(random.gauss(12, 2)))
    heart_rate_variability: int = field(default_factory=lambda: random.randint(50, 80))
    body_temperature: float = field(
        default_factory=lambda: round(random.gauss(99, 0.5), 2)
    )
    blood_pressure: dict = field(
        default_factory=lambda: {
            "systolic": int(random.gauss(105, 2)),
            "diastolic": int(random.gauss(70, 1)),
        }
    )
    activity: str = field(
        default_factory=lambda: random.choice(
            ["Walking", "Running", "Sleeping", "Sitting"]
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


if __name__ == "__main__":
    _data = Assignment4Util.create_data()
    Assignment4Util.print_data(_data)
