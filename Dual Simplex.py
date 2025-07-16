import pandas as pd
import numpy as np

# Dual Simplex Code
# Author : Anand Parikh
# Roll NO: 20CS10007

INF = 10e9

def objective_f_value(CB, B, D, op):

    if op == 'max':
        return np.dot(np.transpose(CB), B) + D

    else:
        return -np.dot(np.transpose(CB), B) + D

def dual(a, c, cn, cb, d, b, non_basic_var, basic_var, all_var, x, op, num_surplus_variables, slack, artificial):
    n_prime = a.shape[1]
    m_prime = a.shape[0]

    it = 0
    while True:
        it += 1

        if it > 10:
            print(
                "The table has repeated. Due to this there is infinite iterations. Hence cannot solve by dual simplex.")
            exit(0)

        print("-" * 60)

        print("Iteration ", it)

        table_print(a, c, d, b, cb, x, non_basic_var, basic_var, op)

        print("f (objective function) =  ", round(objective_f_value(cb, b, d, op), 5))

        print("The values for x are:")
        l = []
        for i in range(len(x)):
            l.append("x" + str(i + 1) + '=' + str(x[i]))
        print(l)
        u = np.argmin(b)
        cv = b[u]
        if cv > 0:
            if it > artificial:
                print("-" * 60)
                print("No negative XB present, process terminated")
                print("List of non basic variables ", non_basic_var)
                print("This is the list of all basic variables are ", basic_var)
                print("The values for x are:")
                l = []
                for i in range(len(x)):
                    l.append("x" + str(i + 1) + '=' + str(x[i]))
                print(l)
                print("Objective value:",
                      round(objective_f_value(cb, b, d, op), 5))
                return
            else:
                print("-" * 60)
                print("Infeasible, as some non basic variables are non-zero")
                print("List of non basic variables", non_basic_var)
                print("Basic variables ", basic_var)
                print("x values:")
                X = []
                for i in range(len(x)):
                    X.append("x" + str(i + 1))
                print(X)
                print("Objective function value :  :",
                      round(objective_f_value(cb, b, d, op), 5))
                return
        if cv == 0:
            x_1 = np.copy(x)
            ratios = np.empty((n_prime,))
            v = 0
            pivot = -1
            min_ratio = INF
            for i in range(n_prime):
                if a[u][i] == 0:
                    continue
                ratios[i] = abs(c[i] / a[u][i])
                if min_ratio > ratios[i] > 0:
                    v = i
                    min_ratio = ratios[i]
                    pivot = a[u][v]
            if min_ratio == INF:
                print("-" * 60)
                print("No more optimal soltions")
                return
            new_a = np.empty((m_prime, n_prime))
            for i in range(m_prime):
                for j in range(n_prime):
                    if i == u and j == v:
                        new_a[i][j] = 1
                    elif i == u:
                        new_a[i][j] = a[i][j] / pivot
                    elif j == v:
                        new_a[i][j] = 0
                    else:
                        new_a[i][j] = (pivot * a[i][j] - a[i][v] * a[u][j]) / pivot
            new_c = np.copy(c)
            for j in range(n_prime):
                if j == v:
                    new_c[j] = 0
                else:
                    new_c[j] = round((pivot * c[j] - c[v] * a[u][j]) / pivot, 6)
            new_b = np.copy(b)
            for j in range(m_prime):
                if j == u:
                    new_b[j] = b[j] / pivot
                else:
                    new_b[j] = (pivot * b[j] - a[j][v] * b[u]) / pivot
            a = np.copy(new_a)
            c = np.copy(new_c)
            b = np.copy(new_b)
            temp2 = cb[u]
            cb[u] = cn[v]
            cn[v] = temp2
            temp1 = non_basic_var[v]
            non_basic_var[v] = basic_var[u]
            basic_var[u] = temp1
            for i in range(m_prime):
                s = basic_var[i]
                x[int(s[1]) - 1] = b[i]
            for i in range(n_prime):
                s = non_basic_var[i]
                x[int(s[1]) - 1] = 0
            x_2 = np.copy(x)
            table_print(a, c, d, b, cb, non_basic_var, basic_var, x,
                        op)
            print("Infinitely many solutions: \u03BB", x_1, " + (1-\u03BB)", x_2)
            return
        else:
            print("Most negative Xb =", cv, " in row", u + 1)
            ratios = np.empty((n_prime,))
            v = 0
            pivot = -1
            min_ratio = INF
            for i in range(n_prime):
                if a[u][i] == 0:
                    continue
                ratios[i] = abs(c[i] / a[u][i])
                if min_ratio > ratios[i] > 0:
                    v = i
                    min_ratio = ratios[i]
                    pivot = a[u][v]
            print("Ratios of corresponding row", ratios)
            print("Minimum ratio: ", min_ratio)
            print("Pivot = ", pivot, " , coordinates : ", u + 1, " ",
                  v + 1)

            if min_ratio == INF:
                print("-" * 60)
                print("Unbounded")
                print("Objective function:", objective_f_value(cb, b, d, op))
                print("x values:", x)
                return

            new_a = np.empty((m_prime, n_prime))
            for i in range(m_prime):
                for j in range(n_prime):
                    if i == u and j == v:
                        new_a[i][j] = 1
                    elif i == u:
                        new_a[i][j] = a[i][j] / pivot
                    elif j == v:
                        new_a[i][j] = 0
                    else:
                        new_a[i][j] = (pivot * a[i][j] - a[i][v] * a[u][j]) / pivot

            new_c = np.copy(c)

            for j in range(n_prime):
                if j == v:
                    new_c[j] = 0
                else:
                    new_c[j] = round((pivot * c[j] - c[v] * a[u][j]) / pivot, 6)

            new_b = np.copy(b)
            for j in range(m_prime):
                if j == u:
                    new_b[j] = b[j] / pivot
                else:
                    new_b[j] = (pivot * b[j] - a[j][v] * b[u]) / pivot

            a = np.copy(new_a)
            c = np.copy(new_c)
            b = np.copy(new_b)

            temp2 = cb[u]
            cb[u] = cn[v]
            cn[v] = temp2

            temp1 = all_var[v]
            non_basic_var.remove(all_var[v])

            if basic_var[u] not in non_basic_var:
                non_basic_var.append(basic_var[u])

            basic_var[u] = temp1

            for i in range(len(basic_var)):
                s = basic_var[i]
                x[int(s[1]) - 1] = b[i]

            for i in range(len(non_basic_var)):
                s = non_basic_var[i]
                x[int(s[1]) - 1] = 0


