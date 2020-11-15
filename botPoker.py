from comb import combinations
from collections import Counter


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

#  Словарь наличия
availabilityList = (
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
)


#  Пот-оддсы на префлопе
potOdds_pref = {
                'suitedCon':3.0,
                'suited1gap':3.5,
                'suited2gap':4.0,
                'suited3gap':5.0,
                'offCon':5.5,
                'off1gap':7.5,
                'off2gap':11.5,
                'off3gap':21.5,
                'any2suited':5.5,
                'offAX':20.5,
                'any2off':27.5,
                'pocketPair':7.5
                }

#  Пот-оддсы на флопе
potOdds_fl = {
                1:22.50,
                2:10.88,
                3:7.01,
                4:5.07,
                5:3.91,
                6:3.14,
                7:2.59,
                8:2.18,
                9:1.86,
                10:1.60,
                11:1.40,
                12:1.22,
                13:1.08,
                14:0.95,
                15:0.85
                }

#  Пот-оддсы на тёрне
potOdds_turn = {
                1:45.0,
                2:22.0,
                3:14.33,
                4:10.50,
                5:8.20,
                6:6.67,
                7:5.57,
                8:4.75,
                9:4.11,
                10:3.60,
                11:3.18,
                12:2.83,
                13:2.54,
                14:2.29,
                15:2.07
                }
                
posDict = {
    10:{
        9:'blinds',
        8:'blinds',
        7:'late',
        6:'late',
        5:'middle',
        4:'middle',
        3:'middle',
        2:'early',
        1:'early',
        0:'early'
    },
    9:{
        9:'blinds',
        8:'blinds',
        7:'late',
        6:'late',
        5:'middle',
        4:'middle',
        3:'middle',
        1:'early',
        0:'early'
    },
    8:{
        9:'blinds',
        8:'blinds',
        7:'late',
        6:'late',
        5:'middle',
        4:'middle',
        3:'early',
        0:'early'
    },
    7:{
        9:'blinds',
        8:'blinds',
        7:'late',
        6:'late',
        5:'middle',
        4:'middle',
        3:'early'
    },
    6:{
        9:'blinds',
        8:'blinds',
        7:'late',
        6:'late',
        5:'middle',
        4:'middle'
    },
    5:{
        9:'blinds',
        8:'blinds',
        7:'late',
        6:'late',
        5:'middle'
    },
    4:{
        9:'blinds',
        8:'blinds',
        7:'late',
        6:'late'
    },
    3:{
        9:'blinds',
        8:'blinds',
        7:'late'
    },
    2:{
        9:'blinds',
        8:'blinds'
    }
}


