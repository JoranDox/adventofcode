filename = "day13input.txt"
filename = "day13inputex.txt"
with open(filename) as infile:
    inputs = infile.read().split("\n")
    startstamp = int(inputs[0])
    busses = [int(bus) for bus in inputs[1].split(",") if bus != "x"]
    bussespart2 = [
        (lambda x: int(x) if x != "x" else 0)(bus) for bus in inputs[1].split(",")
    ]
    print(busses)
    print(bussespart2)
    for bus in bussespart2:
        if bus == "x":
            bus = None
print(bussespart2)


def checkbusses(timestamp):
    for bus in busses:
        if not timestamp % bus:
            print(startstamp, timestamp, bus, (timestamp - startstamp) * bus)
            return True
    return False


timestamp = startstamp
while not checkbusses(timestamp):
    timestamp += 1


# part2
def checkbussespart2(timestamp):
    for t in range(len(bussespart2)):
        bus = bussespart2[t]
        # print(bussespart2, timestamp, t, bus)
        if bus and ((timestamp + t) % bus):
            return False
    print(timestamp, t, timestamp + t, "yess")
    return True


timestamp = 0
incr = max(bussespart2)
timestamp = -bussespart2.index(incr)


# while not checkbussespart2(timestamp):
#     timestamp += incr
#     # if timestamp >= 1068781:
#     #     break
#     if not timestamp % 1000000:
#         print(timestamp, len(bussespart2), timestamp + len(bussespart2))

# from https://rosettacode.org/wiki/Chinese_remainder_theorem#Python
# Python 3.6
from functools import reduce


def chinese_remainder(n, a):
    # n = list of numbers
    # a = list of accompanying remainders
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


n = busses
a = [-bussespart2.index(x) for x in n]
cr = chinese_remainder(n, a)
print(cr, len(bussespart2), cr + len(bussespart2) - 1)
