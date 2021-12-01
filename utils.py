import json
import math

#returns the normalized position (x,y) of the figure on a given tiimestamp
def getFigurePositionAtTimestamp(normalizedPositions, normalIimestamp):
    positionStr = ''
    for pos in normalizedPositions:
        if normalIimestamp <= pos['DurationSoFarInMs']:
            positionStr = pos['ToPoint'];
            break;
    if positionStr == '': positionStr=normalizedPositions[-1]['ToPoint']

    x = float(positionStr.split(',')[0])
    y = float(positionStr.split(',')[1])
    return {'x': x, 'y': y}

def euclid_dist(t1,t2):
    return math.sqrt(sum((t1-t2)**2))

#take the size of the smaller timeserie
def normalizeLength(tList):
    minLen = len(min(tList, key=len))
    new_tList = []
    for t in tList:
        new_tList.append(t[0:minLen])
    return new_tList