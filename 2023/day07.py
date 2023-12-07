import collections
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2023/day06inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2023/day06input.txt")) as f:
    data = f.read().strip()

cardvaluesp1 = {v:k for k,v in enumerate(["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"][::-1])}
cardvaluesp2 = {v:k for k,v in enumerate(["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"][::-1])}
cardvalues = {
    False: cardvaluesp1,
    True: cardvaluesp2,
}

def handtype(hand, use_wildcard_jokers):
    if use_wildcard_jokers:
        temp_c = collections.Counter(hand)
        js = temp_c["J"]
        # print(hand, js)
        if js == 5:
            # shortcut here
            return 7
        c = collections.Counter([c for c in hand if c != "J"])

        # print(c)
        # print(c.most_common()[0][0])
        c[c.most_common(1)[0][0]] += js
    else:
        c = collections.Counter(hand)
    # print(c.most_common())
    match c.most_common():
        case [(_, 5), *_]:
            # Five of a kind, where all five cards have the same label: AAAAA
            return 7
        case [(_, 4), *_]:
            # Four of a kind, where four cards have the same label and one card has a different label: AA8AA
            return 6
        case [(_, 3), (_, 2), *_]:
            # Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
            return 5
        case [(_, 3), *_]:
            # Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
            return 4
        case [(_, 2), (_, 2), *_]:
            # Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
            return 3
        case [(_, 2), *_]:
            return 2
            # One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
        case [(_, 1), *_]:
            # High card, where all cards' labels are distinct: 23456
            return 1


def handsortvalue(hand, use_wildcard_jokers):
    return (handtype(hand, use_wildcard_jokers), tuple(cardvalues[use_wildcard_jokers][c] for c in hand))


for part in False, True:
    hands = [
        (handsortvalue(hand, part), bid, i, hand)
        for i, (hand,bid) in enumerate([
            line.split() for line in data.splitlines()
        ])
    ]
    # print(hands)
    accum = 0

    for i, (handvalue, bid, _, hand) in enumerate(sorted(hands)):
        # print(hand, int(bid), int(bid) * (i+1))
        accum += int(bid) * (i+1)
        # print(accum)
    if part:
        print("p2:", accum)
    else:
        print("p1:", accum)
