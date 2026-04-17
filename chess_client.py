import requests
import pygame
import json
import pygame_gui

api = "https://juravlik.pythonanywhere.com"
piece_w1 = pygame.image.load("Chess_plt45.svg.png")
piece_w2 = pygame.image.load("Chess_nlt45.svg.png")
piece_w3 = pygame.image.load("Chess_blt45.svg.png")
piece_w4 = pygame.image.load("Chess_rlt45.svg.png")
piece_w5 = pygame.image.load("Chess_qlt45.svg.png")
piece_w6 = pygame.image.load("Chess_klt45.svg.png")

piece_b1 = pygame.image.load("Chess_pdt45.svg.png")
piece_b2 = pygame.image.load("Chess_ndt45.svg.png")
piece_b3 = pygame.image.load("Chess_bdt45.svg.png")
piece_b4 = pygame.image.load("Chess_rdt45.svg.png")
piece_b5 = pygame.image.load("Chess_qdt45.svg.png")
piece_b6 = pygame.image.load("Chess_kdt45.svg.png")
pygame.init()
W,H = 800,835
screen = pygame.display.set_mode((W, H))
screen1 = pygame.Surface((W, H), pygame.SRCALPHA)
font = pygame.font.Font(None, 50)


WHITE_PAWN = 1
BLACK_PAWN = -1

images = {
    WHITE_PAWN: piece_w1,
    BLACK_PAWN: piece_b1
}

class Button:
    def __init__(self, x, y, w, h, color,text):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.text = font.render(text, True, (0, 0, 0))
        self.text_rect = self.text.get_rect(center=(self.x+w/2, self.y+h/2))
    def is_clicked(self, x, y):
        if self.x < x < self.x + self.w and self.y < y < self.y + self.h:
            return True
        else:
            return False
    def draw(self):
        pygame.draw.rect(screen, (0,0,0), (self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, self.color, (self.x+1, self.y+1, self.w-2, self.h-2))
        screen.blit(self.text, self.text_rect)



class ChessField:
    def __init__(self):
        self.board = [[0] * 8 for _ in range(8)]

    def draw(self):
        self.board = json.loads(requests.get(f'{api}/show/{id}').text)
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                pygame.draw.rect(screen, (212 + 33 * ((i + j) % 2), 174 + 48 * ((i + j) % 2), 125 + 54 * ((i + j) % 2)),
                                 pygame.Rect(i * 100, j * 100, 100, 100))
                if piece_selected == (i, j):
                    pygame.draw.rect(screen, (135, 206, 235), pygame.Rect(i * 100, j * 100, 100, 100))
                if self.board[i][j] == 1:
                    screen.blit(piece_w1, (i * 100 + 5, j * 100 + 5))
                if self.board[i][j] == -1:
                    screen.blit(piece_b1, (i * 100 + 5, j * 100 + 5))
                if self.board[i][j] == 2:
                    screen.blit(piece_w2, (i * 100 + 5, j * 100 + 5))
                if self.board[i][j] == -2:
                    screen.blit(piece_b2, (i * 100 + 5, j * 100 + 5))
                if self.board[i][j] == 3:
                    screen.blit(piece_w3, (i * 100 + 5, j * 100 + 5))
                if self.board[i][j] == -3:
                    screen.blit(piece_b3, (i * 100 + 5, j * 100 + 5))
                if self.board[i][j] == 4:
                    screen.blit(piece_w4, (i * 100 + 5, j * 100 + 5))
                if self.board[i][j] == -4:
                    screen.blit(piece_b4, (i * 100 + 5, j * 100 + 5))
                if self.board[i][j] == 5:
                    screen.blit(piece_w5, (i * 100 + 5, j * 100 + 5))
                if self.board[i][j] == -5:
                    screen.blit(piece_b5, (i * 100 + 5, j * 100 + 5))
                if self.board[i][j] == 6:
                    screen.blit(piece_w6, (i * 100 + 5, j * 100 + 5))
                if self.board[i][j] == -6:
                    screen.blit(piece_b6, (i * 100 + 5, j * 100 + 5))
        if piece_selected is not None:
            ls = (requests.get(f"{api}/search/{id}/{piece_selected[0]}/{piece_selected[1]}").text).split(" ")
            if ls == [""]:
                return None
            ls = list(map(int, ls))
            for i in ls:
                pygame.draw.circle(screen1, (135, 206, 235, 170), ((i % 8) * 100 + 50, (i // 8) * 100 + 50), 20)

    def move(self, from_x, from_y, to_x, to_y):
        if requests.get(f"{api}/move/{id}/{from_x}/{from_y}/{to_x}/{to_y}/true").text == "ok":
            self.board[to_x][to_y] = self.board[from_x][from_y]
            self.board[from_x][from_y] = 0

    def back_move(self):
        requests.get(f"{api}/reverse/{id}")


manager = pygame_gui.UIManager((800, 800))
input_box = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((250, 505), (300, 50)),
    manager=manager
)


clock = pygame.time.Clock()
chess_field = ChessField()
piece_selected = None
in_game = False
create_button = Button(250, 325, 300, 75, (255, 255, 255), "create a game")
login_button = Button(250, 425, 300, 75, (255, 255, 255), "log in a game")
norm_chess_button = Button(140, 625, 250, 75, (125, 125, 125), "chess")
not_norm_chess_button = Button(410, 625, 250, 75, (255, 255, 255), "drunck chess")
id = None
norm_chess = "true"
while True:
    time_delta = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if in_game:
                if piece_selected is None:
                    piece_selected = x // 100, y // 100
                else:
                    chess_field.move(piece_selected[0], piece_selected[1], x // 100, y // 100)
                    piece_selected = None
            else:
                if create_button.is_clicked(x, y):
                    in_game = True
                    id = int(requests.get(f"{api}/crate_game/{norm_chess}").text)
                    text = font.render(str(id), True, (0, 0, 0))
                    text_rect = text.get_rect(center=(W/2, H-35/2))
                if login_button.is_clicked(x, y):
                    in_game = True
                    id = int(input_box.get_text())
                    text = font.render(str(id), True, (0, 0, 0))
                    text_rect = text.get_rect(center=(W/2, H-35/2))
                if norm_chess_button.is_clicked(x, y):
                    norm_chess = "true"
                    norm_chess_button.color = (125, 125, 125)
                    not_norm_chess_button.color = (255, 255, 255)
                if not_norm_chess_button.is_clicked(x, y):
                    norm_chess = "false"
                    norm_chess_button.color = (255, 255, 255)
                    not_norm_chess_button.color = (125, 125, 125)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and in_game:
                chess_field.back_move()
        manager.process_events(event)
    if in_game:
        screen.fill((255, 255, 255))
        screen1.fill((255, 255, 255, 0))
        chess_field.draw()
        screen.blit(screen1, (0, 0))
        screen.blit(text, text_rect)
    else:
        screen.fill((255, 255, 255))
        create_button.draw()
        login_button.draw()
        norm_chess_button.draw()
        not_norm_chess_button.draw()
        manager.update(time_delta)
        manager.draw_ui(screen)
    pygame.display.update()
    pygame.time.wait(100)
