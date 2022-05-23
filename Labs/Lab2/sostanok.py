from constraint import *

def check_valid_all(s1, s2, s3):
    if s1 == 1 and ((s2 == 1 and s3 == 0) or (s2 == 0 and s3 == 1) or (s2 == 1 and s3 == 1)):
        return True
    else:
        return False

def check_Simona_termin(s1, s2, s3, t):
    SimonaTermini = [13, 14, 16, 19]
    if t in SimonaTermini and check_valid_all(s1, s2, s3):
        return True
    else:
        return False

def check_Marija_termin(s1, s2, s3, t):
    MarijaTermini = [14, 15, 18]
    if t in MarijaTermini and check_valid_all(s1, s2, s3):
        return True
    else:
        return False


def check_Petar_termin(s1, s2, s3, t):
    PetarTermini = [12, 13, 16, 17, 18, 19]
    if t in PetarTermini and check_valid_all(s1, s2, s3):
        return True
    else:
        return False

if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())
    # ---Dadeni se promenlivite, dodadete gi domenite-----
    problem.addVariable("Simona_prisustvo", range(2))
    problem.addVariable("Petar_prisustvo", range(2))
    problem.addVariable("Marija_prisustvo", range(2))
    problem.addVariable("vreme_sostanok", range(12, 21))
    # ----------------------------------------------------
    # Симона како менаџер мора да присуствува на состанокот со најмалку уште една личност. Состанокот трае еден час, и може да се закаже во периодот од 12:00 до 20:00.
    # Почетокот на состанокот може да биде на секој час, односно состанокот може да почне во 12:00, но не во 12:05, 12:10 итн.
    # ---Tuka dodadete gi ogranichuvanjata----------------

    problem.addConstraint(check_valid_all, ["Simona_prisustvo", "Marija_prisustvo", "Petar_prisustvo"])
    problem.addConstraint(check_Simona_termin, ["Simona_prisustvo", "Marija_prisustvo", "Petar_prisustvo", "vreme_sostanok"])
    problem.addConstraint(check_Petar_termin, ["Simona_prisustvo", "Marija_prisustvo", "Petar_prisustvo", "vreme_sostanok"])
    problem.addConstraint(check_Petar_termin, ["Simona_prisustvo", "Marija_prisustvo", "Petar_prisustvo", "vreme_sostanok"])

    # ----------------------------------------------------

    [print(solution) for solution in problem.getSolutions()]