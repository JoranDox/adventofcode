spacewords = """
Asteroid - Small, rocky objects that orbit the Sun.
Asteroid belt - The region between Mars and Jupiter that contains the largest population of asteroids in our solar system.
Astronaut - A person trained to travel in a spacecraft.
Astronomer - A scientist who studies the universe.
Astronomical unit - A unit of measurement that’s roughly the distance from the Earth to the Sun (93 million miles).
Atmosphere - The area of air and gas that envelopes Earth and other astronomical objects.
Atom - Basic units of matter that every solid, liquid, gas and plasma is composed of.
Big Bang - The main theory explaining how the universe started. It states that 13.8 billion years ago, space expanded quickly to form the atoms that would produce stars and galaxies.
Binary star - A system of two stars where one revolves around the other or both revolve around a common centre.
Black dwarf - A star that’s exhausted its own supply of carbon and burnt out.
Black hole - A place in space where the pull of gravity is so strong that even light can’t get out.
Comet - Objects made of frozen gases, rock and dust that orbit the Sun.
Constellation - A group of stars that form a pattern.
Corona - The gaseous outer layer of the Sun’s atmosphere.
Cosmic dust - Small particles of matter in space.
Cosmos - The universe.
Crater - A cavity in the ground of a celestial object, typically caused by explosions or meteor impact.
Dark matter - Particles thought to exist in space that don’t absorb, reflect or emit light, and thus can’t be observed.
Dwarf galaxy - Small dim galaxies that are abundant in the universe.
Dwarf planet - A body in space that resembles a small planet but lacks criteria to class it as such.
Dwarf star - A small star with low luminosity.
Eclipse - When one celestial body blocks light from reaching another by moving between it and its light source.
Elliptical orbit - One object revolving around another in an oval shape. The shape is known as an ellipse.
Equinox - The time when the Sun crosses the celestial equator and day and night are the same length. This happens twice a year.
Force - A push or pull on an object when it interacts with another.
Galaxy - A huge collection of gas, dust and billions of stars and their solar systems held together by gravity.
Gravity - The force that pulls objects towards each other.
Hemisphere - A half of the Earth, when divided along the lines of either North and South or East and West.
Inner planets - Planets whose orbit is within the asteroid belt, including Mercury, Venus, Earth and Mars.
International Space Station - A man-made object that orbits Earth, where astronauts can live and conduct experiments.
Kuiper belt - A cold and dark area of our Solar System which contains thousands of comets, asteroids and other objects.
Light year - The distance light travels in one year (nearly 6 trillion miles).
Mass - How much material an object is made up of, as opposed to weight which measures the pull of gravity on an object.
Meteor - A small body of matter from outer space that enters Earth’s atmosphere and appears like a streak of light.
Meteorite - A piece of rock or metal that lands on Earth’s surface.
Milky Way - Our galaxy that contains over 200 billion stars.
Moon - A large celestial object that acts as a natural satellite to Earth. Most planets in our solar system have at least one moon and some have several.
Nebula - A cloud of dust and gas in space.
Observatory - A building equipped with materials to make astronomical observations.
Orbit - A regular and repeating circuit that one celestial object takes around another.
Outer planets - Planets whose orbits are outside the asteroid belt, including Jupiter, Saturn, Uranus and Neptune.
Penumbra - A partial shadow outside the complete shadow of an opaque object. It occurs when only part of a light source is cut off.
Planet - A celestial body that orbits the sun that has sufficient mass for its gravity to overcome rigid body forces and has not cleared the neighbourhood around its orbit.
Pulsar - Compact stars that spin around hundreds of times a second.
Quasar - Supermassive black holes that suck in materials,
Red dwarf - Stars that are very small and cool compared to others.
Red giant - A star that’s run out of hydrogen and begins to grow bigger and redder.
Satellite - An object intentionally placed into space to orbit a celestial body to collect information.
Shooting star - Streaks of light in the sky that occur when meteoroids fall into the Earth’s atmosphere and burn up.
Solstice - The time when the sun reaches its maximum or minimum declination, causing the shortest and longest days of the year.
Space - The three-dimensional expanse in which all material things exist.
Star - An astronomical object made of bright, glowing matter called plasma. They’re held together by gravity and are incredibly hot.
Starburst - A period of intense activity in a galaxy where lots of stars are formed.
Sun - The star that objects in our solar system orbit.
Telescope - An instrument that allows us to see into space.
Universe - Everything that exists in space.
Waning - When the moon becomes gradually less visible.
Waxing - When the moon becomes gradually more visible.
White dwarf - When a star has burnt up its fuel and begins to collapse inwards.
"""
spacedic = set(spacewords.replace(".","").replace("(","").replace(")","").replace("-","").replace(",","").lower().split())
space_parsed = [(word, len(word)) for word in spacedic]
print(space_parsed)

import pathlib
parent_directory = pathlib.Path(__file__).resolve().absolute().parent

donetokens = {
    "the uniqueness": "a jacket",
    "the uniquenessten": "a hat",
    "newtstr": "the store",
}
tokens = {
    "the path": "the path", # not changed yet
    "your mind": "your mind", # not changed yet
    "a wreath": "a wreath", # not changed yet
    "uniquecounttwo": "uniquecounttwo", # not changed yet
    "uniquecountten": "uniquecountten", # not changed yet
    "space": "space", # not changed yet
    "your mind": "your mind", # not changed yet
    "goup": "goup", # not changed yet
    "goleft": "goleft", # not changed yet
    "goright": "goright", # not changed yet
    "godown": "godown", # not changed yet
    "the rope": "the rope", # not changed yet
    "a rope": "a rope", # not changed yet
    "your heart": "your heart", # not changed yet
    "2": "2", # not changed yet
    "1": "1", # not changed yet
    "0": "0", # not changed yet
    "-1": "-1", # not changed yet
    "-2": "-2", # not changed yet
    "hx": "hx", # not changed yet
    "hy": "hy", # not changed yet
    "dx": "dx", # not changed yet
    "dy": "dy", # not changed yet
    "tx": "tx", # not changed yet
    "ty": "ty", # not changed yet
    "mx": "mx", # not changed yet
    "movey": "movey", # not changed yet
    "tangled": "tangled", # not changed yet
    "the box": "the box", # not changed yet
    "rock": "rock", # don't change lol
    "roll": "roll", # don't change lol
}

remove = [
    "whisper",
    "let memes be",
]

import re
with open(parent_directory.joinpath("2022-12-09part2.rock")) as f_in:
    with open(parent_directory.joinpath("2022-12-09part2idiomatic_generated.rock"), "w") as f_out:
        for line in f_in:
            if any(token in line.lower() for token in remove):
                continue
            # print("1:",line.rstrip())
            line = line.rstrip()
            if not line:
                continue
            line = re.sub(rf"\(.*\)","", line.strip()).strip().lower()
            # print("2:",line)

            for inp,outp in tokens.items():
                line = re.sub(rf"\b{inp}\b", outp, line)

            line = line.capitalize()
            # print("9:", line)
            # print()
            f_out.write(line + "\n")
        f_out.write("(6023, 2533)\n")


with open(parent_directory.joinpath("2022-12-09part2idiomatic_generated.rock")) as f:
    data = f.read()

# for word in set(data.lower().split()):
for word in tokens.values():
    print('"' + word + '"')
    for line in data.splitlines():
        if word in line.lower():
            print('    ' + line)
print("done")
