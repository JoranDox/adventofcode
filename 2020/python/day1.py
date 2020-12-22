inputs = []
with open("day1input.txt") as inputfile:
    for line in inputfile:
        inputs.append(int(line))

import time
t0 = time.time()

for i in range(len(inputs)):
    for j in range(i, len(inputs)):
        if (inputs[i] + inputs[j]) == 2020:
            t1 = time.time()
            print(inputs[i], inputs[j], inputs[i] * inputs[j])
t2 = time.time()

for i in range(len(inputs)):
    for j in range(i, len(inputs)):
        for k in range(j, len(inputs)):
            if (inputs[i] + inputs[j] + inputs[k]) == 2020:
                print(inputs[i], inputs[j], inputs[k], inputs[i] * inputs[j] * inputs[k])

t3 = time.time()

print(t1 - t0)
print(t3 - t2)
