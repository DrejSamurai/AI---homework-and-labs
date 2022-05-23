from constraint import *


if __name__ == '__main__':

    problem = Problem(BacktrackingSolver())
    peopleDomain = []
    leaderDomain = []

    numberOfPeople = int(input())
    elements = [input().split(' ') for _ in range(numberOfPeople)]
    p_weights = [float(p[0]) for p in elements]
    p_names = [p[1] for p in elements]
    peopleList = [(w, n) for w, n in zip(p_weights, p_names)]

    numberOfLeaders = int(input())
    elements = [input().split(' ') for _ in range(numberOfPeople)]
    l_weights = [float(p[0]) for p in elements]
    l_names = [p[1] for p in elements]
    leaderList = [(w, n) for w, n in zip(l_weights, l_names)]

    problem.addVariables(p_names, range(2))


    print(peopleList)
    print(leaderList)