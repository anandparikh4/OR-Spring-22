import numpy as np

# Transportation Method
# Author : Anand Parikh
# Roll NO: 20CS10007

def NWCR(supply, demand):

    supply_2 = supply.copy()
    demand_2 = demand.copy()

    i = 0
    j = 0

    BFS = []

    while len(BFS) < len(supply) + len(demand) - 1:

        s = supply_2[i]
        d = demand_2[j]

        v = min(s, d)

        supply_2[i] -= v
        demand_2[j] -= v

        BFS.append(((i, j), v))

        if supply_2[i] == 0 and i < len(supply) - 1:
            i += 1

        elif demand_2[j] == 0 and j < len(demand) - 1:
            j += 1

    return BFS

def transportation(supply, demand, c):

    bs, bd, bc = make_balanced(supply, demand, c)
    cnt = 0

    def inner(BFS, cnt):

        us, vs = init_uv(BFS, bc)
        ws = init_w(BFS, bc, us, vs)

        if improve(ws):
            cnt += 1
            var = enter_post(ws)
            loop = get_loop([p for p, v in BFS], var)
            print("Iteration", cnt, " The loop is ", loop)
            print("The entering variable position is:", var)
            return inner(loop_pivoting(BFS, loop), cnt)

        return BFS, cnt

    BV, cnt = inner(NWCR(bs, bd), cnt)

    ans = np.zeros((len(bc), len(bc[0])))

    for (i, j), v in BV:

        ans[i][j] = v

    return ans
def get_loop(BFS, p):
    def inner(loop):

        if len(loop) > 3:

            x = len(next_(loop, [p])) == 1
            if x: return loop

        unv = list(set(BFS) - set(loop))

        possible = next_(loop, unv)

        for next_node in possible:

            new_loop = inner(loop + [next_node])
            if new_loop: return new_loop

    return inner([p])


def init_w(b, c, us, vs):
    ws = []
    for i, row in enumerate(c):
        for j, cost in enumerate(row):
            nb = all([p[0] != i or p[1] != j for p, v in b])
            if nb:
                ws.append(((i, j), us[i] + vs[j] - cost))
    return ws

def init_uv(BFS, c):

    us = [None] * len(c)
    vs = [None] * len(c[0])

    us[0] = 0
    bfs_copy = BFS.copy()

    while len(bfs_copy) > 0:

        for index, bv in enumerate(bfs_copy):
            i, j = bv[0]

            if us[i] is None and vs[j] is None:
                continue

            cost = c[i][j]

            if us[i] is None:
                us[i] = cost - vs[j]

            else:
                vs[j] = cost - us[i]

            bfs_copy.pop(index)
            break

    return us, vs

def next_(loop, unvisited):
    last = loop[-1]

    row = [n for n in unvisited if n[0] == last[0]]
    col = [n for n in unvisited if n[1] == last[1]]

    if len(loop) < 2:
        return row + col
    else:

        prev = loop[-2]
        rm = prev[0] == last[0]

        if rm: return col
        return row

def enter_post(w):
    w2 = w.copy()
    w2.sort(key=lambda w: w[1])
    return w2[-1][0]


def loop_pivoting(BFS, loop):

    even = loop[0::2]
    odd = loop[1::2]

    BV = lambda pos: next(v for p, v in BFS if p == pos)
    pos = sorted(odd, key=BV)[0]
    val = BV(pos)
    new_bfs = []

    for p, v in [bv for bv in BFS if bv[0] != pos] + [(loop[0], 0)]:
        if p in even:
            v += val

        elif p in odd:
            v -= val

        new_bfs.append((p, v))

    return new_bfs


def improve(w):

    for dontcare, val in w:
        if val > 0: return True

    return False

def total_cost(c, s):
    total_cost = 0
    for i, row in enumerate(c):
        for j, cost in enumerate(row):
            total_cost += cost * s[i][j]
    return total_cost

def make_balanced(s, d, tc):

    ts = sum(s)
    td = sum(d)

    if ts < td:
        pen = np.zeros((1, len(d)))
        s.append(td - ts)
        new_supply = s
        nc = np.concatenate([tc, pen], axis=0)
        return new_supply, d, nc

    if ts > td:
        d.append(ts - td)
        nd = d
        nc = np.concatenate([tc, np.zeros((len(s), 1))], axis=1)
        return s, nd, nc

    return s, d, tc

def user_input():

    s = [float(i) for i in input().split(" ")]
    d = [float(i) for i in input().split(" ")]

    tc = []
    for i in range(len(s)):
        r = [float(j) for j in input().split(" ")]
        tc.append(r)

    return s, d, np.array(tc)

if __name__ == '__main__':
    supply, demand, transportation_cost = user_input()

    solution = transportation(supply, demand, transportation_cost)

    print("The final solution for each variable is")

    print(solution)

    print('total cost: ', total_cost(transportation_cost, solution))