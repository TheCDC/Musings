from day13_1 import points, instructions, create_grid, fold, count_points


def main():
    grid = create_grid(points)
    folded = grid
    for i in instructions:
        folded = fold(folded, i[1], axis_along=i[0])
    print(*("".join([[".", "#"][c] for c in i]) for i in folded), sep="\n")
    # print(*folded, sep="\n")
    # print(*grid, sep="\n")


if __name__ == "__main__":
    main()
