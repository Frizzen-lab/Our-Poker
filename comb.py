from collections import Counter

#  Функция для удаления дубликатов
def double_del (a_list: list, b_list: list):
  '''
    Данная функция принимает два аргумента - списка, первый из которых содержит значения карт, а второй - масти. Длина обоих списков одинаковая.
    Например у нас есть следующие карты:
    - 6 пик
    - 7 черви
    - 7 крести
    - 7 пик
    - 8 пик
    - 9 пик
    Значит подается два списка:
      [6, 7, 7, 7, 8, 9]
      [3, 0, 2, 3, 3, 3]
    Как нам понять что перед нами СтритФлеш-дро? 
    Очевидно, что одним из вариантов будет найти разницу между каждыми двумя картами. Поэтому первым делом мы сортируем список с картами (в примере список уже представлен отсортированным).
    А для того, чтобы найти именно разницу между уникальными значениями, без повторяющихся карт, мы должны удалить дубликаты.
    Кроме того, нужно учесть, что в некоторых вариантах есть флеш-дро или флеш (это означает то, что дубликат со значением масти, которая повторяется 4 или более раз не должен быть удален).
    Таким образом те 2 списка, которые указаны в текущей документации выше, должны быть преобразованы в 2 других списка БЕЗ ОДИНАКОВЫХ ЗНАЧЕНИЙ, СОХРАНЯЯ ПОПУЛЯРНУЮ МАСТЬ:
      [6, 7, 8, 9]
      [3, 3, 3, 3]
    Были удалены две семерки с мастями черви и крести, а популярная масть (пики) сохранена.
  '''
  
  #  Выберем переменную i для начала отсчета (первый элемент списка всегда 0)
  i = 0
  
  #  Ниже переменная для окончания отсчета, она должна быть на единицу меньше, чем длина списка, так как сравниваться будут 2 близлежащих значения, а последний элемент сранивать больше не с чем
  x = len(a_list) - 1
  
  #  Ниже мы используем счетчик Counter, который подсчитывает количество мастей и сразу же используем его метод most_common (что переводится наиболее популярные). Записываем их в переменную mcmc
  mcmc = Counter(b_list).most_common(1)
  
  #  Далее найдем самую популярную масть. Необходимо помнить, что метод most_common возвращает самые повторяющиеся значения самыми первыми, однако так как аргументом к этому методу мы написали единицу, то метод оставит всего одно - самое популярное значение. Его то мы и запишем в эту же самую переменную mcmc
  mcmc = mcmc[0][1]
  while i < x:
    if a_list[i] == a_list[i+1]: #  Если текущий элемент равен рядомстоящему
      if b_list[i] == mcmc: #  Если текущий элемент с популярной мастью, то удалить рядомстоящий
        del a_list[i+1]
        del b_list[i+1]
      else: #  Иначе удалить текущий
        del a_list[i]
        del b_list[i]
      x -= 1 #  После удаления нужно уменьшить и окончание цикла, так как длина списков уменьшилась на 1 элемент
      continue #  Увеличивать i, когда произошло удаление не стоит, тогда возникает проблема
    i += 1 #  Если удалений не произошло, то увеличиваем шаг
  return (a_list, b_list, len(a_list))
  
