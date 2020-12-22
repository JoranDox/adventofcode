world = {
    "funcpointer" : 0,
    "accumulator" : 0
}

def acc(world, arg):
    return {
        "accumulator": world["accumulator"] + arg
    }

def jmp(world, arg):
    return {
        "funcpointer" : world["funcpointer"] + arg - 1
    }

def nop(world, arg):
    return {}

funcs = {
    "acc": acc,
    "jmp": jmp,
    "nop": nop,
}

def readinstructions(filename):
    with open(filename) as instructions:
        return [
            (ins[0], int(ins[1]))
            for line in instructions
            if (ins := line.strip().split(' '))
        ]

def runone(world, instructions):
    # print("enter")
    # print(world)
    fp = world["funcpointer"]
    if fp == len(instructions):
        # print("terminated")
        return None
    ins, arg = instructions[fp]
    
    diff = funcs[ins](world, arg)
    # print(diff)
    world.update(diff)
    world["funcpointer"] += 1
    # print(world)
    # print("exit")
    return world