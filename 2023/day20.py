import collections
import enum
import pathlib
import functools
import numpy as np
import time
import warnings
np.set_printoptions(edgeitems=60,linewidth=180)
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2023/day20inputtest.txt")) as f:
# with open(aoc_dir.joinpath("input/2023/day20inputtest2.txt")) as f:
with open(aoc_dir.joinpath("input/2023/day20input.txt")) as f:
    data = f.read().strip()

class pulsetype(enum.Enum):
    HIGH = "high"
    LOW = "low"

modtypes: dict[str, str] = {}
states : dict[str, bool | dict[str, pulsetype]] = {}
destinations : dict[str, list[str]] = {}
for line in data.splitlines():
    modname, destinationsstr = line.split(" -> ")

    modtype = modname[0] # b for broadcaster, or % for flipflops, or & for conjunctions

    if modtype != "b":
        modname = modname[1:]
    modtypes[modname] = modtype

    if modtype == "%":
        # flipflops have a boolean state, on or off
        states[modname] = False
    elif modtype == "&":
        # conjunctions remember their inputs, state is a dictionary of Falses for each input (can't do this in creation yet)
        states[modname] = {}
    elif modtype == "b":
        # module name is broadcaster, and no state
        pass

    destinations[modname] = destinationsstr.split(', ')
del modname
print(modtypes)

print(destinations)

links = {
    (s,d)
    for s, dests in destinations.items()
    for d in dests
}
print(links)

sources = collections.defaultdict(set)
for (s,d) in links:
    sources[d].add(s)
sources : dict[str, set] = dict(sources)
print(sources)

def reducesource(col, link):
    s,d = link
    col[d].add(s)
    return col

sourcesreduce: dict = functools.reduce(
    reducesource,
    links,
    collections.defaultdict(set),
)
print(dict(sourcesreduce))
assert sources == sourcesreduce

# todo: refactor from here
for modname, modtype in modtypes.items():
    if modtype == "&":
        states[modname] = {x:pulsetype.LOW for x in sources[modname]}

print("modtypes", modtypes)
print("states", states)
print("destinations", destinations)
print("sources", sources)

recent_states = {n: [s] for n,s in states.items()}
print("recent_states", recent_states)

# part 1
Pulse: tuple[str, pulsetype, str] = collections.namedtuple("Pulse", ["source", "type", "modname"])

def do_pulse(pulse:Pulse):
    try:
        modtype = modtypes[pulse.modname]
    except KeyError:
        # print(pulse)
        return [] #e.g. output module
    # print(pulse, modtype)
    match modtype, pulse.type:
        case "b", _:
            # broadcaster
            return [Pulse(pulse.modname, pulse.type, d) for d in destinations[pulse.modname]]
        case "%", pulsetype.HIGH:
            return [] # nothing happens
        case "%", pulsetype.LOW:
            # inverter is inverting
            newstate = not states[pulse.modname]
            states[pulse.modname] = newstate
            if newstate: # was turned off -> now turned on
                return [Pulse(pulse.modname, pulsetype.HIGH, d) for d in destinations[pulse.modname]]
            else: # was turned on -> now turned off
                return [Pulse(pulse.modname, pulsetype.LOW, d) for d in destinations[pulse.modname]]
        case "&", _:
            states[pulse.modname][pulse.source] = pulse.type
            # print("    state:", states[pulse.modname])
            if all([x == pulsetype.HIGH for x in states[pulse.modname].values()]):
                # print("yes")
                return [Pulse(pulse.modname, pulsetype.LOW, d) for d in destinations[pulse.modname]]
            else:
                # print("no")
                return [Pulse(pulse.modname, pulsetype.HIGH, d) for d in destinations[pulse.modname]]
    print("wtf")
todo = collections.deque()
pulses_sent = {
    pulsetype.HIGH: 0,
    pulsetype.LOW: 0,
}
print("start")

def intifystate(s):
    return int({
        pulsetype.HIGH: 1,
        pulsetype.LOW: 0,
    }.get(s, s))

def flatten(s, accum=[]):
    if type(s) in (list, tuple):
        return [__s for _s in s for __s in flatten(_s)]
    if type(s) in (dict,):
        return [__s for _s in s.values() for __s in flatten(_s)]
        # return [*flatten(_s) for _s in s.values()]
    else:
        return intifystate(s)

def uglyflatten(s):
    return [c for c in str(s) if c in "01"]

def printmaybeonestate(s):
    if type(s) in (list, tuple):
        return [printmaybeonestate(_s) for _s in s]
    if type(s) in (dict,):
        return [printmaybeonestate(_s) for _s in s.values()]
    else:
        return [intifystate(s)]

def printfullstate():
    # print(uglyflatten(states.values()))
    print("".join(f"{k}{uglyflatten(flatten(v))}" for k,v in states.items()))



# import networkx as nx
# # G = nx.complete_graph(5)
# G = nx.DiGraph()
# # G.add_nodes_from(destinations)
# for s, ds in destinations.items():
#     for d in ds:
#         G.add_edge(s + modtypes[s], d + modtypes.get(d,""))
# nx.draw_kamada_kawai(G)

from pyvis.network import Network

def choosecolour(name):
    colour = "red"
    if name not in modtypes:
        return "yellow"
    if modtypes[name] == "&" and all([x == pulsetype.HIGH for x in states[name].values()]):
        colour = "blue"
    if modtypes[name] == "%" and states[name]:
        colour = "green"
    return colour

def shownetwork():
    net = Network(notebook=True, directed=True, cdn_resources='in_line', )
    for s, ds in destinations.items():
        sname = s + modtypes[s]
        net.add_node(sname, color=choosecolour(s))
        for d in ds:
            dname = d + modtypes.get(d,"")
            net.add_node(dname, color=choosecolour(d))
            net.add_edge(sname, dname)

    net.show("net.html", notebook=True)

def printflattenstate():
    return "".join([
        str(intifystate(f))
        for k,v in states.items()
            for f in (tuple(v.values()) if type(v) == dict else [v])
    ])

def flattenstate():
    return [
        intifystate(f)
        for k,v in states.items()
            for f in (tuple(v.values()) if type(v) == dict else [v])
    ]

print(flattenstate())
recent_states_flat = [np.array(flattenstate())]

shownetwork()

cycles = {}
# exit()
i = 0
while True:
    # push button
    todo.append(Pulse("button", pulsetype.LOW, "broadcaster"))
    while todo:
        # do all pulses from the one button press
        to_send = todo.popleft()
        if to_send.type == pulsetype.LOW and to_send.modname == "rx":
            print("p2:", i)
            exit()
        todo.extend(do_pulse(to_send))
        pulses_sent[to_send.type] += 1

    # recent_states = {n: recent_states[n] + [s] for n,s in states.items()}
    # recent_states_flat.append(np.array(flattenstate()))
    i += 1
    if i == 1000:
        print("p1:", pulses_sent, pulses_sent[pulsetype.HIGH] * pulses_sent[pulsetype.LOW])

    # print(states["dt"])
    for key in states["dt"]:
        if states["dt"][key] == pulsetype.HIGH:
            print(key, i)
            shownetwork()
            if key not in cycles:
                cycles[key] = i
                if len(cycles) == 4:
                    print(cycles)
                    exit()
    # print(recent_states)
    # TODO: find loops in here and do LCM between cycles
    # printfullstate()
    # if i == 4095:
    #     shownetwork()
    #     exit()
    print(printflattenstate())
    if not (i % 100000):
        print(i)

    # print(np.vstack(recent_states_flat))

