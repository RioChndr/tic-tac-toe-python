import os

template = """
 [0, 0] | [0, 1] | [0, 2]
---+---+---
 [1, 0] | [1, 1] | [1, 2]
---+---+---
 [2, 0] | [2, 1] | [2, 2]
"""

player_1 = [] # X
player_2 = [] # O
current_player = 1
winner = None

def check_winner_old(player, name):
  global winner

  player_olah = sorted(player) # to return
  
  cell = 0
  win_by_row = []
  win_by_col = []
  win_by_diag_1 = []
  win_by_diag_2 = []
  
  for kolom in range(3):
    for baris in range(3):
      cell += 1
      if cell in player_olah:
        # Check baris
        if baris == 0:
          win_by_row.append(cell)
        if len(win_by_row) > 0:
          if win_by_row[-1] + 1 == cell:
            win_by_row.append(cell)
          else:
            win_by_row = []
          if len(win_by_row) == 3:
            winner = name
            return True

        # Check Kolom
        if kolom == 0:
          win_by_col.append(cell)
        if len(win_by_col) > 0:
          if win_by_col[-1] + 3 == cell:
            win_by_col.append(cell)
          else:
            win_by_col = []
          if len(win_by_col) == 3:
            winner = name
            return True

        # Check Diagonal
        if (kolom == 0 and baris == 0):
          win_by_diag_1.append(cell)
        if len(win_by_diag_1) > 0:
          if win_by_diag_1[-1] + 4 == cell:
            win_by_diag_1.append(cell)
          else:
            win_by_diag_1 = []
          if len(win_by_diag_1) == 3:
            winner = name
            return True
        
        if (kolom == 0 and baris == 2):
          win_by_diag_2.append(cell)
        if len(win_by_diag_2) > 0:
          if win_by_diag_2[-1] + 2 == cell:
            win_by_diag_2.append(cell)
          else:
            win_by_diag_2 = []
          if len(win_by_diag_2) == 3:
            winner = name
            return True

def check_winner(player, name):
  global winner

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
        winner = name
        return True

    # Check win by col
    if pos[1] not in win_by_col:
      win_by_col[pos[1]] = 1
    else:
      win_by_col[pos[1]] += 1
      if win_by_col[pos[1]] == 3:
        winner = name
        return True
    
    # Check win by diag
    if pos[0] == pos[1]:
      win_by_diag[1].append(pos)
      if len(win_by_diag[1]) == 3:
        winner = name
        return True
    
    pos_diag_win_2 = [[0,2], [1,1], [2,0]]
    if pos in pos_diag_win_2:
      win_by_diag[2].append(pos)
      if len(win_by_diag[2]) == 3:
        winner = name
        return True


def loop(err = None):
  global template
  global player_1
  global player_2
  global current_player
  global winner
  os.system("cls") # clear screen, "clear" for linux
  check_winner(player_1, "X")
  check_winner(player_2, "O")

  
  if err is not None:
    print(err)
  for pos_1 in player_1:
    template = template.replace(str(pos_1), "X")
  for pos_2 in player_2:
    template = template.replace(str(pos_2), "O")
  if current_player == 1:
    message = "Player X masukkan posisi : "
  elif current_player == 2:
    message = "Player O masukkan posisi : "
  
  # remove number
  new_template = template
  # Discomment this to remove position information
  #  for col in range(3):
  #   for row in range(3):
  #     new_template = new_template.replace(str([col, row]), " ")
  
  # Check is draw
  if len(player_1) + len(player_2) == 9:
    message = "Game over, DRAW !!"
    print(new_template)
    print(message)
    exit()
  if winner is not None:
    message = "Game Over, pemenangnya adalah " + winner
    print(new_template)
    print(message)  
    exit()
  else:
    print(new_template)
    print("Contoh Input : 0 1 untuk kolom 0 baris 1, (pilih 0-2)")
    print(message)
    new_pos = input()
  
  # Change "0 1" to ['0', '1']
  new_pos = new_pos.split()
  if len(new_pos) is not 2:
    loop("Input tidak valid")
    return False
  new_pos[0] = int(new_pos[0])
  new_pos[1] = int(new_pos[1])
  if new_pos[0] not in range(3) or new_pos[1] not in range(3):
    loop("Input hanya diterima 0-2 saja")
    return False
    
  if new_pos in player_1 or new_pos in player_2:
    loop("posisi {} tidak tersedia".format(new_pos))
    return False

  if current_player == 1:
    player_1.append(new_pos)
    current_player = 2
  elif current_player == 2:
    player_2.append(new_pos)
    current_player = 1
  loop()
  return False


loop()