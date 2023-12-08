realinput = 14788856, 19316454

exampleinput = 5764801, 17807724

card, door = exampleinput
card, door = realinput
print(card, door)


def loop(iters, value=1, subnum=7):
    return (value * pow(subnum, iters, 20201227)) % 20201227


def confirmloopsize(iters, key):
    return loop(iters) == key


print(confirmloopsize(8, card))
print(confirmloopsize(11, door))

i = 1
cardkey = doorkey = None
while cardkey is None or doorkey is None:
    res = loop(i)
    # print(i,res)
    if res == card:
        cardkey = i
        print("found card", cardkey, res)
    if res == door:
        doorkey = i
        print("found door", doorkey, res)
    i += 1
print(cardkey, doorkey)
print(loop(cardkey, subnum=door))
