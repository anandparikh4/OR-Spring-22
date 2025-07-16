"""
  Author  : Abhay Kumar Keshari
  Roll No : 20CS10001
  Date    : Spring 2022
  Course  : Operation Research MA30014
"""

import numpy as np

INFINITY = 10e9


def second_phase(matrix, col, c, cb, cn, c_original, x, b_var, nb_var, art_var, slack_var, sur_var):
    rm_indices = []
    while len(c_original) < len(b_var) + len(nb_var):
        c_original.append(0)
    for i, var in enumerate(nb_var):
        cn[i] = c_original[int(var[1]) - 1]
    for i, var in enumerate(b_var):
        cb[i] = c_original[int(var[1]) - 1]
    for i in range(len(nb_var)):
        c[i] = -1 * (np.dot(np.transpose(cb), matrix[:, i]) - cn[i])
    for i, var in enumerate(nb_var):
        if var in art_var:
            rm_indices.append(i)
    for var in art_var:
        nb_var.remove(var)
    cn = np.delete(cn, rm_indices, axis=0)
    matrix = np.delete(matrix, rm_indices, axis=1)
    c = np.delete(c, rm_indices, axis=0)

    return matrix, col, c, cn, cb, b_var, nb_var, sur_var, slack_var, art_var


def first_phase(n, m, a, d, b, s):
    n_art_var = 0
    n_sur_var = 0
    n_slack_var = 0
    k = n + 1
    x = []
    add_col = []
    nb_var = []
    b_var = []
    slack_var = []
    art_var = []
    sur_var = []
    a = np.array(a)
    b = np.array(b)
    for i in range(n):
        nb_var.append("x" + str(i + 1))
        x.append(0)
    constraints = []
    for j, row in enumerate(a):
        constraint = ""
        for i, z in enumerate(row):
            constraint += str(z) + "x" + str(i + 1) + " + " * (i != len(row) - 1)
        if s[j] == "=":
            constraint += " + x" + str(k)
            b_var.append("x" + str(k))
            art_var.append("x" + str(k))
            x.append(b[j])
            k += 1
            n_art_var += 1
        elif s[j] == "<=":
            constraint += " + x" + str(k)
            b_var.append("x" + str(k))
            slack_var.append("x" + str(k))
            x.append(b[j])
            k += 1
            n_slack_var += 1
        else:
            constraint += " - x" + str(k) + " + x" + str(k + 1)
            b_var.append("x" + str(k + 1))
            art_var.append("x" + str(k + 1))
            x.append(0)
            nb_var.append("x" + str(k))
            sur_var.append("x" + str(k))
            x.append(b[j])
            n_sur_var += 1
            temp_col = np.zeros((m,))
            temp_col[j] = -1
            add_col.append(temp_col)
            n_art_var += 1
            k += 2
        constraint += " = " + str(b[j])
        constraints.append(constraint)
    if len(sur_var) > 0:
        additional = np.array(add_col).transpose()
        a = np.concatenate([a, additional], axis=1)

    cn = np.zeros((len(nb_var)))
    cb = np.zeros(((len(b_var))))
    for i, var in enumerate(b_var):
        if var in art_var:
            cb[i] = -1
    c = np.zeros((len(nb_var)))
    for i in range(len(nb_var)):
        c[i] = -1 * (np.dot(np.transpose(cb), a[:, i]) - cn[i])
    print("%" * 90)
    print("This is Phase-1")
    print("The artificial objective function to maximize is")
    obj_func = ""
    for i, var in enumerate(art_var):
        obj_func += "-" + str(var) + " "
    print(obj_func + " + ", d)
    for constraint in constraints:
        print(constraint)
    return a, b, cb, cn, c, np.array(
        x), nb_var, b_var, art_var, slack_var, sur_var


def print_table(matrix, c, d, col, cb, x, nb_var, b_var, objective):
    l_ = []
    for basic in nb_var:
        l_.append(basic + '=' + str(x[int(basic[1]) - 1]))
    print("Non Basic Variables = ", l_)
    l_ = []
    for non_basic in b_var:
        l_.append(non_basic + '=' + str(x[int(non_basic[1]) - 1]))
    print("Basic Variables = ", l_)
    print("Matrix: ", matrix)
    print("Xb: ", col)
    print("Bottom row of table: ", -c)
    print("Coefficients of basic variable: ", cb)
    print("Coefficients of non-basic variable: ", cn)
    print("Optimal value of objective function: ", round(evaluate_obj_fn(cb, col, d, objective), 5))


