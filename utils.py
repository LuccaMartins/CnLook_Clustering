import json

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

