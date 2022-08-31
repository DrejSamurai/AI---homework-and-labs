from constraint import *

if __name__ == '__main__':
    num = int(input())
    participants = dict()
    participants_info = input()
    while participants_info != 'end':
        p_id, area = participants_info.split(' ')
        participants[p_id] = area
        participants_info = input()

    #Tuka definirajte gi promenlivite

    domain = [f'T{i + 1}' for i in range(num)]

    variables = []
    for key in participants:
        variables.append(f'{key} {participants.get(key)}')

    #print(variables)

    problem = Problem(BacktrackingSolver())

    # Dokolku vi e potrebno promenete gi varijablite

    problem.addVariables(variables, domain)

    # Tuka dodadete gi ogranicuvanjata



    print(problem.getSolution())