
import pathlib
parent_directory = pathlib.Path(__file__).resolve().absolute().parent
# with open(parent_directory.joinpath("day06inputtest.txt")) as f:
with open(parent_directory.joinpath("day06input.txt")) as f:
    data = f.read().strip()

# for line in data.splitlines():
#for line in data.split("\n\n"):
# print(data)
# print(list(zip(data, data[1:], data[2:], data[3:])))
# print(list(enumerate((zip(data, data[1:], data[2:], data[3:])))))
def fourdifferent(data):
    for i,s in enumerate(zip(data, data[1:], data[2:], data[3:])):
        if len(set(s)) == 4:
            return i

def ndifferent(data, n=4):
    prepdata = []
    for i in range(n):
        prepdata.append(data[i:])
    # print(prepdata)
    for i,s in enumerate(zip(*prepdata)):
        if len(set(s)) == n:
            return i
    return -n-1

def startmarkern(data,n):
    print(ndifferent(line,n) + n)

print("p1:")
for line in data.splitlines():
    startmarkern(data,4)

print("p2:")
for line in data.splitlines():
    startmarkern(data,14)


