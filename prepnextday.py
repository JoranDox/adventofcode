import os

try:
    import inspect
    import pathlib

    def realpath(inpath):
        return pathlib.Path(inpath).resolve().absolute()

    def get_script_dir():
        """
        uses inspect to get the calling script (assumes the calling script is the last one in the stack trace)
        then uses pathlib to get the parent directory of the calling script
        then returns the absolute path of that directory
        """

        return realpath(inspect.stack()[-1].filename).parent

    prefix = get_script_dir()
    print("script dir:", prefix)

except:
    # if something goes wrong there, just ignore and fallback
    print("failure in getting script dir")
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
#for line in data.split("\\n\\n"):


""")
        with open(os.path.join(prefixpath,basename + "inputtest.txt"), "w") as f:
            pass
        with open(os.path.join(prefixpath,basename + "input.txt"), "w") as f:
            pass
        break