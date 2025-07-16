"""
  Author  : Abhay Kumar Keshari
  Roll No : 20CS10001
  Date    : Spring 2022
  Course  : Operation Research MA30014
"""
from itertools import combinations


def GaussSiedelMethod(matrix, col, permissible_error):
    # variables with zero coefficients are removed
    rows = len(matrix)
    currSoln = [0 for i in range(rows)]
    prevSoln = [0 for i in range(rows)]
    for iteration in range(10000):
        isErrorPermissible = True

        for i in range(rows):
            value = 0

            for j in range(rows):
                if j > i:
                    value = matrix[j][i] * prevSoln[j]
                elif j < i:
                    value += matrix[j][i] * currSoln[j]

            if matrix[i][i] != 0:
                currSoln[i] = (col[i] - value) / matrix[i][i]

            if abs(currSoln[i] - prevSoln[i]) > permissible_error:
                isErrorPermissible = False

        for i in range(rows):
            prevSoln[i] = currSoln[i]

        if isErrorPermissible:
            break
    isFeasible = all(element > 0 for element in currSoln)

    if isFeasible:
        print(currSoln)

    return (currSoln, isFeasible)


def basic_feasible_solutions(matrix, col, permissible_error, objective_fn, objective):
    if objective == "max":
        optimal_value = -9999999999
    else:
        optimal_value = +9999999999

    n = len(matrix)
    m = len(matrix[0])
    variables = ["x" + str(i + 1) for i in range(n)]
    matrix_ = list(combinations(matrix, m))
    variables_ = list(combinations(variables, m))

    optimal_solution = None

    for M, var in zip(matrix_, variables_):
        solution, isFeasible = GaussSiedelMethod(M, col, permissible_error)
        if isFeasible:
            print(" are the values for ", end=" ")
            print(var, " with value of objective func =", end=" ")
            value = objective_function(objective_fn, solution, var)
            print(value)
            if objective == "max":
                isOptimal = (optimal_value < value)
            else:
                isOptimal = (optimal_value > value)

            if isOptimal:
                optimal_value = value
                optimal_solution = (solution, var)

    if optimal_value == -9999999999 or optimal_value == +9999999999:
        print("No optimal Solution found using BFS Method")
    else:
        print("Optimal solution is ", optimal_solution, " and optimal value is ", optimal_value)


def objective_function(function, values, var):
    m = len(var)
    n = len(function)
    val = 0
    for i in range(m):
        index = int(var[i][1]) - 1
        if index < n:
            val += function[index] * values[i]
    return val


if __name__ == '__main__':

    err = 10e-6
    test_case = int(input("Enter number of Optimisation Problems: "))
    for counter in range(test_case):
        print("Enter 2 spaced integers m and n, where m = #constraint, n = #variables")
        m, n = map(int, input().split())
        matrix = [[0 for i in range(m)] for j in range(n + m)]
        col = [0 for i in range(m)]

        print("Enter the constraints")
        for i in range(m):
            print("Enter the type of constraint. Type >= or <=")
            constraint = input()
            print("Enter the coefficients of equation " + str(i) + ": a1 a2 ... an b")
            coeff = input().split()

            valid_coeff = []
            if constraint == "<=":
                valid_coeff = [float(i) for i in coeff]
            else:
                valid_coeff = [-float(i) for i in coeff]

            for j in range(n):
                matrix[j][i] = valid_coeff[j]

            matrix[i + n][i] = 1
            col[i] = valid_coeff[n]

        print("What is type of your optimisation Problem? Type min for minimization and max for maximization")
        objective = input()
        print("Enter the coefficients of objective function")
        z = list(map(float, input().split()))

        basic_feasible_solutions(matrix, col, err, z, objective)
