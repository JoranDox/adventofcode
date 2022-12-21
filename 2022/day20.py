
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2022/day20inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2022/day20input.txt")) as f:
    data = f.read().strip()

const = 100001
message = []

# p1 = True
p1 = False
if p1:
    key = 1
    nmixes = 1
else:
    key = 811589153
    nmixes = 10
message = [int(num) * key for num in data.splitlines()]

# print(message)
unique_message = list(enumerate(message))
# print(unique_message)
assert len(set(unique_message)) == len(unique_message)

def makeneighbours(message):
    n = {
        num: {
            "l": l,
            "r": r,
        }
        for l,num,r
        in zip(
            [message[-1]] + message[:-1],
            message,
            message[1:] + [message[0]],
        )
    }
    # n["front"] = message[0]
    return n

def llpop(num, ll):
    left, right = ll[num]["l"], ll[num]["r"]
    # if ll["front"] == num:
        # ll["front"] = right
    del ll[num]
    ll[right]["l"] = left
    ll[left]["r"] = right
    return left, right

def llpush(num, ll, left, right):
    newleft = ll[right]["l"]
    newright = ll[left]["r"]
    assert left == newleft, (left, newright)
    assert right == newright, (right, newleft)
    ll[num] = {
        "l": newleft,
        "r": newright,
    }
    ll[right]["l"] = num
    ll[left]["r"] = num

def llright(num, ll):
    return ll[num]["r"]

def llrightmany(num, ll, intogo):
    intogo = intogo % len(ll)
    if intogo == 0:
        intogo = len(ll)
    for i in range(intogo):
        num = llright(num,ll)
    return num

def llleft(num, ll):
    return ll[num]["l"]

def llleftmany(num, ll, intogo):
    intogo = intogo % len(ll)
    if intogo == 0:
        intogo = len(ll)
    for i in range(intogo):
        num = llleft(num,ll)
    return num

def neightomess(ll, front=None):
    if front is None:
        front = (message.index(0), 0)
    accum = [front]
    r = llright(front, ll)
    while r != front:
        accum.append(r)
        r = llright(r, ll)
    return accum

# print(unique_message)
# print(makeneighbours(unique_message))
# print(neightomess(makeneighbours(unique_message)))

def mix(message, numtimes=1):
    todo = [x for x in message] * numtimes
    neighbours = makeneighbours(message)

    for i in todo:
        val = i[1]
        if val == 0:
            continue
        left, right = llpop(i, neighbours)
        if val > 0:
            newleft = llrightmany(left, neighbours, val)
            newright = llrightmany(right, neighbours, val)
        if val < 0:
            newleft = llleftmany(left, neighbours, -val)
            newright = llleftmany(right, neighbours, -val)

        llpush(i, neighbours, newleft, newright)
        # print(neightomess(neighbours))

    return neightomess(neighbours)

mixed = mix(unique_message, nmixes)
n = makeneighbours(mixed)
front = (message.index(0), 0)
# print(front)
# answer = message[(1000+i0) % len(message)], message[(2000+i0) % len(message)], message[(3000+i0) % len(message)]
answer = llrightmany(front,n,1000)[1], llrightmany(front,n,2000)[1], llrightmany(front,n,3000)[1]
# print(answer)
print(sum(answer))

