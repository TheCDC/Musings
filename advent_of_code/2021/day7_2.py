from day7_1 import solve, nums


def cost_triangle(x: int):
    return (x * (x + 1)) // 2


print(solve(nums=nums, distance_cost=cost_triangle))
# 146343915 high
# 95851339 correct
