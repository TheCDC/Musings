from day12_1 import solve, node_is_legal, mapping
from util import AdventTimer


def main():
    with AdventTimer() as t:
        paths_final = solve(
            mapping,
            neighbor_legality=lambda a, b, **kwargs: node_is_legal(
                a,
                b,
                **kwargs,
                allowed_num_small_cave=2,
            ),
        )
        print(t.duration)
    print(len(paths_final))


# 147848 correct
if __name__ == "__main__":
    main()
