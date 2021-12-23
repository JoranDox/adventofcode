from functools import lru_cache
from typing import DefaultDict
import numpy as np
import heapq

testinput = """
#############
#...........#
###B#C#B#D###
  #D#C#B#A#  
  #D#B#A#C#  
  #A#D#C#A#  
  #########  
"""

myinput = """
#############
#...........#
###A#D#B#C###
  #D#C#B#A#  
  #D#B#A#C#  
  #B#C#D#A#  
  #########  
"""

emptyinput = """
#############
#...........#
###.#.#.#.###
  #.#.#.#.#  
  #.#.#.#.#  
  #.#.#.#.#  
  #########  
"""

endinput = """
#############
#...........#
###A#B#C#D###
  #A#B#C#D#  
  #A#B#C#D#  
  #A#B#C#D#  
  #########  
"""

print(testinput)
part1 = False
# part1 = True
if part1:
    testinput = '\n'.join(testinput.splitlines()[:4] + testinput.splitlines()[6:])
    myinput = '\n'.join(myinput.splitlines()[:4] + myinput.splitlines()[6:])
    emptyinput = '\n'.join(emptyinput.splitlines()[:4] + emptyinput.splitlines()[6:])
    endinput = '\n'.join(endinput.splitlines()[:4] + endinput.splitlines()[6:])

def genworld(worldstr):
    return np.array([
        tuple(line.strip("\n"))
        for line in worldstr.strip('\n').splitlines()
    ])

def printworld(world):
    for line in world:
        print(''.join(line))

printworld(genworld(emptyinput))
print(genworld(emptyinput))

nostopping = {(3, 1), (5, 1), (7, 1), (9, 1)}

print(nostopping)

def getneighbours(loc):
    x,y = loc
    return {
        (x,y-1),
        (x+1,y),
        (x,y+1),
        (x-1,y),
    }

def getvalidmoves(world, startloc,others):
    tocheck = {(startloc,())}
    validmoves = set()
    while tocheck:
        l, path = tocheck.pop()
        # print(l, path)
        for neighbour in getneighbours(l):
            # print(neighbour)
            nval = world.T[neighbour]
            # print(nval)
            if neighbour in path:
                # print("already been here")
                # don't backtrack
                pass
            elif neighbour in others:
                # print("someone's here")
                pass
            elif nval == "#":
                # print("wall")
                pass
            elif nval in ".wxyz": # just move past finished people in the rooms, doesn't matter for final calc
                # print("yes")
                
                # valid location to pass
                if neighbour not in nostopping:
                    validmoves.add((neighbour))
                tocheck.add((neighbour, (*path, l)))
            else:
                print("oh no!")
    return validmoves

if part1:
    startlocs = {
        (3, 2), (5, 2), (7, 2), (9, 2),
        (3, 3), (5, 3), (7, 3), (9, 3),
    }
else:
    startlocs = {
        (3, 2), (5, 2), (7, 2), (9, 2),
        (3, 3), (5, 3), (7, 3), (9, 3),
        (3, 4), (5, 4), (7, 4), (9, 4),
        (3, 5), (5, 5), (7, 5), (9, 5),
    }

endlocs = {
    "A": {(3,2), (3,3), (3,4), (3,5)} & startlocs,
    "B": {(5,2), (5,3), (5,4), (5,5)} & startlocs,
    "C": {(7,2), (7,3), (7,4), (7,5)} & startlocs,
    "D": {(9,2), (9,3), (9,4), (9,5)} & startlocs,
    "a": {(3,2), (3,3), (3,4), (3,5)} & startlocs,
    "b": {(5,2), (5,3), (5,4), (5,5)} & startlocs,
    "c": {(7,2), (7,3), (7,4), (7,5)} & startlocs,
    "d": {(9,2), (9,3), (9,4), (9,5)} & startlocs,
}

costs = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}

progression = {
    "A": "a",
    "B": "b",
    "C": "c",
    "D": "d",
    "a": "w",
    "b": "x",
    "c": "y",
    "d": "z",
}

