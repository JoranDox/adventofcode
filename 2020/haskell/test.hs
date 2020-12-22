-- fac :: (Eq p, Num p) => p -> p
-- fac 0 = 1
-- fac n = n * fac (n-1)

-- main :: IO ()
-- main = print (fac 42)

-- -- import qualified Data.Text    as Text
-- -- import qualified Data.Text.IO as Text

-- main = do
--     ls <- fmap Text.lines (Text.readFile "day1inputex.txt")

--     mapM print ls

--     print $ [ x + y | x <- ls, y <- ls ] 


import Debug.Trace

fib :: Int -> Int
fib n | trace ("fib input:" ++ show n) False = undefined
fib 0 = 0
fib 1 = 1
fib n = fib (n-1) + fib (n-2)



stackreverse_ a b | trace ("stackreverse input:" ++ show a ++ show b) False = undefined
stackreverse_ [] ys = ys
stackreverse_ x ys = stackreverse_ (tail x) (head x:ys)
