import random

numbers = list(range(1, 129))

random.shuffle(numbers)

file_name = "rng_data.txt"

with open(file_name, "w") as file:
    for number in numbers:
        file.write(str(number) + "\n")