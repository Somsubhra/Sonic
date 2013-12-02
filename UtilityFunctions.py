import math, random


def trueDist(pos1, pos2):
    return ( math.sqrt(math.pow(pos2.getX() - pos1.getX(), 2) + math.pow(pos2.getY() - pos1.getY(), 2)) )


def getRandom(val1, val2):
    if (val1 >= 0):
        rand = random.random() * (val2 - val1) + val1
    else:
        rand = random.random()
        if (random.random() > .5):
            rand *= val1
        else:
            rand *= val2
    return (rand)