def standard_form(n, m, a, c, d, b, s):
    artificial = 0
    num_surplus_variables = 0

    slack = 0
    k = n + 1
    x = []

    add_col = []
    basic_var = []
    non_basic_var = []

    slack_var = []
    artificial_var = []
    surplus_var = []
    all_var = []

    a = np.array(a)
    b = np.array(b)

    for i in range(n):
        non_basic_var.append("x" + str(i + 1))
        x.append(0)

    constraints = []

    for j, row in enumerate(a):
        constraint = ""

        for i, z in enumerate(row):
            constraint += str(z) + "x" + str(i + 1) + " + " * (i != len(row) - 1)

        if s[j] == "<=":
            constraint += " + x" + str(k)
            basic_var.append("x" + str(k))
            slack_var.append("x" + str(k))
            x.append(b[j])
            temp_col = np.zeros((m,))
            temp_col[j] = 1
            add_col.append(temp_col)
            k += 1
            slack += 1

        constraint += " = " + str(b[j])
        constraints.append(constraint)

    all_var = non_basic_var + basic_var

    cn = np.zeros((len(all_var)))
    cb = np.zeros((len(basic_var)))

    for i, var in enumerate(basic_var):
        cb[i] = 0

    for i in range(len(non_basic_var)):
        cn[i] = c[i]

    c = np.empty((len(all_var)))
    a = np.concatenate([a, np.array(add_col)], axis=1)

    for i in range(len(all_var)):
        c[i] = 0
        c[i] += (np.dot(np.transpose(cb), a[:, i]) - cn[i])

    print("Objective function (max): ")
    obj_func = ""

    for i, var in enumerate(non_basic_var):
        obj_func += "-" + str(-c[i]) + str(var) + " "

    print(obj_func + " + ", d)

    for constraint in constraints:
        print(constraint)

    return a, b, cb, cn, c, np.array(
        x), non_basic_var, basic_var, all_var, artificial_var, slack_var, surplus_var

def table_print(a, c, d, b, cb, x, non_basic_var, basic_var, op):
    l = []
    for basic in non_basic_var:
        l.append(basic)
    print("Non-basic variables = ", l)
    l = []
    for non_basic in basic_var:
        l.append(non_basic)
    print("Basic variables = ", l)

    print("Matrix A"), print(a)

    print("XB"), print(b)

    print("Row c:"), print(-c)

    print("CB"), print(cb)

    print("CN"), print(cn)

    print("Optimal Value:", round(objective_f_value(cb, b, d, op), 5))

def pivot_print(CV, v, u, r, minimumratio, p):

    print("c = ", -CV, " for column", v + 1)

    print("Column ratios", r)

    print("Min ratio:", minimumratio)

    print("Pivot element ", p, "  ,coordinates ", u + 1, " ", v + 1)

def user_input():

    op = str(input())

    print("Number of variables")
    n = int(input())

    print("Number of constraints")
    m = int(input())

    print("Coefficients in objective function f: ")
    coeff = [float(i) for i in input().split(" ")]
    if op == 'min':
        coeff = [-x for x in coeff]

    print("Constant in objective function (0 if not present)")
    constant = float(input())

    print("Enter the matrix A, row by row")
    a = []

    for i in range(m):
        a.append([float(j) for j in input().split(" ")])

    print("Enter the constants/RHS bi of each equation")
    b = [float(i) for i in input().split(" ")]

    print("Enter equation / in-equation type")
    s = input().split(" ")

    for i,k in enumerate(s):

        if(k == '='):
            print("Equality type constraint NOT ALLOWED")
            exit(-1)

        if(k == '>='):
            for j in range(n):
                a[i][j] *= -1
            b[i] *= -1
            s[i] = '<='

    return n, m, a, np.array(coeff), constant, b, s, op

if __name__ == '__main__':

    test_cases = int(input("Number of test cases:"))

    M = 10000

    for i in range(test_cases):
        print("*" * 60)
        # print("This is the solution to the testcase number ", i + 1)
        n, m, a, c, d, b, s, op = user_input()

        a, b, cb, cn, c, x, non_basic_var, basic_var, all_var, artificial_var, slack_var, surplus_var = standard_form(n, m, a, c, d, b, s)

        dual(a, c, cn, cb, d, b, non_basic_var, basic_var, all_var, x, op, len(surplus_var), len(slack_var), len(artificial_var))