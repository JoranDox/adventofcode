
# with open("day18inputtest.txt") as f:
with open("day18input.txt") as f:
    data = [d.strip() for d in f.readlines()]

def sfsplit(a: int):
    return a//2, (a+1)//2

def sfreduce(inlist):
    opens = 0
    for i, char in enumerate(inlist):
        if char == "[":
            opens += 1
        elif char == "]":
            opens -= 1
        elif char == ",":
            pass
        else:
            # char should be a number
            char = int(char)
            if opens > 4:
                # print("explode")
                assert inlist[i+1] == ","
                char2 = int(inlist[i+2])
                for j in range(i-1,0,-1):
                    try:
                        c = int(inlist[j])
                        inlist[j] = c + char
                        break
                    except:
                        pass
                for j in range(i+3,len(inlist)):
                    try:
                        c = int(inlist[j])
                        inlist[j] = c + char2
                        break
                    except:
                        pass

                return [*inlist[:i-1], 0, *inlist[i+4:]]
    # print("no explode")
    for i, char in enumerate(inlist):
        if char == "[":
            opens += 1
        elif char == "]":
            opens -= 1
        elif char == ",":
            pass
        else:
            char = int(char)
            if char > 9:
                # print("split")
                a,b = sfsplit(int(char))
                return [*inlist[:i], "[", a, ",", b, "]", *inlist[i+1:]]
    # print("nothing")
    return inlist

def sfsum(a,b):
    return ["[", *a, ",", *b, "]"]

def tostr(inlist):
    return "".join(str(s) for s in inlist)

def keepreducing(inlist):
    s = tostr(inlist)
    s2 = None
    while s != s2:
        # print(s)
        s2 = s
        inlist = sfreduce(inlist)
        s = tostr(inlist)
    return inlist

# instring = "[[[[[9,8],1],2],3],4]"
# instring = "[7,[6,[5,[4,[3,2]]]]]"
# instring = [11]
# inlist = [s for s in instring]

# inlista = list("[[[[4,3],4],4],[7,[[8,4],9]]]")
# inlistb = list("[1,1]")


# print(tostr(inlista), tostr(inlistb))
# inlist = sfsum(inlista,inlistb)
# print(tostr(inlist))
# reduced = keepreducing(inlist)

def submag(n):
    # print("entered submag with", n)
    try:
        ret = int(n)
        # print("sreturning", ret)
        return ret
    except:
        pass
    a,b = n
    ret = 3*submag(a) + 2*submag(b)
    # print("areturning", ret)
    return ret

def getmagnitude(inlist):
    from ast import literal_eval
    elist = literal_eval(tostr(inlist))
    return submag(elist)

# reduced = list("[[9,1],[1,9]]")
# print(getmagnitude(reduced))
# print(''.join(str(s) for s in reduced))

# part 1
sumnumbers = [list(a) for a in data]
while len(sumnumbers) > 1:
    sumnumbers = [
        keepreducing(sfsum(sumnumbers[0], sumnumbers[1])),
        *sumnumbers[2:]
    ]
final = sumnumbers[0]
print(tostr(final), getmagnitude(final))


# part 2
sumnumbers = [list(a) for a in data]
maxmag = 0
for i in sumnumbers:
    for j in sumnumbers:
        if i != j:
            maxmag = max(maxmag,getmagnitude(keepreducing(sfsum(i,j))))
print(maxmag)