
import matplotlib.pyplot as plt


def distanceToFigure_Horizontal(normalizedPositions, recordSamples):
    leftEyeDistances = []
    rightEyeDistances = []
    allTimestamps = []
    for sample in recordSamples:
        sampleTime = sample.timestamp - recordSamples[0].timestamp
        allTimestamps.append(sampleTime/1000)
        figurePosition = getFigurePositionAtTimestamp(normalizedPositions, sampleTime)
        sampleLeftNormal = sample.left_normal.replace('(','').replace(')','').split(',')
        sampleRightNormal = sample.right_normal.replace('(','').replace(')','').split(',')

        leftDistance = abs(float(sampleLeftNormal[0]) - figurePosition['x'])
        rightDistance = abs(float(sampleRightNormal[0]) - figurePosition['x'])

        leftEyeDistances.append(leftDistance)
        rightEyeDistances.append(rightDistance)


    plt.title('Horizontal Distance to Figure')
    plt.xlabel('Timestamp (ms)')
    plt.ylabel('Normalized Distance')
    plt.plot(allTimestamps, leftEyeDistances, label = "Left Eye Distance")
    plt.plot(allTimestamps, rightEyeDistances, label = "Right Eye Distance")
    plt.legend()
    plt.show()

def getFigurePositionAtTimestamp(normalizedPositions, timestamp):
    positionStr = ''
    for pos in normalizedPositions:
        if timestamp <= pos['DurationSoFarInMs']:
            positionStr = pos['ToPoint'];
            break;
    if positionStr == '': positionStr=normalizedPositions[-1]['ToPoint']

    x = float(positionStr.split(',')[0])
    y = float(positionStr.split(',')[1])
    return {'x': x, 'y': y}
