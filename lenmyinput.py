f = open ('input_w.txt', 'r')
i_w = f.readlines()
f.close()

f = open ('w_true.txt', 'r')
t_w = f.readlines()
f.close()

print(len(i_w))
print(len(t_w))