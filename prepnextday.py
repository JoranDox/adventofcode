import os

prefix = "adventofcode"
currentyear = 2022
prefixpath = os.path.join(prefix, str(currentyear))
existing = (os.listdir(prefixpath))
print(existing)
for day in range(1,26):
    basename = f"day{str(day).zfill(2)}"
    pyname = basename + ".py"
    if pyname not in existing:
        with open(os.path.join(prefixpath,pyname), "w") as f:
            f.write(f"""
with open("{basename}inputtest.txt") as f:
#with open("{basename}input.txt") as f:
    data = f.read().strip()

for line in data.splitlines():
#for line in data.split("\n\n"):


""")
        with open(os.path.join(prefixpath,basename + "inputtest.txt"), "w") as f:
            pass
        with open(os.path.join(prefixpath,basename + "input.txt"), "w") as f:
            pass
        break