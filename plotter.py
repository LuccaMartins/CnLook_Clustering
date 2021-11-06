
import matplotlib.pyplot as plt


def distanceToFigure_HV(objRecord):
    plt.title('Horizontal Distance to Figure')
    plt.xlabel('Timestamp (ms)')
    plt.ylabel('Normalized Distance')
    [leftDistances_H, rightDistances_H] = objRecord.distanceToFigure_Horizontal()
    plt.plot(objRecord.timestamps, leftDistances_H, label = "Left Eye Distance")
    plt.plot(objRecord.timestamps, rightDistances_H, label = "Right Eye Distance")
    plt.legend()
    plt.show()


def positions_HV(objRecord):
    [leftEyePos, rightEyePos] = objRecord.getPositions_HV()
    figPos = objRecord.task.getFigurePositions_HV(objRecord.timestamps)

    plt.title('Horizontal Position')
    plt.xlabel('Timestamp (ms)')
    plt.ylabel('<-Left    -    Right->')

    plt.plot(objRecord.timestamps, list(map(lambda x: float(x[0]), figPos)), label="Figure Position", linewidth=5, color='#33FF60')
    plt.plot(objRecord.timestamps, list(map(lambda x: float(x[0]), leftEyePos)), label="Left Eye Position", color='#333EFF')
    plt.plot(objRecord.timestamps, list(map(lambda x: float(x[0]), rightEyePos)), label="Right Eye Position", color='#FF3333')

    plt.show()