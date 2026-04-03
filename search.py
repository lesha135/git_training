def move_pawn(Field, from_x, from_y, to_x, to_y, do_move):
    if Field[to_x][to_y] == 0 and to_y == from_y - 1 * Field[from_x][from_y] and to_x == from_x:
        if do_move == "true":
            Field[to_x][to_y] = Field[from_x][from_y]
            Field[from_x][from_y] = 0
        return "ok"
    if Field[from_x][from_y - 1 * Field[from_x][from_y]] == 0 and from_y - 2 * Field[from_x][
        from_y] == to_y and from_y in (1, 6) and to_x == from_x:
        if do_move == "true":
            Field[to_x][to_y] = Field[from_x][from_y]
            Field[from_x][from_y] = 0
        return "ok"
    if Field[to_x][to_y] != 0 and to_y == from_y - 1 * Field[from_x][from_y] and (
            to_x == from_x + 1 or to_x == from_x - 1):
        if do_move == "true":
            Field[to_x][to_y] = Field[from_x][from_y]
            Field[from_x][from_y] = 0
        return "ok"
    return "ne_ok"


def move_bishop(Field, from_x, from_y, to_x, to_y, do_move):
    if (abs(to_y - from_y) == abs(to_x - from_x) and
            [Field[from_x + i * ((to_x - from_x) // abs(from_x - to_x))][
                 from_y + i * ((to_y - from_y) // abs(from_y - to_y))]
             for i in range(1, abs(from_x - to_x))] == [0] * (abs(from_x - to_x) - 1)):
        if do_move == "true":
            Field[to_x][to_y] = Field[from_x][from_y]
            Field[from_x][from_y] = 0
        return "ok"
    return "ne_ok"


def move_queen(Field, from_x, from_y, to_x, to_y, do_move):
    if move_bishop(Field, from_x, from_y, to_x, to_y, do_move) == "ok" or move_rook(Field, from_x, from_y, to_x, to_y,
                                                                             do_move) == "ok":
        return "ok"
    return "ne_ok"


def move_king(Field, from_x, from_y, to_x, to_y, do_move):
    if abs(to_y - from_y) <= 1 and abs(to_x - from_x) <= 1:
        if do_move == "true":
            Field[to_x][to_y] = Field[from_x][from_y]
            Field[from_x][from_y] = 0
        return "ok"
    return "ne_ok"


def move_rook(Field, from_x, from_y, to_x, to_y, do_move):
    if to_x == from_x:
        if [Field[from_x][i] for i in range(min(from_y, to_y) + 1, max(from_y, to_y))] == [0] * (
                abs(from_y - to_y) - 1):
            if do_move == "true":
                Field[to_x][to_y] = Field[from_x][from_y]
                Field[from_x][from_y] = 0
            return "ok"
    elif to_y == from_y:
        if [Field[i][from_y] for i in range(min(from_x, to_x) + 1, max(from_x, to_x))] == [0] * (
                abs(from_x - to_x) - 1):
            if do_move == "true":
                Field[to_x][to_y] = Field[from_x][from_y]
                Field[from_x][from_y] = 0
            return "ok"
    return "ne_ok"


def move_knight(Field, from_x, from_y, to_x, to_y, do_move):
    if ((abs(to_y - from_y) == 1 and abs(to_x - from_x) == 2) or (
            abs(to_y - from_y) == 2 and abs(to_x - from_x) == 1)):
        if do_move == "true":
            Field[to_x][to_y] = Field[from_x][from_y]
            Field[from_x][from_y] = 0
        return "ok"


def move(Field, from_x, from_y, to_x, to_y, do_move):
    if Field[from_x][from_y] * Field[to_x][to_y] > 0:
        return "ne_ok"
    ans = move_funcs[Field[from_x][from_y]](Field,from_x, from_y, to_x, to_y, do_move)
    return ans


def search(Field, from_x, from_y):
    ls = []
    for i in range(8):
        for j in range(8):
            if move(Field, from_x, from_y, i, j, "false") == "ok":
                ls.append(i + 8 * j)
                if Field[from_x][from_y] in (6,-6):
                    will_be_attacked(Field, from_x, from_y, i, j, ls)
    return ls


def will_be_attacked(Field, from_x, from_y, i, j, ls):
    p = Field[i][j]
    Field[i][j] = Field[from_x][from_y]
    Field[from_x][from_y] = 0
    for ii in range(8):
        for jj in range(8):
            if Field[i][j] * Field[ii][jj] < 0:
                if move(Field, ii, jj, i, j, "false") == "ok":
                    ls.pop()
                    Field[from_x][from_y] = Field[i][j]
                    Field[i][j] = p
                    return
    Field[from_x][from_y] = Field[i][j]
    Field[i][j] = p


move_funcs = {
    0: lambda _, __, ___, ____, _____, ______: None,
    1: move_pawn,
    -1: move_pawn,
    2: move_knight,
    -2: move_knight,
    3: move_bishop,
    -3: move_bishop,
    4: move_rook,
    -4: move_rook,
    5: move_queen,
    -5: move_queen,
    6: move_king,
    -6: move_king,
}
