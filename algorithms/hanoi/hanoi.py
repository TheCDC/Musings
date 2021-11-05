import sys
from time import sleep
from typing import Callable, List, Optional
from pathlib import Path


def move(state: List[List[int]], a: int, b: int):
    state = [i[:] for i in state]
    v = state[a].pop()
    if len(state[b]) > 0:
        m = min(state[b])
        if m < v:
            raise ValueError(f"Cannot move {v} onto {m}")
    state[b].append(v)
    return state


def solve(size: int = 2, pegs: int = 3, each_step: Optional[Callable] = None):
    state = [
        list(reversed(range(size))),
    ] + [[] for _ in range(pegs - 1)]
    disc_to_move = size - 1  # want to move biggest disc
    peg_target = pegs - 1  # to endmost peg
    print(state, disc_to_move, peg_target)
    return solve_inner(size, state, disc_to_move, peg_target, each_step=each_step)


def solve_inner(
    size: int,
    state: List[List[int]],
    disc_to_move: int,
    peg_target: int,
    each_step: Optional[Callable] = None,
    depth: int = 0,
):
    peg_with_my_disc = max(
        enumerate(state), key=lambda tup: tup[1].count(disc_to_move)
    )[0]

    src_blocked_by_discs_above = min(state[peg_with_my_disc]) < disc_to_move
    dest_blocked_by_discs_below = (
        min(state[peg_target], default=disc_to_move) < disc_to_move
    )
    debug_vars = {
        "state": state,
        "disc_to_move": disc_to_move,
        "peg_target": peg_target,
        "idx_desired_disc": peg_with_my_disc,
    }
    # print(*debug_vars.items())
    if len(state[-1]) == size:
        return state
    if peg_with_my_disc == peg_target:
        return state

    if dest_blocked_by_discs_below or src_blocked_by_discs_above:

        blocker = (
            max(
                d for d in state[peg_with_my_disc] if d < disc_to_move
            )  # dest_blocked_by_discs_below
            if src_blocked_by_discs_above
            else min(state[peg_target])
        )
        target = (
            (peg_with_my_disc + 1) % len(state)
            if src_blocked_by_discs_above
            else (peg_target + 1) % len(state)
        )
        target = (
            (target + 1) % len(state)
            if target in [peg_with_my_disc, peg_target]
            else target
        )
        state_move_target = solve_inner(
            size,
            solve_inner(
                size,
                state,
                blocker,
                peg_target=target,
                each_step=each_step,
                depth=depth + 1,
            ),
            disc_to_move,
            peg_target,
            each_step=each_step,
            depth=depth + 1,
        )
        return (
            solve_inner(
                size,
                state_move_target,
                blocker,
                peg_target,
                each_step=each_step,
                depth=depth + 1,
            )
            if blocker != 0 or len(state[-1]) != size
            else state_move_target
        )
    state_moved_desired = move(state, peg_with_my_disc, peg_target)
    if each_step:
        each_step(
            size,
            state,
            state_moved_desired,
            disc_to_move,
            peg_target,
            peg_with_my_disc,
            peg_target,
            depth,
        )
    return state_moved_desired


def render_move(
    size: int,
    state: List[List[int]],
    state_next: List[List[int]],
    disc_to_move: int,
    peg_target: int,
    peg_from: int,
    peg_to: int,
    depth: int,
):
    """"""
    char_disc_segment = "-"
    # return '\n'.join([])
    width_column_size = size + 1
    header_row_blank = [" " * (width_column_size * 2 - 1) for _ in state]
    header_row = header_row_blank[:]
    header_space_padding = " " * (width_column_size - 1)
    header_row[peg_from] = header_space_padding + "^" + header_space_padding
    header_row[peg_to] = header_space_padding + "v" + header_space_padding
    rows = [header_row, header_row_blank]
    for index_row in range(size):
        tokens = []
        for index_peg, peg in enumerate(state_next):
            index_to_get = size - index_row - 1
            if len(peg) > index_to_get:
                disc_value = peg[index_to_get] + 1
                num_spaces = size - disc_value
                chars_spaces = " " * num_spaces
                chars_disc = char_disc_segment * disc_value

                tokens.extend([chars_spaces, chars_disc,
                              "|", chars_disc, chars_spaces])
            else:

                tokens.extend([" " * size, "|", " " * size])
        rows.append(tokens)
    rows.append([len("".join(header_row_blank)) * "_"])
    return "\n".join(["".join(row) for row in rows])


def create_callback(f=sys.stdout, delay=0):
    count = 0

    def inner(
        size: int,
        state: List[List[int]],
        state_next: List[List[int]],
        disc_to_move: int,
        peg_target: int,
        peg_from: int,
        peg_to: int,
        depth: int,
    ):
        nonlocal count
        if delay:
            sleep(delay)
        # print(
        #     depth,
        #     state_next,
        #     "move disc",
        #     disc_to_move,
        #     "from peg",
        #     peg_from,
        #     "to peg",
        #     peg_target,
        # ),
        print(count, file=f)
        print(
            render_move(
                size,
                state,
                state_next,
                disc_to_move,
                peg_target,
                peg_from,
                peg_to,
                depth,
            ),
            file=f,
            flush=True,
        )
        count += 1

    return inner


for size in range(1, 12):
    with open(Path(__file__).parent/'solutions' / f"hanoi-solution-{size}.txt", "w") as f:
        print(solve(size, each_step=create_callback(f)))
print(solve(8, 3, each_step=create_callback(sys.stdout, 0.05)))
