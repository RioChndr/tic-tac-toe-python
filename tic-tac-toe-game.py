import sys, pygame, random

class TicTacToe:
  def __init__(self):
    pygame.init()

    self.size = width, height = 640, 320
    self.background = (224, 241, 244)
    self.color_game = (0, 55, 61)
    self.screen = pygame.display.set_mode(self.size)

    self.player_x = pygame.image.load('assets/backup/player_x.png')
    self.player_o = pygame.image.load('assets/backup/player_o.png')

    self.player_pos = {
      1: [], # x
      2: []  # o
    }
    self.current_player = self.random_first_player()
    self.winner = None
    self.is_running = True
    self.cross_winner = None

    self.size_board = self.height_board, self.width_board = 200, 200

    self.cell_tic_tac_toe = {}
    ## Create collide rectangle
    padding_left, padding_top = self.get_padding()

    char_rect = self.player_x.get_rect()
    for col in range(3):
        for row in range(3):
          centerx = padding_left + (self.height_board/3) * (row)
          centery = padding_top + (self.width_board/3) * (col)
          self.cell_tic_tac_toe[(row, col)] = pygame.Rect(centerx, centery, char_rect.width, char_rect.height)
    
    self.play_game()

  def random_first_player(self):
    # To make more random chance
    rand_num = random.randint(1,10)
    return (rand_num % 2) + 1

  def play_game(self):
    while True:
      self.screen.fill(self.background)

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:
          pos_mouse = pygame.mouse.get_pos()
          clicked_rect = [pos_rect for pos_rect in self.cell_tic_tac_toe if self.cell_tic_tac_toe[pos_rect].collidepoint(pos_mouse)]

          if len(clicked_rect) > 0:
            if self.is_running:
              next_player = 1 if self.current_player == 2 else 2

              if clicked_rect[0] not in self.player_pos[self.current_player] and clicked_rect[0] not in self.player_pos[next_player]:
                self.player_pos[self.current_player].append(clicked_rect[0])
                self.check_winner()
                self.current_player = next_player
      
      self.draw_line()
      self.show_pos_player()
      self.draw_info()
      self.draw_cross()

      if self.winner is not None:
        self.is_running = False
      pygame.display.flip()

  def get_padding(self):
    padding_top = int(self.size[1]/2 - self.height_board/2)
    padding_left = int(self.size[0]/2 - self.width_board/2)
    return (padding_left, padding_top)

  def draw_info(self):
    padding_left, padding_top = self.get_padding()

    font = pygame.font.Font('assets/backup/Poppins-Regular.ttf', 25)
    name_player = "X" if self.current_player == 1 else "O"
    info_current_player = font.render('Sekarang Giliran {}'.format(name_player), True, self.color_game)
    
    self.screen.blit(info_current_player, (padding_left, padding_top - info_current_player.get_height()))

    if self.winner is not None:
      if self.winner != "Draw":
        info_winner = font.render('Pemenangnya adalah {}'.format(self.winner), True, self.color_game)
      else:
        info_winner = font.render('Draw !!', True, self.color_game)
      self.screen.blit(info_winner, (padding_left, padding_top + self.height_board + 20))

  def draw_cross(self):
    padding_left, padding_top = self.get_padding()
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

  def draw_line(self):
    lines = [
      {
        'start': [self.width_board/3, 0],
        'end' : [self.width_board/3, self.height_board]
      },
      {
        'start': [self.width_board/3 * 2, 0],
        'end' : [self.width_board/3 * 2, self.height_board]
      },
      {
        'start': [0, self.height_board/3],
        'end' : [self.width_board, self.height_board/3]
      },
      {
        'start': [0, self.height_board/3 * 2],
        'end' : [self.width_board, self.height_board/3 * 2]
      },
      
    ]
    
    padding_left, padding_top = self.get_padding()

    for line in lines:
      line_start = [line['start'][0] + padding_left, line['start'][1] + padding_top]
      line_end = [line['end'][0] + padding_left, line['end'][1] + padding_top]
      pygame.draw.line(self.screen, self.color_game, line_start, line_end, width=3)

  def show_pos_player(self):
    padding_left, padding_top = self.get_padding()

    for player in self.player_pos:
      if player == 1:
        char = self.player_x
      elif player == 2:
        char = self.player_o
      char_rect = char.get_rect()
      positions = self.player_pos[player]

      for pos in positions:
        char_rect.centerx = padding_left + (self.height_board/3) * (pos[0] + 1) - char_rect.width /2
        char_rect.centery = padding_top + (self.width_board/3) * (pos[1] + 1) - char_rect.height /2
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

if __name__ == "__main__":
  TicTacToe()