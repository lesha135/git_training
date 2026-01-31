from flask import Flask
import copy

app = Flask(__name__)

Field = [[0] * 8 for _ in range(8)]
for i in range(8):
    Field[i][1] = -1
    Field[i][6] = 1
Field[0][0] = -4
Field[7][0] = -4
Field[0][7] = 4
Field[7][7] = 4
Field[1][0] = -2
Field[1][7] = 2
Field[6][0] = -2
Field[6][7] = 2
Field[2][0] = -3
Field[2][7] = 3
Field[5][0] = -3
Field[5][7] = 3
Field[4][0] = -5
Field[4][7] = 5
Field[3][0] = -6
Field[3][7] = 6

Fields = [copy.deepcopy(Field)]

@app.route('/move/<from_x>/<from_y>/<to_x>/<to_y>/<move>')
def move(from_x, from_y, to_x, to_y,move):
    from_x, from_y, to_x, to_y = int(from_x), int(from_y), int(to_x), int(to_y)
    if Field[from_x][from_y] * Field[to_x][to_y] > 0:
        return "ne_ok"
    if Field[from_x][from_y] in (1, -1):
        if Field[to_x][to_y] == 0 and to_y == from_y - 1 * Field[from_x][from_y] and to_x == from_x:
            if move == "true":
                Field[to_x][to_y] = Field[from_x][from_y]
                Field[from_x][from_y] = 0
                Fields.append(copy.deepcopy(Field))
            return "ok"
        if Field[to_x][to_y] != 0 and to_y == from_y - 1 * Field[from_x][from_y] and (
                to_x == from_x + 1 or to_x == from_x - 1):
            if move == "true":
                Field[to_x][to_y] = Field[from_x][from_y]
                Field[from_x][from_y] = 0
                Fields.append(copy.deepcopy(Field))
            return "ok"
    if Field[from_x][from_y] in (2, -2):
        if ((abs(to_y - from_y) == 1 and abs(to_x - from_x) == 2) or (
                abs(to_y - from_y) == 2 and abs(to_x - from_x) == 1)):
            if move == "true":
                Field[to_x][to_y] = Field[from_x][from_y]
                Field[from_x][from_y] = 0
                Fields.append(copy.deepcopy(Field))
            return "ok"
    if Field[from_x][from_y] in (3, -3, 5, -5):
        if (abs(to_y - from_y) == abs(to_x - from_x) and
                [Field[from_x + i * ((to_x - from_x) // abs(from_x - to_x))][from_y + i * ((to_y - from_y) // abs(from_y - to_y))]
                 for i in range(1, abs(from_x - to_x))] == [0] * (abs(from_x - to_x) - 1)):
            if move == "true":
                Field[to_x][to_y] = Field[from_x][from_y]
                Field[from_x][from_y] = 0
                Fields.append(copy.deepcopy(Field))
            return "ok"
    if Field[from_x][from_y] in (4, -4, -5, 5):
        if to_x == from_x:
            if [Field[from_x][i] for i in range(min(from_y, to_y) + 1, max(from_y, to_y))] == [0] * (abs(from_y - to_y) - 1):
                if move == "true":
                    Field[to_x][to_y] = Field[from_x][from_y]
                    Field[from_x][from_y] = 0
                    Fields.append(copy.deepcopy(Field))
                return "ok"
        if to_y == from_y:
            if [Field[i][from_y] for i in range(min(from_x, to_x) + 1, max(from_x, to_x))] == [0] * (abs(from_x - to_x) - 1):
                if move == "true":
                    Field[to_x][to_y] = Field[from_x][from_y]
                    Field[from_x][from_y] = 0
                    Fields.append(copy.deepcopy(Field))
                return "ok"
    if Field[from_x][from_y] in (-6, 6):
        if abs(to_y - from_y)<=1 and abs(to_x - from_x)<=1:
            if move == "true":
                Field[to_x][to_y] = Field[from_x][from_y]
                Field[from_x][from_y] = 0
                Fields.append(copy.deepcopy(Field))
            return "ok"
    return "ne_ok"

@app.route('/search/<from_x>/<from_y>')
def search(from_x, from_y):
    from_x, from_y = int(from_x), int(from_y)
    ls=[]
    for i in range(8):
        for j in range(8):
            if move(from_x, from_y, i, j, "false") == "ok":
                ls.append(str(i+8*j))
                if Field[from_x][from_y] in (6, -6):
                    will_be_attacked(from_x, from_y, i, j, ls)
    return " ".join(ls)

@app.route('/reverse')
def reverse():
    global Field
    global Fields
    if len(Fields)>1:
        Field = copy.deepcopy(Fields[-2])
        Fields.pop()
        return "ok"

@app.route('/show')
def show():
    return Field

def will_be_attacked(from_x, from_y, i, j, ls):
    p = Field[i][j]
    Field[i][j] = Field[from_x][from_y]
    Field[from_x][from_y] = 0
    for ii in range(8):
        for jj in range(8):
            if Field[i][j] * Field[ii][jj] < 0:
                if move(ii, jj, i, j, "false") == "ok":
                    ls.pop()
                    Field[from_x][from_y] = Field[i][j]
                    Field[i][j] = p
                    return
    Field[from_x][from_y] = Field[i][j]
    Field[i][j] = p

if __name__ == '__main__':
    app.run()
