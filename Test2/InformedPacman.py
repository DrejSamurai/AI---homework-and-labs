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


class Pacman(Problem):
    def __init__(self, stars_num, initial, goal=None):
        super().__init__(initial, goal)
        self.obstacles = [(6, 0), (4, 1), (5, 1), (6, 1), (8, 1), (1, 2), (6, 2), (1, 3), (1, 4), (8, 4),
                          (9, 4), (4, 5), (0, 6), (3, 6), (4, 6), (5, 6), (4, 7), (9, 7), (8, 7), (9, 7),
                          (0, 8), (8, 8), (9, 8), (0, 9), (1, 9), (2, 9), (3, 9), (4, 9), (6, 9)]
        self.grid_size = [10, 10]
        self.stars_num2 = stars_num

    def successor(self, state):
        successors = dict()
        pacman_x = state[0]
        pacman_y = state[1]
        pacman_direction = state[2]
        stars = state[3]

        # east
        # forward
        if pacman_x + 1 < self.grid_size[0] and pacman_direction == "istok" and (
                pacman_x + 1, pacman_y) not in self.obstacles:
            stars_new = list(stars)
            if (pacman_x + 1, pacman_y) in stars:
                stars_new.remove((pacman_x + 1, pacman_y))
            successors["ProdolzhiPravo"] = (pacman_x + 1, pacman_y, "istok", tuple(stars_new))

        # backwards
        if pacman_x - 1 >= 0 and pacman_direction == "istok" and (pacman_x - 1, pacman_y) not in self.obstacles:
            stars_new = list(stars)
            if (pacman_x - 1, pacman_y) in stars:
                stars_new.remove((pacman_x - 1, pacman_y))
            successors["ProdolzhiNazad"] = (pacman_x - 1, pacman_y, "zapad", tuple(stars_new))
        # left
        if pacman_y + 1 < self.grid_size[1] and pacman_direction == "istok" and (
                pacman_x, pacman_y + 1) not in self.obstacles:
            stars_new = list(stars)
            if (pacman_x, pacman_y + 1) in stars:
                stars_new.remove((pacman_x, pacman_y + 1))
            successors["SvrtiLevo"] = (pacman_x, pacman_y + 1, "sever", tuple(stars_new))

        # right
        if pacman_y - 1 >= 0 and pacman_direction == "istok" and (pacman_x, pacman_y - 1) not in self.obstacles:
            stars_new = list(stars)
            if (pacman_x, pacman_y - 1) in stars:
                stars_new.remove((pacman_x, pacman_y - 1))
            successors["SvrtiDesno"] = (pacman_x, pacman_y - 1, "jug", tuple(stars_new))

        # west
        # forward
        if pacman_x - 1 >= 0 and pacman_direction == "zapad" and (pacman_x - 1, pacman_y) not in self.obstacles:
            stars_new = list(stars)
            if (pacman_x - 1, pacman_y) in stars:
                stars_new.remove((pacman_x - 1, pacman_y))
            successors["ProdolzhiPravo"] = (pacman_x - 1, pacman_y, "zapad", tuple(stars_new))

        # backwards
        if pacman_x + 1 < self.grid_size[0] and pacman_direction == "zapad" and (
                pacman_x + 1, pacman_y) not in self.obstacles:
            stars_new = list(stars)
            if (pacman_x + 1, pacman_y) in stars:
                stars_new.remove((pacman_x + 1, pacman_y))
            successors["ProdolzhiNazad"] = (pacman_x + 1, pacman_y, "istok", tuple(stars_new))

        # left
        if pacman_y - 1 >= 0 and pacman_direction == "zapad" and (pacman_x, pacman_y - 1) not in self.obstacles:
            stars_new = list(stars)
            if (pacman_x, pacman_y - 1) in stars:
                stars_new.remove((pacman_x, pacman_y - 1))
            successors["SvrtiLevo"] = (pacman_x, pacman_y - 1, "jug", tuple(stars_new))

        # right
        if pacman_y + 1 < self.grid_size[1] and pacman_direction == "zapad" and (
                pacman_x, pacman_y + 1) not in self.obstacles:
            stars_new = list(stars)
            if (pacman_x, pacman_y + 1) in stars:
                stars_new.remove((pacman_x, pacman_y + 1))
            successors["SvrtiDesno"] = (pacman_x, pacman_y + 1, "sever", tuple(stars_new))

        # north
        # forward
        if pacman_y + 1 < self.grid_size[1] and pacman_direction == "sever" and (
                pacman_x, pacman_y + 1) not in self.obstacles:
            stars_new = list(stars)
            if (pacman_x, pacman_y + 1) in stars:
                stars_new.remove((pacman_x, pacman_y + 1))
            successors["ProdolzhiPravo"] = (pacman_x, pacman_y + 1, "sever", tuple(stars_new))

        # backwards
        if pacman_y - 1 >= 0 and pacman_direction == "sever" and (pacman_x, pacman_y - 1) not in self.obstacles:
            stars_new = list(stars)
            if (pacman_x, pacman_y - 1) in stars:
                stars_new.remove((pacman_x, pacman_y - 1))
            successors["ProdolzhiNazad"] = (pacman_x, pacman_y - 1, "jug", tuple(stars_new))

        # left
        if pacman_x - 1 >= 0 and pacman_direction == "sever" and (pacman_x - 1, pacman_y) not in self.obstacles:
            stars_new = list(stars)
            if (pacman_x - 1, pacman_y) in stars:
                stars_new.remove((pacman_x - 1, pacman_y))
            successors["SvrtiLevo"] = (pacman_x - 1, pacman_y, "zapad", tuple(stars_new))

        # right
        if pacman_x + 1 < self.grid_size[0] and pacman_direction == "sever" and (
                pacman_x + 1, pacman_y) not in self.obstacles:
            stars_new = list(stars)
            if (pacman_x + 1, pacman_y) in stars:
                stars_new.remove((pacman_x + 1, pacman_y))
            successors["SvrtiDesno"] = (pacman_x + 1, pacman_y, "istok", tuple(stars_new))

        # south
        # forward
        if pacman_y - 1 >= 0 and pacman_direction == "jug" and (
                pacman_x, pacman_y - 1) not in self.obstacles:
            stars_new = list(stars)
            if (pacman_x, pacman_y - 1) in stars:
                stars_new.remove((pacman_x, pacman_y - 1))
            successors["ProdolzhiPravo"] = (pacman_x, pacman_y - 1, "jug", tuple(stars_new))

        # backwards
        if pacman_y + 1 < self.grid_size[1] and pacman_direction == "jug" and (
                pacman_x, pacman_y + 1) not in self.obstacles:
            stars_new = list(stars)
            if (pacman_x, pacman_y + 1) in stars:
                stars_new.remove((pacman_x, pacman_y + 1))
            successors["ProdolzhiNazad"] = (pacman_x, pacman_y + 1, "sever", tuple(stars_new))

        # right
        if pacman_x - 1 >= 0 and pacman_direction == "jug" and (
                pacman_x - 1, pacman_y) not in self.obstacles:
            stars_new = list(stars)
            if (pacman_x - 1, pacman_y) in stars:
                stars_new.remove((pacman_x - 1, pacman_y))
            successors["SvrtiDesno"] = (pacman_x - 1, pacman_y, "zapad", tuple(stars_new))

        # left
        if pacman_x + 1 < self.grid_size[0] and pacman_direction == "jug" and (
                pacman_x + 1, pacman_y) not in self.obstacles:
            stars_new = list(stars)
            if (pacman_x + 1, pacman_y) in stars:
                stars_new.remove((pacman_x + 1, pacman_y))
            successors["SvrtiLevo"] = (pacman_x + 1, pacman_y, "istok", tuple(stars_new))

        return successors

    def h(self, node):
        min_star = min(stars_list)
        pacman_x_pos = node.state[0]
        pacman_y_pos = node.state[1]
        min1 = len(node.state[3]) / self.stars_num2
        min2 = abs(pacman_x_pos - min_star[0]) + abs(pacman_y_pos - min_star[1])
        return min(min1, min2)

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        return len(state[3]) == 0

    def path_cost(self, c, state1, action, state2):
        return super().path_cost(c, state1, action, state2)

    def value(self):
        pass


if __name__ == '__main__':
    pacman_x = int(input())
    pacman_y = int(input())
    pacman_pos = input()
    stars_num = int(input())
    stars_list = []
    for i in range(0, stars_num):
        element = input()
        a = tuple(int(x) for x in element.split(','))
        stars_list.append(a)
    new_star_list = tuple(stars_list)

    pacman = Pacman(stars_num, (pacman_x, pacman_y, pacman_pos, new_star_list))
    result = astar_search(pacman)
    print(result.solution())
