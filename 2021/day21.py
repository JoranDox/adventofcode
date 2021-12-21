#teststart


from collections import defaultdict


start = (4,8)
# realstart
start = (10,9)

def highmod(num,add,mod):
    return ((num + add - 1) % mod + 1)

class Die():
    def __init__(self) -> None:
        self.state = 1

    def roll(self):
        s = self.state
        self.state = highmod(self.state,1,100)
        return s

# dtest = Die()
# print(dtest.roll())
# print(dtest.roll())
# print(dtest.roll())
# for i in range(95):
#     dtest.roll()
# print(dtest.roll())
# print(dtest.roll())
# print(dtest.roll())
# print(dtest.roll())
# print(dtest.roll())

d1 = Die()

p1score, p2score = 0,0
p1pos, p2pos = start

dierolls = 0
turnplayer = 0
while p1score < 1000 and p2score < 1000:
    dierolls += 3
    r = (d1.roll() + d1.roll() + d1.roll())
    # print("r", r,  r % 10)
    r = r % 10
    if not turnplayer:
        p1pos = highmod(p1pos,r,10)

        p1score += p1pos
        # print(p1pos,p1score)
    else:
        p2pos = highmod(p2pos,r,10)
        p2score += p2pos
        # print(p2pos,p2score)
    turnplayer = not turnplayer
print(p1score,p2score,dierolls,min(p1score,p2score)*dierolls)

scores = {
    (start[0],0,start[1],0): 1
}

wins = [0,0]

turnplayer = 0
nonwinning = True
# while any(p < 21 for p in scores.values()):
rounds = 0
while nonwinning:
    rounds += 1
    print(rounds)
    nonwinning = False
    newdict = defaultdict(int)

    # for (loc,score),universes in scores.items():
    for (p1pos,p1score,p2pos,p2score),universes in scores.items():
        # print("u before", p1pos,p1score,p2pos,p2score,universes)
        if not turnplayer:
            # print("p1")
            loc = p1pos
            score = p1score
            # print(loc,score)
        else:
            # print("p2")
            loc = p2pos
            score = p2score
            # print(loc,score)

        # print("u after",loc,score,universes)
        for i in range(1,4):
            for j in range(1,4):
                for k in range(1,4):
                    
                    l = highmod(loc,i+j+k,10)
                    s = score + l
                    # print("uni", i, l, s)
                    if s >= 21:
                        wins[turnplayer] += universes
                    else:
                        nonwinning = True
                        if not turnplayer:
                            newdict[
                                (l,score+l,p2pos,p2score)
                            ] += universes
                        else:
                            newdict[
                                (p1pos,p1score,l,score+l)
                            ] += universes

    scores = newdict.copy()
    # print(scores)
    # if not turnplayer:
    #     print("end p1")
    #     p1scores = newdict.copy()
    #     p1wins = wins
    #     # print(p1scores)
    # else:
    #     print("end p2")
    #     p2scores = newdict.copy()
    #     p2wins = wins
        # print(p2scores)
    turnplayer = not turnplayer
    # if rounds > 3:
    #     break
    
print(wins,max(*wins))
