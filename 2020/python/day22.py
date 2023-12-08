from collections import deque
import copy

infilename = "day22input.txt"
# infilename = "day22inputex.txt"
# infilename = "day22inputexinf.txt"

with open(infilename) as infile:
    deck1, deck2 = infile.read().strip().split("\n\n")

deck1 = deque([int(n) for n in deck1.split("\n")[1:]])
deck2 = deque([int(n) for n in deck2.split("\n")[1:]])

print(deck1, deck2)

print(tuple(deck1), tuple(deck2))


def oneround(deck1, deck2):
    if (c1 := deck1.popleft()) > (c2 := deck2.popleft()):
        deck1.append(c1)
        deck1.append(c2)
    else:
        deck2.append(c2)
        deck2.append(c1)
    return deck1 and deck2


def score(d):
    accum = 0
    counter = 1
    while d:
        accum += d.pop() * counter
        counter += 1
    return accum


# part 1
# while oneround(deck1, deck2):
#     # print(deck1, deck2)
#     pass
# print("part 1")
# print(deck1, deck2)
# print(score(deck1), score(deck2))


def game(deck1, deck2, depth=0):
    knownconfigs = set()

    while deck1 and deck2:
        checktuple = (tuple(deck1), tuple(deck2))
        # print(checktuple)
        if checktuple in knownconfigs:
            print("player1 wins through repeated config")
            return True
        else:
            knownconfigs |= set((checktuple,))
            if depth == 0:
                print(len(knownconfigs))

        c1 = deck1.popleft()
        c2 = deck2.popleft()

        if c1 <= len(deck1) and c2 <= len(deck2):
            # True = player1, False = player2
            subdeck1 = deque(tuple(deck1)[:c1])
            subdeck2 = deque(tuple(deck2)[:c2])
            print("recursing")
            roundwinner = None
            while roundwinner is None:
                roundwinner = game(subdeck1, subdeck2, depth + 1)
        else:
            # True = player1, False = player2
            roundwinner = c1 > c2

        assert type(roundwinner) == bool

        if roundwinner:
            # print(f"{depth=} player 1 wins")
            deck1.append(c1)
            deck1.append(c2)
        else:
            # print(f"{depth=} player 2 wins")
            deck2.append(c2)
            deck2.append(c1)

    if deck1:
        return True
    else:
        return False


print("part2")
game(deck1, deck2)
print(deck1, deck2)
print(score(deck1), score(deck2))