chartDict = {
    aAce:{
        'early':
            {
            'allFold':(2,2,3,1),
            'haveColl':(2,2,3,1),
            'haveRaise':(2,2,3,1)
            },
        'middle':
            {
            'allFold':(2,2,3,1),
            'haveColl':(2,2,3,1),
            'haveRaise':(2,2,3,1)
            },
        'late':
            {
            'allFold':(2,2,3,1),
            'haveColl':(2,2,3,1),
            'haveRaise':(2,2,3,1)
            },
        'blinds':
            {
            'allFold':(2,2,3,1),
            'haveColl':(2,2,3,1),
            'haveRaise':(2,2,3,1)
            }
        },
    kKing:
        {
        'early':
            {
            'allFold':(2,2,3,1),
            'haveColl':(2,2,3,1),
            'haveRaise':(2,2,3,1)
            },
        'middle':
            {
            'allFold':(2,2,3,1),
            'haveColl':(2,2,3,1),
            'haveRaise':(2,2,3,1)
            },
        'late':
            {
            'allFold':(2,2,3,1),
            'haveColl':(2,2,3,1),
            'haveRaise':(2,2,3,1)
            },
        'blinds':
            {
            'allFold':(2,2,3,1),
            'haveColl':(2,2,3,1),
            'haveRaise':(2,2,3,1)
            }
        },
    qQuinn:{
        'early':
            {
            'allFold':(2,2,3,1),
            'haveColl':(2,2,3,1),
            'haveRaise':(2,2,3,1)
            },
        'middle':
            {
            'allFold':(2,2,3,1),
            'haveColl':(2,2,3,1),
            'haveRaise':(2,2,3,1)
            },
        'late':
            {
            'allFold':(2,2,3,1),
            'haveColl':(2,2,3,1),
            'haveRaise':(2,2,3,1)
            },
        'blinds':
            {
            'allFold':(2,2,3,1),
            'haveColl':(2,2,3,1),
            'haveRaise':(2,2,3,1)
            }},
    jJack:{
        'early':
            {
            'allFold':(2,2,3,1),
            'haveColl':(2,2,3,1),
            'haveRaise':('C20',-1,-1,-1)
            },
        'middle':
            {
            'allFold':(2,2,3,1),
            'haveColl':(2,2,3,1),
            'haveRaise':('C20',-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,2,3,1),
            'haveColl':(2,2,3,1),
            'haveRaise':('C20',-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,2,3,1),
            'haveColl':(2,2,3,1),
            'haveRaise':('C20',-1,-1,-1)
            }},
    tTen:{
        'early':
            {
            'allFold':(2,2,3,1),
            'haveColl':(2,2,3,1),
            'haveRaise':('C20',-1,-1,-1)
            },
        'middle':
            {
            'allFold':(2,2,3,1),
            'haveColl':(2,2,3,1),
            'haveRaise':('C20',-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,2,3,1),
            'haveColl':(2,2,3,1),
            'haveRaise':('C20',-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,2,3,1),
            'haveColl':(2,2,3,1),
            'haveRaise':('C20',-1,-1,-1)
            }},
    nNine:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(1,'C20',-1,-1),
            'haveColl':(1,'C20',-1,-1),
            'haveRaise':('C20',-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,'C20',-1,-1),
            'haveRaise':('C20',-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,'C20',-1,-1),
            'haveRaise':('C20',-1,-1,-1)
            }},
    eEight:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(1,'C20',-1,-1),
            'haveColl':(1,'C20',-1,-1),
            'haveRaise':('C20',-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,'C20',-1,-1),
            'haveRaise':('C20',-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,'C20',-1,-1),
            'haveRaise':('C20',-1,-1,-1)
            }},
    sSeven:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(1,'C20',-1,-1),
            'haveColl':(1,'C20',-1,-1),
            'haveRaise':('C20',-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,'C20',-1,-1),
            'haveRaise':('C20',-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,'C20',-1,-1),
            'haveRaise':('C20',-1,-1,-1)
            }},
    sSix:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(1,'C20',-1,-1),
            'haveColl':(1,'C20',-1,-1),
            'haveRaise':('C20',-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,'C20',-1,-1),
            'haveRaise':('C20',-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,'C20',-1,-1),
            'haveRaise':('C20',-1,-1,-1)
            }},
    fFive:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(1,'C20',-1,-1),
            'haveColl':(1,'C20',-1,-1),
            'haveRaise':('C20',-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,'C20',-1,-1),
            'haveRaise':('C20',-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,'C20',-1,-1),
            'haveRaise':('C20',-1,-1,-1)
            }},
    fFour:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(1,'C20',-1,-1),
            'haveColl':(1,'C20',-1,-1),
            'haveRaise':('C20',-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,'C20',-1,-1),
            'haveRaise':('C20',-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,'C20',-1,-1),
            'haveRaise':('C20',-1,-1,-1)
            }},
    tThree:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(1,'C20',-1,-1),
            'haveColl':(1,'C20',-1,-1),
            'haveRaise':('C20',-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,'C20',-1,-1),
            'haveRaise':('C20',-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,'C20',-1,-1),
            'haveRaise':('C20',-1,-1,-1)
            }},
    tTwo:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(1,'C20',-1,-1),
            'haveColl':(1,'C20',-1,-1),
            'haveRaise':('C20',-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,'C20',-1,-1),
            'haveRaise':('C20',-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,'C20',-1,-1),
            'haveRaise':('C20',-1,-1,-1)
            }},
    kingAce:{
        'early':
            {
            'allFold':(2,2,3,1),
            'haveColl':(2,2,3,1),
            'haveRaise':(2,2,3,1)
            },
        'middle':
            {
            'allFold':(2,2,3,1),
            'haveColl':(2,2,3,1),
            'haveRaise':(2,2,3,1)
            },
        'late':
            {
            'allFold':(2,2,3,1),
            'haveColl':(2,2,3,1),
            'haveRaise':(2,2,3,1)
            },
        'blinds':
            {
            'allFold':(2,2,3,1),
            'haveColl':(2,2,3,1),
            'haveRaise':(2,2,3,1)
            }},
    tenAce:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(2,1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(2,1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    jackAce:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(2,1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(2,1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    quinnAce:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(2,1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(2,1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    twoAceT:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    threeAceT:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    fourAceT:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    fiveAceT:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    sixAceT:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    sevenAceT:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    eightAceT:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    nineAceT:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,1,-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    quinnKingT:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    jackKingT:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    tenKingT:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    jackQuinnT:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    tenQuinnT:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    tenJackT:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    quinnKingF:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    jackKingF:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    tenKingF:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    jackQuinnF:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    tenQuinnF:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    tenJackF:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    nineTenT:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    eightNineT:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    sevenEightT:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    sixSevenT:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    fiveSixT:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }},
    fourFiveT:{
        'early':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'middle':
            {
            'allFold':(-1,-1,-1,-1),
            'haveColl':(-1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'late':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            },
        'blinds':
            {
            'allFold':(2,'C20',-1,-1),
            'haveColl':(1,-1,-1,-1),
            'haveRaise':(-1,-1,-1,-1)
            }}
        }
        
flopDict = {
            }
            
turnDict = {
            }
            
riverDict = {
            }
        
def botPoker(tab248):
    howMany = -1
    move = -1
    #  --- Ниже логика бота на префлопе
    if tab248[30] in (0,1,2):
        #  Ниже мы устанавливаем карманную руку и проверяем на словаре наличия без одномастности, если её нету, то проверяем с одномастностью
        pocketDeck = list()
        for i in range(7,9):
            pocketDeck.append(tab248[i] - 1)
        pocketDeck = sorted(pocketDeck)
        pocketDeck = tuple(pocketDeck)
        if pocketDeck not in availabilityList:
            pocketDeck = list(pocketDeck)
            pocketDeck.append(tab248[14]==tab248[15])
            pocketDeck = tuple(pocketDeck)
        print(pocketDeck)
        #  --- Ниже логика игры, когда карманные карты есть в таблице
        if pocketDeck in availabilityList:
            movies_cnt = Counter(tab248[155:tab248[31]])
            if 2 in movies_cnt or 3 in movies_cnt:
                movDes = 'haveRaise'
            elif 1 in movies_cnt:
                movDes = 'haveColl'
            else:
                movDes = 'allFold'
            #  Присваиваем актуальное значение переменной move
            move = chartDict[pocketDeck][posDict[tab248[28]][tab248[21]]][movDes][tab248[30] % 3]
            
        #  --- Если карманных карт нет в таблице либо таблица выдала фолд в качестве рекомендации, используем пот-оддсы для префлопа
        if pocketDeck not in availabilityList or move == -1:
            diffCards = pocketDeck[1] - pocketDeck[0]
            if diffCards == 1:
                if pocketDeck[2]:
                    potOdd = 'suitedCon'
                else:
                    potOdd = 'offCon'
            elif diffCards == 2:
                if pocketDeck[2]:
                    potOdd = 'suited1gap'
                else:
                    potOdd = 'off1gap'
            elif diffCards == 3:
                if pocketDeck[2]:
                    potOdd = 'suited2gap'
                else:
                    potOdd = 'off2gap'
            elif diffCards == 4:
                if pocketDeck[2]:
                    potOdd = 'suited3gap'
                else:
                    potOdd = 'off3gap'
            elif diffCards == 0:
                potOdd = 'pocketPair'
            elif pocketDeck[1] == 12:
                potOdd = 'offAX'
            elif pocketDeck[2]:
                potOdd = 'any2suited'
            else:
                potOdd = 'any2off'
            
            #  --- Если стек меньше 15 рискуем
            if tab248[24] < 15:
                if tab248[33]/tab248[32] > (potOdds_pref[potOdd] * 0.75):
                    move = 1
                else:
                    move = -1
                    
            #  --- Если стек меньше 10 рискуем сильнее
            elif tab248[24] < 10:
                if tab248[33]/tab248[32] > (potOdds_pref[potOdd] * 0.5):
                    move = 1
                else:
                    move = -1
            else:
                if tab248[33]/tab248[32] > potOdds_pref[potOdd]:
                    move = 1
                else:
                    move = -1
                
    #  --- Ниже логика бота на флопе
    elif tab248[30] in (3,4,5):
        pass
    #  --- Ниже логика бота на тёрне
    elif tab248[30] in (6,7,8):
        pass
    #  --- Ниже логика бота на ривере
    elif tab248[30] in (9,10,11):
        pass
        
    if move == 'C20':
        if tab248[32]//tab248[23] < 21:
            move = 1
        else:
            move = -1
        
    if move == -1:
        howMany = -1
    elif move == 0:
        howMany = 0
    elif move == 1:
        howMany = tab248[32]
    elif move == 2:
        howMany = tab248[32] * 3
    elif move == 3:
        howMany = tab248[22]
    
    return howMany