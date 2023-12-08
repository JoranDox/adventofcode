correct = 0
wrong = 0

with open("day2input.txt") as file:
    for line in file:
        #  print(line)
        nums, letter, password = line.split(" ")
        nummin, nummax = nums.split("-")
        nummin = int(nummin)
        nummax = int(nummax)
        accum = 0
        #     print(nummin)
        #      print(nummax)
        #       print(letter)
        #        print(password)
        letter = letter[0]
        for l in password:
            if l == letter:
                accum += 1
        if nummin <= accum <= nummax:
            #        print("correct")
            correct += 1
        else:
            #       print("wrong")
            wrong += 1
print(correct)

correct = 0
with open("day2input.txt") as file:
    for line in file:
        nums, letter, password = line.split(" ")
        nummin, nummax = nums.split("-")
        nummin = int(nummin)
        nummax = int(nummax)
        accum = 0
        letter = letter[0]
        if (password[nummin - 1] == letter) ^ (password[nummax - 1] == letter):
            correct += 1
        else:
            wrong += 1
print(correct)
