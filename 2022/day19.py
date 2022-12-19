from collections import deque
import itertools
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2022/day19inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2022/day19input.txt")) as f:
    data = f.read().strip()

# example splitted
# Blueprint 1:
#   Each ore robot costs 4 ore.
#   Each clay robot costs 2 ore.
#   Each obsidian robot costs 3 ore and 14 clay.
#   Each geode robot costs 2 ore and 7 obsidian.

# Blueprint 2:
#   Each ore robot costs 2 ore.
#   Each clay robot costs 3 ore.
#   Each obsidian robot costs 3 ore and 8 clay.
#   Each geode robot costs 3 ore and 12 obsidian.

order = {
    "ore": 0,
    "clay": 1,
    "obsidian": 2,
    "geode": 3,
}

blueprints = {}
for line in data.splitlines()[:3]:
    bnum, rest = line.split(":")
    bnum = int(bnum.split()[-1])
    blueprints[bnum] = {}

    prodcosts = rest.split(".")[:-1]
    for prodcost in prodcosts:
        # print(prodcost)
        name, costs = prodcost.split("costs")
        _, rtype, _ = name.split()
        blueprints[bnum][order[rtype]] = {}
        for cost in costs.split("and"):
            # print(cost)
            num, what = cost.split()
            blueprints[bnum][order[rtype]][order[what]] = int(num)

        blueprints[bnum][order[rtype]] = (
            blueprints[bnum][order[rtype]].get(0,0),
            blueprints[bnum][order[rtype]].get(1,0),
            blueprints[bnum][order[rtype]].get(2,0),
            blueprints[bnum][order[rtype]].get(3,0),
        )

print(blueprints)



# ore, clay, obsidian, geode
robots = (1,0,0,0)
# ore, clay, obsidian, geode
inventory = (0,0,0,0)

def uniqueintparts(num):
    for i in range(num):
        for nums in itertools.combinations(range(1,num+1), i):
            if sum(nums) == num:
                yield(nums)

print(list(uniqueintparts(12)))
print(list(uniqueintparts(9)))

# robot value (bp1): {1: {0: {0: 4}, 1: {0: 2}, 2: {0: 3, 1: 14}, 3: {0: 2, 2: 7}}
#{0: (4, 0, 0, 0), 1: (2, 0, 0, 0), 2: (3, 14, 0, 0), 3: (2, 0, 7, 0)}
# geode = V, costs = (2, 0, 7, 0) = 2 ore, 7 obsidian
# obsidian bot: only for geode bots
# clay bot: only for obsidian bots
# ore bot: for everything
#
# 1 geode bot = 7 obsidian + 2 ore
#

def earliestgeode(blueprint):
    # bp looks like:
    # {0: (4, 0, 0, 0), 1: (2, 0, 0, 0), 2: (3, 14, 0, 0), 3: (2, 0, 7, 0)}
    #
    # for a geode we need 2 ore and 7 obsidian
    initialrobots = (1,0,0,0)
    initialinventory = (0,0,0,0)
    pass



def vsum(*v):
    return tuple(sum(x) for x in zip(*v))

def vmul(v, num):
    return tuple(vx * num for vx in v)

# print(vsum(robots,inventory,(1,2,3,4)))

def enough(vresources, vcost):
    return all(v1>=v2 for v1,v2 in zip(vresources,vcost))

def maxgeodestogo(minutes_to_go,bots=0,geodes=0):

    for i in range(minutes_to_go):
        geodes += bots
        bots += 1
    return geodes

print("maxes:")
print(maxgeodestogo(1))
print(maxgeodestogo(2))
print(maxgeodestogo(3))
print(maxgeodestogo(4))

def neg(v):
    return tuple(-x for x in v)

for v1,v2 in [
    ((1,),(2,)),
    ((1,1),(2,0)),
    ((1,2,3,4),(1,2,4,0)),
    ((1,2,3,4),(1,2,4,0)),
]:
    print(v1,v2,v1<v2, enough(v1, v2))

def onehot(n, maxlen=4):
    return tuple((1 if x == n else 0) for x in range(maxlen))

print(onehot(0))
print(onehot(1))
print(onehot(2))
print(onehot(3))

def nexttime(robots, inventory, cost):
    # print("entering nexttime with")
    # print(robots)
    # print(inventory)
    # print(cost)
    realcost = vsum(cost, neg(inventory))
    # print(realcost)
    if any([ r==0 and c > 0 for r,c in zip(robots,realcost) ]):
        return None
    else:
        i = 0
        while True:
            if enough(vmul(r,i),realcost):
                return i
            i+=1

