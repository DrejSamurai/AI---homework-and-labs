import bisect

"""
Дефинирање на класа за структурата на проблемот кој ќе го решаваме со пребарување.
Класата Problem е апстрактна класа од која правиме наследување за дефинирање на основните 
карактеристики на секој проблем што сакаме да го решиме
"""


class Problem:
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    def successor(self, state):
        """За дадена состојба, врати речник од парови {акција : состојба}
        достапни од оваа состојба. Ако има многу следбеници, употребете
        итератор кој би ги генерирал следбениците еден по еден, наместо да
        ги генерирате сите одеднаш.
        :param state: дадена состојба
        :return:  речник од парови {акција : состојба} достапни од оваа
                  состојба
        :rtype: dict
        """
        raise NotImplementedError

    def actions(self, state):
        """За дадена состојба state, врати листа од сите акции што може да
        се применат над таа состојба
        :param state: дадена состојба
        :return: листа на акции
        :rtype: list
        """
        raise NotImplementedError

    def result(self, state, action):
        """За дадена состојба state и акција action, врати ја состојбата
        што се добива со примена на акцијата над состојбата
        :param state: дадена состојба
        :param action: дадена акција
        :return: резултантна состојба
        """
        raise NotImplementedError

    def goal_test(self, state):
        """Врати True ако state е целна состојба. Даденава имплементација
        на методот директно ја споредува state со self.goal, како што е
        специфицирана во конструкторот. Имплементирајте го овој метод ако
        проверката со една целна состојба self.goal не е доволна.
        :param state: дадена состојба
        :return: дали дадената состојба е целна состојба
        :rtype: bool
        """
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Врати ја цената на решавачкиот пат кој пристигнува во состојбата
        state2 од состојбата state1 преку акцијата action, претпоставувајќи
        дека цената на патот до состојбата state1 е c. Ако проблемот е таков
        што патот не е важен, оваа функција ќе ја разгледува само состојбата
        state2. Ако патот е важен, ќе ја разгледува цената c и можеби и
        state1 и action. Даденава имплементација му доделува цена 1 на секој
        чекор од патот.
        :param c: цена на патот до состојбата state1
        :param state1: дадена моментална состојба
        :param action: акција која треба да се изврши
        :param state2: состојба во која треба да се стигне
        :return: цена на патот по извршување на акцијата
        :rtype: float
        """
        return c + 1

    def value(self):
        """За проблеми на оптимизација, секоја состојба си има вредност.
        Hill-climbing и сличните алгоритми се обидуваат да ја максимизираат
        оваа вредност.
        :return: вредност на состојба
        :rtype: float
        """
        raise NotImplementedError


"""
Дефинирање на класата за структурата на јазел од пребарување.
Класата Node не се наследува
"""


class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Креирај јазол од пребарувачкото дрво, добиен од parent со примена
        на акцијата action
        :param state: моментална состојба (current state)
        :param parent: родителска состојба (parent state)
        :param action: акција (action)
        :param path_cost: цена на патот (path cost)
        """
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0  # search depth
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node %s>" % (self.state,)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """Излистај ги јазлите достапни во еден чекор од овој јазол.
        :param problem: даден проблем
        :return: листа на достапни јазли во еден чекор
        :rtype: list(Node)
        """

        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """Дете јазел
        :param problem: даден проблем
        :param action: дадена акција
        :return: достапен јазел според дадената акција
        :rtype: Node
        """
        next_state = problem.result(self.state, action)
        return Node(next_state, self, action,
                    problem.path_cost(self.path_cost, self.state,
                                      action, next_state))

    def solution(self):
        """Врати ја секвенцата од акции за да се стигне од коренот до овој јазол.
        :return: секвенцата од акции
        :rtype: list
        """
        return [node.action for node in self.path()[1:]]

    def solve(self):
        """Врати ја секвенцата од состојби за да се стигне од коренот до овој јазол.
        :return: листа од состојби
        :rtype: list
        """
        return [node.state for node in self.path()[0:]]

    def path(self):
        """Врати ја листата од јазли што го формираат патот од коренот до овој јазол.
        :return: листа од јазли од патот
        :rtype: list(Node)
        """
        x, result = self, []
        while x:
            result.append(x)
            x = x.parent
        result.reverse()
        return result

    """Сакаме редицата од јазли кај breadth_first_search или 
    astar_search да не содржи состојби - дупликати, па јазлите што
    содржат иста состојба ги третираме како исти. [Проблем: ова може
    да не биде пожелно во други ситуации.]"""

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)


"""
Дефинирање на помошни структури за чување на листата на генерирани, но непроверени јазли
"""


class Queue:
    """Queue е апстрактна класа / интерфејс. Постојат 3 типа:
        Stack(): Last In First Out Queue (стек).
        FIFOQueue(): First In First Out Queue (редица).
        PriorityQueue(order, f): Queue во сортиран редослед (подразбирливо,од најмалиот кон
                                 најголемиот јазол).
    """

    def __init__(self):
        raise NotImplementedError

    def append(self, item):
        """Додади го елементот item во редицата
        :param item: даден елемент
        :return: None
        """
        raise NotImplementedError

    def extend(self, items):
        """Додади ги елементите items во редицата
        :param items: дадени елементи
        :return: None
        """
        raise NotImplementedError

    def pop(self):
        """Врати го првиот елемент од редицата
        :return: прв елемент
        """
        raise NotImplementedError

    def __len__(self):
        """Врати го бројот на елементи во редицата
        :return: број на елементи во редицата
        :rtype: int
        """
        raise NotImplementedError

    def __contains__(self, item):
        """Проверка дали редицата го содржи елементот item
        :param item: даден елемент
        :return: дали queue го содржи item
        :rtype: bool
        """
        raise NotImplementedError


class Stack(Queue):
    """Last-In-First-Out Queue."""

    def __init__(self):
        self.data = []

    def append(self, item):
        self.data.append(item)

    def extend(self, items):
        self.data.extend(items)

    def pop(self):
        return self.data.pop()

    def __len__(self):
        return len(self.data)

    def __contains__(self, item):
        return item in self.data


class FIFOQueue(Queue):
    """First-In-First-Out Queue."""

    def __init__(self):
        self.data = []

    def append(self, item):
        self.data.append(item)

    def extend(self, items):
        self.data.extend(items)

    def pop(self):
        return self.data.pop(0)

    def __len__(self):
        return len(self.data)

    def __contains__(self, item):
        return item in self.data


class PriorityQueue(Queue):
    """Редица во која прво се враќа минималниот (или максималниот) елемент
    (како што е определено со f и order). Оваа структура се користи кај
    информирано пребарување"""
    """"""

    def __init__(self, order=min, f=lambda x: x):
        """
        :param order: функција за подредување, ако order е min, се враќа елементот
                      со минимална f(x); ако order е max, тогаш се враќа елементот
                      со максимална f(x).
        :param f: функција f(x)
        """
        assert order in [min, max]
        self.data = []
        self.order = order
        self.f = f

    def append(self, item):
        bisect.insort_right(self.data, (self.f(item), item))

    def extend(self, items):
        for item in items:
            bisect.insort_right(self.data, (self.f(item), item))

    def pop(self):
        if self.order == min:
            return self.data.pop(0)[1]
        return self.data.pop()[1]

    def __len__(self):
        return len(self.data)

    def __contains__(self, item):
        return any(item == pair[1] for pair in self.data)

    def __getitem__(self, key):
        for _, item in self.data:
            if item == key:
                return item

    def __delitem__(self, key):
        for i, (value, item) in enumerate(self.data):
            if item == key:
                self.data.pop(i)


from sys import maxsize as infinity

"""
Информирано пребарување во рамки на граф
"""


def memoize(fn, slot=None):
    """ Запамети ја пресметаната вредност за која била листа од
    аргументи. Ако е специфициран slot, зачувај го резултатот во
    тој slot на првиот аргумент. Ако slot е None, зачувај ги
    резултатите во речник.
    :param fn: зададена функција
    :type fn: function
    :param slot: име на атрибут во кој се чуваат резултатите од функцијата
    :type slot: str
    :return: функција со модификација за зачувување на резултатите
    :rtype: function
    """
    if slot:
        def memoized_fn(obj, *args):
            if hasattr(obj, slot):
                return getattr(obj, slot)
            else:
                val = fn(obj, *args)
                setattr(obj, slot, val)
                return val
    else:
        def memoized_fn(*args):
            if args not in memoized_fn.cache:
                memoized_fn.cache[args] = fn(*args)
            return memoized_fn.cache[args]

        memoized_fn.cache = {}
    return memoized_fn


def best_first_graph_search(problem, f):
    """Пребарувај низ следбениците на даден проблем за да најдеш цел. Користи
     функција за евалуација за да се одлучи кој е сосед најмногу ветува и
     потоа да се истражи. Ако до дадена состојба стигнат два пата, употреби
     го најдобриот пат.
    :param problem: даден проблем
    :type problem: Problem
    :param f: дадена функција за евалуација (проценка)
    :type f: function
    :return: Node or None
    :rtype: Node
    """
    f = memoize(f, 'f')
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node
    frontier = PriorityQueue(min, f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                incumbent = frontier[child]
                if f(child) < f(incumbent):
                    del frontier[incumbent]
                    frontier.append(child)
    return None


def greedy_best_first_graph_search(problem, h=None):
    """ Greedy best-first пребарување се остварува ако се специфицира дека f(n) = h(n).
    :param problem: даден проблем
    :type problem: Problem
    :param h: дадена функција за хевристика
    :type h: function
    :return: Node or None
    """
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, h)


def astar_search(problem, h=None):
    """ A* пребарување е best-first graph пребарување каде f(n) = g(n) + h(n).
    :param problem: даден проблем
    :type problem: Problem
    :param h: дадена функција за хевристика
    :type h: function
    :return: Node or None
    """
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


def recursive_best_first_search(problem, h=None):
    """Recursive best first search - ја ограничува рекурзијата
    преку следење на f-вредноста на најдобриот алтернативен пат
    од било кој јазел предок (еден чекор гледање нанапред).
    :param problem: даден проблем
    :type problem: Problem
    :param h: дадена функција за хевристика
    :type h: function
    :return: Node or None
    """
    h = memoize(h or problem.h, 'h')

    def RBFS(problem, node, flimit):
        if problem.goal_test(node.state):
            return node, 0  # (втората вредност е неважна)
        successors = node.expand(problem)
        if len(successors) == 0:
            return None, infinity
        for s in successors:
            s.f = max(s.path_cost + h(s), node.f)
        while True:
            # Подреди ги според најниската f вредност
            successors.sort(key=lambda x: x.f)
            best = successors[0]
            if best.f > flimit:
                return None, best.f
            if len(successors) > 1:
                alternative = successors[1].f
            else:
                alternative = infinity
            result, best.f = RBFS(problem, best, min(flimit, alternative))
            if result is not None:
                return result, best.f

    node = Node(problem.initial)
    node.f = h(node)
    result, bestf = RBFS(problem, node, infinity)
    return result


def move_right(x1, y1, x2, y2, x3, y3, obstacles):
    while x1 < 8 and [x1 + 1, y1] not in obstacles and [x1 + 1, y1] != [x2, y2] and [x1 + 1, y1] != [y3, x3]:
        x1 += 1
    return x1


def move_left(x1, y1, x2, y2, x3, y3, obstacles):
    while x1 > 0 and [x1 - 1, y1] not in obstacles and [x1 - 1, y1] != [x2, y2] and [x1 - 1, y1] != [y3, x3]:
        x1 -= 1
    return x1


def move_up(x1, y1, x2, y2, x3, y3, obstacles):
    while y1 < 6 and [x1, y1 + 1] not in obstacles and [x1, y1 + 1] != [x2, y2] and [x1, y1 + 1] != [y3, x3]:
        y1 += 1
    return y1


def move_down(x1, y1, x2, y2, x3, y3, obstacles):
    while y1 > 0 and [x1, y1 - 1] not in obstacles and [x1, y1 - 1] != [x2, y2] and [x1, y1 - 1] != [y3, x3]:
        y1 -= 1
    return y1


class Molecule(Problem):

    def __init__(self, obstacles, initial, goal=None):
        super().__init__(initial, goal)
        self.obstacles = obstacles

    def successor(self, state):
        successors = dict()

        h1_x, h1_y = state[0], state[1]
        o_x, o_y = state[2], state[3]
        h2_x, h2_y = state[4], state[5]

        # H1
        x1_new = move_right(h1_x, h1_y, o_x, o_y, h2_x, h2_y, self.obstacles)
        if x1_new != h1_x:
            successors["RightH1"] = (x1_new, h1_y, o_x, o_y, h2_x, h2_y)

        x1_new = move_left(h1_x, h1_y, o_x, o_y, h2_x, h2_y, self.obstacles)
        if x1_new != h1_x:
            successors["LeftH1"] = (x1_new, h1_y, o_x, o_y, h2_x, h2_y)

        y1_new = move_up(h1_x, h1_y, o_x, o_y, h2_x, h2_y, self.obstacles)
        if y1_new != h1_y:
            successors["UpH1"] = (h1_x, y1_new, o_x, o_y, h2_x, h2_y)

        y1_new = move_down(h1_x, h1_y, o_x, o_y, h2_x, h2_y, self.obstacles)
        if y1_new != h1_y:
            successors["DownH1"] = (h1_x, y1_new, o_x, o_y, h2_x, h2_y)

        # O
        x_new = move_right(o_x, o_y, h1_x, h1_y, h2_x, h2_y, self.obstacles)
        if x_new != o_x:
            successors["RightO"] = (h1_x, h1_y, x_new, o_y, h2_x, h2_y)

        x_new = move_left(o_x, o_y, h1_x, h1_y, h2_x, h2_y, self.obstacles)
        if x_new != o_x:
            successors["LeftO"] = (h1_x, h1_y, x_new, o_y, h2_x, h2_y)

        y_new = move_up(o_x, o_y, h1_x, h1_y, h2_x, h2_y, self.obstacles)
        if y_new != o_y:
            successors["UpO"] = (h1_x, h1_y, o_x, y_new, h2_x, h2_y)

        y_new = move_down(o_x, o_y, h1_x, h1_y, h2_x, h2_y, self.obstacles)
        if y_new != o_y:
            successors["DownO"] = (h1_x, h1_y, o_x, y_new, h2_x, h2_y)

        # H2
        x2_new = move_right(h2_x, h2_y, o_x, o_y, h1_x, h1_y, self.obstacles)
        if x2_new != h2_x:
            successors["RightH2"] = (x2_new, h2_y, o_x, o_y, h1_x, h1_y)

        x2_new = move_right(h2_x, h2_y, o_x, o_y, h1_x, h1_y, self.obstacles)
        if x2_new != h2_x:
            successors["LeftH2"] = (x2_new, h1_y, o_x, o_y, h2_x, h2_y)

        y2_new = move_up(h2_x, h2_y, o_x, o_y, h1_x, h1_y, self.obstacles)
        if y1_new != h1_y:
            successors["UpH2"] = (h2_x, y2_new, o_x, o_y, h1_x, h1_y)

        y2_new = move_up(h2_x, h2_y, o_x, o_y, h1_x, h1_y, self.obstacles)
        if y2_new != h2_y:
            successors["DownH2"] = (h2_x, y2_new, o_x, o_y, h1_x, h1_y)

        return successors

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        return state[1] == state[3] == state[5] and state[0]+1 == state[2] and state[2] == state[4]+1

    def h(self, node):
        # Хевристичка функција која за секоја состојба пресметува минимален
        # број на турнувања на паровите од атоми за тие да се спојат
        state = node.state
        h1 = state[0], state[1]
        o = state[2], state[3]
        h2 = state[4], state[5]
        value = 0

        # проверка за позициите на H1 и O и потребниот број на чекори за да се спојат
        if h1[0] != o[0]:
            if h1[1] != (o[1] - 1):
                # ако атомот на водорот не е во иста редица и во колона веднаш до атомот
                # на кислород ни требаат најмалку 2 турнувања (turn down/up + left/right)
                # за да се спојат
                value += 2
            else:
                # ако атомот на водорот не е во иста редица, но е во колона веднаш до атомот
                # на кислород ни треба најмалку 1 турнувањe (turn up or down) за да се спојат
                value += 1
        else:  # h1[0] == o[0]
            if h1[1] > o[1]:
                # ако атомот на водорот е во иста редица, но во колона од десна страна на
                # атомот на кислород ни требаат најмалку 3 турнувања (turn 2 x down/up + left/right)
                # за да се спојат
                value += 3
            elif h1[1] < (o[1] - 1):
                # ако атомот на водорот е во иста редица, но во колона од лева страна на
                # атомот на кислород ни треба најмалку 1 турнување (turn right) за да се спојат
                value += 1

        # проверка за позициите на H2 и O и потребниот број на чекори за да се спојат
        if h2[0] != o[0]:
            if h2[1] != (o[1] + 1):
                # ако атомот на водорот не е во иста редица и во колона веднаш до атомот
                # на кислород ни требаат најмалку 2 турнувања (turn down/up + left/right)
                # за да се спојат
                value += 2
            else:
                # ако атомот на водорот не е во иста редица, но е во колона веднаш до атомот
                # на кислород ни треба најмалку 1 турнувањe (turn up or down) за да се спојат
                value += 1
        else:  # h2[0] == o[0]
            if h2[1] < o[1]:  # ако атомот на водорот е во иста редица, но во колона од лева страна на
                # атомот на кислород ни требаат најмалку 3 турнувања (turn 2 x down/up + left/right)
                # за да се спојат
                value += 3
            elif h2[1] > (o[1] + 1):
                # ако атомот на водорот е во иста редица, но во колона од десна страна на
                # атомот на кислород ни треба најмалку 1 турнување (turn left) за да се спојат
                value += 1

        if h1[0] == h2[0] and h1[0] != o[0]:
            # ако водородните атоми се во ист ред тогаш можеме да имаме само едно турнување на
            # атомот на кислород up/down (а претходно сме пресметале турнување на H1 и турнување на H2)
            value -= 1

        return value



if __name__ == "__main__":
    h1_atom_column = int(input())
    h1_atom_row = int(input())
    o_atom_column = int(input())
    o_atom_row = int(input())
    h2_atom_column = int(input())
    h2_atom_row = int(input())

    molecule = Molecule((h1_atom_column, h1_atom_row, o_atom_column,
                         o_atom_row, h2_atom_column, h2_atom_row))

    answer = astar_search(molecule)
    print(answer.solution())
