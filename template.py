import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QGroupBox, QAction, QFileDialog, qApp, QHBoxLayout, QSplitter, QStyleFactory
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtGui import QIcon
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import cv2

##########################################
## Do not forget to delete "return NotImplementedError"
## while implementing a function
########################################

class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.title = 'Histogram Equalization'
        # You can define other things in here
        self.inputLoaded = False
        self.targetLoaded = False
        self.initUI()
        
    def openInputImage(self):
        print("Open Input")
        # This function is called when the user clicks File->Input Image.
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;PNG Files (*.png)", options=options)
        if fileName:
            print(fileName)
            pixmap = QPixmap(fileName)
            res = QLabel()
            res.setPixmap(pixmap)
            left_layout = QHBoxLayout()
            left_layout.addWidget(res)
            self.left.setLayout(left_layout)
            self.inputLoaded = True

    def openTargetImage(self):
        print("Open Target")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;PNG Files (*.png)", options=options)
        if fileName:
            print(fileName)
            pixmap = QPixmap(fileName)
            res = QLabel()
            res.setPixmap(pixmap)
            left_layout = QHBoxLayout()
            left_layout.addWidget(res)
            self.mid.setLayout(left_layout)
            self.targetLoaded = True

    def initUI(self):
        wid = QWidget(self)
        self.setCentralWidget(wid)
        hbox = QHBoxLayout()
        wid.setLayout(hbox)
 

        inputAct = QAction(QIcon('exit.png'), 'Input file', self)        
        inputAct.setShortcut('Ctrl+I')
        inputAct.setStatusTip('Input File')
        inputAct.triggered.connect(self.openInputImage)

        targetAct = QAction(QIcon('exit.png'), 'Target file', self)        
        targetAct.setShortcut('Ctrl+T')
        targetAct.setStatusTip('Target File')
        targetAct.triggered.connect(self.openTargetImage)


        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        fileMenu.addAction(inputAct)
        fileMenu.addAction(targetAct)
        

        self.left = QGroupBox()
        self.left.setTitle("Input")

        self.mid = QGroupBox()
        self.mid.setTitle("Target")

        self.right = QGroupBox()
        self.right.setTitle("Result")

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.left)
        splitter1.addWidget(self.mid)
        splitter1.addWidget(self.right)
        splitter1.setSizes([100,100,100])

        #button
        self.bottom = QGroupBox()

        
        button = QPushButton('Equalize Histogram', self)
        button.clicked.connect(self.histogramButtonClicked)
        BUTTON_SIZE = QSize(100, 100);
        button.setMinimumSize(BUTTON_SIZE);
        bot_layout = QHBoxLayout()
        bot_layout.addWidget(button)

        self.bottom.setLayout(bot_layout)

        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(self.bottom)
        splitter2.setSizes([400,100])
        hbox.addWidget(splitter2)

        
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
          
        self.setGeometry(1000, 1000, 1000, 1000)
        self.setWindowTitle('CV')
        self.show()
        # Write GUI initialization code
  

    def histogramButtonClicked(self):

        if not self.inputLoaded and not self.targetLoaded:
            QMessageBox.question(self, 'ZORT', "First load input and target images", QMessageBox.Yes | QMessageBox.Yes, QMessageBox.Yes)
        elif not self.inputLoaded:
            QMessageBox.question(self, 'ZORT', "Load input image", QMessageBox.Yes | QMessageBox.Yes, QMessageBox.Yes)
        elif not self.targetLoaded:
            QMessageBox.question(self, 'ZORT', "Load target image", QMessageBox.Yes | QMessageBox.Yes, QMessageBox.Yes)
        else:
            print("yey")

    def calcHistogram(self, I):
        # Calculate histogram
        return NotImplementedError

class PlotCanvas(FigureCanvas):
    def __init__(self, hist, parent=None, width=5, height=4, dpi=100):
        return NotImplementedError
        # Init Canvas
        self.plotHistogram(hist)

    def plotHistogram(self, hist):
        return NotImplementedError
        # Plot histogram

        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())