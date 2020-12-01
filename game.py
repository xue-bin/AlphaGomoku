import pygame
from board import Board, Color
from agent import AlphaGomoku
"""
drawing the ui and handle the game process using pygame
"""
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

class Game:

    def __init__(self, width=800, height=800, edge_length=50, board = Board(12), wait_click = True, agent=None):
        self.screen_width = width
        self.screen_height = height
        self.screen_edge_length = edge_length
        self.tile_length = (min(width, height) - 2 * edge_length) // (board.size-1)
        self.board = board
        self.wait_click = wait_click
        self.agent=agent
        self.agent_color = None
        self.botton_size = (100,50)
        self.screen = None
        self.draw()

    def need_to_choose_color(self):
        return self.agent is not None and self.agent_color is None

    def draw(self):
        pygame.init()
        screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        pygame.display.set_caption("GOMOKU")
        pygame.display.update()
        self.screen = screen
        if self.need_to_choose_color():
            self.draw_choose_color()
        else:
            self.draw_board()

    def draw_choose_color(self):
        self.screen.fill(COLOR_WHITE)
        large_text = pygame.font.SysFont("comicsansms",90)
        hint_message = large_text.render("Choose your color",True,COLOR_BLACK)
        hint_message_rect = hint_message.get_rect()
        hint_message_rect.center = (self.screen_width // 2, self.screen_height // 3)
        self.screen.blit(hint_message,hint_message_rect)
        self.draw_botton("BLACK!",self.screen_width//4,2*self.screen_height//3,Color.BLACK)
        self.draw_botton("WHITE!",3*self.screen_width//4,2*self.screen_height//3,Color.BLACK)
        pygame.display.update()

    def draw_botton(self,message,x,y,color):
        small_text = pygame.font.SysFont("comicsansms",50)
        botton_text = small_text.render(message,True,COLOR_BLACK)
        botton_text_rect = botton_text.get_rect()
        botton_text_rect.center = ( x,y )
        self.screen.blit(botton_text,botton_text_rect)

    def draw_board(self):
        self.screen.fill(COLOR_WHITE)
        width = min(self.screen_height, self.screen_width)
        for x in range(self.screen_edge_length, width, self.tile_length):
            pygame.draw.line(self.screen, COLOR_BLACK, (x, self.screen_edge_length),
                             (x, width - self.screen_edge_length))
            pygame.draw.line(self.screen, COLOR_BLACK, (self.screen_edge_length,
                                                   x), (width - self.screen_edge_length, x))
        pygame.display.update()

    def wait_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if self.need_to_choose_color():
                self.choose_color_event(event)
            else:
                self.in_game_event(event)
        return True

    def choose_color_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # print(event.pos)
            if 2*self.screen_height//3-0.5*self.botton_size[1]<event.pos[1]<2*self.screen_height//3+0.5*self.botton_size[1]:
                if self.screen_width//4-self.botton_size[0]<event.pos[0]<self.screen_width//4+self.botton_size[0]:
                    self.agent_color=Color.WHITE
                    self.draw_board()
                elif 3*self.screen_width//4-self.botton_size[0]<event.pos[0]<3*self.screen_width//4+self.botton_size[0]:
                    self.agent_color=Color.BLACK
                    self.draw_board()

    def in_game_event(self,event):
        if self.wait_click  and event.type == pygame.MOUSEBUTTONDOWN:
            if not self.board.end:
                if self.legal_pos(event.pos)and self.this_turn_clickable():
                    self.play_move(self.pos_to_coord(event.pos))
            else:
                self.agent_color = None
                self.board.reset()
                self.draw()

    def legal_pos(self, pos):
        # x in bound
        constrains = [pos[0], self.screen_width -
                      pos[0], pos[1], self.screen_height - pos[1]]
        if min(constrains) > 0.5 * self.screen_edge_length:
            return True
        return False

    def pos_to_coord(self, pos):
        x = int((pos[0] - self.screen_edge_length) / self.tile_length + 0.5)
        y = int((pos[1] - self.screen_edge_length) / self.tile_length + 0.5)
        return x, y

    def coord_to_pos(self, coord):
        x = (coord[0]) * self.tile_length + self.screen_edge_length
        y = (coord[1]) * self.tile_length + self.screen_edge_length
        return x, y

    def draw_stone(self, pos, player):
        if player == Color.BLACK:
            pygame.draw.circle(self.screen, COLOR_BLACK,
                               pos, self.tile_length // 2 - 2)
        elif player == Color.WHITE:
            pygame.draw.circle(self.screen, COLOR_BLACK, pos,
                               self.tile_length // 2 - 2, 2)
        pygame.display.update()

    def show_result(self, winner):
        self.screen.fill(COLOR_WHITE)
        font = pygame.font.Font('freesansbold.ttf', 32)
        if winner == None:
            text = font.render("draw", True, COLOR_BLACK)
        else:
            text = font.render(winner.name + " wins", True, COLOR_BLACK)
        text_rect = text.get_rect()
        text_rect.center = (self.screen_width // 2, self.screen_height // 2)
        self.screen.blit(text, text_rect)
        pygame.display.update()

    def run(self):
        game_continue = True
        while game_continue:
            if not self.board.end and not self.need_to_choose_color() and  not self.this_turn_clickable():
                move = self.agent.get_move()
                if move is None:
                    self.show_result(winner=opponent(self.agent_color))
                    self.board.end = True
                else:
                    self.play_move(move)
            game_continue = self.wait_event()

    def this_turn_clickable(self):
        return self.agent is None or (self.agent_color is not None and self.agent_color != self.board.current_player)

    def play_move(self,move):
        player = self.board.play_stone(move)
        self.draw_stone(self.coord_to_pos(move), player)
        if self.board.end:
            self.show_result(self.board.winner)

def opponent(color):
    return Color.WHITE.value + Color.BLACK.value - color

if __name__ == '__main__':
    board = Board(11)
    agent = AlphaGomoku(board = board)
    game = Game(board=board,wait_click=True,agent=agent)
    game.run()
    # game_continue = True
    # while game_continue:
    #     game_continue = game.wait_event()
