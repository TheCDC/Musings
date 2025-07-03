from itertools import permutations

digits_free = tuple(range(1, 9 + 1))
BEST = 0


def calculate(solution: tuple[int]) -> tuple[int]:
    global BEST
    a, b, c, d, e, f, g, h, _ = solution
    checks = [  # (expression, target value)
        ((a + b) / c, 1),
        ((d + 5) / e, 1),
        (f + g + h, 15),
        ((a + d) / f, 2),
        ((b + 5) * g, 44),
        ((c + e) * h, 13),
    ]
    count = sum(a == b for a, b in checks)
    if count > BEST:
        # print(, checks, count)
        render(solution, count)
        BEST = count
    return checks


def check(solution: tuple[int]) -> bool:
    checks = calculate(solution)
    return all(a == b for a, b in checks)


def solve():
    for p in permutations(digits_free):
        if check(p):
            return p
    return None


def render(solution, count):
    a, b, c, d, e, f, g, h, _ = solution
    if count is not None:
        print()
    print(
        f"""Score: {count}/{len(solution)}
{a}+{b}/{c}=1
+■+■+■
{d}+5/{e}=1
/■x■x■
{f}+{e}+{g}=15
=■=■=■
2_4_1_
__4_3_
"""
    )


def main():
    print(f"Using digits {digits_free}")
    print(solve())


if __name__ == "__main__":
    main()
