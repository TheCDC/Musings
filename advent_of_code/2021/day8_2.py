"""
acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
abcdefg bcdef acdfg abcdf abd abcdef bcdefg abef abcdeg ab
1111111 0111110 1011011 1111010 1101000 1111110 0111111 1100110 1111101 1100000

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



"""
