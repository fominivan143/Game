class Point:
    def __init__(self, n, x, y):
        self.n = n
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_coords(self):
        return self.x, self.y

    def __invert__(self):
        return Point(self.n, self.y, self.x)

    def __repr__(self):
        return f"Point('{self.n}', {self.x}, {self.y})"

    def __str__(self):
        return f'{self.n}({self.x}, {self.y})'

    def __eq__(self, other):
        return self.n == other.n and self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if self.n == other.n:
            if self.x == other.x:
                return self.y < other.y
            return self.x < other.x
        return self.n < other.n

    def __gt__(self, other):
        if self.n == other.n:
            if self.x == other.x:
                return self.y > other.y
            return self.x > other.x
        return self.n > other.n

    def __ge__(self, other):
        return not self.__lt__(other)

    def __le__(self, other):
        return not self.__gt__(other)


class CheckMark(Point):
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        super().__init__(p1.n, p1.x, p1.y)

    def __str__(self):
        return f'{self.p1.n}{self.p2.n}{self.p3.n}'

    def __bool__(self):
        if ((self.p1.x == self.p2.x and self.p1.y == self.p2.y) or
                (self.p3.x == self.p2.x and self.p3.y == self.p2.y) or
                (self.p1.x == self.p3.x and self.p1.y == self.p3.y)):
            return False
        elif (self.p2.x - self.p1.x) * (self.p3.y - self.p1.y) - (self.p3.x - self.p1.x) * (self.p2.y - self.p1.y) == 0:
            return False
        return True

    def __eq__(self, other):
        if ((self.p1.x, self.p1.y) == (other.p1.x, other.p1.y) and
                (self.p2.x, self.p2.y) == (other.p2.x, other.p2.y) and
                    (self.p3.x, self.p3.y) == (other.p3.x, other.p3.y)
            or (self.p1.x, self.p1.y) == (other.p3.x, other.p3.y) and
                (self.p3.x, self.p3.y) == (other.p1.x, other.p1.y) and
                (self.p2.x, self.p2.y) == (other.p2.x, other.p2.y)):
            return True
        return False

p_A = Point('A', 1, 2)
p_B = Point('B', 0, 1)
p_C = Point('C', -1, 2)
p_D = Point('D', 2, 2)
p_E = Point('E', 2, 0)
p_F = Point('F', 2, -1)
cm_ABC = CheckMark(p_A, p_B, p_C)
cm_DEF = CheckMark(p_D, p_E, p_F)
cm_ABB = CheckMark(p_A, p_B, p_B)
print(cm_ABC, bool(cm_ABC))
print(cm_DEF, bool(cm_DEF))
print(cm_ABB, bool(cm_ABB))