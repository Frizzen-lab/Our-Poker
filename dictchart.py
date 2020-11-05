#  Старшие пары
aAce = (12,12)
kKing = (11,11)
qQuinn = (10,10)

#  Средние пары
jJack = (9,9)
tTen = (8,8)

#  Младшие пары
nNine = (7,7)
eEight = (6,6)
sSeven = (5,5)
sSix = (4,4)
fFive = (3,3)
fFour = (2,2)
tThree = (1,1)
tTwo = (0,0)

#  Сильные тузы
kingAce = (11,12)

#  Средние тузы
tenAce = (8,12)
jackAce = (9,12)
quinnAce = (10,12)

#  Малые одномастные тузы
twoAceT = (0,12,True)
threeAceT = (1,12,True)
fourAceT = (2,12,True)
fiveAceT = (3,12,True)
sixAceT = (4,12,True)
sevenAceT = (5,12,True)
eightAceT = (6,12,True)
nineAceT = (7,12,True)

#  Одномастные картинки
quinnKingT = (10,11,True)
jackKingT = (9,11,True)
tenKingT = (8,11,True)
jackQuinnT = (9,10,True)
tenQuinnT = (8,10,True)
tenJackT = (8,9,True)

#  Разномастные картинки
quinnKingF = (10,11,False)
jackKingF = (9,11,False)
tenKingF = (8,11,False)
jackQuinnF = (9,10,False)
tenQuinnF = (8,10,False)
tenJackF = (8,9,False)

#  Одномастные коннекторы
nineTenT = (7,8,True)
eightNineT = (6,7,True)
sevenEightT = (5,6,True)
sixSevenT = (4,5,True)
fiveSixT = (3,4,True)
fourFiveT = (2,3,True)

availabilityList = [
	aAce,
	kKing,
	qQuinn,
	jJack,
	tTen,
	nNine,
	eEight,
	sSeven,
	sSix,
	fFive,
	fFour,
	tThree,
	tTwo,
	kingAce,
	quinnAce,
	jackAce,
	tenAce,
	nineAceT,
	eightAceT,
	sevenAceT,
	sixAceT,
	fiveAceT,
	fourAceT,
	threeAceT,
	twoAceT,
	quinnKingT,
	jackKingT,
	tenKingT,
	jackQuinnT,
	tenQuinnT,
	tenJackT,
	quinnKingF,
	jackKingF,
	tenKingF,
	jackQuinnF,
	tenQuinnF,
	tenJackF,
	nineTenT,
	eightNineT,
	sevenEightT,
	sixSevenT,
	fiveSixT,
	fourFiveT
]

'''
dict = {
	aAce:{
		early:,
		middle:,
		late:,
		blinds:
		},
	kKing:{
		early:,
		middle:,
		late:,
		blinds:
		},
	qQuinn:{
		early:,
		middle:,
		late:,
		blinds:},
	jJack:{
		early:,
		middle:,
		late:,
		blinds:},
	tTen:{
		early:,
		middle:,
		late:,
		blinds:},
	nNine:{
		early:,
		middle:,
		late:,
		blinds:},
	eEight:{
		early:,
		middle:,
		late:,
		blinds:},
	sSeven:{
		early:,
		middle:,
		late:,
		blinds:},
	sSix:{
		early:,
		middle:,
		late:,
		blinds:},
	fFive:{
		early:,
		middle:,
		late:,
		blinds:},
	fFour:{
		early:,
		middle:,
		late:,
		blinds:},
	tThree:{
		early:,
		middle:,
		late:,
		blinds:},
	tTwo:{
		early:,
		middle:,
		late:,
		blinds:},
	kingAce:{
		early:,
		middle:,
		late:,
		blinds:},
	tenAce:{
		early:,
		middle:,
		late:,
		blinds:},
	jackAce:{
		early:,
		middle:,
		late:,
		blinds:},
	quinnAce:{
		early:,
		middle:,
		late:,
		blinds:},
	twoAceT:{
		early:,
		middle:,
		late:,
		blinds:},
	threeAceT:{
		early:,
		middle:,
		late:,
		blinds:},
	fourAceT:{
		early:,
		middle:,
		late:,
		blinds:},
	fiveAceT:{
		early:,
		middle:,
		late:,
		blinds:},
	sixAceT:{
		early:,
		middle:,
		late:,
		blinds:},
	sevenAceT:{
		early:,
		middle:,
		late:,
		blinds:},
	eightAceT:{
		early:,
		middle:,
		late:,
		blinds:},
	nineAceT:{
		early:,
		middle:,
		late:,
		blinds:},
	quinnKingT:{
		early:,
		middle:,
		late:,
		blinds:},
	jackKingT:{
		early:,
		middle:,
		late:,
		blinds:},
	tenKingT:{
		early:,
		middle:,
		late:,
		blinds:},
	jackQuinnT:{
		early:,
		middle:,
		late:,
		blinds:},
	tenQuinnT:{
		early:,
		middle:,
		late:,
		blinds:},
	tenJackT:{
		early:,
		middle:,
		late:,
		blinds:},
	quinnKingF:{
		early:,
		middle:,
		late:,
		blinds:},
	jackKingF:{
		early:,
		middle:,
		late:,
		blinds:},
	tenKingF:{
		early:,
		middle:,
		late:,
		blinds:},
	jackQuinnF:{
		early:,
		middle:,
		late:,
		blinds:},
	tenQuinnF:{
		early:,
		middle:,
		late:,
		blinds:},
	tenJackF:{
		early:,
		middle:,
		late:,
		blinds:},
	nineTenT:{
		early:,
		middle:,
		late:,
		blinds:},
	eightNineT:{
		early:,
		middle:,
		late:,
		blinds:},
	sevenEightT:{
		early:,
		middle:,
		late:,
		blinds:},
	sixSevenT:{
		early:,
		middle:,
		late:,
		blinds:},
	fiveSixT:{
		early:,
		middle:,
		late:,
		blinds:},
	fourFiveT:{
		early:,
		middle:,
		late:,
		blinds:}
		}
'''
