import dataclasses

with open("day02inputtest.txt") as f:
    # with open("day02input.txt") as f:
    data = f.readlines()


@dataclasses.dataclass
class State:
    depth: int = 0
    hor: int = 0
    aim: int = 0


state = State()


def forward(state, x):
    state.hor += x


def down(state, x):
    state.depth += x


def up(state, x):
    state.depth -= x


actions = {
    "forward": forward,
    "down": down,
    "up": up,
}

for line in data:
    action, amount = line.split()
    actions[action](state, int(amount))

print(state)
print(state.hor * state.depth)

state = State()


def forward(state, x):
    state.hor += x
    state.depth += state.aim * x


def down(state, x):
    state.aim += x


def up(state, x):
    state.aim -= x


actions = {
    "forward": forward,
    "down": down,
    "up": up,
}
for line in data:
    action, amount = line.split()
    actions[action](state, int(amount))

print(state)
print(state.hor * state.depth)
