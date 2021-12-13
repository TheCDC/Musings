from day13_1 import points, instructions, create_grid, fold, count_points


def main():
    print(max(x[0] for x in points), max(x[1] for x in points))
    grid = create_grid(points)
    print(count_points(grid))
    folded = grid
    for i in instructions:
        folded = fold(grid, i[1], axis_along=i[0])
    print(count_points(folded))
    # print(*folded, sep="\n")
    # print(*grid, sep="\n")


if __name__ == "__main__":
    main()
