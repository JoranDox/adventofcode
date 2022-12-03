import os
import pathlib
currentyear = 2022
dry_run = False
path = pathlib.Path(__file__).resolve().absolute()
print(path, type(path))

prefix = path.parent
print(prefix)

prefixpath = prefix.joinpath(str(currentyear))
print(prefixpath)
existing = (os.listdir(prefixpath))
print(existing)

for day in range(1,26):
    basename = f"day{str(day).zfill(2)}"
    pyname = basename + ".py"

    if pyname not in existing and not dry_run:
        with open(os.path.join(prefixpath,pyname), "w") as f:
            f.write(f"""
import pathlib
parent_directory = pathlib.Path(__file__).resolve().absolute().parent
with open(parent_directory.joinpath("{basename}inputtest.txt")) as f:
#with open(parent_directory.joinpath("{basename}input.txt")) as f:
    data = f.read().strip()

for line in data.splitlines():
#for line in data.split("\\n\\n"):


""")
        with open(os.path.join(prefixpath,basename + "inputtest.txt"), "w") as f:
            pass
        with open(os.path.join(prefixpath,basename + "input.txt"), "w") as f:
            pass
        break