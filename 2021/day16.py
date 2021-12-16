
# test
# data = "".join([str(bin(int(x,16)))[2:].zfill(4) for x in "9C0141080250320F1802104A08"])
# input
data = "".join([str(bin(int(x,16)))[2:].zfill(4) for x in "820D4A801EE00720190CA005201682A00498014C04BBB01186C040A200EC66006900C44802BA280104021B30070A4016980044C800B84B5F13BFF007081800FE97FDF830401BF4A6E239A009CCE22E53DC9429C170013A8C01E87D102399803F1120B4632004261045183F303E4017DE002F3292CB04DE86E6E7E54100366A5490698023400ABCC59E262CFD31DDD1E8C0228D938872A472E471FC80082950220096E55EF0012882529182D180293139E3AC9A00A080391563B4121007223C4A8B3279B2AA80450DE4B72A9248864EAB1802940095CDE0FA4DAA5E76C4E30EBE18021401B88002170BA0A43000043E27462829318F83B00593225F10267FAEDD2E56B0323005E55EE6830C013B00464592458E52D1DF3F97720110258DAC0161007A084228B0200DC568FB14D40129F33968891005FBC00E7CAEDD25B12E692A7409003B392EA3497716ED2CFF39FC42B8E593CC015B00525754B7DFA67699296DD018802839E35956397449D66997F2013C3803760004262C4288B40008747E8E114672564E5002256F6CC3D7726006125A6593A671A48043DC00A4A6A5B9EAC1F352DCF560A9385BEED29A8311802B37BE635F54F004A5C1A5C1C40279FDD7B7BC4126ED8A4A368994B530833D7A439AA1E9009D4200C4178FF0880010E8431F62C880370F63E44B9D1E200ADAC01091029FC7CB26BD25710052384097004677679159C02D9C9465C7B92CFACD91227F7CD678D12C2A402C24BF37E9DE15A36E8026200F4668AF170401A8BD05A242009692BFC708A4BDCFCC8A4AC3931EAEBB3D314C35900477A0094F36CF354EE0CCC01B985A932D993D87E2017CE5AB6A84C96C265FA750BA4E6A52521C300467033401595D8BCC2818029C00AA4A4FBE6F8CB31CAE7D1CDDAE2E9006FD600AC9ED666A6293FAFF699FC168001FE9DC5BE3B2A6B3EED060"])
print(data)
# while data.endswith("0"):
#     data = data[:-1]
# print(data)

# data = "11010001010"

def getpart(n, data):
    return data[:n], data[n:]
global allversions
allversions = 0
def dopacket(instr):
    rest = ''.join([d for d in instr])
    print("rest",rest)
    version, rest = getpart(3,rest)
    print("version",int(version,2))
    global allversions
    allversions += int(version,2)
    print("allversions", allversions)
    ptype, rest = getpart(3,rest)
    ptype = int(ptype,2)
    print("ptype",ptype)
    if ptype == 4:
        # literal
        # print("literal")
        packet, rest = getpart(5,rest)
        # print(packet[0],packet[1:])
        full = []
        while packet[0] == '1':
            full.append(packet[1:])
            packet, rest = getpart(5,rest)
            # print(packet[0], packet[1:])
        full.append(packet[1:])
        value = int(''.join(full),2)
        # print("literal", full, ''.join(full), int(''.join(full),2))
        print("literal", value)
    else:
        print("operator")
        values = []
        # operator
        lengttypeid, rest = getpart(1,rest)
        if lengttypeid == "0":
            totallength, rest = getpart(15, rest)
            print("subpackets of length", int(totallength,2))
            subrest, rest = getpart(int(totallength,2), rest)
            while subrest:
                tvalue, subrest = dopacket(subrest)
                values.append(tvalue)

        elif lengttypeid == "1":
            npackets, rest = getpart(11, rest)
            print(int(npackets,2), "subpackets")
            for i in range(int(npackets,2)):
                tvalue, rest = dopacket(rest)
                values.append(tvalue)
        if ptype == 0:
            value = sum(values)
        elif ptype == 1:
            value = 1
            for v in values:
                value *= v
        elif ptype == 2:
            value = min(values)
        elif ptype == 3:
            value = max(values)
        elif ptype == 5:
            value = int(values[0] > values[1])
        elif ptype == 6:
            value = int(values[0] < values[1])
        elif ptype == 7:
            value = int(values[0] == values[1])

    return value, rest

print(allversions)
print(dopacket(data))