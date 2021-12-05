import os

currentyear = 2021
existing = (os.listdir(str(currentyear)))
print(existing)
for day in range(1,26):
    basename = f"day{str(day).zfill(2)}"
    pyname = basename + ".py"
    if pyname not in existing:
        with open(f"{currentyear}/{pyname}", "w") as f:
            f.write(f"""
with open("{basename}inputtest.txt") as f:
#with open("{basename}input.txt") as f:
    data = f.readlines()
            """)
        with open(f"{currentyear}/{basename}inputtest.txt", "w") as f:
            pass
        with open(f"{currentyear}/{basename}input.txt", "w") as f:
            pass
        break