import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt
import random


class Example(QWidget):

    def __init__(self, path):
        super().__init__()

        # Set canvas
        self.path = path
        self.guiWidth = 1000
        self.guiHeight = 500
        self.guiUnit = 50
        self.windowTitle = 'Scatter Plot'
        self.chartTitle = 'Scatter Plot'
        self.xName = 'x'
        self.yName = 'y'

        # Read data from file
        self.categories, self.idSequence, self.xSequence, self.ySequence = self.readFile()
        self.xMax, self.xMin = max(self.xSequence), min(self.xSequence)
        self.yMax, self.yMin = max(self.ySequence), min(self.ySequence)

        # Generate color for circles and notes
        self.colorList, self.colorDict = self.generateColor()

        # Generate GUI
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, self.guiWidth + 50, self.guiHeight)
        self.setWindowTitle(self.windowTitle)
        self.show()

    # Paint in canvas
    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawAxis(qp)
        self.drawCircle(qp)
        self.drawTitle(qp)
        self.drawNote(qp)
        qp.end()

    # Read from local file, each column (category, id, x, y) stored in a list
    def readFile(self):
        file = open(self.path, 'r')
        read = file.readlines()
        categories, idSequence, xSequence, ySequence = [], [], [], []

        for line in read[1:]:
            line = line.strip()
            catagory, id, x, y = line.split(',')
            x, y = float(x), float(y)
            categories.append(catagory)
            idSequence.append(id)
            xSequence.append(x)
            ySequence.append(y)

        return categories, idSequence, xSequence, ySequence

    # Generate scales for x axis and y axis
    def generateScale(self):

        # Generate scales for x axis
        xScaleNum = int((self.guiWidth - 4 * self.guiUnit) / self.guiUnit + 1)
        xUnit = (self.xMax - self.xMin) / (xScaleNum - 1)
        xScales = []
        for i in range(xScaleNum):
            scale = str(float(format((self.xMin + i * xUnit), '.1f')))
            xScales.append(scale)

        # Generate scales for x axis
        yScaleNum = int((self.guiHeight - 4 * self.guiUnit) / self.guiUnit + 1)
        yUnit = (self.yMax - self.yMin) / (yScaleNum - 1)
        yScales = []
        for i in range(yScaleNum):
            scale = str(float(format((self.yMin + i * yUnit), '.1f')))
            yScales.append(scale)

        return xScales, yScales

    # Generate color for circles and notes randomly
    def generateColor(self):
        colorList = []
        colorDict = {}
        for i in range(len(self.categories)):
            if self.categories[i] not in colorDict:
                cr = int(255 * random.random())
                cg = int(255 * random.random())
                cb = int(255 * random.random())
                colorDict[self.categories[i]] = ([cr, cg, cb])
            colorList.append([cr, cg, cb])

        return colorList, colorDict

    # Draw x axis and y axis
    def drawAxis(self, qp):

        # Set parameters
        pen = QPen(Qt.black, 1, Qt.SolidLine)
        qp.setPen(pen)
        xScales, yScales = self.generateScale()

        # Line for x axis 
        qp.drawLine(self.guiUnit, self.guiHeight - self.guiUnit, self.guiWidth - self.guiUnit,
                    self.guiHeight - self.guiUnit)
        qp.drawLine(self.guiWidth - self.guiUnit - 10, self.guiHeight - self.guiUnit + 5,
                    self.guiWidth - self.guiUnit, self.guiHeight - self.guiUnit)
        qp.drawLine(self.guiWidth - self.guiUnit - 10, self.guiHeight - self.guiUnit - 5,
                    self.guiWidth - self.guiUnit, self.guiHeight - self.guiUnit)
        qp.drawText(self.guiWidth - self.guiUnit, self.guiHeight - self.guiUnit + 20, self.xName)

        # Line for y axis
        qp.drawLine(self.guiUnit, self.guiHeight - self.guiUnit, self.guiUnit, self.guiUnit)
        qp.drawLine(self.guiUnit, self.guiUnit, self.guiUnit + 5, self.guiUnit + 10)
        qp.drawLine(self.guiUnit, self.guiUnit, self.guiUnit - 5, self.guiUnit + 10)
        qp.drawText(self.guiUnit - 20, self.guiUnit, self.yName)

        # Scales on x axis
        for i in range(len(xScales)):
            xGui = int(self.guiUnit * 2 + self.guiUnit * i)
            yGui = int(self.guiHeight - self.guiUnit)
            qp.drawLine(xGui, yGui, xGui, yGui - 10)
            qp.drawText(xGui - 10, yGui + 20, xScales[i])

        # Scales on y axis
        for i in range(len(yScales)):
            xGui = int(self.guiUnit)
            yGui = int(self.guiHeight - self.guiUnit * 2 - self.guiUnit * i)
            qp.drawLine(xGui, yGui, xGui + 10, yGui)
            qp.drawText(xGui - 30, yGui + 5, yScales[i])

    # Draw data
    def drawCircle(self, qp):

        # Set parameters
        pen = QPen(Qt.black, 1, Qt.SolidLine)
        qp.setPen(pen)
        qp.setFont(QFont('Decorative', 10))
        diameter = 10
        width = self.guiWidth - self.guiUnit * 4
        height = self.guiHeight - self.guiUnit * 4

        for i in range(len(self.xSequence)):
            # Calculate the coordinates of each data in the GUI coordinate system
            x = int((self.xSequence[i] - self.xMin) * width / (self.xMax - self.xMin)) + self.guiUnit
            y = int((self.ySequence[i] - self.yMin) * height / (self.yMax - self.yMin)) + self.guiUnit
            cr = self.colorList[i][0]
            cg = self.colorList[i][1]
            cb = self.colorList[i][2]
            xGui = self.guiUnit + x - int(diameter / 2)
            yGui = self.guiHeight - y - self.guiUnit - int(diameter / 2)

            # Draw circle and label
            color = QColor(cr, cg, cb)
            qp.setBrush(color)
            qp.drawEllipse(xGui, yGui, diameter, diameter)
            qp.drawText(xGui + int(diameter * 1.5), yGui + diameter, self.idSequence[i])

    # Draw title
    def drawTitle(self, qp):
        qp.setPen(Qt.black)
        qp.setFont(QFont('Decorative', 20))
        qp.drawText(int(self.guiWidth / 2), self.guiUnit, self.chartTitle)

    # Draw note
    def drawNote(self, qp):

        # Set parameters
        pen = QPen(Qt.black, 1, Qt.SolidLine)
        qp.setPen(pen)
        qp.setFont(QFont('Decorative', 10))

        index = 0
        for category in self.colorDict:
            cr = self.colorDict[category][0]
            cg = self.colorDict[category][1]
            cb = self.colorDict[category][2]
            color = QColor(cr, cg, cb)
            qp.setBrush(color)
            xGui = self.guiWidth - self.guiUnit
            yGui = int(self.guiUnit * 1.5) + int(self.guiUnit / 2) * index
            qp.drawRect(xGui, yGui, 10, 10)
            qp.drawText(xGui + 15, yGui + 10, category)
            index += 1

def main():
    random.seed(500)
    app = QApplication(sys.argv)
    ex = Example('data.txt')
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
