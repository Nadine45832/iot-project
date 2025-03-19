from lib2to3.pygram import pattern_symbols
import random
import math
import matplotlib.pyplot as plt


class DataGenerator:
    def __init__(self, data_range=(0, 1), pattern="random", frequency=0.1, mean=0.5,std_dev=0.1):
        self.min_value = data_range[0]
        self.max_value = data_range[1]
        self.multiplier = data_range[1] - data_range[0]
        self.shift = self.min_value
        self.pattern = pattern
        self.frequency = frequency
        self.mean = mean
        self.std_dev = std_dev
        self.step = 0

    # generate data depends on the pattern
    def __generate(self):
        if self.pattern == "random":
            return random.random()
        elif self.pattern == "sine":
            value = (math.sin(self.step * self.frequency) + 1 / 2)
            self.step += 1
            return value
        elif self.pattern == "gaussian":
            return random.gauss(self.mean, self.std_dev)

    @property
    def value(self):
         raw_value = self.__generate()
         return max(self.min_value, min(self.max_value, raw_value * self.multiplier + self.shift))

 # Visualize
def plot_generated_data(pattern="random"):
    generator = DataGenerator(data_range=(10, 50), pattern=pattern, frequency=0.05)

    data = [generator.value for _ in range(500)]

    plt.plot(data, label=f"Pattern: {pattern}")
    plt.xlabel("Time Step")
    plt.ylabel("Generated Value")
    plt.title(f"Generated Data using {pattern} pattern")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    plot_generated_data("random") 
    plot_generated_data("sine")    
    plot_generated_data("gaussian")