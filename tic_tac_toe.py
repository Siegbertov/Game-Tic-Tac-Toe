from copy import deepcopy
import numpy as np
import pygame

pygame.init()
pygame.display.set_caption('TIC-TAC-TOE')
logo = pygame.image.load("logo.png")
pygame.display.set_icon(logo)


def quit_game():
    pygame.quit()
    quit()


class Metadata:
    D_WIDTH = 450
    D_HEIGHT = 450
    C_SIZE = D_WIDTH // 3

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    LIGHT_RED = (200, 0, 0)
    GREEN = (0, 255, 0)
    LIGHT_GREEN = (0, 200, 0)

    # =================================================> COMMENT IT IF YOU WANT TO PLAY IN CONSOLE (call console_game)
    X_IMG = pygame.transform.scale(pygame.image.load("CROSS.png"), (C_SIZE, C_SIZE))
    O_IMG = pygame.transform.scale(pygame.image.load("NOUGHT.png"), (C_SIZE, C_SIZE))
    WINDOW = pygame.display.set_mode((D_WIDTH, D_HEIGHT))


class TTT(Metadata):
    run = True
    winner = None
    turn = 0

    def __init__(self, other=None):
        self.board = np.zeros((3, 3))
        self.player = 1
        self.enemy = 2
        if other:
            self.__dict__ = deepcopy(other.__dict__)

    def draw_lines(self):
        for i in range(1, 3):
            pygame.draw.line(self.WINDOW, self.BLACK, (0, i * self.C_SIZE), (self.D_WIDTH, i * self.C_SIZE), 2)
            pygame.draw.line(self.WINDOW, self.BLACK, (i * self.C_SIZE, 0), (i * self.C_SIZE, self.D_HEIGHT), 2)

    def draw_images(self):
        for c in range(3):
            for r in range(3):
                x = c * self.C_SIZE
                y = r * self.C_SIZE
                if self.board[r][c] == 1:
                    self.WINDOW.blit(self.X_IMG, (x, y))
                if self.board[r][c] == 2:
                    self.WINDOW.blit(self.O_IMG, (x, y))

    def move_image(self):
        if self.turn == 0:
            self.WINDOW.blit(self.X_IMG, (pos_x - self.C_SIZE//2, pos_y - self.C_SIZE//2))
        if self.turn == 1:
            self.WINDOW.blit(self.O_IMG, (pos_x - self.C_SIZE//2, pos_y - self.C_SIZE//2))

    def draw(self):
        self.draw_lines()
        self.draw_images()
        if self.winner is None and not self.tie():
            self.move_image()

    def make_move(self, position):
        b = TTT(self)
        b.board[position//3][position % 3] = b.player
        b.player, b.enemy = b.enemy, b.player
        return b

    def tie(self):
        for c in range(3):
            for r in range(3):
                if self.board[r][c] == 0:
                    return False
        return True

    def check_for_winner(self):
        for r in range(3):
            if self.board[r][0] != 0 and self.board[r][0] == self.board[r][1] and self.board[r][1] == self.board[r][2]:
                self.winner = self.board[r][0]
        for c in range(3):
            if self.board[0][c] != 0 and self.board[0][c] == self.board[1][c] and self.board[1][c] == self.board[2][c]:
                self.winner = self.board[0][c]
        if self.board[0][0] != 0 and self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2]:
            self.winner = self.board[0][0]
        if self.board[2][0] != 0 and self.board[2][0] == self.board[1][1] and self.board[1][1] == self.board[0][2]:
            self.winner = self.board[2][0]

    def won(self):
        for i in range(3):
            if self.board[i][0] == self.enemy and self.board[i][0] == self.board[i][1] and self.board[i][1] == self.board[i][2]:
                return True

            if self.board[0][i] == self.enemy and self.board[0][i] == self.board[1][i] and self.board[1][i] == self.board[2][i]:
                return True

        if self.board[0][0] == self.enemy and self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2]:
            return True

        if self.board[0][2] == self.enemy and self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0]:
            return True
        return False

    def __str__(self):
        return self.board.__str__()

    def best(self):
        return self.algorithm(True)[1]

    def algorithm(self, player):
        if self.won():
            if player:
                return (-1, None)
            else:
                return (1, None)
        elif self.tie():
            return (0, None)
        elif player:
            best = (-2, None)
            for i in range(9):
                if self.board[i//3][i%3] == 0:
                    value = self.make_move(i).algorithm(not player)[0]
                    if value > best[0]:
                        best = (value, i)
            return best
        else:
            best = (2, None)
            for i in range(9):
                if self.board[i//3][i%3] == 0:
                    value = self.make_move(i).algorithm(not player)[0]
                    if value < best[0]:
                        best = (value, i)
            return best


def intro():
    global pos_x, pos_y
    new = TTT()

    text_font = pygame.font.Font("freesansbold.ttf", 30)
    button_font = pygame.font.Font("freesansbold.ttf", 20)

    text = "TIC TAC TOE"
    text_surf = text_font.render(text, True, new.BLACK)
    text_rect = text_surf.get_rect()
    text_rect.center = (new.D_WIDTH // 2, new.D_HEIGHT // 4)


    btn_w = 60
    btn_h = 60

    def button(txt, x, y, btn_w, btn_h, c, c_c, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + btn_w > mouse[0] > x and y < mouse[1] < y + btn_h:
            pygame.draw.rect(new.WINDOW, c_c, (x, y, btn_w, btn_h))
            if click[0] == 1 and action is not None:
                action()
        else:
            pygame.draw.rect(new.WINDOW, c, (x, y, btn_w, btn_h))

        buttonSurf = button_font.render(txt, True, new.BLACK)
        buttonRect = buttonSurf.get_rect()
        buttonRect.center = (x + btn_w // 2, y + btn_h // 2)
        new.WINDOW.blit(buttonSurf, buttonRect)

    while new.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.MOUSEMOTION:
                pos_x = event.pos[0]
                pos_y = event.pos[1]

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_game()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

        new.WINDOW.fill(new.WHITE)
        new.WINDOW.blit(text_surf, text_rect)
        button("Player vs Player", btn_w, new.D_HEIGHT - 3 * btn_h, new.D_WIDTH - 3 * btn_w - 3, btn_h - 3, new.LIGHT_GREEN, new.GREEN, game_loop)
        button("Player vs AI", btn_w, new.D_HEIGHT - 2 * btn_h + 3, new.D_WIDTH - 3 * btn_w - 3, btn_h - 3, new.LIGHT_GREEN, new.GREEN, ai_loop)
        button("EXIT", new.D_WIDTH - 2 * btn_w, new.D_HEIGHT - 3 * btn_h, btn_w, 2 * btn_h, new.LIGHT_RED, new.RED, quit_game)
        pygame.display.update()


def game_loop():
    global pos_x, pos_y
    new = TTT()

    def draw_winning_screen():
        if new.winner == 1:
            new.WINDOW.fill(new.GREEN)
            X_IMG = pygame.transform.scale(pygame.image.load("CROSS.png"), (new.D_WIDTH, new.D_HEIGHT))
            new.WINDOW.blit(X_IMG, (0, 0))

        if new.winner == 2:
            new.WINDOW.fill(new.GREEN)
            O_IMG = pygame.transform.scale(pygame.image.load("NOUGHT.png"), (new.D_WIDTH, new.D_HEIGHT))
            new.WINDOW.blit(O_IMG, (0, 0))

        if new.winner is None:
            text_font = pygame.font.Font("freesansbold.ttf", 90)
            text = "DRAW"
            new.WINDOW.fill(new.BLUE)
            text_surf = text_font.render(text, True, new.BLACK)
            text_rect = text_surf.get_rect()
            text_rect.center = (new.D_WIDTH // 2, new.D_HEIGHT // 2)
            new.WINDOW.blit(text_surf, text_rect)

    while new.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.MOUSEMOTION:
                pos_x = event.pos[0]
                pos_y = event.pos[1]

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()

                if event.key == pygame.K_ESCAPE:
                    intro()

            if event.type == pygame.MOUSEBUTTONDOWN:
                r = pos_y//new.C_SIZE
                c = pos_x//new.C_SIZE
                pos = r * 3 + c

                if  new.turn == 0 and new.winner is None:
                    new = new.make_move(pos)
                if new.turn == 1 and new.winner is None:
                    new = new.make_move(pos)

                new.check_for_winner()
                if new.winner is None:
                    new.turn += 1
                    new.turn = new.turn % 2


        if new.winner is None and not new.tie():
            new.WINDOW.fill(new.WHITE)
            new.draw()
        else:
            draw_winning_screen()

        pygame.display.update()


def ai_loop():
    pass


intro()