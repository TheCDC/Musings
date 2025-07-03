from itertools import product


options = (
    ("+2", "+8"),
    ("*2", "*5"),
    ("+4", "+7"),
    ("+3", "+12"),
    ("-5", "-17"),
    ("+2", "+9"),
)
for p in product(*options):
    pp = (p for p in p)
    x = next(pp)
    for xx in pp:
        x = eval(f"({x}){xx}")
    print("YES" if x == 30 else "NO", x, "\t".join(p), sep="\t")
