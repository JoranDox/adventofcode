import computer

instructions = computer.readinstructions("day8input.txt")
# instructions = computer.readinstructions("day8inputex.txt")
print(instructions)


def nodoubles(instructions):
    world = computer.world.copy()
    seen = [0]
    while True:
        lastaccum = world["accumulator"]
        # print("current accum & funcpointer:", lastaccum, print(world["funcpointer"]))
        world = computer.runone(world, instructions)
        if world == None:
            return True, lastaccum  # terminated
        if (fp := world["funcpointer"]) in seen:
            # print("already been here!")
            return False, lastaccum
        seen.append(fp)


# part1
print(nodoubles(instructions))

for i in range(len(instructions)):
    temp_instructions = instructions.copy()
    ins, arg = temp_instructions[i]
    if ins == "acc":
        continue
    elif ins == "nop":
        temp_instructions[i] = ("jmp", arg)
    elif ins == "jmp":
        temp_instructions[i] = ("nop", arg)

    result, lastaccum = nodoubles(temp_instructions)
    if result:
        print("yes, it's", i, "lastaccum =", lastaccum)
        break
    # else:
    # print("alas, not", i)
