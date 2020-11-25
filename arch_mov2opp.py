def chart4hands(a_list):
  global tab2pl, x, mov_list, m_p
  rcmd=(
  'RAISE, если RR иди ALL IN',
  'RAISE, если RR коллируй',
  'RAISE, если RR ФОЛД',
  'COLL, если RR ФОЛД',
  'RAISE, если RR с парами КОЛЛ 15-20',
  'COLL, если RR РеРейз сам',
  'RAISE/LIMP(если 3 и более лимпа)\nЕсли RR ФОЛД'
  )
  #all_Fold[0], all_FL[1], len(limp_pl)[2], limp_pl[3], len(raise_pl)[4], raise_pl[5]
  mopp = mov2opp(mov_list)
  for i in range(len(mopp[5])):
    j = (players * 18 - 1 - m_p) % players
    mopp[5][i] = players_pos[players][j]
  pos = tab2pl[x][2]
  output = 'FOLD'
  if len(a_list) == 2: 
    a,b = a_list[0] // 4, a_list[1] // 4
    c = a_list[0] % 4 == a_list[1] % 4
    
    #1 рука
    if ((a in (12, 11, 10)) and (a == b)):
      output = rcmd[0]
    #2 руки
    elif (((a == 12) and (b == 11)) or (a == b == 9)):
      if mopp[1]:
        if pos in (0, 1):
          output = rcmd[1]
        else:
          output = rcmd[0]
      elif mopp[4] > 0:
        if mopp[4] > 2:
          output = 'FOLD'
        elif mopp[4] == 2:
          if (mopp[5][0] in (6, 7, 8)) and (mopp[5][1] in (6, 7, 8)):
            if pos == 9:
              output = rcmd[3]  
          elif (mopp[5][0] in (0, 1, 2, 3, 4, 5)) and (mopp[5][1] in (0, 1, 2, 3, 4, 5)):
            if pos in (8, 9):
              output = rcmd[0]
          else:
            if pos in (8, 9):
              output = rcmd[3]
        elif mopp[4] == 1:
          for i in mopp[5]:
            if i in (list(range(5))):
              if tab2pl[x][3] in (list(range(5))):
                output = rcmd[2]
              else:
                output = rcmd[3]
            elif i in (list(range(5, 10))):
              if tab2pl[x][3] in (6, 7, 8, 9):
                output = rcmd[0]
              else:
                output = 'FOLD'
    #3 руки
    elif ((a == 12 and b == 10) or (a == b == 8) or (a == b == 7)):
      if mopp[1]:
        if pos in (8, 9):
          output = rcmd[0]
        else:
          output = rcmd[4]
      elif mopp[4] > 1:
        output = 'FOLD'
      elif mopp[4] == 1:
        if mopp[5][0] in (0, 1, 2, 3, 4):
          if pos > 1:
            output = rcmd[3]
        elif mopp[5][0] in (5, 6):
          if pos > 5:
            output = rcmd[2]
        elif mopp[5][0] in (7, 8):
          output = rcmd[0]
    #4 руки
    elif ((a == b == 6) or (a == b == 5)):
      if mopp[1]:
        output = rcmd[4]
      elif mopp[2] > 1:
        if pos > 1:
          output = rcmd[3]
      elif mopp[4] > 1:
        output = 'FOLD'
      elif mopp[4] == 1:
        if mopp[5][0] in (list(range(7))):
          output = rcmd[5]
        elif mopp[5][0] in (7, 8):
          output = rcmd[2]
    #5 руки
    elif ((a == b == 4) or (a == b == 3) or (a == b == 2) or (a == b == 1) or (a == b == 0)):
      if mopp[0]:
        if pos in (0, 1, 2, 3, 4):
          output = rcmd[3]
        else:
          output = rcmd[4]
      elif mopp[2] > 0:
        if pos != 9:
          output = rcmd[3]
      elif mopp[4] == 1:
        if pos in (5, 6, 7, 8, 9):
          output = rcmd[5]
    #6 руки
    elif (((a == 12) and (b == 9)) or ((a == 12) and (b == 8) and c) or ((a == 11) and (b == 10) and c)):
      if mopp[1]:
        if pos in (2, 3, 4):
          output = rcmd[2]
        elif pos in (5, 6, 9):
          output = rcmd[6]
        elif pos in (7, 8):
          output = rcmd[1]
      elif mopp[4] == 1:
        if mopp[5][0] in (2, 3, 4, 5):
          if pos in (6, 7, 8, 9):
            output = rcmd[3]
        elif mopp[5][0] in (6, 7, 8):
          if pos > 6:
            output = rcmd[2]
    #7 руки
    elif ((a == 12 and b == 8) or (a == 12 and b == 7 and c) or (a == 11 and b == 9 and c) or (a == 11 and b == 10)):
      if mopp[1]:
        if pos > 4:
          output = rcmd[6]
      elif mopp[4] == 1:
        if mopp[5][0] in (6, 7, 8):
          if pos > 6:
            output = rcmd[3]
    #8 руки
    elif ((a == 12 and b == 7) or (a == 11 and b == 9) or (a == 12 and b == 6 and c) or (a == 12 and b == 5 and c) or (a == 12 and b == 4 and c) or (a == 12 and b == 3 and c) or (a == 12 and b == 1 and c) or (a == 12 and b == 0 and c) or (a == 11 and b == 8 and c) or (a == 11 and b == 7 and c) or (a == 10 and b == 9) or (a == 10 and b == 8 and c) or (a == 9 and b == 8) or (a == 8 and b == 7) or (a == 7 and b == 6) or (a == 12 and b == 2 and c)):
      if mopp[1]:
        if pos > 5:
          output = rcmd[2]
      elif mopp[2] > 0:
        if pos in (6, 7, 8):
          output = rcmd[3]
      elif 8 in mopp[3]:
        output = rcmd[2]
      elif mopp[4] == 1:
        if mopp[5][0] in (6, 7, 8):
          if pos > 6:
            output = rcmd[3]
    #9 руки
    elif ((a == 12 and b == 6) or (a == 12 and b == 5) or (a == 11 and b == 7) or (a == 10 and b == 8) or (a == 9 and b == 8) or (a == 8 and b == 7) or (a == 11 and b == 6 and c) or (a == 10 and b == 7 and c) or (a == 9 and b == 7 and c) or (a == 9 and b == 6 and c) or (a == 8 and b == 6 and c) or (a == 7 and b == 5 and c) or (a == 6 and b == 5) or (a == 5 and b == 4) or (a == 4 and b == 3)):
      if mopp[0]:
        if pos > 6:
          output = rcmd[2]
      elif mopp[2] > 0:
        if pos in (7, 8):
          output = rcmd[3]
      elif 8 in mopp[3]:
        output = rcmd[2]
      elif mopp[4] == 1:
        if mopp[5][0] in (7, 8):
          if pos in (8, 9):
            output = rcmd[3]
    else:
      output = 'FOLD'
    
  else:
    output = 'Это не префлоп'
        
  return output
  
def mov2opp(a_list):
  global j, x, tab2pos, players_pos
  bbet = tab2pos[23]
  all_Fold = True
  all_FL = True
  raise_pl = list()
  limp_pl = list()
  for i in a_list:
    if i == bbet:
      all_Fold = False
      limp_pl.append(j)
    elif i > bbet:
      bbet = i
      all_Fold = False
      all_FL = False
      raise_pl.append(j)
  mop = [all_Fold, all_FL, len(limp_pl), limp_pl, len(raise_pl), raise_pl]
  return mop