firstmovevalid = {(x,1) for x in range(12)}
secondmovevalid = {(x,2) for x in range(12)} | {(x,3) for x in range(12)}

def distance(l1,l2):
    x1,y1 = l1
    x2,y2 = l2
    return abs(x2-x1) + abs(y2-y1)

# w = genworld(emptyinput)
# for move in getvalidmoves(genworld(emptyinput), (1,1), ()):
#     w.T[move] = "O"
# printworld(w)


# startworld = genworld(testinput)
startworld = genworld(myinput)
emptyworld = genworld(emptyinput)

fishlocs = DefaultDict(set)
for loc in startlocs:
    fishlocs[startworld.T[loc]].add(loc)
print(fishlocs)

# def freeze(fishdict):
#     return tuple(fishdict.items())

# def thaw(frozenfish):
#     return DefaultDict(set,frozenfish)

# print("freezer test")
# print(fishlocs)
# print(freeze(fishlocs))
# print(thaw(freeze(fishlocs)))
# assert fishlocs == thaw(freeze(fishlocs))

# frozenfish = tuple(
#     (letter, tuple(fishlocs[letter])) for letter in "ABCD"
# )
# print(frozenfish)

fishes = set()
for letter in fishlocs:
    for loc in fishlocs[letter]:
        fishes.add((letter,loc))


# tocheck = [(0,fishes)]

# heapq.heapify(tocheck)
# print(tocheck)

prevcost = 0
prevclose = 50
lowestcost = 1000000

def printstate(fishes):
    world = genworld(emptyinput)
    for letter,loc in fishes:
        world.T[loc] = letter
    printworld(world)

if part1:
    costbounds = 20000
else:
    costbounds = 60000


steps = 0
# while tocheck:
@lru_cache(maxsize=None)
def check(cost, fishes):
    global steps
    global prevcost
    global prevclose
    global lowestcost
    global costbounds
    steps += 1
    fishes = set(fishes)
    # s = sorted(tocheck)
    # cost,fishes = heapq.heappop(tocheck)
    if cost > costbounds:
        return # nothing to be gained here
    if cost >= prevcost:
        prevcost = cost
        # print(cost, fishes)
    alllocs = {
        loc
        for letter,loc in fishes
    }

    close = sum(letter in progression for letter,loc in fishes) + sum(letter == letter.upper() for letter,loc in fishes)
    if close < prevclose:
        print("getting closer", close, fishes, steps)
        printstate(fishes)
        prevclose = close
    if close == 0:
        costbounds = min(cost,costbounds)
        return cost, ()

    attempts = []
    # bestcost = costbounds
    for letter, loc in fishes:
        if letter in progression:
            if letter == letter.upper():
                comp = firstmovevalid
            else:
                comp = secondmovevalid & endlocs[letter]

                okay = True
                for fish, floc in (fishes - {(letter,loc)}):
                    if (
                        # the fish we're comparing to is in the endlocs of the letter we're looking at
                        floc in endlocs[letter]
                        and
                        # the fish we're comparing to is the wrong letter
                        progression[letter] != fish
                    ):
                        # wrong fish inside
                        okay = False
                        break
                if not okay:
                    continue # don't move into a room if wrong fish still in there
                

            for move in getvalidmoves(emptyworld,loc,alllocs) & comp:
                # print(letter, loc, move)

                d = distance(loc,move) * costs[letter.upper()]
                newfishes = fishes - {(letter,loc)} | {(progression[letter],move)}

                assert len(newfishes) == len(startlocs)

                r = check(cost + d, tuple(newfishes))
                if r:
                    rcost, rpath = r
                    attempts.append((rcost,((letter,loc,move), *rpath)))
                # heapq.heappush(tocheck,(cost + d, newfishes))
    if attempts:
        mc, mf = min(attempts)
        if cost < lowestcost: # and len(mf) == len(startlocs) * 2:
            print(mc,len(mf),mf)
            # printstate(fishes)
            lowestcost = cost
            # print("done!", cost, lowestcost, steps)

        return mc,mf

print(check(0,tuple(fishes)))
print(steps)