# nexttime(robots, inventory, cost)
accum = 0
# print({} | {(0, (1, 0, 0, 0), (0, 0, 0, 0))})
for bname, blueprint in blueprints.items():
    print("checking bp:", bname, blueprint)
    # print(list(blueprint.values())[2][1])
    maxcosts = tuple(max(x) for x in zip(*blueprint.values()))
    print("costs:", maxcosts)
    # foundlist = {}
    seenstates = set()
    maxgeodes = 0
    # maxmins = 24
    maxmins = 32
    statesperminute = [deque() for _ in range(maxmins+1)]
    statesperminute[0].append((robots, inventory))
    clay = False
    obsi = False
    geo = False
    highestminute = 0
    for minute,states in enumerate(statesperminute):
        minstogo = maxmins-minute
        print("time is:", minute, ",", minstogo, "minutes to go, with", len(states), "states")
        if states:
            print("a state here is:", states[0])
        for state in states:
            r,i = state
            # print(state)
            if not clay and r[1] > 0:
                print("first claybot at", minute)
                clay = True
            if not obsi and r[2] > 0:
                print("first obsibot at", minute)
                obsi = True
            if not geo and r[3] > 0:
                print("first geobot at", minute)
                geo = True

            for rname,rcost in blueprint.items():
                if maxcosts[rname] > 0: # avoid skipping geode bots
                    if r[rname] >= maxcosts[rname]: # if we already have enough bots of this kind
                        # print("skipping building bot", rname, "because we already have enough in state", r, maxcosts)
                        continue
                nt = nexttime(r, i, rcost)
                # if we can build the bot somewhere in the future:
                if nt is not None:
                    # if we can build the bot in reasonable time
                    if minute+nt+1 <= maxmins:
                        # we'll see the state again
                        newstate = (
                            vsum(r, onehot(rname)), # new robot
                            vsum(i, vmul(r,nt+1), neg(rcost)), # minus cost, plus working robots until then
                        )
                        # if rname in (3,) and minute < 14:
                        # if state == ((1, 3, 1, 0), (2, 4, 0, 0)):
                        #     print("** new state in", nt, "minutes, costing", rcost)
                        #     print("** from:", r, i)
                        #     print("** to  :", newstate[0], newstate[1])
                        statesperminute[minute+nt+1].append(newstate)

            projected_geodes = vsum(vmul(r,minstogo),i)[3]
            if projected_geodes > maxgeodes:
                maxgeodes = projected_geodes
                print("new max geodes:", projected_geodes)

    print("== blueprint:", bname, "max geodes:", maxgeodes)

    # # end of each minute
    # example_states = [
    #     ((1,0,0,0), (0,0,0,0)), # 0
    #     ((1,0,0,0), (1,0,0,0)), # 1
    #     ((1,0,0,0), (2,0,0,0)), # 2
    #     ((1,1,0,0), (1,0,0,0)), # 3 build claybot
    #     ((1,1,0,0), (2,1,0,0)), # 4
    #     ((1,2,0,0), (1,2,0,0)), # 5 another claybot
    #     ((1,2,0,0), (2,4,0,0)), # 6
    #     ((1,3,0,0), (1,6,0,0)), # 7 another claybot
    #     ((1,3,0,0), (2,9,0,0)), # 8
    #     ((1,3,0,0), (3,12,0,0)), # 9
    #     ((1,3,0,0), (4,15,0,0)), # 10
    #     ((1,3,1,0), (2,4,0,0)), # 11 build obsibot
    #     ((1,4,1,0), (1,7,1,0)), # 12 another claybot
    #     ((1,4,1,0), (2,11,2,0)), # 13
    #     ((1,4,1,0), (3,15,3,0)), # 14
    #     ((1,4,2,0), (1,5,4,0)), # 15 another obsidibot
    #     ((1,4,2,0), (2,9,6,0)), # 16
    #     ((1,4,2,0), (3,13,8,0)), # 17
    #     ((1,4,2,1), (2,17,3,0)), # 18 build geobot (2 ore 7 obsi)
    #     ((1,4,2,1), (3,21,5,1)), # 19
    #     ((1,4,2,1), (4,25,7,2)), # 20
    #     ((1,4,2,2), (3,29,2,3)), # 21 another geobot
    #     ((1,4,2,2), (4,33,4,5)), # 22
    #     ((1,4,2,2), (5,37,6,7)), # 23
    #     ((1,4,2,2), (6,41,8,9)), # 24
    # ]
    # prevrobots = (1,0,0,0)
    # if bname == 1:
    #     for minute,(r,i) in enumerate(example_states):
    #         if r != prevrobots:
    #             assert (r,i) in statesperminute[minute], (r,i,statesperminute[minute])
    #             print("state found:", (minute,r,i))
    #             prevrobots = r

    accum += bname * maxgeodes
    print(f"accum @ {bname}: {accum}")