def artificial_obj_function_val(artificial_variables_list, x, d, objective):
    c = np.zeros((len(x),))
    for var in artificial_variables_list:
        c[int(var[1]) - 1] = 1
    if objective == 'max':
        return np.dot(c, x) + d
    else:
        return -np.dot(c, x) + d


def phase_one_simplex(matrix, col, cb, cn, c, d, x, nb_var, b_var,
                      art_var, slack_var, sur_var):
    ite = 0
    n_prime = matrix.shape[1]
    m_prime = matrix.shape[0]
    n_art_var = len(art_var)
    while True:
        ite += 1
        print("-" * 60)
        print("Iteration ", ite)
        print_table(matrix, c, d, col, cb, x, nb_var, b_var, objective)
        v = np.argmax(c)
        cv = c[v]
        if cv <= 0:
            if ite > n_art_var:
                print("First phase")
                print("Basic variables: ", nb_var)
                print("Non-basic variables: ", b_var)

                li = []
                for i in range(len(x)):
                    li.append("x" + str(i + 1) + '=' + str(round(x[i], 5)))
                print("The values for x:", li)
                print("Final value of the artificial objective function after phase one is:",
                      round(artificial_obj_function_val(art_var, x, d, objective), 5))
                return matrix, col, c, x, ite, 1
            else:
                print("Infeasible Solution")
                print("Basic variables: ", nb_var)
                print("Non-basic variables: ", b_var)
                li = []
                for i in range(len(x)):
                    li.append("x" + str(i + 1) + '=' + str(round(x[i], 5)))
                print("The values for x are:", li)
                print("As you can see the the value of artificial objective function is :",
                      round(artificial_obj_function_val(art_var, x, d, objective), 5), "which is not zero")
                return matrix, col, c, x, ite, 0
        else:
            print("The value of most negative c is", -cv, " Corresponding to column", v + 1)
            ratios = np.empty((m_prime,))
            u = 0
            pivot = -1
            min_ratio = INFINITY
            for i in range(m_prime):
                if matrix[i][v] == 0:
                    continue
                ratios[i] = col[i] / matrix[i][v]
                if min_ratio > ratios[i] >= 0:
                    u = i
                    min_ratio = ratios[i]
                    pivot = matrix[u][v]
            print("The ratios are for corresponding column", ratios)
            print("The minimum ratio is:", min_ratio)
            print("The pivot element is ", pivot, " and corresponding coordinates(1 based indexing) is", u + 1, " ",
                  v + 1)
            if min_ratio == INFINITY:
                print("The problem is unbounded")
                print(print("the value of artificial objective function is :",
                            round(artificial_obj_function_val(art_var, x, d, objective), 5)))
                print("The values for x are:", x)
                return matrix, col, c, x, ite, 0
            a_new = np.empty((m_prime, n_prime))
            for i in range(m_prime):
                for j in range(n_prime):
                    if i == u and j == v:
                        a_new[i][j] = 1 / matrix[i][j]
                    elif i == u:
                        a_new[i][j] = matrix[i][j] / pivot
                    elif j == v:
                        a_new[i][j] = -matrix[i][j] / pivot
                    else:
                        a_new[i][j] = (pivot * matrix[i][j] - matrix[i][v] * matrix[u][j]) / pivot
            c_new = np.copy(c)
            for j in range(n_prime):
                if j == v:
                    c_new[j] = round(-c[j] / pivot, 6)
                else:
                    c_new[j] = round((pivot * c[j] - c[v] * matrix[u][j]) / pivot, 6)
                if abs(c_new[j]) <= 0.0001:
                    c_new[j] = 0
            b_new = np.copy(col)
            for j in range(m_prime):
                if j == u:
                    b_new[j] = col[j] / pivot
                else:
                    b_new[j] = (pivot * col[j] - matrix[j][v] * col[u]) / pivot
            matrix = np.copy(a_new)
            c = np.copy(c_new)
            col = np.copy(b_new)
            temp1 = nb_var[v]
            nb_var[v] = b_var[u]
            b_var[u] = temp1
            temp2 = cb[u]
            cb[u] = cn[v]
            cn[v] = temp2
            for i in range(m_prime):
                s = b_var[i]
                x[int(s[1]) - 1] = col[i]
            for i in range(n_prime):
                s = nb_var[i]
                x[int(s[1]) - 1] = 0


