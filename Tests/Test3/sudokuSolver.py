from constraint import *


if __name__ == '__main__':

    problem = Problem()
    solver = input()
    if solver == 'RecursiveBacktrackingSolver':
        problem = Problem(RecursiveBacktrackingSolver())
    if solver == 'BacktrackingSolver':
        problem = Problem(BacktrackingSolver())
    if solver == 'MinConflictsSolver':
        problem = Problem(MinConflictsSolver())

    variables = range(0, 81)
    domain = range(1, 10)

    problem.addVariable(variables, domain)

    # ---Tuka dodadete gi ogranichuvanjata----------------

    # ----------------------------------------------------

    print(problem.getSolution())