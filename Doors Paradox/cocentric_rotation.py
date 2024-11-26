coefficients = [(1, 0, 0, -1), (0, -1, 1, 0), (1, -1, 0, -1)]


def check(t):
    return all(i == 0 for i in t)


def add(t, cs, base=8):
    return tuple((tt + cc) % base for tt, cc in zip(t, cs))


def runlengths(state):
    count = 0
    cur = state[0]
    out = []
    for i in state:
        if i == cur:
            count += 1
        else:
            out.append((cur, count))
            count = 1
            cur = i

    out.append((cur, count))
    return out


def search(state):
    mem = []

    def inner(
        state, target=(0, 0, 0, 0), history_state=None, history_moves=None, depth=1000
    ):
        if check(state):
            print(state, len(history_moves), runlengths(history_moves))
            return state
        if state in mem:
            # print(state)
            return False
        if depth == 0:
            # print("depth error", state, history_moves)
            return
        mem.append(state)
        history_state = history_state if history_state else []
        history_moves = history_moves if history_moves else []
        if state == target:
            print(state, target, history_moves)
            return history_state
        for index_move, move in reversed(list(enumerate(coefficients))):
            state_next = add(state, move)
            if state_next in history_state:
                continue
            inner(
                state_next,
                history_state=history_state + [state_next],
                history_moves=history_moves + [index_move],
                depth=depth - 1,
            )

    return inner(state)


def main():
    state = [int(i) for i in input("enter puzzle state: ").split()]
    print(state)
    search(state)


if __name__ == "__main__":
    main()