#  Функция, считающая количество аутов для определенного дро
def draw (a_list: list, b_list: list):
  '''
    Данная функция принимает два аргумента - списка, первый из которых содержит значения карт, а второй - масти. Списки должны быть отсортированны и к ним должна быть применена функция удаления дубликатов. Длина обоих списков одинаковая, а так же не должна быть ниже 4, так как минимально-возможное значение любого дро может быть только при наличии 4х карт. Так же хоть функция и называется дро, однако она ищет только дро-последовательности (а именно карты, которые представляют стрит-комбинации). Флеш-дро при этом ищется совсем по-другому и это единственное исключение из правил будет рассмотрено подробнее ниже.
    Функция работает следующим образом:
    Чтобы найти стрит-последовательность мы должны найти разницу между значениями близлежащих карт. Таким образом, если на вход подаются карты: 6, 7, 8, 10; то разницей между близлежащими картами будет: 1, 1, 2 (7 минус 6, 8 минус 7, 10 минус 8).
    Как видно из примера выше подается список из 4х карт, а высчитывается список из 3х карт (на один меньше). Но и тут бывает исключение.
    Рассмотрим случай, когда возможен самый минимальный стрит [A, 2, 3, 4, 5]. А точнее любая его модификация без одной карты (дро) [A, 2, 4, 5]. Так как список подается отсортированным, то в программном виде он подается в эту функцию в следующем виде: [2, 4, 5, 12]. Далее проверяется условие - если последняя карта туз и первая двойка, то добавить в список вычислений разницу 1: [1]
    После этого добавляются стандартная разница между 2 и 4, 4 и 5, 5 и 12 - [1, 2, 1, 7]  
    Так мы получили вычисляемый список длины такой же, как входной. Такое редкое свойство бывает только в случаях, когда первая карта 2 или 3, а последняя Туз.
    Следующий момент, который мы не должны упустить из виду, это одинаковые масти. Если мы нашли стрит-дро, каким образом мы определяем являются ли эти карты дополнительно одинаковой масти (СтритФлеш-дро)? Мы смотрим на одинаковость мастей тех карт, которые стоят рядом друг с другом. Как отобразить это для машины? Если две рядомстоящие карты похожи, то мы должны добавить единицу, а если они различны, то ноль. По сути нас не интересуют сами масти как таковые, нас интересует их похожесть (одномастые/разномастные).
    Таким образом (пример) нам подается список: [крести, крести, черви, крести] на выходе мы получаем: [1, 0, 0] (крести похожа с крести, крести НЕ похожа с черви, черви НЕ похожа с крести). Опять замечание: список вычислений всегда на единицу меньше входного (кроме случая, описанного выше).
    Для более обширного понимания рассмотрим, как программа "видит" наши карты на входе и вычисляет промежуточные списки (список разности и список похожести):
    
    1 пример:
      Значения карт: [0, 2, 3, 5, 7]
      Масти карт:  [3, 2, 0, 0, 0] 
      #  пики, крести, черви, черви, черви
      1 список выч.:  [2, 1, 2, 2]
      2 список выч.:  [0, 0, 1, 1]
    
    2 пример:
      Значения карт: [0, 2, 3, 5, 12]
      Масти карт:  [3, 2, 0, 0, 0] 
      #  пики, крести, черви, черви, черви
      1 список выч.:  [1, 2, 1, 2, 7]
      2 список выч.:  [0, 0, 0, 1, 1]
      
    3 пример:
      Значения карт: [5, 6, 7, 8, 11]
      Масти карт:  [0, 0, 2, 0, 0] 
      #  черви, черви, крести, черви, черви
      1 список выч.:  [1, 1, 1, 3]
      2 список выч.:  [1, 0, 0, 1]
      
    Как видно из последнего примера, независимо от того, что мастей черви во входном списке аж 4 штуки, во 2 списке вычислений отображены единицы, отражающие похожесть ТОЛЬКО близлежащих карт.
    А первые два примера показывают разницу наличия/отсутствия комбинации с двойкой и тузом (двойка представлена как 0, а туз как 12).
    
    После того, как вычислены оба списка, мы начинаем искать сумму трех значений ПЕРВОГО списка вычислений (valueAnswer), перебирая эти суммы по мере прохождения по самому списку (круглыми скобками выделено прохождение по списку):
      [(1, 2, 1), 4, 2] #  Сумма 4
      [1, (2, 1, 4), 2] #  Сумма 7
      [1, 2, (1, 4, 2)] #  Сумма 7
    Параллельно таким же образом проходится 2 список вычислений (markAnswer).
    Почему ищется сумма именно трех значений? Потому что три значения полностью отражают зависимость(!) четырех близлежащих карт.
    Итак для того, чтобы определить любое стрит-дро, нам нужно, чтобы сумма трёх значений ПЕРВОГО списка вычислений (valueAnswer), идущих подряд была равна трем или четырём. 
    Если мы нашли 4, то это стрит-дро с дыркой (4 аута), а если 3, то это линейный стрит-дро (8 аутов, если этот стрит-дро не [0,1,2,3] или [9,10,11,12]).
  '''
  valueAnswer = list() #  1 список вычислений
  markAnswer = list() #  2 список вычислений
  removal = 3
  programDraw = 'NoDRAW'
  
  if a_list[0] == 0:
    if a_list[-1] == 12:
      if b_list[0] == b_list[-1]:
        valueAnswer.append(1)
        markAnswer.append(1)
      else:
        valueAnswer.append(1)
        markAnswer.append(0)
      removal -= 1
  elif a_list[0] == 1:
    if a_list[-1] == 12:
      if b_list[0] == b_list[-1]:
        valueAnswer.append(2)
        markAnswer.append(1)
      else:
        valueAnswer.append(2)
        markAnswer.append(0)
      removal -= 1

  for i in range(len(a_list)-1):
    valueAnswer.append(a_list[i+1]-a_list[i])
    if b_list[i+1] == b_list[i]:
      markAnswer.append(1)
    else:
      markAnswer.append(0)
  
  for i in range(len(valueAnswer)-2):
    sumValue3 = sum(valueAnswer[i:i+3])
    sumMark3 = sum(markAnswer[i:i+3])
    if (sumValue3 == 4):
      if (sumMark3 == 3):
        if (a_list[i + removal] == 12):
          programDraw = 'RFDH'
        else:
          programDraw = 'SFDH'
      else:
        programDraw = 'SDH'
    elif (sumValue3 == 3):
      if (sumMark3 == 3):
        if ((a_list[i] == 0) and (a_list[-1] == 12)):
          programDraw = 'SFDHL'
        elif (a_list[i + removal] == 12):
          programDraw = 'RFDHH'
        else:
          programDraw = 'SFDL'
      else:
        programDraw = 'SDL'
    
  return programDraw
      
