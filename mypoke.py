import numpy as np
import random2
from collections import Counter
import time
from comb import parComb, m_drawBoard
from showCards import show_cards
from botPoker import botPoker

#  Функция активации гиперболический тангенс
def tanh(x):
  return np.tanh(x)

#  Функция активации обратного распространения гиперболический тангенс
def tanh2deriv(output):
  return 1-(output**2)
  
#  Функция активации сигмоид
def sigmoid(x):
  return 1/(1+np.exp(-x))
  
#  Функция активации обратного распространения сигмоид
def sigmoid2deriv(output):
  return output*(1-output)

#  Функция активации мягкий максимум (для одного примера - строки)
def softmax4one(x):
  temp = np.exp (x)
  return temp / np.sum(temp, keepdims=True)
  
#  Функция активации мягкий макмимум (для примера с несколькими строками)
def softmax(x):
  temp = np.exp (x)
  return temp / np.sum(temp, axis = 1, keepdims = True)
    
#  Создание таблицы позиции (входной таблицы для нейросети) и заполнение ее нулями
tab2pos = np.full((300), 0)
'''
  Даётся объяснение каждому элементу таблицы
  ...
  [275] - дро
  [276] - комбинация
  [277] - сумма комбинации
  [278] - среднее комбинации
  [279] - карта 1 в комбинации
  [280] - карта 2 в комбинации
  [281] - кикер
  [282] - карта 1 в дро
  [283] - карта 2 в дро
  [284] - возможное дро у других
'''

#  Создание таблицы 
tab2pl = np.full((10, 12), 0)

#  Количество скрытых узлов (нейронов)
hidden_size = 2000
hidden_size_hm = 150

#  Веса первой нейросети, предсказывающей действие, связывающих входной слой со скрытым
weights_01_w = 0.2 * np.random.random((300, hidden_size)) - 0.1

#  Веса первой нейросети, предсказывающей действие, связывающих скрытый слой с выходным
weights_12_w = 0.02 * np.random.random((hidden_size, 5)) - 0.01

#  Веса второй нейросети, предсказывающей количество денег, связывающих входной слой со скрытым
weights_01_hm = 0.02 * np.random.random((301, hidden_size_hm)) - 0.01

#  Веса второй нейросети, предсказывающей количество денег, связывающих скрытый слой с выходным
weights_12_hm = 0.02 * np.random.random((hidden_size_hm, 1)) - 0.01

#  Альфа-коэф (скорость) первой нейросети
alpha_w = 0.01

#  Второй нейросети
alpha_hm = 0.1

#  Размер пакета
batch_size = 100

#  Ниже идет по порядку открытие файлов с весами и преобразование текста в числа с помощью циклов
#with open('weights_01_w.txt', 'r') as f:
#  w01w = f.readlines()
#  for i in w01w:
#    w01w = i.split()
#  for i in range(len(w01w)):
#    w01w[i] = float(w01w[i])
#  w01w = np.array(w01w)
#  weights_01_w = w01w.reshape(weights_01_w.shape)
#  
#with open('weights_12_w.txt', 'r') as f:
#  w12w = f.readlines()
#  for i in w12w:
#    w12w = i.split()
#  for i in range(len(w12w)):
#    w12w[i] = float(w12w[i])
#  w12w = np.array(w12w)
#  weights_12_w = w12w.reshape(weights_12_w.shape)
#  
#with open('weights_01_hm.txt', 'r') as f:
#  w01hm = f.readlines()
#  for i in w01hm:
#    w01hm = i.split()
#  for i in range(len(w01hm)):
#    w01hm[i] = float(w01hm[i])
#  w01hm = np.array(w01hm)
#  weights_01_hm = w01hm.reshape(weights_01_hm.shape)
#  
#with open('weights_12_hm.txt', 'r') as f:
#  w12hm = f.readlines()
#  for i in w12hm:
#    w12hm = i.split()
#  for i in range(len(w12hm)):
#    w12hm[i] = float(w12hm[i])
#  w12hm = np.array(w12hm)
#  weights_12_hm = w12hm.reshape(weights_12_hm.shape)

#  Создание списка с текстовыми ['3B', '4B', ... , '100B']
#  Пока не используется
bets = list()
for i in range(2,101):
  y = str(i)
  bets.append(y + 'B')

