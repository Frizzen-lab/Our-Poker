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
  [0:2] - карты игрока
  [2:7] - карты борда
  [7:9] - значения карт игрока
  [9:14] - значения карт борда
  [14:16] - масти карт игрока
  [16:21] - масти карт борда
  [21] - позиция игрока
  [22] - деньги игрока
  [23] - большой блайнд
  [24] - стек игрока
  [25] - m % p инициатора
  [26:28] - оба пустые
  [28] - количество игроков
  [29] - число активных игроков
  [30] - стадия игры
  [31] - номер игрока который ходит
  [32] - максбет
  [33] - банк
  [34] - число оллиновых игроков
  [35:65] - префлоп (ставка)
  [65:95] - флоп (ставка)
  [95:125] - тёрн (ставка)
  [125:155] - ривер (ставка)
  [155:185] - префлоп (действие)
  [185:215] - флоп (действие)
  [215:245] - тёрн (действие)
  [245:275] - ривер (действие)
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
  [285:295] - стек игроков
  ...
'''

#  Создание таблицы 
tab2pl = np.full((10, 12), 0)

#  Количество скрытых узлов (нейронов)
hidden_size = 20000
hidden_size_hm = 600

#  Веса первой нейросети, предсказывающей действие, связывающих входной слой со скрытым
weights_01_w = 0.2 * np.random.random((300, hidden_size)) - 0.1

#  Веса первой нейросети, предсказывающей действие, связывающих скрытый слой с выходным
weights_12_w = 0.02 * np.random.random((hidden_size, 5)) - 0.01

#  Веса второй нейросети, предсказывающей количество денег, связывающих входной слой со скрытым
weights_01_hm = 0.02 * np.random.random((301, hidden_size_hm)) - 0.01

#  Веса второй нейросети, предсказывающей количество денег, связывающих скрытый слой с выходным
weights_12_hm = 0.02 * np.random.random((hidden_size_hm, 1)) - 0.01

#  Альфа-коэф (скорость) первой нейросети
alpha_w = 0.001

#  Второй нейросети
alpha_hm = 0.01

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
  
#  Функция для определения количества ставки, каким действием эта ставка является и установки ставки в нужное место
def set_bet(my_bet):
  global movies, tab2pos, tab2pl, x, pos2ind, fold_pl, not_fold, max_bet, not_raise, allin_pl, playersStep
  out = False
  if my_bet == tab2pl[x][3]:
    my_bet = 'a'
  if type(my_bet) == int:
    my_bet = my_bet
  elif my_bet in ('Fold', 'f', 'F') or my_bet == '' or my_bet == -1:
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
    
  pos = tab2pos[35 + 10 * tab2pos[30] + tab2pos[31]]
  money = tab2pl[x][3]    
    
  if type(my_bet) != str:
    mxbetprv = max_bet
    pos_bet = int(tab2pos[35 + 30 * (tab2pos[30] // 3) + tab2pos[31]] + tab2pos[45 + 30 * (tab2pos[30] // 3) + tab2pos[31]] + tab2pos[55 + 30 * (tab2pos[30] // 3) + tab2pos[31]])
    
    if x in allin_pl:
      my_bet = my_bet
      
    elif my_bet != -1:
      my_bet -= pos_bet
  
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
    playersStep += 1
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
      tab2pos[155 + 10 * tab2pos[30] + tab2pos[31]] = -1
#      rng = (265 - (25 + 10 * tab2pos[30])) // 10
#      for i in range(rng):
#        tab2pos[35 + 10 * tab2pos[30] + 10 * i + tab2pos[31]] = -1
    elif tab2pl[x][3] == 0:
      tab2pos[155 + 10 * tab2pos[30] + tab2pos[31]] = 3
#      rng = (265 - (155 + 10 * tab2pos[30])) // 10
#      for i in range(rng):
#        tab2pos[155 + 10 * tab2pos[30] + 10 * i + tab2pos[31]] = 3
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
              

#  --- НИЖЕ ИГРА        
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
  playersStep = 0
  l = 0  #  Номер первой строки для записи
  layer_0_w = np.zeros((batch_size, 300))
  layer_0_hm = np.zeros((batch_size, 301))
  w_true = np.zeros((batch_size, 5))
  hm_true = np.zeros((batch_size, 1))
  
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
    tab2pl[i][3] = 20
    #  Количество денег
    
  while (players > 1):
    #  Здесь будет начинаться каждый сет
    if flag:
      break
    tab2pos[:28] = 0
    tab2pos[29:] = 0
    
    
#    for i in range(10 - players):
#      for j in range(24):
#        tab2pos[44 + 10 * j - i] = -2 #  ОТСУТСТВУЮЩИЕ ИГРОКИ В -2

#    for i in range(5):
#      tab2pos[2 + i] = 0
#      tab2pos[9 + i] = 0
#      tab2pos[16 + i] = 0

    pos2ind = get_cards(players)  #  Получаем словарь Позиция - Индекс и раздаем карты
    for i in range (players):
      deck = []
      tab2pl[i][11] = 0
      for j in range(2):
        deck.append(tab2pl[i][j])
      for j in range(5):
        deck.append(tab2pl[i][4 + j])
      _, tab2pl[i][9], tab2pl[i][10], _, _, _, tab2pl[i][11], _, _, _ = parComb(deck)
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
    tab2pos[25] = -1
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
          if i != 0:
            d_list.append(i - 4)

        tab2pos[275], tab2pos[276], tab2pos[277], tab2pos[278], tab2pos[279], tab2pos[280], tab2pos[281], tab2pos[282], tab2pos[283], tab2pos[284] = parComb(d_list)
        
        if tab2pos[275] <= 5:
          if tab2pos[276] == 2:
            tab2pos[275] = 4
          elif tab2pos[276] == 3:
            if tab2pos[30] // 3 == 1: #  Flop
              tab2pos[275] == 7
            elif tab2pos[30] // 3 == 2: #  Turn
              tab2pos[275] = 10
        
        for i in range(10):
          tab2pos[285 + i] = tab2pl[i][3] // tab2pos[23]  #  Добавить актуальный стек всех игроков с 285 по 294 элемент

        if x == 0:
          print('________________________________________________')
          print('Позиция: ' + str(position_dict[tab2pos[21]]), end = '')
          print('  Денег: ' + str(tab2pl[x][3]))
          print('Банк: ' + str(tab2pos[33]), end = '')
          print('  Игроков: ' + str(players))
          print('До Вас: ', end = '')
          if tab2pos[30] in (0, 1, 2):
            i_bet = tab2pos[23]
          else:
            i_bet = 0
          
          for i in range(35 + 30 * (tab2pos[30] // 3), 35 + 10 * tab2pos[30] + tab2pos[31]):
            if tab2pos[i] == -1:
              print('F>', end = '')
            elif i % 10 in ignrd:
              continue
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
            print('Дро: ' + str(tab2pos[275]) + ' аутов ' + '   Комбинация: ' + str(c2w[tab2pos[276]]))
            
          print('Уже поставлено: ' + str(tab2pos[35 + 30 * (tab2pos[30] // 3) + tab2pos[31]] + tab2pos[45 + 30 * (tab2pos[30] // 3) + tab2pos[31]] + tab2pos[55 + 30 * (tab2pos[30] // 3) + tab2pos[31]]), end = ' ')
          
          print('Не хватает: ' + str(max_bet - (tab2pos[35 + 30 * (tab2pos[30] // 3) + tab2pos[31]] + tab2pos[45 + 30 * (tab2pos[30] // 3) + tab2pos[31]] + tab2pos[55 + 30 * (tab2pos[30] // 3) + tab2pos[31]])))
            
#          layer_0_w[l] = tab2pos.copy()
#          layer_1_w = tanh (np.dot(layer_0_w[l : l + 1], weights_01_w))
#          layer_2_w = softmax4one (layer_1_w.dot(weights_12_w))
#          
#          if np.argmax (layer_2_w) == 0:
#            outmove = 'Фолд'
#          elif np.argmax (layer_2_w) == 1:
#            outmove = 'Чекай'
#          elif np.argmax (layer_2_w) == 2:
#            outmove = 'Коллируй'
#          elif np.argmax (layer_2_w) == 3:
#            outmove = 'Рейзи'
#          else:
#            outmove = 'Алл Ин'
#  
#          print('ДЕЙСТВИЕ: ' + outmove + ' ', end = '')
#          
#          l2w = np.argmax(layer_2_w)
#          layer_0_hm[l] = np.hstack((tab2pos.copy(), l2w))
#          layer_1_hm = tanh (layer_0_hm[l].dot(weights_01_hm))
#          layer_2_hm = layer_1_hm.dot(weights_12_hm)
#          print('СТАВКА: ' + str(layer_2_hm[0]))
#          print('ДО ОБУЧЕНИЯ: ' + str(batch_size - l) + ' ШАГОВ')
#          print('БОТ РЕКОМЕНДУЕТ: ', botPoker(tab2pos))
          
          while True:
            if tab2pos[30] in (2, 5, 8, 11):
              answer = input('Только Coll(' + str(max_bet) + ')/Fold: ')
              if answer in ('Coll', 'Fold', 'f', 'F', 'C', 'c'):
                stb = set_bet(answer)
                if stb[0]:
                  mov_list.append(stb[1])
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
                
                if tab2pos[30] // 3 == 0 and stb[2] in (2, 3):
                  tab2pos[25] = tab2pos[31]
                
                if tab2pos[25] != -1 and stb[2] == -1 and tab2pos[31] == tab2pos[25]:
                  tab2pos[25] = -1
                break
        else:
          answer = int(botPoker(tab2pos))
            
          if answer == -1:
            answer = 'f'
              
          stb = set_bet(answer)