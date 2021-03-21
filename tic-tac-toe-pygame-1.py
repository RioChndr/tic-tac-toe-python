import pygame
import sys
import random

class TicTacToe:
  def __init__(self):
    pygame.init()

    self.size = width, height = 300, 300
    self.background = (224, 241, 244)
    self.color_game = (0, 55, 61)
    self.screen = pygame.display.set_mode(self.size)
    self.player_x = pygame.image.load('assets/player_x_100.png')
    self.player_o = pygame.image.load('assets/player_o_100.png')
    self.player_pos = {
      1: [], # x
      2: []  # o
    }
    self.current_player = random.randint(1,2)
    self.cross_winner = None
    self.winner = None
    self.cell_tic_tac_toe = {}
    ## Create collide rectangle

    char_rect = self.player_x.get_rect()
    for col in range(3):
        for row in range(3):
          centerx = (height/3) * (row)
          centery = (width/3) * (col)
          self.cell_tic_tac_toe[(row, col)] = pygame.Rect(centerx, centery, char_rect.width, char_rect.height)
    self.play_game()

  def play_game(self):
    while True:
      self.screen.fill(self.background)
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit()  

        if event.type == pygame.MOUSEBUTTONUP:
          pos_mouse = pygame.mouse.get_pos()
          clicked_rect = [pos_rect for pos_rect in self.cell_tic_tac_toe if self.cell_tic_tac_toe[pos_rect].collidepoint(pos_mouse)]

          if len(clicked_rect) > 0 and self.winner is None:
            next_player = 1 if self.current_player == 2 else 2

            if clicked_rect[0] not in self.player_pos[self.current_player] and clicked_rect[0] not in self.player_pos[next_player]:
              self.player_pos[self.current_player].append(clicked_rect[0])
              self.check_winner()
              self.current_player = next_player  
      
      self.draw_border()
      self.show_pos_player()
      self.draw_cross()
      pygame.display.flip()

  def draw_border(self):
    screen_width, screen_height = self.size

    lines = [
      # horizontal 2 lines
      {
        'start': [screen_width/3, 0],
        'end' : [screen_width/3, screen_height]
      },
      {
        'start': [screen_width/3 * 2, 0],
        'end' : [screen_width/3 * 2, screen_height]
      },
      # vertical 2 lines
      {
        'start': [0, screen_height/3],
        'end' : [screen_width, screen_height/3]
      },
      {
        'start': [0, screen_height/3 * 2],
        'end' : [screen_width, screen_height/3 * 2]
      },
    ]

    for line in lines:
        pygame.draw.line(self.screen, self.color_game, line['start'], line['end'], width=3)
  
  def show_pos_player(self):
    width_board, height_board = self.size

    for player in self.player_pos:
      if player == 1:
        char = self.player_x
      elif player == 2:
        char = self.player_o
      char_rect = char.get_rect()
      positions = self.player_pos[player]

      for pos in positions:
        char_rect.centerx = (height_board/3) * (pos[0] + 1) - char_rect.width /2
        char_rect.centery = (width_board/3) * (pos[1] + 1) - char_rect.height /2
        self.screen.blit(char, char_rect)
  
  def check_winner(self):
    pos_win_1 = self.is_win(self.player_pos[1], "X")
    pos_win_2 = self.is_win(self.player_pos[2], "O")
    if pos_win_1 is not None or pos_win_2 is not None:
      self.cross_winner = pos_win_1 if pos_win_1 is not None else pos_win_2
    if self.winner is None and len(self.player_pos[1]) + len(self.player_pos[2]) >= 9:
      self.winner = "Draw"

  def is_win(self, player, name):
    # Check win by Row
    win_by_row = {}
    # Check win by col
    win_by_col = {}
    # Check win by diag
    win_by_diag = {
      1: [],
      2: []
    }

    for pos in player:
      # Check win by Row
      if pos[0] not in win_by_row:
        win_by_row[pos[0]] = 1
      else:
        win_by_row[pos[0]] += 1
        if win_by_row[pos[0]] == 3:
          self.winner = name
          return [(pos[0], x) for x in range(3)]

      # Check win by col
      if pos[1] not in win_by_col:
        win_by_col[pos[1]] = 1
      else:
        win_by_col[pos[1]] += 1
        if win_by_col[pos[1]] == 3:
          self.winner = name
          return [(x, pos[1]) for x in range(3)]
      
      # Check win by diag
      if pos[0] == pos[1]:
        win_by_diag[1].append(pos)
        if len(win_by_diag[1]) == 3:
          self.winner = name
          return [(x, x) for x in range(3)]
      
      pos_diag_win_2 = [(0,2), (1,1), (2,0)]
      if pos in pos_diag_win_2:
        win_by_diag[2].append(pos)
        if len(win_by_diag[2]) == 3:
          self.winner = name
          return pos_diag_win_2
    return None

  def draw_cross(self):
    if self.cross_winner is not None:
      line_1 = {
        'start': self.cell_tic_tac_toe[self.cross_winner[0]].center,
        'end' : self.cell_tic_tac_toe[self.cross_winner[1]].center
      }
      line_2 = {
        'start' : self.cell_tic_tac_toe[self.cross_winner[1]].center,
        'end' : self.cell_tic_tac_toe[self.cross_winner[2]].center
      }
      color_cross = 255, 82, 3
      pygame.draw.line(self.screen, color_cross, line_1['start'], line_1['end'], width=5)
      pygame.draw.line(self.screen, color_cross, line_2['start'], line_2['end'], width=5)


if __name__ == "__main__":
  TicTacToe()
