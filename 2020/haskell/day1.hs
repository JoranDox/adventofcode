import Prelude

-- lines splits the input on \n
-- read reads the input and casts to Int in this case
-- map applies read to lines in this case
-- apply f (see below) to this list
-- show does to string
-- ++"\n" does add \n to string
-- interact does ?
main = interact $ (++"\n") . show . fgen 2020 . map (read :: String -> Int) . lines

-- if 
-- elem a b means a in b 
f :: [Int] -> [Int]
f (x:xs) = 
    if elem (2020 - x) xs 
        then [x, 2020-x, 2020-x, x * (2020 - x)]
    else f xs

-- same but with var instead of 2020
fvar a (x:xs) = 
    if elem (a - x) xs 
        then [x, a-x, a-x, x * (a - x)]
    else fvar a xs

fgen n lst = head [ [x, y, z, x*y*z] | x<-lst, y<-lst, let z = n-x-y, elem z lst]
-- same but using fvar as subfunc
-- f2 :: [Int] -> [Int]
-- f2 (x:xs) =
--     if elem (2020 - a - b) xs
--         then [a, b, 2020-a-b, a * b * (2020 - a - b)] 
--     else f2 (b:xs)