def evaluate_obj_fn(c, b, d, objective):
    if objective == 'max':
        return np.dot(np.transpose(c), b) + d
    else:
        return -np.dot(np.transpose(c), b) + d


def print_pivot(cv, v, u, ratios, min_ratio, pivot):
    print("Value of c: ", -cv, "column: ", v + 1)
    print("Column-wise ratios: ", ratios)
    print("Minimum ratio:", min_ratio)
    print("Pivot element: ", pivot, "Co-ordinates: ", u + 1, " ", v + 1)


def second_phase_simplex(matrix, c, cn, cb, d, col, nb_var, b_var, x, objective, n_sur_var, num_slack_variables,
                         n_art_var, ite):
    n_prime = matrix.shape[1]
    m_prime = matrix.shape[0]
    while True:
        ite += 1
        print("Iteration ", ite)
        print_table(matrix, c, d, col, cb, x, nb_var, b_var,
                    objective)
        v = np.argmax(c)
        cv = c[v]
        if cv < 0:
            if ite > n_art_var:
                print("\nNon-basic variables: ", nb_var)
                print("Basic variables: ", b_var)
                print("values of x: ")
                li = []
                for i in range(len(x)):
                    li.append("x" + str(i + 1) + '=' + str(round(x[i], 5)))
                print(li)
                print("Final value of objective function: ", round(evaluate_obj_fn(cb, col, d, objective), 5))
                return
            else:
                print("Infeasible Solution")
                print("Non-basic variables: ", nb_var)
                print("Basic variables: ", b_var)
                li = []
                for i in range(len(x)):
                    li.append("x" + str(i + 1) + '=' + str(round(x[i], 5)))
                print("values for x: ", li)
                print("Value of objective function: ", round(evaluate_obj_fn(cb, col, d, objective), 5))
                return
        if cv == 0:
            x_1 = np.copy(x)
            ratios = np.empty((m_prime,))
            u = 0
            pivot = -1
            min_ratio = INFINITY
            for i in range(m_prime):
                if matrix[i][v] == 0:
                    continue
                ratios[i] = col[i] / matrix[i][v]
                if min_ratio > ratios[i] > 0:
                    u = i
                    min_ratio = ratios[i]
                    pivot = matrix[u][v]
            if min_ratio == INFINITY:
                print("No more optimal solutions")
                return
            a_new = np.empty((m_prime, n_prime))
            for i in range(m_prime):
                for j in range(n_prime):
                    if i == u and j == v:
                        a_new[i][j] = 1 / matrix[i][j]
                    elif i == u:
                        a_new[i][j] = matrix[i][j] / pivot
                    elif j == v:
                        a_new[i][j] = -matrix[i][j] / pivot
                    else:
                        a_new[i][j] = (pivot * matrix[i][j] - matrix[i][v] * matrix[u][j]) / pivot
            c_new = np.copy(c)
            for j in range(n_prime):
                if j == v:
                    c_new[j] = round(-c[j] / pivot, 6)
                else:
                    c_new[j] = round((pivot * c[j] - c[v] * matrix[u][j]) / pivot, 6)
            b_new = np.copy(col)
            for j in range(m_prime):
                if j == u:
                    b_new[j] = col[j] / pivot
                else:
                    b_new[j] = (pivot * col[j] - matrix[j][v] * col[u]) / pivot
            matrix = np.copy(a_new)
            c = np.copy(c_new)
            col = np.copy(b_new)
            temp2 = cb[u]
            cb[u] = cn[v]
            cn[v] = temp2
            temp1 = nb_var[v]
            nb_var[v] = b_var[u]
            b_var[u] = temp1
            for i in range(m_prime):
                s = b_var[i]
                x[int(s[1]) - 1] = col[i]
            for i in range(n_prime):
                s = nb_var[i]
                x[int(s[1]) - 1] = 0
            x_2 = np.copy(x)
            print_table(matrix, c, d, col, c, nb_var, b_var, x, objective)
            print("Infinitely many solutions of the form: \u03BB", x_1, " + (1-\u03BB)", x_2)
            return
        else:
            print("The value of most negative c is", -cv, " Corresponding to column", v + 1)
            ratios = np.empty((m_prime,))
            u = 0
            pivot = -1
            min_ratio = INFINITY
            for i in range(m_prime):
                if matrix[i][v] == 0:
                    continue
                ratios[i] = col[i] / matrix[i][v]
                if min_ratio > ratios[i] >= 0:
                    u = i
                    min_ratio = ratios[i]
                    pivot = matrix[u][v]
            print("Column-wise ratios: ", ratios)
            print("Minimum ratio: ", min_ratio)
            print("Pivot element: ", pivot, "Co-ordinates: ", u + 1, " ", v + 1)
            if min_ratio == INFINITY:
                print("Unbounded problem")
                print("Value of objective function: ", evaluate_obj_fn(c, x, d, objective))
                print("Values for x: ", x)
                return
            a_new = np.empty((m_prime, n_prime))
            for i in range(m_prime):
                for j in range(n_prime):
                    if i == u and j == v:
                        a_new[i][j] = 1 / matrix[i][j]
                    elif i == u:
                        a_new[i][j] = matrix[i][j] / pivot
                    elif j == v:
                        a_new[i][j] = -matrix[i][j] / pivot
                    else:
                        a_new[i][j] = (pivot * matrix[i][j] - matrix[i][v] * matrix[u][j]) / pivot
            c_new = np.copy(c)
            for j in range(n_prime):
                if j == v:
                    c_new[j] = round(-c[j] / pivot, 6)
                else:
                    c_new[j] = round((pivot * c[j] - c[v] * matrix[u][j]) / pivot, 6)
            b_new = np.copy(col)
            for j in range(m_prime):
                if j == u:
                    b_new[j] = col[j] / pivot
                else:
                    b_new[j] = (pivot * col[j] - matrix[j][v] * col[u]) / pivot
            matrix = np.copy(a_new)
            c = np.copy(c_new)
            col = np.copy(b_new)
            temp2 = cb[u]
            cb[u] = cn[v]
            cn[v] = temp2
            temp1 = nb_var[v]
            nb_var[v] = b_var[u]
            b_var[u] = temp1
            for i in range(m_prime):
                s = b_var[i]
                x[int(s[1]) - 1] = col[i]
            for i in range(n_prime):
                s = nb_var[i]
                x[int(s[1]) - 1] = 0


