from flask import Flask
import chess
app = Flask(__name__)
chessboard = chess.Board()

@app.route('/move')
def move():

    return "ok"

app.run()