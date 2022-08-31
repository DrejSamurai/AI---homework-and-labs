from constraint import *

"""
Потребно е да направите распоред за презентација на трудови за некоја конференција. На конференцијата треба да бидат презентирани вкупно
10 трудови од неколку области. Вештачка интелигенција АИ, Машинско учење МЛ и обработка на природни јазици НЛП. Ваша задача е да направите
распоред за конференција по термини и при тоа да се земат предвид следните граничувања.
- Во секој од термините може да презентираат најногу 4 труда.
- Ако бројот на трудови од дадена област е помала или еднаква на максималниот број трудови кои може да бидат презентирани во даден термин, 
тогаш тие трудови треба да бидат распределени во ист термин.
"""


def in_single_session(termin_num, predmet_num):
    if predmet_num <= termin_num:
        return True
    else:
        return False


if __name__ == '__main__':
    num = int(input())

    papers = dict()

    paper_info = input()

    while paper_info != 'end':
        title, topic = paper_info.split(' ')
        papers[title] = topic
        paper_info = input()

    print(papers)

    # Tuka definirajte gi promenlivite

    domain = [f'T{i + 1}' for i in range(num)]
    problem = Problem(BacktrackingSolver())

    # Dokolku vi e potrebno moze da promenite delot za dodavanje na promenlvite
    ai_papers, ml_papers, nlp_papers = 0, 0, 0
    for paper in papers:
        problem.addVariable(paper, domain)

    print()
    #problem.addConstraint(in_single_session(num,))
    # Tuka dodadete go kodot za pecatenje
    result = problem.getSolution()
    print(result)
