# with open("day04inputtest.txt") as f:
with open("thorvaldday4.txt") as f:
    # with open("day04input.txt") as f:
    data = f.read()

data = data.split("\n\n")
# print(len(data))


def notint(i):
    i = int(i)
    if i == 0:
        return 9999
    return i


numbers = [notint(i) for i in data[0].split(",")]


bingocards = [
    [[notint(num) for num in line.split()] for line in card.splitlines()]
    for card in data[1:]
]

# print(bingocards)


def checkwinner():
    for icard, card in enumerate(bingocards):
        # check winner
        for c in range(5):
            r = sum(card[c])
            c = sum([card[i][c] for i in range(5)])
            if not (r):
                # print("rowwin")
                return icard, sum(sum(g) for g in card)
            if not (c):
                # print("colwin")
                return icard, sum(sum(g) for g in card)


winners = []
print("winning cards in order: (cardid, value, last called number, answer)")

for drawn in numbers:
    # print(drawn)
    # mark
    bingocards = [
        [[num if (num != drawn) else 0 for num in line] for line in card]
        for card in bingocards
    ]
    # print(bingocards)
    nwinners = 0
    while w := checkwinner():
        nwinners += 1
        icard, w = w
        bingocards[icard] = [[9998] * 5] * 5  # replace with fake card
        winners.append(icard)
        print(icard + 1, w, drawn, w * drawn)
        # print(bingocards)
    # print(nwinners, "this round")

# print(winners)