def scanner():
    print("What is type of your optimisation Problem? Type min for minimization and max for maximization")
    objective = str(input())
    print("Enter the number of variables in the objective function")
    n = int(input())
    print("Enter the number of constraints")
    m = int(input())
    print("Enter the coefficients of the Objective Function")
    c = [float(i) for i in input().split(" ")]
    if objective == 'min':
        c = [-z for z in c]
    print("Enter the value of the constant in the objective function")
    d = float(input())
    print("Enter the matrix A which is the coefficient of the constraints row by row")
    a = []
    for i in range(m):
        a.append([float(j) for j in input().split(" ")])
    print("Enter the constants/RHS bi for the constraint equations")
    b = [float(i) for i in input().split(" ")]
    print("Enter the equation or in-equation type fo the variable")
    s = input().split(" ")
    return n, m, a, c, d, b, s, objective


if __name__ == '__main__':
    t = int(input("Enter the number of test cases:"))
    M = 10000
    for i in range(t):
        n, m, a, c_original, d, b, s, objective = scanner()

        a, b, cb, cn, c, x, nb_var, b_var, art_var, slack_var, sur_var = first_phase(n, m, a, d, b, s)

        a, b, c, x, ite, code = phase_one_simplex(a, b, cb, cn, c, d, x, nb_var, b_var, art_var, slack_var, sur_var)
        if code == 0:
            print("There is no Phase two for the problem")
        elif code == 1:
            a, b, c, cn, cb, b_var, nb_var, sur_var, slack_var, art_var = second_phase(a, b, c, cb, cn, c_original, x,
                                                                                       b_var, nb_var, art_var,
                                                                                       slack_var, sur_var)
            second_phase_simplex(a, c, cn, cb, d, b, nb_var, b_var, x, objective, len(sur_var), len(slack_var),
                                 len(art_var), ite)
