import random
from flask import Flask, request

app = Flask(__name__)


class Game():
    def __init__(self,normal_chess):
        self.Field = [[0] * 8 for _ in range(8)]
        for i in range(8):
            self.Field[i][1] = -1
            self.Field[i][6] = 1
        self.Field[0][0] = -4
        self.Field[7][0] = -4
        self.Field[0][7] = 4
        self.Field[7][7] = 4
        self.Field[1][0] = -2
        self.Field[1][7] = 2
        self.Field[6][0] = -2
        self.Field[6][7] = 2
        self.Field[2][0] = -3
        self.Field[2][7] = 3
        self.Field[5][0] = -3
        self.Field[5][7] = 3
        self.Field[4][0] = -5
        self.Field[4][7] = 5
        self.Field[3][0] = -6
        self.Field[3][7] = 6

        self.normal_chess = normal_chess
        self.Fields = []
        self.move = True

        self.move_funcs = {
            0: lambda _, __, ___, ____, _____: None,
            1: self.move_pawn,
            -1: self.move_pawn,
            2: self.move_knight,
            -2: self.move_knight,
            3: self.move_bishop,
            -3: self.move_bishop,
            4: self.move_rook,
            -4: self.move_rook,
            5: self.move_queen,
            -5: self.move_queen,
            6: self.move_king,
            -6: self.move_king,
        }

    def move_pawn(self, from_x, from_y, to_x, to_y, do_move):
        if self.Field[to_x][to_y] == 0 and to_y == from_y - 1 * self.Field[from_x][from_y] and to_x == from_x:
            if do_move == "true":
                self.Fields.append((from_x, from_y, self.Field[from_x][from_y], to_x, to_y, self.Field[to_x][to_y]))
                self.Field[to_x][to_y] = self.Field[from_x][from_y]
                if to_y == 0:
                    self.Field[to_x][to_y] = random.randint(2, 6)
                if to_y == 7:
                    self.Field[to_x][to_y] = random.randint(-6, -2)
                self.Field[from_x][from_y] = 0
            return "ok"
        if self.Field[from_x][from_y - 1 * self.Field[from_x][from_y]] == 0 and from_y - 2 * self.Field[from_x][
            from_y] == to_y and from_y in (1, 6) and to_x == from_x:
            if do_move == "true":
                self.Fields.append((from_x, from_y, self.Field[from_x][from_y], to_x, to_y, self.Field[to_x][to_y]))
                self.Field[to_x][to_y] = self.Field[from_x][from_y]
                self.Field[from_x][from_y] = 0
            return "ok"
        if self.Field[to_x][to_y] != 0 and to_y == from_y - 1 * self.Field[from_x][from_y] and (
                to_x == from_x + 1 or to_x == from_x - 1):
            if do_move == "true":
                self.Fields.append((from_x, from_y, self.Field[from_x][from_y], to_x, to_y, self.Field[to_x][to_y]))
                self.Field[to_x][to_y] = self.Field[from_x][from_y]
                if to_y == 0:
                    self.Field[to_x][to_y] = random.randint(2, 6)
                if to_y == 7:
                    self.Field[to_x][to_y] = random.randint(-6, -2)
                self.Field[from_x][from_y] = 0
            return "ok"
        return "ne_ok"

    def move_bishop(self, from_x, from_y, to_x, to_y, do_move):
        if (abs(to_y - from_y) == abs(to_x - from_x) and
                [self.Field[from_x + i * ((to_x - from_x) // abs(from_x - to_x))][
                     from_y + i * ((to_y - from_y) // abs(from_y - to_y))]
                 for i in range(1, abs(from_x - to_x))] == [0] * (abs(from_x - to_x) - 1)):
            if do_move == "true":
                self.Fields.append((from_x, from_y, self.Field[from_x][from_y], to_x, to_y, self.Field[to_x][to_y]))
                self.Field[to_x][to_y] = self.Field[from_x][from_y]
                self.Field[from_x][from_y] = 0
            return "ok"
        return "ne_ok"

    def move_queen(self, from_x, from_y, to_x, to_y, do_move):
        if self.move_bishop(from_x, from_y, to_x, to_y, do_move) == "ok" or self.move_rook(from_x, from_y, to_x, to_y,
                                                                                        do_move) == "ok":
            return "ok"

    def move_king(self, from_x, from_y, to_x, to_y, do_move):
        if abs(to_y - from_y) <= 1 and abs(to_x - from_x) <= 1:
            if do_move == "true":
                self.Fields.append((from_x, from_y, self.Field[from_x][from_y], to_x, to_y, self.Field[to_x][to_y]))
                self.Field[to_x][to_y] = self.Field[from_x][from_y]
                self.Field[from_x][from_y] = 0
            return "ok"
        return "ne_ok"

    def move_rook(self, from_x, from_y, to_x, to_y, do_move):
        if to_x == from_x:
            if [self.Field[from_x][i] for i in range(min(from_y, to_y) + 1, max(from_y, to_y))] == [0] * (
                    abs(from_y - to_y) - 1):
                if do_move == "true":
                    self.Fields.append((from_x, from_y, self.Field[from_x][from_y], to_x, to_y, self.Field[to_x][to_y]))
                    self.Field[to_x][to_y] = self.Field[from_x][from_y]
                    self.Field[from_x][from_y] = 0
                return "ok"
        elif to_y == from_y:
            if [self.Field[i][from_y] for i in range(min(from_x, to_x) + 1, max(from_x, to_x))] == [0] * (
                    abs(from_x - to_x) - 1):
                if do_move == "true":
                    self.Fields.append((from_x, from_y, self.Field[from_x][from_y], to_x, to_y, self.Field[to_x][to_y]))
                    self.Field[to_x][to_y] = self.Field[from_x][from_y]
                    self.Field[from_x][from_y] = 0
                return "ok"
        return "ne_ok"

    def move_knight(self, from_x, from_y, to_x, to_y, do_move):
        if ((abs(to_y - from_y) == 1 and abs(to_x - from_x) == 2) or (
                abs(to_y - from_y) == 2 and abs(to_x - from_x) == 1)):
            if do_move == "true":
                self.Fields.append((from_x, from_y, self.Field[from_x][from_y], to_x, to_y, self.Field[to_x][to_y]))
                self.Field[to_x][to_y] = self.Field[from_x][from_y]
                self.Field[from_x][from_y] = 0
            return "ok"


games = []


@app.route('/crate_game/<normal_chess>')
def crate_game(normal_chess):
    if normal_chess == "true":
        games.append(Game(True))
    else:
        games.append(Game(False))
    return str(len(games) - 1)


@app.route('/move/<id>/<from_x>/<from_y>/<to_x>/<to_y>/<do_move>')
def move(id, from_x, from_y, to_x, to_y, do_move):
    from_x, from_y, to_x, to_y = int(from_x), int(from_y), int(to_x), int(to_y)
    id = int(id)
    if (games[id].move and games[id].Field[from_x][from_y] < 0) or (not games[id].move and games[id].Field[from_x][from_y] > 0):
        return "ne_ok"
    if games[id].normal_chess:
        s = request.args.get('select')
        if games[id].Field[from_x][from_y] * games[id].Field[to_x][to_y] > 0:
            return "ne_ok"
        ans = games[id].move_funcs[games[id].Field[from_x][from_y]](from_x, from_y, to_x, to_y, do_move)
        if ans == "ok" and do_move == "true":
            games[id].move = not games[id].move
        return ans
    else:
        if from_x == to_x and from_y == to_y:
            return "ok"
        ls = list(map(int,search(id,from_x, from_y).split(" ")))
        for i in range(len(ls)):
            games[id].Field[ls[i]%8][ls[i]//8] = games[id].Field[from_x][from_y]
        games[id].move = not games[id].move
        return "ok"


@app.route('/search/<id>/<from_x>/<from_y>')
def search(id, from_x, from_y):
    id = int(id)
    from_x, from_y = int(from_x), int(from_y)
    normal_chess = games[id].normal_chess
    games[id].normal_chess = True
    ls = []
    for i in range(8):
        for j in range(8):
            if move(id, from_x, from_y, i, j, "false") == "ok":
                #games[id].Field[i][j] = games[id].Field[from_x][from_y]
                ls.append(str(i + 8 * j))
                if games[id].Field[from_x][from_y] in (6, -6):
                    will_be_attacked(id, from_x, from_y, i, j, ls)
    games[id].normal_chess = normal_chess
    return " ".join(ls)


@app.route('/reverse/<id>')
def reverse(id):
    id = int(id)
    global games
    if len(games[id].Fields) > 0:
        games[id].Field[games[id].Fields[-1][0]][games[id].Fields[-1][1]] = games[id].Fields[-1][2]
        games[id].Field[games[id].Fields[-1][3]][games[id].Fields[-1][4]] = games[id].Fields[-1][5]
        games[id].Fields.pop()
        games[id].move = not games[id].move
        return "ok"
    return "ne_ok"


@app.route('/show/<id>')
def show(id):
    id = int(id)
    return games[id].Field


def will_be_attacked(id, from_x, from_y, i, j, ls):
    id = int(id)
    p = games[id].Field[i][j]
    games[id].Field[i][j] = games[id].Field[from_x][from_y]
    games[id].Field[from_x][from_y] = 0
    for ii in range(8):
        for jj in range(8):
            if games[id].Field[i][j] * games[id].Field[ii][jj] < 0:
                if move(id, ii, jj, i, j, "false") == "ok":
                    ls.pop()
                    games[id].Field[from_x][from_y] = games[id].Field[i][j]
                    games[id].Field[i][j] = p
                    return
    games[id].Field[from_x][from_y] = games[id].Field[i][j]
    games[id].Field[i][j] = p


if __name__ == '__main__':
    app.run("0.0.0.0", port=5000)
