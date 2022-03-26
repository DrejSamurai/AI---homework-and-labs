from constraint import *


def not_attacking(rook, rook_cmp):
    return rook[0] != rook_cmp[0] and rook[1] != rook_cmp[1]


if __name__ == '__main__':
    domain = [(i, j) for i in range(0, 8) for j in range(0, 8)]

    rooks = range(1, 9)

    problem = Problem()

    problem.addVariable(rooks, domain)

    for rook1 in rooks:
        for rook2 in rooks:
            if rook1 != rook2:
                problem.addConstraint(not_attacking(rook1, rook2))

    solution = problem.getSolution()
    print(solution)