#  Словарь "обратного" веса (для показа комбинации пользователю)
c2w = {
0 : 'H. Card',
1 : 'Pair',
2 : 'T. Pairs',
3 : 'Trips',
4 : 'Street',
5 : 'Flash',
6 : 'Full House',
7 : 'Kare',
8 : 'Str. Flash',
9 : 'Royal Flash'
}

#  Словарь с названием позиций
position_dict = {
0 : 'UTG1',
1 : 'UTG2',
2 : 'MP1',
3 : 'MP2',
4 : 'MP3',
5 : 'HJ',
6 : 'CO',
7 : 'BU',
8 : 'SB',
9 : 'BB'
}

#  Словарь с порядком позиций (как они должны идти в обратном порядке)
players_pos = {
2 : (8, 7),
3 : (9, 8, 7),
4 : (9, 8, 7, 6),
5 : (9, 8, 7, 6, 5),
6 : (9, 8, 7, 6, 5, 4),
7 : (9, 8, 7, 6, 5, 4, 3),
8 : (9, 8, 7, 6, 5, 4, 3, 0),
9 : (9, 8, 7, 6, 5, 4, 3, 1, 0),
10 : (9, 8, 7, 6, 5, 4, 3, 2, 1, 0)
}


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
  
#  Функция для определения количества ставки, каким действием эта ставка является и установки ставки в нужное место
def set_bet(my_bet):
  global movies, tab2pos, tab2pl, x, pos2ind, fold_pl, not_fold, max_bet, not_raise, allin_pl
  out = False
  if type(my_bet) == int:
    my_bet = my_bet
  elif my_bet in ('Fold', 'f', 'F') or my_bet == '':
    my_bet = -1
    out = True
  elif my_bet in ('Coll', 'c', 'C'):
    my_bet = int(max_bet)
  elif my_bet in ('Check', 'Ch', 'ch'):
    if max_bet == 0:
      my_bet = 0
  elif my_bet in ('All in', 'A', 'a'):
    my_bet = int(tab2pl[x][3])
    if x not in allin_pl:
      allin_pl.append(x)
      tab2pos[34] += 1
  elif my_bet == 'b':
    if max_bet != 0:
      my_bet = int(3 * max_bet)
    else:
      my_bet = int(3 * tab2pos[23])
  elif len(my_bet) >= 2:
    if my_bet[-1] in ('b', 'B'):
      if my_bet[:-1].isdigit():
        if max_bet != 0:
          my_bet = int(int(my_bet[:-1]) * max_bet)
        else:
          my_bet = int(int(my_bet[:-1]) *  tab2pos[23])
  elif my_bet in ('1/3', '2/3', '1/4', '1/2', '3/4'):
    print(my_bet)
    my_bet = int((int(my_bet[0]) / int(my_bet[-1])) * tab2pos[33])
    
  elif my_bet.isdigit():
    my_bet = int(my_bet)
  
  if x not in not_fold:
    not_fold.append(x)
    tab2pos[29] += 1
    
  if type(my_bet) != str:
    mxbetprv = max_bet
    pos_bet = int(tab2pos[35 + 30 * (tab2pos[30] // 3) + tab2pos[31]] + tab2pos[45 + 30 * (tab2pos[30] // 3) + tab2pos[31]] + tab2pos[55 + 30 * (tab2pos[30] // 3) + tab2pos[31]])
    if x in allin_pl:
      my_bet = my_bet
    elif my_bet != -1:
      my_bet -= pos_bet
  
  pos = tab2pos[35 + 10 * tab2pos[30] + tab2pos[31]]
  money = tab2pl[x][3]
  
  if type(my_bet) == int:
    if my_bet >= money:
      my_bet = money
      if x not in allin_pl:
        allin_pl.append(x)
        tab2pos[34] += 1
    if (my_bet + pos_bet) >= max_bet:
      out = True
    if ((my_bet + pos_bet) < max_bet) and (my_bet == money):
      out = True
  
  if my_bet == 's_blind':
    tab2pos[35 + players - 2] = tab2pos[23] // 2
    tab2pl[pos2ind[8]][3] -= tab2pos[23] // 2
    pos = tab2pos[23] // 2
    not_fold.remove(x)
    tab2pos[29] -= 1
    tab2pos[33] += tab2pos[23] // 2
    out = True
  elif my_bet == 'b_blind':
    tab2pos[35 + players - 1] = tab2pos[23]
    if players == 2:
      tab2pl[pos2ind[8]][3] -= tab2pos[23]
      not_fold.append(pos2ind[8])
      tab2pos[29] += 1
    else:
      tab2pl[pos2ind[9]][3] -= tab2pos[23]
      not_fold.append(pos2ind[9])
      tab2pos[29] += 1
    pos = tab2pos[23]
    tab2pos[33] += tab2pos[23]
    not_fold.remove(x)
    tab2pos[29] -= 1
    out = True
  elif out:
    if my_bet == -1:
      not_fold.remove(x)
      tab2pos[29] -= 1
      if x not in fold_pl:
        fold_pl.append(x)
      pos = -1
    else:
      if (my_bet + pos_bet) > max_bet:
        not_raise = 0
        max_bet = my_bet + pos_bet
        tab2pos[32] = max_bet
      pos += my_bet
      money -= my_bet
      tab2pos[33] += my_bet
      
  if type(my_bet) != str:
    tab2pos[35 + 10 * tab2pos[30] + tab2pos[31]] = pos
    tab2pl[x][3] = money
    if pos == -1:
      rng = (265 - (25 + 10 * tab2pos[30])) // 10
      for i in range(rng):
        tab2pos[35 + 10 * tab2pos[30] + 10 * i + tab2pos[31]] = -1
    elif tab2pl[x][3] == 0:
      rng = (265 - (155 + 10 * tab2pos[30])) // 10
      for i in range(rng):
        tab2pos[155 + 10 * tab2pos[30] + 10 * i + tab2pos[31]] = 3
    elif pos == 0:
      tab2pos[155 + 10 * tab2pos[30] + tab2pos[31]] = 0
    elif (pos_bet + pos) == mxbetprv:
      tab2pos[155 + 10 * tab2pos[30] + tab2pos[31]] = 1
    elif (pos_bet + pos) > mxbetprv:
      tab2pos[155 + 10 * tab2pos[30] + tab2pos[31]] = 2
    
  return (out, pos, tab2pos[155 + 10 * tab2pos[30] + tab2pos[31]])
  
  
#  Функция раздачи карт игрокам по позициям, принимает значение - количество игроков, возвращает словарь Позиция-Индекс  
def get_cards(n):
  global tab2pos, tab2pl, players_pos, removal_rnd, num_game, players
  a_list = list()
  while (len(a_list) < ((n * 2) + 5)):
    i = random2.randint(0, 51)
    if i not in a_list:
      a_list.append(i)
  a_list = np.array(a_list)
  x = 0
  pos2ind = {}
  for i in range(players):
    for k in range(5):
      tab2pl[i][4 + k] = a_list[-5 + k]
    for j in range(2):
      tab2pl[i][j] = a_list[x]
      x += 1
    if tab2pl[i][1] > tab2pl[i][0]:
      tab2pl[i][1], tab2pl[i][0] = tab2pl[i][0], tab2pl[i][1]
    tab2pl[i][2] = players_pos[players][(i + removal_rnd + num_game) % players]
    pos2ind[tab2pl[i][2]] = i
  return pos2ind
 
flag = False

while True:
  #  Лобби, предложение зайти в игру
  if flag:
    break
  #  Счетчик для полного выхода из программы
  print()
  print('-Игра Техасский Холдем-')
  answer = input('Играем? n - для выхода\n')
  print()
  if (answer == 'n'):
    break
  num_game = 0  #  Номер игры
  l = 0  #  Номер первой строки для записи
  layer_0_w = np.zeros((batch_size, 300))
  layer_0_hm = np.zeros((batch_size, 301))
  w_true = np.zeros((batch_size, 5))
  hm_true = np.zeros((batch_size, 1))
  comb = np.full((10, 1), 'No Combination')
  my_mask = np.full((300), 0)
  my_mask[7:21] = 1
  my_mask[26] = 1
  my_mask[32] = 1
  
  while True:
    if flag:
      break
    answer = input('Сколько игроков будет за столом? от 2 до 10: ')
    if answer.isdigit():
      if int(answer) in list(range(2,11)):
        tab2pos[28] = int(answer)
        break
        
  removal_rnd = random2.randint(0,tab2pos[28])
  players = int(tab2pos[28])
  
  for i in range(players):
    tab2pl[i][3] = 200
    #  Количество денег
    
  while (players > 1):
    #  Здесь будет начинаться каждый сет
    if flag:
      break
    tab2pos[:28] = 0
    tab2pos[29:] = 0
    
    
    for i in range(10 - players):
      for j in range(24):
        tab2pos[44 + 10 * j - i] = -2 #  ОТСУТСТВУЮЩИЕ ИГРОКИ В -2
    for i in range(5):
      tab2pos[2 + i] = 0
      tab2pos[9 + i] = 0
      tab2pos[16 + i] = 0
    pos2ind = get_cards(players)  #  Получаем словарь Позиция - Индекс и раздаем карты
    for i in range (players):
      deck = []
      tab2pl[i][11] = 0
      for j in range(2):
        deck.append(tab2pl[i][j])
      for j in range(5):
        deck.append(tab2pl[i][4 + j])
      _, tab2pl[i][9], tab2pl[i][10], _, _, _, tab2pl[i][11], _, _, _ = parComb(deck)
      comb[i][0] = c2w[tab2pl[i][9]]
    print(tab2pl)
    
    movies = 0
    print('\n________________________________________________\n')
    print('\t\t','+++  НОВЫЙ СЕТ  +++')
    print('________________________________________________')
    ignrd = []
    for i in range(10 - players):
      if (10 - i) == 10:
        ignrd.append(0)
      else:
        ignrd.append(10 - i)
    x = 0
    fold_pl = list()
    not_fold = list()
    allin_pl = list()
    tab2pos[29] = len(not_fold)
    tab2pos[34] = len(allin_pl)
    not_raise = 0
    if players == 2:
      tab2pos[23] = 1
      set_bet('b_blind')
    else:
      tab2pos[23] = 2
      set_bet('s_blind')
      set_bet('b_blind')
    max_bet = int(tab2pos[23])
    tab2pos[32] = max_bet
    
    while True:
      if flag:
        break
      if (not_raise == (players-1)) or (len(not_fold) == 1 and len(fold_pl) == players - 1):
        d_list = list()
        for i in tab2pl[0][4:9]:
          d_list.append(i)
        print('Карты на столе: ' + str(show_cards(d_list)))
        if tab2pos[30] in (9, 10, 11):
          win_pl = []
          for i in range(players):
            if i not in fold_pl:
              if (len(win_pl) == 0):
                win_pl.append(i)
              elif tab2pl[i][9] > tab2pl[win_pl[0]][9]:
                win_pl = []
                win_pl.append(i)
              elif tab2pl[i][9] == tab2pl[win_pl[0]][9]:
                if tab2pl[i][10] > tab2pl[win_pl[0]][10]:
                  win_pl = []
                  win_pl.append(i)
                elif tab2pl[i][10] == tab2pl[win_pl[0]][10]:
                  if tab2pl[i][11] > tab2pl[win_pl[0]][11]:
                    win_pl = []
                    win_pl.append(i)
                  elif tab2pl[i][11] == tab2pl[win_pl[0]][11]:
                    win_pl.append(i)

          win_money = tab2pos[33] // len(win_pl)
          num_game += 1
          print('Победили игроки: ', end = '')
          for i in win_pl:
            print(str(i) + ' ', end = '')
            tab2pl[i][3] += win_money
          print()
            
          correct_pl = []
          for i in range(players):
            if tab2pl[i][3] == 0:
              correct_pl.append(i)
          
          tab2pos[28] -= len(correct_pl)
          players -= len(correct_pl)
          if len(correct_pl) > 0:
            tab4tab2pl = tab2pl.copy()
            m = 0
            m_list = list(range(10))
            for i in range(len(correct_pl)):
              m_list.remove(correct_pl[i])
            while m < len(m_list):
              tab4tab2pl[m] = tab2pl[m_list[m]]
              m += 1
            for i in range(m,10):
              for j in range(12):
                tab4tab2pl[i][j] = 0
            tab2pl = tab4tab2pl
          break
      not_raise =- 1
      mov_list = list()
      
      while True:
        if flag:
          break
        tab2pos[30] = movies // players
        tab2pos[31] = movies % players
        m_p = movies % players
        if not_raise == players:
          not_raise -= 1
        if len(not_fold) == 1 and len(fold_pl) == players - 1:
          tab2pos[30] = 10
          break
          
        if (not_raise == (players - 1)):
          if tab2pos[30] not in (9, 10, 11):
            movies = players * (3 + 3 * (tab2pos[30] // 3))
            not_raise = -1
            max_bet = 0
            tab2pos[32] = max_bet
          break
          
        if tab2pos[30] == 3 and tab2pos[31] == 0:
          t = 0
          for i in tab2pl[0][4:7]:
            tab2pos[2 + t] = i + 4
            t += 1
          tab2pos[9:12] = tab2pos[2:5] // 4
          tab2pos[16:19] = 1 + tab2pos[2:5] % 4
        elif tab2pos[30] == 6 and tab2pos[31] == 0:
          tab2pos[5] = tab2pl[0][7] + 4
          tab2pos[12] = tab2pos[5] // 4
          tab2pos[19] = 1 + tab2pos[5] % 4
        elif tab2pos[30] == 9 and tab2pos[31] == 0:
          tab2pos[6] = tab2pl[0][8] + 4
          tab2pos[13] = tab2pos[6] // 4
          tab2pos[20] = 1 + tab2pos[6] % 4
          
        j = (players * 18 - 1 - m_p) % players
        x = pos2ind[players_pos[players][j]]
        movies += 1
        not_raise += 1
        if l == batch_size:
          l = 0
          layer_0_w_c = layer_0_w.copy()
          layer_0_w_c *= my_mask
          layer_1_w = tanh (layer_0_w_c.dot(weights_01_w))
          dropout_mask = np.random.randint (2, size = layer_1_w.shape)
          layer_1_w *= dropout_mask * 2
          layer_2_w = softmax (layer_1_w.dot(weights_12_w))
          delta_2_w = (layer_2_w - w_true) / batch_size
          delta_1_w = delta_2_w.dot(weights_12_w.T) * tanh2deriv(layer_1_w)
          delta_1_w *= dropout_mask
          correct_cnt = 0
          for i in range(batch_size):
            correct_cnt += int (np.argmax(layer_2_w[i : i+1]) == np.argmax(w_true[i : i+1]))
          print('ТОЧНОСТЬ: ' + str(correct_cnt / batch_size))
          weights_12_w -= alpha_w * layer_1_w.T.dot(delta_2_w)
          weights_01_w -= alpha_w * layer_0_w_c.T.dot(delta_1_w)
          w_true = np.zeros((batch_size, 5))
          '''weights_01_w=0.02*np.random.random((275,hidden_size))-0.01
          weights_12_w=0.02*np.random.random((hidden_size,5))-0.01'''
          
          
          f = open('weights_12_w.txt', 'w')
          for i in weights_12_w:
            for j in i:
              f.write(str(j) + ' ')
          f.close()
          
          f = open('weights_01_w.txt', 'w')
          for i in weights_01_w:
            for j in i:
              f.write(str(j) + ' ')
          f.close()
          
          '''
          layer_1_hm = tanh (layer_0_hm.dot(weights_01_hm))
          dropout_mask = np.random.randint (2, size = layer_1_hm.shape)
          layer_1_hm *= dropout_mask * 2
          layer_2_hm = layer_1_hm.dot(weights_12_hm)
          delta_2_hm = (layer_2_hm - hm_true) / 100
          delta_1_hm = delta_2_hm.dot(weights_12_hm.T) * tanh2deriv(layer_1_hm)
          delta_1_hm *= dropout_mask
          weights_12_hm -= alpha_hm * layer_1_hm.T.dot(delta_2_hm)
          weights_01_hm -= alpha_hm * layer_0_hm.T.dot(delta_1_hm)
          hm_true = np.zeros((100, 1))
          
          f = open('weights_12_hm.txt', 'w')
          for i in weights_12_hm:
            for j in i:
              f.write(str(j) + ' ')
          f.close()
          
          f = open('weights_01_hm.txt', 'w')
          for i in weights_01_hm:
            for j in i:
              f.write(str(j) + ' ')
          f.close()
          '''
        
        if x in fold_pl:
          mov_list.append(-1)
          continue
        if x in allin_pl:
          continue
        if ((len(not_fold) - len(allin_pl)) == 1) and (len(fold_pl) == (players - (len(not_fold)))):
          if (players - len(fold_pl) - len(allin_pl)) == 1:
            not_raise += 1
          if not_raise == (players - len(fold_pl) - len(allin_pl)):
            continue
        
        t = 0
        for i in tab2pl[x][0:2]:
          tab2pos[0 + t] = i + 4
          t += 1
        tab2pos[7:9] = tab2pos[0:2] // 4
        tab2pos[14:16] = 1 + tab2pos[0:2] % 4
        tab2pos[21] = tab2pl[x][2]
        tab2pos[22] = tab2pl[x][3]
        tab2pos[24] = tab2pos[22] // tab2pos[23]
        
        d_list = []
        for i in tab2pos[0:7]:
          if i == 0:
            d_list.append(i)
          elif i != 0:
            d_list.append(i - 4)

        tab2pos[275], tab2pos[276], tab2pos[277], tab2pos[278], tab2pos[279], tab2pos[280], tab2pos[281], tab2pos[282], tab2pos[283], tab2pos[284] = parComb(d_list)
        
        for i in range(10):
          tab2pos[285 + i] = tab2pl[i][3] // tab2pos[23]  #  Добавить актуальный стек всех игроков с 285 по 294 элемент

        print('________________________________________________')
        print('Позиция: ' + str(position_dict[tab2pos[21]]) + '  Денег: ' +str(tab2pl[x][3]))
        print('Банк: ' + str(tab2pos[33]) + '   Игроков: ' + str(players))
        print('До Вас: ', end = '')
        if tab2pos[30] in (0, 1, 2):
          i_bet = tab2pos[23]
        else:
          i_bet = 0
        
        for i in range(35 + 30 * (tab2pos[30] // 3), 35 + 10 * tab2pos[30] + tab2pos[31]):
          if i % 10 in ignrd:
            continue
          elif tab2pos[i] == -1:
            print('F>', end = '')
          elif tab2pos[i] == 0:
            print('Ch>', end = '')
          elif tab2pos[i] > i_bet and i_bet != 0:
            print(str(tab2pos[i] // i_bet) + 'B>', end = '')
            i_bet = tab2pos[i]
          elif tab2pos[i] == tab2pos[23]:
            print('L>', end = '')
            if i_bet != tab2pos[23]:
              i_bet = tab2pos[23]
          elif tab2pos[i] > i_bet:
            print('R>', end = '')
            i_bet = tab2pos[i]
          elif tab2pos[i] == i_bet:
            print('C>', end = '')
        print('\nВаши карты: ' + str(show_cards(d_list[0:2])))
        if tab2pos[30] not in (0, 1, 2):
          print('Карты на столе: ' + str(show_cards(d_list[2:7])))
          print('Дро: ' + str(tab2pos[25]) + ' аутов ' + '   Комбинация: ' + str(c2w[tab2pos[26]]))
        print('Уже поставлено: ' + str(tab2pos[35 + 30 * (tab2pos[30] // 3) + tab2pos[31]] + tab2pos[45 + 30 * (tab2pos[30] // 3) + tab2pos[31]] + tab2pos[55 + 30 * (tab2pos[30] // 3) + tab2pos[31]]), end = ' ')
        print('Не хватает: ' + str(max_bet - (tab2pos[35 + 30 * (tab2pos[30] // 3) + tab2pos[31]] + tab2pos[45 + 30 * (tab2pos[30] // 3) + tab2pos[31]] + tab2pos[55 + 30 * (tab2pos[30] // 3) + tab2pos[31]])))
        if tab2pos[30] in (0, 1, 2):
          d_list = list(d_list[0:2])
          d_list = sorted(d_list, reverse = True)
          print(chart4hands(d_list))
          
        layer_0_w [l] = tab2pos.copy()
        layer_1_w = tanh (np.dot(layer_0_w[l : l + 1], weights_01_w))
        dropout_mask = np.random.randint (2, size = layer_1_w.shape)
        layer_1_w *= dropout_mask * 2
        layer_2_w = softmax4one (layer_1_w.dot(weights_12_w))
        if np.argmax (layer_2_w) == 0:
          outmove = 'Фолд'
        elif np.argmax (layer_2_w) == 1:
          outmove = 'Чекай'
        elif np.argmax (layer_2_w) == 2:
          outmove = 'Коллируй'
        elif np.argmax (layer_2_w) == 3:
          outmove = 'Рейзи'
        else:
          outmove = 'Алл Ин'
        print('ДЕЙСТВИЕ: ' + outmove + ' ', end = '')
        '''
        l2w = np.argmax(layer_2_w)
        layer_0_hm[l] = np.hstack((tab2pos.copy(), l2w))
        layer_1_hm = tanh (layer_0_hm[l].dot(weights_01_hm))
        dropout_mask = np.random.randint (2, size = layer_1_hm.shape)
        layer_1_hm *= dropout_mask * 2
        layer_2_hm = layer_1_hm.dot(weights_12_hm)
        print('СТАВКА: ' + str(layer_2_hm[0]))
        '''
        print('ДО ОБУЧЕНИЯ: ' + str(batch_size - l) + ' ШАГОВ')
        print('БОТ РЕКОМЕНДУЕТ: ', botPoker(tab2pos))
        
        while True:
          if tab2pos[30] in (2, 5, 8, 11):
            answer = input('Только Coll(' + str(max_bet) + ')/Fold: ')
            if answer in ('Coll', 'Fold', 'f', 'F', 'C', 'c'):
              stb = set_bet(answer)
              if stb[0]:
                mov_list.append(stb[1])
                f = open ('input_w.txt', 'a')
                for i in range (len(tab2pos)):
                  if i == len(tab2pos) - 1:
                    f.write(str(tab2pos[i]) + '\n')
                  else:
                    f.write(str(tab2pos[i]) + ' ')
                f.close()
                w_true[l][stb[2] + 1] = 1
                f = open ('w_true.txt', 'a')
                f.write(str(stb[2] + 1) + '\n')
                f.close()
                
                hm_true[l] = stb[1]
                f = open ('hm_true.txt', 'a')
                f.write(str(stb[1]) + '\n')
                f.close()
                l += 1
                
                layer_0_hm[l] = np.hstack ((tab2pos, np.array(stb[2])))
                f = open ('input_hm.txt', 'a')
                for i in range (len(tab2pos) + 1):
                  if i == len(tab2pos):
                    f.write(str(stb[2]) + '\n')
                  else:
                    f.write(str(tab2pos[i]) + ' ')
                f.close()
                break
          else:
            answer = input('Check/Coll(' + str(max_bet) + ')/Fold/3B/All in: ')
            if tab2pos[30] in (0,1,2):
              if answer not in ('1/3', '2/3', '1/4', '1/2', '3/4'):
                stb = set_bet(answer)
              else:
                stb = set_bet(0)
            else:
              stb = set_bet(answer)
            if stb[0]:
              mov_list.append(stb[1])
              w_true[l][stb[2] + 1] = 1
              hm_true[l] = stb[1]
              layer_0_hm[l] = np.hstack ((tab2pos, np.array(stb[2])))
              l += 1
              
              f = open ('input_hm.txt', 'a')
              for i in range (len(tab2pos) + 1):
                if i == len(tab2pos):
                  f.write(str(stb[2]) + '\n')
                else:
                  f.write(str(tab2pos[i]) + ' ')
              f.close()
              
              f = open ('input_w.txt', 'a')
              for i in range (len(tab2pos)):
                if i == len(tab2pos) - 1:
                  f.write(str(tab2pos[i]) + '\n')
                else:
                  f.write(str(tab2pos[i]) + ' ')
              f.close()
              
              f = open ('w_true.txt', 'a')
              f.write(str(stb[2] + 1) + '\n')
              f.close()
              
              f = open ('hm_true.txt', 'a')
              f.write(str(stb[1]) + '\n')
              f.close()
              break