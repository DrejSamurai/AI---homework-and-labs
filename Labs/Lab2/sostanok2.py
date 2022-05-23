from constraint import *

def check_valid_all(s1, s2, s3):
    if s1 == 1 and ((s2 == 1 and s3 == 0) or (s2 == 0 and s3 == 1) or (s2 == 1 and s3 == 1)):
        return True
    return False

def check_Simona_termin(prisustvo, vreme):
    if prisustvo == 0 or vreme in [13, 14, 16, 19]:
        return True
    return False

def check_Marija_termin(prisustvo, vreme):
    if prisustvo == 0 or vreme in [14, 15, 18]:
        return True
    return False

def check_Petar_termin(prisustvo, vreme):
    if prisustvo == 0 or vreme in [12, 13, 16, 17, 18, 19]:
        return True
    return False


if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())

    # ---Dadeni se promenlivite, dodadete gi domenite-----
    problem.addVariable("Simona_prisustvo", range(2))
    problem.addVariable("Marija_prisustvo", range(2))
    problem.addVariable("Petar_prisustvo", range(2))
    problem.addVariable("vreme_sostanok", range(12, 21))

    problem.addConstraint(check_valid_all, ["Simona_prisustvo", "Marija_prisustvo", "Petar_prisustvo"])
    problem.addConstraint(check_Simona_termin, ["Simona_prisustvo", "vreme_sostanok"])
    problem.addConstraint(check_Marija_termin, ["Marija_prisustvo", "vreme_sostanok"])
    problem.addConstraint(check_Petar_termin, ["Petar_prisustvo", "vreme_sostanok"])

    [print(solution) for solution in problem.getSolutions()]