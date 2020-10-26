import numpy as np
import time

def tanh(x):
	return np.tanh(x)
	
def tanh2deriv(output):
	return 1-(output**2)
	
def sigmoid(x):
	return 1/(1+np.exp(-x))
	
def sigmoid2deriv(output):
	return output*(1-output)
	
def softmax1(x):
	temp = np.exp (x)
	return temp / np.sum(temp, keepdims=True)
	
def softmax(x):
	temp = np.exp (x)
	return temp / np.sum(temp, axis = 1, keepdims = True)

batch_size = 100
hidden_size = 2000
alpha_w = 0.001
sizen = 33000
sizeEnd = 35000
'''weights_01_hm=0.02*np.random.random((276,hidden_size))-0.01
weights_12_hm=0.02*np.random.random((hidden_size,1))-0.01
alpha_hm = 0.1'''
my_mask = np.full((275), 0)
my_mask[7:21] = 1
my_mask[26] = 1
my_mask[32] = 1

f = open ('input_w.txt', 'r')
i_w = f.readlines()
f.close()

f = open ('w_true.txt', 'r')
t_w = f.readlines()
f.close()

for i in range(len(i_w)):
	i_w[i] = i_w[i].split()
	for j in range(len(i_w[i])):
		i_w[i][j] = float(i_w[i][j])

for i in range(len(t_w)):
	t_w[i] = int(t_w[i])
	
i_train = i_w[0 : sizen]
i_train = np.array(i_train)
t_train = t_w[0 : sizen]

i_test = i_w[sizen : sizeEnd]
i_test = np.array(i_test)
t_test = t_w[sizen : sizeEnd]

t_1_train = np.full((len(t_train), 5), 0)
for i in range(len(t_train)):
	t_1_train[i][t_train[i]] = 1
t_train = t_1_train.copy()

t_1_train = np.full((len(t_test), 5), 0)
for i in range(len(t_test)):
	t_1_train[i][t_test[i]] = 1
t_test = t_1_train.copy()

iterations_train = i_train.shape[0] // batch_size
iterations_test = i_test.shape[0] // batch_size

trainMean = list()

'''Имеем i_train, t_train, i_test, t_test. Создаем архитектуру нейросети'''
while True:
	mean_test = 0
	weights_01_w = 0.2 * np.random.random((275, hidden_size)) - 0.1
	weights_12_w = 0.02 * np.random.random((hidden_size, 5)) - 0.01
	for i in range(iterations_train):
		i_batch = i_train [i * batch_size: (i + 1) * batch_size]
		t_batch = t_train [i * batch_size: (i + 1) * batch_size]
		
		layer_0_w_c = i_batch
		#  layer_0_w_c *= my_mask
		layer_1_w = tanh (layer_0_w_c.dot(weights_01_w))
		dropout_mask = np.random.randint (2, size = layer_1_w.shape)
		layer_1_w *= dropout_mask * 2
		layer_2_w = softmax (layer_1_w.dot(weights_12_w))
		delta_2_w = (layer_2_w - t_batch) / batch_size
		delta_1_w = delta_2_w.dot(weights_12_w.T) * tanh2deriv (layer_1_w)
		delta_1_w *= dropout_mask
		weights_12_w -= alpha_w * layer_1_w.T.dot(delta_2_w)
		weights_01_w -= alpha_w * layer_0_w_c.T.dot(delta_1_w)
		
		correct_cnt = 0
		for i in range(batch_size):
			correct_cnt += int (np.argmax(layer_2_w[i : i+1]) == np.argmax(t_batch[i : i+1]))
		trainMean.append(correct_cnt / batch_size)
		if len(trainMean) == 10:
			endl = ' '
		else:
			endl = '\n'
		print('ТОЧНОСТЬ (обучающий набор): ' + str(correct_cnt/batch_size), end = endl)
		if len(trainMean) == 10:
			trainMean = sum(trainMean) / 10
			trainMean = '%.3f' % trainMean
			print('Среднее: ', trainMean)
			trainMean = list()
		
	for i in range(iterations_test):
		i_batch = i_test [i * batch_size: (i + 1) * batch_size]
		t_batch = t_test [i * batch_size: (i + 1) * batch_size]
		
		layer_0_w_c = i_batch
		#  layer_0_w_c *= my_mask
		layer_1_w = tanh (layer_0_w_c.dot(weights_01_w))
		dropout_mask = np.random.randint (2, size = layer_1_w.shape)
		layer_1_w *= dropout_mask * 2
		layer_2_w = softmax (layer_1_w.dot(weights_12_w))
		delta_2_w = (layer_2_w - t_batch) / batch_size
		delta_1_w = delta_2_w.dot(weights_12_w.T) * tanh2deriv (layer_1_w)
		delta_1_w *= dropout_mask
		
		correct_cnt = 0
		for i in range(batch_size):
			correct_cnt += int (np.argmax(layer_2_w[i : i+1]) == np.argmax(t_batch[i : i+1]))
		print('ТОЧНОСТЬ (тест): ' + str(correct_cnt/batch_size))
		mean_test += correct_cnt / batch_size
		
	print('Среднее значение: ', mean_test / iterations_test)
	answer = input('Повторим?')
	if answer == 'n':
		break
	
while True:
	answer = input('Сохранить веса?!')
	if answer == 'y':
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
		break
	elif answer == 'n':
		break