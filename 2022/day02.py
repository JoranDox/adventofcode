
# with open("day02inputtest.txt") as f:
with open("day02input.txt") as f:
    data = f.read().strip()

# rock       A   X
# paper      B   Y
# scissors   C   Z
#
rps = {
    "A": 1,
    "B": 2,
    "C": 3,
    "X": 1,
    "Y": 2,
    "Z": 3,
}

"""
AR1 -- YP2 --> W6
BP2 -- XR1 --> L0
CS3 -- ZS3 --> D3
AR1 -- ZS3 --> L0
CS3 -- XR1 --> W6
"""
score = 0
for line in data.splitlines():
    elf,me = line.split()
    # s1,s2 = rps[me], (((rps[me]-rps[elf])+1%3))*3
    s1,s2 = rps[me], ((((rps[me]-rps[elf])+1)%3))*3


    score += s1 + s2
    # print(s1,s2, rps[me], rps[elf], (rps[me]-rps[elf])+1, (rps[me]-rps[elf])+1 , )
print("p1:",score)

rps2 = {
    "A": 1,
    "B": 2,
    "C": 3,
    "X": 1, # lose
    "Y": 2, # draw
    "Z": 3, # win
}
"""
AR1 --> R1 <-- YD3
BP2 --> R1 <-- XL0
CS3 --> R1 <-- ZW6
"""
score2 = 0
for line in data.splitlines():
    elf,outcome = line.split()
    # score for outcome
    s2 = (rps2[outcome] -1) * 3
    # score for choice
    # me - elf = outcome
    # => me = outcome + elf
    # 1-indexed -> +1 outside of the %
    s1 = (rps2[outcome] + rps2[elf]) %3 + 1
    print(s1,s2,elf,outcome)
    score2 += s1 + s2
    print(score2)

