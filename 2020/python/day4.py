parsedpassports = []
with open("day4input.txt") as infile:
    # with open("day4inputex.txt") as infile:
    # with open("day4valid.txt") as infile:
    # with open("day4invalid.txt") as infile:
    passports = infile.read()
    for passport in passports.split("\n\n"):
        entries = [entry.split(":") for entry in passport.split()]
        parsedpass = {k: v for k, v in entries}
        parsedpassports.append(parsedpass)

neededfields = [
    "byr",  # (Birth Year)
    "iyr",  # (Issue Year)
    "eyr",  # (Expiration Year)
    "hgt",  # (Height)
    "hcl",  # (Hair Color)
    "ecl",  # (Eye Color)
    "pid",  # (Passport ID)
    # "cid", #(Country ID)
]


def validpass(pp):
    for field in neededfields:
        if field not in pp:
            return False

    return True


def checkheight(num):
    n = int(num[:-2])
    end = num[-2:]
    if end == "cm":
        if 150 <= n <= 193:
            return True
    elif end == "in":
        if 59 <= n <= 76:
            return True
    return False


validatedfields = {
    "byr": (lambda x: 1920 <= int(x) <= 2002),
    "iyr": (lambda x: 2010 <= int(x) <= 2020),
    "eyr": (lambda x: 2020 <= int(x) <= 2030),
    "hgt": checkheight,
    "hcl": (lambda x: x[0] == "#" and int(x[1:], 16)),
    "ecl": (lambda x: x in "amb blu brn gry grn hzl oth".split()),
    "pid": (lambda x: (len(x) == 9) and all([str.isdigit(c) for c in x])),
    "cid": (lambda x: True),
}


def realvalidpass(pp):
    try:
        return validpass(pp) and all(
            [validatedfields[key](value) for key, value in pp.items()]
        )
    except:
        return False


print(sum([validpass(p) for p in parsedpassports]))


print(sum([realvalidpass(p) for p in parsedpassports]))
