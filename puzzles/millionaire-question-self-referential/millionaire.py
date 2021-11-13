from itertools import combinations, permutations, product
from functools import reduce

question = """If you choose an answer to this question at random what is the chance you will get it correct.
A: 25%
B: 0%
C: 50%
D: 25%
"""

assumptions = """1. Each question has exactly one correct answer.
2. Answer A = Answer D."""
legend = """~ : boolean negation AKA \"not\". True iff operand is false.
& : boolean \"and\". True iff both operands are true."""
solution_notes = """Recall that A=B.
This gives us a new expression."""
N = 4


def print_table(expression_final, tup):
    expr_val = (
        bool(
            reduce(
                lambda x, y: x ^ y,
                tup,
            )
        )
        and all(not (x and y) for x, y in combinations(tup, 2))
    )
    print(
        (len(expression_final) - 8) * " ",
        expr_val,
        *tup,
        tup,
        sep="\t",
    )


def table_exactly_one():
    s = ord("a")
    vars = [chr(s + i) for i in range(N)]

    odds = "^".join(vars)
    no_two = "&".join(["~(" + "&".join(t) + ")" for t in combinations(vars, 2)])
    print('1. "an odd number are true"', ":", odds)
    print(
        '2. "No more than one true"',
        "=",
        no_two,
        '\n\tAKA "no combination of two"',
    )
    print('"exactly one is true" = "an odd number are true and no two are true"')
    expression_final = f"({odds})&({no_two})"
    print('"exactly one is true"', "=", expression_final)
    print(" === Truth Table === ")
    print(expression_final, "a", "b", "c", "d", sep="\t")
    for tup in product([False, True], repeat=4):
        values = list(tup)
        # values[2] = values[0]
        print_table(expression_final=expression_final, tup=tup)
    return expression_final


def solution(expr: str):
    expr = expr.replace("b", "a")
    print(expr, "a", "b", "c", "d", sep="\t")
    for tup in product([False, True], repeat=4):
        values = list(tup)
        values[2] = values[0]
        print_table(expression_final=expr, tup=values)


def main():
    print(question)
    print("GIVENS")
    print(assumptions)
    print()
    print("LEGEND")
    print(legend)
    print()
    print("DEFINITIONS")
    expr = table_exactly_one()
    print()
    print("SOLUTION")
    solution(expr)


if __name__ == "__main__":
    main()
