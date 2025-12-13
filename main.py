from flask import Flask

app = Flask(__name__)

Field = [[0] * 8 for _ in range(8)]
for i in range(8):
    Field[i][1] = 1
    Field[i][6] = -1
Field[0][0] = 4
Field[7][0] = 4
Field[0][7] = -4
Field[7][7] = -4
Field[1][0] = 2
Field[1][7] = -2
Field[6][0] = 2
Field[6][7] = -2
Field[2][0] = 3
Field[2][7] = -3
Field[5][0] = 3
Field[5][7] = -3
Field[4][0] = 5
Field[4][7] = -5
Field[3][0] = 6
Field[3][7] = -6


@app.route('/move/<from_x>/<from_y>/<to_x>/<to_y>')
def move(from_x, from_y, to_x, to_y):
    from_x, from_y, to_x, to_y = int(from_x), int(from_y), int(to_x), int(to_y)
    if Field[from_x][from_y] == 1:
        if Field[to_x][to_y] == 0 and to_y == from_y + 1 and to_x == from_x:
            Field[to_x][to_y] = Field[from_x][from_y]
            Field[from_x][from_y] = 0
            return "ok"
        if Field[to_x][to_y] != 0 and to_y == from_y + 1 and (to_x == from_x + 1 or to_x == from_x - 1):
            Field[to_x][to_y] = Field[from_x][from_y]
            Field[from_x][from_y] = 0
            return "ok"
        else:
            return "ne_ok"
    if Field[from_x][from_y] == -1:
        if Field[to_x][to_y] == 0 and to_y == from_y - 1 and to_x == from_x:
            Field[to_x][to_y] = Field[from_x][from_y]
            Field[from_x][from_y] = 0
            return "ok"
        if Field[to_x][to_y] != 0 and to_y == from_y - 1 and (to_x == from_x + 1 or to_x == from_x - 1):
            Field[to_x][to_y] = Field[from_x][from_y]
            Field[from_x][from_y] = 0
            return "ok"
        else:
            return "ne_ok"
    if Field[from_x][from_y] == 2:
        if Field[to_x][to_y] < 1 and ((abs(to_y - from_y) == 1 and abs(to_x - from_x) == 2) or (abs(to_y - from_y) == 2 and abs(to_x - from_x) == 1)):
            Field[to_x][to_y] = Field[from_x][from_y]
            Field[from_x][from_y] = 0
            return "ok"
        else:
            return "ne_ok"
    if Field[from_x][from_y] == -2:
        if Field[to_x][to_y] >= 0 and ((abs(to_y - from_y) == 1 and abs(to_x - from_x) == 2) or (abs(to_y - from_y) == 2 and abs(to_x - from_x) == 1)):
            Field[to_x][to_y] = Field[from_x][from_y]
            Field[from_x][from_y] = 0
            return "ok"
        else:
            return "ne_ok"
app.run()
