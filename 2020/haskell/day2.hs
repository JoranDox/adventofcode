import Prelude
import Debug.Trace ( trace )


-- strip trailing newline
--main = interact $ (++"\n") . show . boolsum . map (part1correct . fullsplit ' ') . fullsplit '\n' . init
main = interact $ (++"\n") . show . boolsum . map (part2correct . fullsplit ' ') . fullsplit '\n' . init
-- 1-3 a: abcde
-- 1-3 b: cdefg
-- 2-9 c: ccccccccc

-- x = [[char]]

revsplit :: Eq a => a -> [[a]] -> [a] -> [[a]]
revsplit _ x [] = x
revsplit splitvar x (y:more) = 
    if y == splitvar
        then revsplit splitvar ([]:x) more
    else revsplit splitvar ((y:head x):tail x) more

deepreverse x = deepreverse_ x []
deepreverse_ :: [[a]] -> [[a]] -> [[a]]
deepreverse_ [] ys = ys
deepreverse_ x ys = deepreverse_ (tail x) (stackreverse (head x):ys)

stackreverse x = stackreverse_ x []
stackreverse_ :: [a] -> [a] -> [a]
stackreverse_ [] ys = ys
stackreverse_ x ys = stackreverse_ (tail x) (head x:ys)

fullsplit char = deepreverse . revsplit char [[]]

-- this is how map works
-- mymap f [] = []
-- mymap f (x:xs) = (f x):mymap f xs

boolsum x = sum $ map fromEnum x

count char x = count_ char x 0
count_ _ [] n = n
count_ char (x:xs) n | char == x = count_ char xs (n+1) 
count_ char xs n                 = count_ char (tail xs) n

-- part1

-- after being split we have a list like this:
-- [
--     ["1-3","a:","abcde"],
--     ["1-3","b:","cdefg"],
--     ["2-9","c:","ccccccccc"]
-- ]

-- splitnums :: String => [Int]
splitnums str =  map (read::String->Int) (fullsplit '-' str)

part1correct [numstring, char, string] =
    ((head (splitnums numstring)) <= (count (head char) string))
    &&
    ((head (reverse (splitnums numstring))) >= (count (head char) string))



-- note this is 1-indexed :cries:
nthchar 1 s = head s
nthchar num s = nthchar (num-1) (tail s)

xor True False = True
xor False False = False
xor True True = False
xor False True = True
-- xor (x:xs) | x = not xor xs 
-- xor xs     = xor tail xs 
    

part2correct [numstring, char, string] =
    xor
    (nthchar (head (splitnums numstring)) string == head char)
    (nthchar (last (splitnums numstring)) string == head char)

