"""
acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
abcdefg bcdef acdfg abcdf abd abcdef bcdefg abef abcdeg ab
1111111 0111110 1011011 1111010 1101000 1111110 0111111 1100110 1111101 1100000


METHOD 1
digits char "no other than"
Table 1
1111111 = "8" abcdefg,abcdefg,abcdefg,abcdefg,abcdefg,abcdefg,abcdefg
1100000 = "1" cf,   cf,   ,    ,     ,     ,
1101000 = "7" acf,  acf,  , acf,     ,     ,
1100110 = "4" bcdf, bcdf, ,    , bcdf, bcdf, 

The digit that the "7" has that the "1" does not is a.
Table 2
1111111 = "8" cf,   cf, bdeg, bdeg, bdeg, bdeg, bdeg
1100000 = "1" cf,   cf,     ,     ,     ,     ,
1101000 = "7" cf,   cf,     ,    a,     ,     ,
1100110 = "4" bcdf, bcdf,   ,     , bcdf, bcdf, 

digit places frequencies
a=8,b=6,c=8,d=7,e=4,f=9,g=7
unique: b=6,d=7,e=4,f=9

Apply to this datum:
1111111
0111110
1011011
1111010
1101000
1111110
0111111
1100110
1111101
1100000
8,9,7,8,6,7,4
Possibilities:
Table 3
ac,f,dg,ac,b,dg,e

Apply Table 3 to Table 1
Table 4
xxxxxxx =          ac,      f,       dg,      ac,       b,      dg,       e  
1111111 = "8" abcdefg, abcdefg, abcdefg, abcdefg, abcdefg, abcdefg, abcdefg
1100000 = "1"      cf,      cf,        ,        ,        ,        ,
1101000 = "7"     acf,     acf,        ,     acf,        ,        ,
1100110 = "4"    bcdf,    bcdf,        ,        ,    bcdf,    bcdf, 


Do Sudoku to Table 4
Table 5
xxxxxxx =     c, f, g, a, b, d, e  
1111111 = "8" c, f, g, a, b, d, e
1100000 = "1" c, f, g, a, b, d, e
1101000 = "7" c, f, g, a, b, d, e
1100110 = "4" c, f, g, a, b, d, e


METHOD 2
Handwritten table
-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
	0	1	2	3	4	5	6	7	8	9	|	0	1	2	3	4	5	6	7	8	9
a	1	0	1	1	0	1	1	1	1	1	8	8	0	8	8	0	8	8	8	8	8
b	1	0	0	0	1	1	1	0	1	1	6	6	0	0	0	6	6	6	0	6	6
c	1	1	1	1	1	0	0	1	1	1	8	8	8	8	8	8	0	0	8	8	8
d	0	0	1	1	1	1	1	0	1	1	7	0	0	7	7	7	7	7	0	7	7
e	1	0	1	0	0	0	1	0	1	0	4	4	0	4	0	0	0	4	0	4	0
f	1	1	0	1	1	1	1	1	1	1	9	9	9	0	9	9	9	9	9	9	9
g	1	0	1	1	0	1	1	0	1	1	7	7	0	7	7	0	7	7	0	7	7
	6	2	5	5	4	5	6	3	7	6	|										
-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   
"""

from typing import Dict, List, TypeVar

from collections import Counter


with open("inputs/day8.txt") as f:
    lines = f.readlines()
    logs = [[x.split() for x in l.split(" | ")] for l in lines]
T = TypeVar("T", bound=List[str])
CounterStrInt = TypeVar("CounterStrInt", bound=Dict[str, int])


def get_segment_frequencies(population: T):
    vals = [c for p in population for c in p]
    return Counter(vals)


def encode_unknown_digit(d: str, frequencies: CounterStrInt):
    x = {k: frequencies[k] for k in frequencies for k in d}
    return tuple(sorted(x.values()))


LOG_MASTER = {
    "0": "abcefg",
    "1": "cf",
    "2": "acdeg",
    "3": "acdfg",
    "4": "bcdf",
    "5": "abdfg",
    "6": "abdefg",
    "7": "acf",
    "8": "abcdefg",
    "9": "abcdfg",
}
FREQS_MASTER = get_segment_frequencies([v for _, v in LOG_MASTER.items()])
ENCODING_TO_DIGIT_MASTER = {
    encode_unknown_digit(v, FREQS_MASTER): k for k, v in LOG_MASTER.items()
}


def main():
    s = 0
    for log in logs:
        population = log[0]
        output = log[1]
        freqs = get_segment_frequencies(population)
        encoding_to_digit = {encode_unknown_digit(d, freqs): d for d in population}
        assert len(encoding_to_digit) == 10
        output_scalar = sum(
            int(ENCODING_TO_DIGIT_MASTER[encode_unknown_digit(digit, freqs)])
            * 10 ** exp
            for digit, exp in zip(output, range(len(output) - 1, -1, -1))
        )
        s += output_scalar
    print(s)


# 294088 too low
# 907130 too low
if __name__ == "__main__":
    main()
