import random
import math
import matplotlib.pyplot as plt


class DataGenerator:
    def __init__(
        self,
        data_range=(0, 1),
        pattern="random",
        frequency=0.1,
        mean=0.5,
        std_dev=0.1,
    ):
        self.min_value = data_range[0]
        self.max_value = data_range[1]
        self.multiplier = data_range[1] - data_range[0]
        self.shift = self.min_value
        self.middle = (self.min_value + self.max_value) / 2
        self.pattern = pattern
        self.frequency = frequency
        self.mean = mean
        self.std_dev = std_dev
        self.step = 0
        self.current_amplitude = 1.0
        self.random_walk = 0.0

    # generate data depends on the pattern
    def __generate(self):
        if self.pattern == "random":
            return self.signal_random()
        elif self.pattern == "sine":
            return self.signal_shine()
        elif self.pattern == "gaussian":
            return self.signal_gaussian()
        elif self.pattern == "value_with_random_noise":
            return self.value_with_random_noise()
        elif self.pattern == "random_signal_with_noise":
            return self.random_signal_with_noise()

    def random_signal_with_noise(self):
        sine_wave = math.sin(math.pi * self.step)
        self.random_walk += random.gauss(0, self.frequency)
        self.current_amplitude = 1 + 0.5 * (sine_wave + self.random_walk)
        self.current_amplitude = max(
            self.min_value, min(self.max_value, self.current_amplitude)
        )
        signal = self.current_amplitude + random.gauss(0, self.std_dev)
        return self.mean + signal

    def value_with_random_noise(self):
        sine_wave = math.sin(math.pi * self.step)
        self.random_walk += random.gauss(0, self.frequency)
        self.current_amplitude = 1 + 0.5 * (sine_wave + self.random_walk)
        self.current_amplitude = max(
            self.min_value, min(self.max_value, self.current_amplitude)
        )
        signal = self.current_amplitude * random.gauss(0, self.std_dev)
        return self.mean + signal

    def signal_gaussian(self):
        return max(
            self.min_value,
            min(
                self.max_value,
                random.gauss(self.mean, self.std_dev) * self.multiplier + self.shift,
            ),
        )

    def signal_shine(self):
        raw_value = (
            math.sin(self.step * self.frequency) * self.multiplier / 2 + self.middle
        )
        return raw_value

    def signal_random(self):
        return max(
            self.min_value,
            min(self.max_value, random.random() * self.multiplier + self.shift),
        )

    @property
    def value(self):
        self.step += 1
        raw_value = self.__generate()
        return raw_value


# Visualize
def plot_generated_data(
    pattern="random", data_range=(10, 50), frequency=0.5, std_dev=0.1
):
    generator = DataGenerator(
        data_range=data_range,
        pattern=pattern,
        frequency=frequency,
        std_dev=std_dev,
    )
    data = [generator.value for _ in range(500)]
    plt.plot(data, label=f"Pattern: {pattern}", color="green")
    plt.xlabel("Time Step")
    plt.ylabel("Generated Value")
    plt.title(f"Generated Data using {pattern} pattern")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    plot_generated_data("random")
    plot_generated_data("sine")
    plot_generated_data("gaussian")
    plot_generated_data(
        "value_with_random_noise",
        std_dev=1,
        data_range=(-50, 50),
        frequency=2,
    )
    plot_generated_data(
        "random_signal_with_noise",
        std_dev=1,
        data_range=(-50, 50),
        frequency=1,
    )
