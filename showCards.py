

def show_cards(a_list):
  a_list = sorted(a_list)
  
  mark_dict = {
  0 : '\u2665',
  1 : '\u2666',
  2 : '\u2663',
  3 : '\u2660'
  }
  
  val_dict = {
  2 : '2',
  3 : '3',
  4 : '4',
  5 : '5',
  6 : '6',
  7 : '7',
  8 : '8',
  9 : '9',
  10 : 'T',
  11 : 'J',
  12 : 'Q',
  13 : 'K',
  14 : 'A'
  }
  b_list = []
  for i in range(len(a_list)):
    if i not in (0, 1):
      if a_list[i] == 0:
        continue
    i = a_list[i]
    b_list.append(val_dict[(i // 4) + 2] + mark_dict[i % 4])
  return b_list
  