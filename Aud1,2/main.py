operators = ['+', '-', '/', '//', '*', '**', "%"]


class Student:
    def __init__(self, n, a):
        self.full_Name = n
        self.age = a

        def get_age(self):
            return self.age


def calculator(op1, op, op2):
    if op in operators:
        if op == '+':
            return op1 + op2
        elif op == '-':
            return op1 - op2
        elif op == "*":
            return op1 * op2
        else:
            return op1 / op2
    else:
        print('Porgresen operator')


if __name__ == '__main__':
    operand1 = int(input())
    operand2 = input()
    operand3 = int(input())

    print(calculator(operand1, operand2, operand3))
