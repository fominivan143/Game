WHITE = 1
BLACK = 2


# Удобная функция для вычисления цвета противника
def opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def print_board(board):  # Распечатать доску в текстовом виде (см. скриншот)
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(col, end='    ')
    print()


def main():
    # Создаём шахматную доску
    board = Board()
    # Цикл ввода команд игроков
    while True:
        # Выводим положение фигур на доске
        print_board(board)
        # Подсказка по командам
        print('Команды:')
        print('    exit                               -- выход')
        print('    move <row> <col> <row1> <row1>     -- ход из клетки (row, col)')
        print('                                          в клетку (row1, col1)')
        # Выводим приглашение игроку нужного цвета
        if board.current_player_color() == WHITE:
            print('Ход белых:')
        else:
            print('Ход чёрных:')
        command = input()
        if command == 'exit':
            break
        move_type, row, col, row1, col1 = command.split()
        row, col, row1, col1 = int(row), int(col), int(row1), int(col1)
        if board.move_piece(row, col, row1, col1):
            print('Ход успешен')
        else:
            print('Координаты некорректы! Попробуйте другой ход!')


def correct_coords(row, col):
    '''Функция проверяет, что координаты (row, col) лежат
    внутри доски'''
    return 0 <= row < 8 and 0 <= col < 8


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        '''Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела.'''
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def get_piece(self, row, col):
        if correct_coords(row, col):
            return self.field[row][col]
        else:
            return None

    def move_piece(self, row, col, row1, col1):
        '''Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет --- вернёт False'''

        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        self.color = opponent(self.color)
        return True

    def move_and_promote_pawn(self, row, col, row1, col1, new_char):
        if new_char not in('Q', 'R', 'N', 'B'):
            return False

        piece = self.field[row][col]

        if (piece is None) or (piece.char() != 'P'):
            return False
        if piece.get_color() == WHITE and row1 != 7:
            return False
        if piece.get_color() == BLACK and row1 != 0:
            return False

        if self.move_piece(row, col, row1, col1):
            if new_char == 'Q':
                self.field[row1][col1] = Queen(piece.get_color())
            elif new_char == 'R':
                self.field[row1][col1] = Rook(piece.get_color())
            elif new_char == 'N':
                self.field[row1][col1] = Knight(piece.get_color())
            elif new_char == 'B':
                self.field[row1][col1] = Bishop(piece.get_color())

            return True

        return False


class Rook:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            # Если на пути по горизонтали есть фигура
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            # Если на пути по вертикали есть фигура
            if not (board.get_piece(row, c) is None):
                return False

        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Pawn:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        # Пешка может ходить только по вертикали
        # "взятие на проходе" не реализовано
        if col != col1:
            return False

        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        # ход на 1 клетку
        if row + direction == row1:
            return True

        # ход на 2 клетки из начального положения
        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            return True

        return False

    def can_attack(self, board, row, col, row1, col1):
        direction = 1 if (self.color == WHITE) else -1
        return (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1))


class Knight:
    '''Класс коня. Пока что заглушка, которая может ходить в любую клетку.'''

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'N'  # kNight, буква 'K' уже занята королём

    def can_move(self, board, row, col, row1, col1):
        return True  # Заглушка

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(self, board, row, col, row1, col1)


class King:
    '''Класс короля. Пока что заглушка, которая может ходить в любую клетку.'''

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'K'

    def can_move(self, board, row, col, row1, col1):
        return True  # Заглушка

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(self, board, row, col, row1, col1)


class Queen:
    '''Класс ферзя. Пока что заглушка, которая может ходить в любую клетку.'''

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
        if not correct_coords(row1, col1):
            return False
        piece1 = board.get_piece(row1, col1)
        if not (piece1 is None) and piece1.get_color() == self.color:
            return False
        if row == row1 or col == col1:
            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1, step):
                if not (board.get_piece(r, col) is None):
                    return False
            step = 1 if (col1 >= col) else -1
            for c in range(col + step, col1, step):
                if not (board.get_piece(row, c) is None):
                    return False
            return True
        if row - col == row1 - col1:
            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1, step):
                c = col - row + r
                if not (board.get_piece(r, c) is None):
                    return False
            return True
        if row + col == row1 + col1:
            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1, step):
                c = row + col - r
                if not (board.get_piece(r, c) is None):
                    return False
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(self, board, row, col, row1, col1)


class Bishop:
    '''Класс слона. Пока что заглушка, которая может ходить в любую клетку.'''

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):
        return True  # Заглушка

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(self, board, row, col, row1, col1)


if __name__ == "__main__":
    board = Board()
    board.field = [([None] * 8) for i in range(8)]
    board.field[0][3] = Queen(WHITE)
    queen = board.get_piece(0, 3)

    for row in range(7, -1, -1):
        for col in range(8):
            if queen.can_move(board, 0, 3, row, col):
                print('x', end='')
            else:
                cell = board.cell(row, col)[1]
                cell = cell if cell != ' ' else '-'
                print(cell, end='')
        print()

sp = []
for i in range(int(input())):
    x, y = map(int, input().split(' '))
    sp.append((x, y))
    if abs(x) > abs(y):
        print((x, y,))
sp1 = sorted(sp, key=lambda a: a[0])
if len(sp1) == 1 or (sp1[0][0] != sp1[1][0] and sp1[-1][0] != sp1[-2][0]):
    print(f'left: {sp1[0]}')
    print(f'right: {sp1[-1]}')
else:
    print(f'left: {sp1[min(sp.index(sp1[0]), sp.index(sp1[1]))]}')
    print(f'right: {sp1[min(sp.index(sp1[-1]), sp.index(sp1[-2]))]}')
sp1 = sorted(sp, key=lambda a: a[1])
print(sp1, sp)
if len(sp1) == 1 or (sp1[0][1] != sp1[1][1] and sp1[-1][1] != sp1[-2][1]):
    print(f'top: {sp1[-1]}')
    print(f'bottom: {sp1[0]}')
    print(sp1[-1][1], sp1[-2][1])
else:
    print(sp.index(sp1[0]), sp.index(sp1[1]))
    print(f'top: {sp1[min(sp.index(sp1[-1]), sp.index(sp1[-2]))]}')
    print(f'bottom: {sp1[min(sp.index(sp1[0]), sp.index(sp1[1]))]}')


import sys


dt = {}
data = sys.stdin.read().split('\n')
for el in data:
    if len(el) != 0 and (el[-1].isdigit() or el[-1] == 0):
        if el[-1] == '0':
            if el[-2:] in dt.keys():
                dt[el[-2:]] += ', ' + el[:-2]
            else:
                dt[el[-2:]] = el[:-2]
        else:
            if el[-1] in dt.keys():
                dt[el[-1]] +=', ' + el[:-1]
            else:
                dt[el[-1]] = el[:-1]
                print(dt[el[-1]])
    else:
        data.remove(el)
for k in sorted(dt.keys(), key=int):
    print(k + ':', dt[k])