def queue (a_list, b_list):
  valueAnswer = list()
  markAnswer = list()
  queueOutput = 'H. Card'
  queueSum = 0
  if a_list[0] == 0:
    if a_list[-1] == 12:
      if b_list[0] == b_list[-1]:
        valueAnswer.append(1)
        markAnswer.append(1)
      else:
        valueAnswer.append(1)
        markAnswer.append(0)
  elif a_list[0] == 1:
    if a_list[-1] == 12:
      if b_list[0] == b_list[-1]:
        valueAnswer.append(2)
        markAnswer.append(1)
      else:
        valueAnswer.append(2)
        markAnswer.append(0)

  for i in range(len(a_list)-1):
    valueAnswer.append(a_list[i+1]-a_list[i])
    if b_list[i+1] == b_list[i]:
      markAnswer.append(1)
    else:
      markAnswer.append(0)

  for i in range(len(valueAnswer)-3):
    sumValue4 = sum(valueAnswer[i:i+4])
    sumMark4 = sum(markAnswer[i:i+4])
    if (sumValue4 == 4):
      if (sumMark4 == 4):
        if (a_list[i+3] == 12):
          queueOutput = 'Royal Flash'
        else:
          queueOutput = 'Str. Flash'
          queueSum = 0
          queueSum = sum(a_list[i:i+5])
      else:
        queueOutput = 'Street'
        queueSum = 0
        queueSum = sum(a_list[i:i+5])
    
  return (queueOutput, queueSum)

