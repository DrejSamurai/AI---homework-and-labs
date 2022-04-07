from constraint import *

def not_attacking(queen1, queen2):
        return queen1[0] != queen2[0] and queen1[1] != queen2[1] and abs(queen1[0] - queen2[0]) != abs(queen1[1] - queen2[1])


if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())
    n = int(input())

    variables = range(1, n + 1)

    domain = [(i, j) for i in range(0, n) for j in range(0, n)]

    problem.addVariables(variables, domain)

    # ---Tuka dodadete gi ogranichuvanjata----------------
    for queen1 in variables:
        for queen2 in variables:
            if queen1 < queen2:
                problem.addConstraint(not_attacking, (queen1, queen2))
    # ----------------------------------------------------

    print(variables)
    #print(domain)

    if n <= 6:
        solution = problem.getSolutions()
        print(len(solution))
    else:
        solution = problem.getSolution()
        print(solution)