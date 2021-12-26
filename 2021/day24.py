from collections import deque
import tqdm
import os
from sympy import *

# with open("day24inputtest.txt") as f:
with open("day24input.txt") as f:
    data = f.read().strip().splitlines()

ycounter = 0
xcounter = 0
for line in data:
    if line.startswith("add y "):
        ycounter += 1
    if line.startswith("add x "):
        xcounter += 1
    if ycounter == 4:
        ycounter = 0
        print(line)
    if xcounter == 2:
        xcounter = 0
        print(line)

# raise

instuctionblock = []

for line in data:
    if line.startswith("inp w"):
        instuctionblock.append([line])
    else:
        instuctionblock[-1].append(line)

# print(len(data))
def inp(vars,a, queue):
    # print('inp',a,queue)
    vars[a], queue = (queue[0]), queue[1:]
    return queue

def add(vars,a,b):
    # print('add',a,b)
    # vars[a] = f"({vars[a]} + {b})"
    vars[a] = vars[a] + b

def mul(vars,a,b):
    # print('mul',a,b)
    # if b == "0":
    #     vars[a] = "0"
    # else:
    #     vars[a] = f"{vars[a]} * {b}"
    vars[a] = vars[a] * b

def div(vars,a,b):
    # print('div',a,b)f
    # vars[a] = f"({vars[a]} / {b})"
    vars[a] = int(vars[a] / b)

def mod(vars,a,b):
    # print('mod',a,b)
    # vars[a] = f"({vars[a]} % {b})"
    vars[a] = vars[a] % b

def eql(vars,a,b):
    # print('eql',a,b)
    # vars[a] = f"({vars[a]} == {b})"
    vars[a] = int(vars[a] == b)


inputqueue = 13579246899999
# inputqueue = symbols("a b c d e f g h i j k l m n")
print(inputqueue)

def getsvars(vars,literalorchar):
    if literalorchar in "wxyz":
        literalorchar = vars[literalorchar]
    # return int(literalorchar)
    return int(literalorchar)

def runprog(inputqueue):
    newdata = []
    vars = {
        "w": 0,
        "x": 0,
        "y": 0,
        "z": 0,
    }

    inputqueue = list(str(inputqueue))
    
    for line in data:
        # varsbefore = vars.copy()
        s = line.strip().split()
        sfunc, svars = s[0], s[1:]

        # print(sfunc, svars)
        if sfunc == "inp":
            inputqueue = inp(vars, *svars, inputqueue)
        else:
            a,b = svars
        
        if sfunc == "add":
            # if b == "0":
            #     print('no-op add 0')
            #     continue
            # b = getsvars(vars,b)
            # if getsvars(vars,a) is None:
            #     print('no-op add 0 by history (a)')
            #     continue
            # if b is None:
            #     print('no-op add 0 by history (b)')
            #     continue
            add(vars, a, getsvars(vars,b))
        if sfunc == "mul":
            # if b == "1":
            #     print('no-op mul 1')
            #     continue
            # b = getsvars(vars,b)
            # if b is None:
            #     print("destroy b by history")
            #     b = '0'
            # if vars[a] is None:
            #     vars[a] = "0"
            #     print('no-op mul 0 by 0 by history (a)')
            #     continue
            mul(vars, a, getsvars(vars,b))
        if sfunc == "div":
            # if vars[a] is None:
            #     vars[a] = "0"
            # if b == "1":
            #     print('no-op div 1')
            #     continue
            div(vars, a, getsvars(vars,b))
        if sfunc == "mod":
            mod(vars, a, getsvars(vars,b))
        if sfunc == "eql":
            # if vars[a] == getsvars(vars,b):
            #     vars[a] = "1"
            # else:
            #     eql(vars, a, b)
            eql(vars, a, getsvars(vars,b))
        newdata.append(line)

        # print(varsbefore, vars)
        # if sfunc == "inp" or tuple(vars.items()) != tuple(varsbefore.items()):
        #     newdata.append(line)
        # else:
        #     print("removed no-op", line)
        # if sfunc == "div":
            # break
        # print(vars)
    return vars, newdata

r,data = runprog(93959993429899)
print(r)
r,data = runprog(11815671117121)
print(r)

print("done")
# print(r['y'])


# for number in tqdm.tqdm(range(99999999999999 + 1, 13579246899999, -1)):
#     if "0" in str(number):
#         continue
#     r, data = runprog(number)
#     if not r["z"]:
#         print(number, "wins")
#         break