def combinations (a_list): 
  #  Функция, вычисляющая комбинации
  #  Словарь с обозначением "веса" комбинаций:
  #  Как трипс всегда больше пары, так и 3 всегда больше 1
  
  weight_comb = {
  'H. Card' : 0,
  'Pair' : 1,
  'T. Pairs' : 2,
  'Trips' : 3,
  'Street' : 4,
  'Flash' : 5,
  'Full House' : 6,
  'Kare' : 7,
  'Str. Flash' : 8,
  'Royal Flash' : 9
  }
  
  meanComb = 0
  kicker = -1
  a_list = sorted(a_list) #  Сортирует входящий список
  draw_dict = {
    'NoDRAW' : 0,
    'RFDH' : 9,
    'SFDH' : 12,
    'SDH' : 4,
    'SFDHL' : 9,
    'RFDHH' : 9,
    'SDL' : 8,
    'Flash Draw' : 9,
    'SFDL' : 15
  } #Словарь со значениями дро
  values = list()
  marks = list()
  for i in a_list:
    values.append(i // 4) #добавляем целочисленное деление на 4 (как значение карты)
    marks.append(i % 4) #добавляем остаток от деления на 4 (как обозначение масти)
  mark_cnt = Counter(marks) #подсчитывает количество одинаковых значений
  value_cnt = Counter(values) #подсчитывает количество одинаковых мастей
  valueCommon = value_cnt.most_common() #записывает 2 самых частых значения в переменную valueCommon
  markCommon = mark_cnt.most_common() #записывает 2 самых частых масти в переменную markCommon
  outputComb = 'H. Card'
  outputDraw = 'NoDRAW'
  sumDeck = 0
  if (valueCommon[0][1] == 2):
    outputComb = 'Pair'
    sumDeck = 0
    sumDeck = valueCommon[0][0]
    meanComb = 0
    meanComb = valueCommon[0][0]
    try:
      if (valueCommon[1][1] == 2):
        outputComb = 'T. Pairs'
        sumDeck = valueCommon[0][0] + valueCommon[1][0]
        meanComb = 0
        meanComb = (valueCommon[0][0] + valueCommon[1][0]) / 2
    except:
      pass
  if (valueCommon[0][1] == 3):
    outputComb = 'Trips'
    sumDeck = 0
    sumDeck = valueCommon[0][0]
    meanComb = 0
    meanComb = valueCommon[0][0]
  if (markCommon[0][1] >= 5):
    outputComb = 'Flash'
    sumDeck = 0
    meanComb = 0
    i = 0
    for j in range(len(a_list)-1, 0, -1):
      if i == 5:
        break
      elif a_list[j] % 4 == markCommon[0][0]:
        i += 1
        sumDeck += a_list[j] // 4
      meanComb = sumDeck / 5
        
  try:
    if ((valueCommon[0][1] == 3) and (valueCommon[1][1] == 2)):
      outputComb = 'Full House'
      sumDeck = 0
      sumDeck = valueCommon[0][0] * 3
      meanComb = 0
      meanComb = sumDeck / 5
  except:
    pass
  
  if (valueCommon[0][1] == 4):
    outputComb = 'Kare'
    sumDeck = 0
    sumDeck = valueCommon[0][0]
    
  if (markCommon[0][1] >= 4):
    outputDraw = 'Flash Draw'
  
  a,b,c = double_del(values,marks)
    
  if (c > 3):
    testDraw = draw(a,b)
    if (testDraw in ('SDH', 'SDL')):
      if (outputDraw != 'Flash Draw'):
        outputDraw = testDraw
    elif (testDraw in ('RFDH', 'SFDH', 'SFDHL', 'RFDHH', 'SFDL')):
      outputDraw = testDraw
    
  if (c > 4):
    testQueue = queue(a,b)
    if testQueue[0] == 'Street':
      if (outputComb not in ('Kare', 'Full House', 'Flash')):
        outputComb = testQueue[0]
        sumDeck = 0
        sumDeck = testQueue[1]
        meanComb = 0
        meanComb = sumDeck / 5
    elif testQueue[0] in ('Royal Flash', 'Str. Flash'):
      outputComb = testQueue[0]
      sumDeck = 0
      sumDeck = testQueue[1]
      meanComb = 0
      meanComb = sumDeck / 5
      
    if weight_comb[outputComb] in (0, 1, 2, 3):
      for i in range(len(valueCommon) - 1, -1, -1):
        if valueCommon[i][1] == 1:
          kicker = valueCommon[i][0]
          break
        
  return (draw_dict[outputDraw], weight_comb[outputComb], sumDeck, meanComb, kicker)
  
def m_drawBoard (a_list: list, b_list: list):
  valueAnswer = list() #  1 список вычислений
  markAnswer = list() #  2 список вычислений
  removal = 2
  programDraw = 0
  
  if a_list[0] == 0:
    if a_list[-1] == 12:
      if b_list[0] == b_list[-1]:
        valueAnswer.append(1)
        markAnswer.append(1)
      else:
        valueAnswer.append(1)
        markAnswer.append(0)
      removal -= 1
  elif a_list[0] == 1:
    if a_list[-1] == 12:
      if b_list[0] == b_list[-1]:
        valueAnswer.append(2)
        markAnswer.append(1)
      else:
        valueAnswer.append(2)
        markAnswer.append(0)
      removal -= 1

  for i in range(len(a_list)-1):
    valueAnswer.append(a_list[i+1]-a_list[i])
    if b_list[i+1] == b_list[i]:
      markAnswer.append(1)
    else:
      markAnswer.append(0)
  
  for i in range(len(valueAnswer)-1):
    sumValue2 = sum(valueAnswer[i:i+2])
    sumMark2 = sum(markAnswer[i:i+2])
    if (sumValue2 == 2):
      if (sumMark2 == 2):
        if ((a_list[i] == 0) and (a_list[-1] == 12)):
          programDraw = 13
        elif (a_list[i + removal] == 12):
          programDraw = 12
        else:
          programDraw = 15
      else:
        programDraw = 8
    elif (sumValue2 == 3):
      if (sumMark2 == 2):
        if (((a_list[i] == 0) or (a_list[i] == 1)) and (a_list[-1] == 12)):
          programDraw = 9
        elif (a_list[i + removal] == 12):
          programDraw = 9
        else:
          programDraw = 11
      else:
        programDraw = 6
    elif (sumValue2 == 4):
      if (sumMark2 == 2):
        if (((a_list[i] == 0) or (a_list[i] == 1)) and (a_list[-1] == 12)):
          programDraw = 7
        elif (a_list[i + removal] == 12):
          programDraw = 7
        else:
          programDraw = 10
      else:
        programDraw = 5
  
  bCnt = Counter(b_list).most_common(1)
  if bCnt[0][1] > 2:
    if programDraw < 9:
      programDraw = 9
      
  return programDraw
  
def parComb(a_list):
  pocketCards = list()
  boardCards = list()
  for i in range(2):
    pocketCards.append(a_list[i]) #  Карманные карты
  for i in range(5):
    boardCards.append(a_list[2+i]) #  Карты на борде
  card1, card2, card1draw, card2draw, kicker = (0, 0, 0, 0, 0) #  Переменные для определения карт, участвующих в комбинациях и дро
  
  drawBoard, combBoard, sumBoard, meanBoard, kickerBoard = combinations(boardCards) #  Определение дро, комбинации, суммы и среднего на борде
  
  listOne, listTwo = list(), list()
  for i in boardCards:
    listOne.append(i // 4)
    listTwo.append(i % 4)
  mDrBrd = m_drawBoard(listOne, listTwo)
  
  boardCards.append(pocketCards[0]) #  Добавление одной карты к списку карт борда
  
  draw1card, comb1card, sum1card, mean1card, kicker1card = combinations(boardCards) #  Определение дро, комбинации,суммы и среднего с первой картой
  
  del boardCards[-1] #  Удаление добавленной карты
  boardCards.append(pocketCards[1]) #  Добавление второй карты
  
  draw2card, comb2card, sum2card, mean2card, kicker2card = combinations(boardCards) #  Определение дро, комбинации, суммы и среднего со второй картой
  
  drawFull, combFull, sumFull, meanFull, kickerFull = combinations(a_list) #  Определение дро, комбинации, суммы и среднего с обеими картами
  
  #  --- Ниже вычисление если с первой картой больше, чем на борде И(!) больше, чем со второй
  if comb1card > combBoard and comb1card > comb2card:
    card1 = pocketCards[0]
    if pocketCards[1] >= kickerFull:
      kicker = pocketCards[1]
    
  #  --- Ниже вычисление если со второй картой больше, чем на борде И(!) больше, чем с первой. Использован блок if,а не elif, потому что условия взаимоисключающие
  if comb2card > combBoard and comb2card > comb1card:
    card2 = pocketCards[1]
    if pocketCards[0] >= kickerFull:
      kicker = pocketCards[0]
    
  #  --- Ниже вычисление если полная больше, чем на борде И(!) больше, чем с первой И(!) больше, чем со второй. Использован блок if,а не elif, потому что это условие поглощает первые два
  if combFull > combBoard and combFull > comb1card and combFull > comb2card:
    card1 = pocketCards[0]
    card2 = pocketCards[1]
    kicker = -1
  
  #  --- Ниже аналогичная ситуация для определения карт, участвующих в дро
  if draw1card > drawBoard and draw1card > draw2card:
    card1draw = pocketCards[0]
    
  if draw2card > drawBoard and draw2card > draw1card:
    card2draw = pocketCards[1]
    
  if drawFull > drawBoard and drawFull > draw1card and drawFull > draw2card:
    card1draw = pocketCards[0]
    card2draw = pocketCards[1]
    
  if kicker == -1:
    kicker = -8
  
  
  
  return drawFull, combFull, sumFull, meanFull, card1 + 4, card2 + 4, (kicker + 4) // 4, card1draw + 4, card2draw + 4, mDrBrd