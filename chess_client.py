import copy
import requests
import pygame

piece_w1 = pygame.image.load("Chess_plt45.svg.png")
piece_w2 = pygame.image.load("Chess_nlt45.svg.png")
piece_w3 = pygame.image.load("Chess_blt45.svg.png")
piece_w4 = pygame.image.load("Chess_rlt45.svg.png")
piece_w5 = pygame.image.load("Chess_qlt45.svg.png")
piece_w6 = pygame.image.load("Chess_klt45.svg.png")

piece_b1 = pygame.image.load("Chess_plt45.svg.png")
piece_b2 = pygame.image.load("Chess_nlt45.svg.png")
piece_b3 = pygame.image.load("Chess_blt45.svg.png")
piece_b4 = pygame.image.load("Chess_rlt45.svg.png")
piece_b5 = pygame.image.load("Chess_qlt45.svg.png")
piece_b6 = pygame.image.load("Chess_klt45.svg.png")
pygame.init()
screen = pygame.display.set_mode((800, 800))


class ChessField:
    def __init__(self):
        self.board = [[0] * 8 for _ in range(8)]
        for i in range(8):
            self.board[i][1] = 1
            self.board[i][6] = -1
        self.board[0][0] = 4
        self.board[7][0] = 4
        self.board[0][7] = -4
        self.board[7][7] = -4
        self.board[1][0] = 2
        self.board[1][7] = -2
        self.board[6][0] = 2
        self.board[6][7] = -2
        self.board[2][0] = 3
        self.board[2][7] = -3
        self.board[5][0] = 3
        self.board[5][7] = -3
        self.board[4][0] = 5
        self.board[4][7] = -5
        self.board[3][0] = 6
        self.board[3][7] = -6
        self.boards = [copy.deepcopy(self.board)]

    def draw(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                pygame.draw.rect(screen, (212 + 33 * ((i + j) % 2), 174 + 48 * ((i + j) % 2), 125 + 54 * ((i + j) % 2)),
                                 pygame.Rect(i * 100, j * 100, 100, 100))
                if self.board[i][j] == 1:
                    screen.blit(piece_w1, (i * 100 + 5, j * 100 + 5))
                if self.board[i][j] == 2:
                    screen.blit(piece_w2, (i * 100 + 5, j * 100 + 5))
                if self.board[i][j] == 3:
                    screen.blit(piece_w3, (i * 100 + 5, j * 100 + 5))
                if self.board[i][j] == 4:
                    screen.blit(piece_w4, (i * 100 + 5, j * 100 + 5))
                if self.board[i][j] == 5:
                    screen.blit(piece_w5, (i * 100 + 5, j * 100 + 5))
                if self.board[i][j] == 6:
                    screen.blit(piece_w6, (i * 100 + 5, j * 100 + 5))



    def move(self, from_x, from_y, to_x, to_y):
        if requests.get(f"http://127.0.0.1:5000/move/{from_x}/{from_y}/{to_x}/{to_y}").text == "ok":
            self.board[to_x][to_y] = self.board[from_x][from_y]
            self.board[from_x][from_y] = 0
            self.boards.append(copy.deepcopy(self.board))

    def back_move(self):
        if len(self.boards) > 1:
            self.board = copy.deepcopy(self.boards[-2])
            self.boards.pop()


chess_field = ChessField()
piece_selected = None
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if piece_selected is None:
                piece_selected = x // 100, y // 100
            else:
                chess_field.move(piece_selected[0], piece_selected[1], x // 100, y // 100)
                piece_selected = None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                chess_field.back_move()
    screen.fill((255, 255, 255))
    chess_field.draw()
    pygame.display.update()
