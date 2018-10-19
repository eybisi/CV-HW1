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
import collections #For counting r g b values

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
            self.inputFile = fileName
            res = QLabel()
            res.setPixmap(pixmap)
            left_layout = QVBoxLayout()
            left_layout.addWidget(res)
            left_layout.setAlignment(res,Qt.AlignHCenter)
            left_layout.addStretch()
            #left_layout.setAlignment(Qt.)
            self.inputLoaded = True
            input_b = []
            input_img = cv2.imread(self.inputFile)
            


            i_b = [x[0] for y in input_img for x in y]
            i_g = [x[1] for y in input_img for x in y]
            i_r = [x[2] for y in input_img for x in y]

            
            b =PlotCanvas(hist=i_b,c="b")
            g = PlotCanvas(hist=i_g,c="g")
            r = PlotCanvas(hist=i_r,c="r")
            left_layout.addWidget(r)
            left_layout.addWidget(g)
            left_layout.addWidget(b)

            self.left.setLayout(left_layout)
            """
            #print(i_b)
            data = np.array(i_b)
            plt.hist(data,bins=255)

            # And finally plot the cdf
            #plt.plot(bin_edges[1:], cdf)
            plt.show()
            """
    def openTargetImage(self):
        print("Open Target")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;PNG Files (*.png)", options=options)
        if fileName:
            print(fileName)
            pixmap = QPixmap(fileName)
            self.targetFile = fileName
            res = QLabel()
            res.setPixmap(pixmap)
            mid_layout = QVBoxLayout()
            mid_layout.addWidget(res)
            mid_layout.setAlignment(res,Qt.AlignHCenter)
            self.targetLoaded = True
            target_img = cv2.imread(self.targetFile)

            t_b = [x[0] for y in target_img for x in y]
            t_g = [x[1] for y in target_img for x in y]
            t_r = [x[2] for y in target_img for x in y]

            
            b =PlotCanvas(hist=t_b,c="b")
            g = PlotCanvas(hist=t_g,c="g")
            r = PlotCanvas(hist=t_r,c="r")
            mid_layout.addWidget(r)
            mid_layout.addWidget(g)
            mid_layout.addWidget(b)

            self.mid.setLayout(mid_layout)
 
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
            calcHistogram()


    def calcHistogram(self, I):
        print("not yet")

class PlotCanvas(FigureCanvas):
    def __init__(self, hist, c,parent=None, width=5, height=4, dpi=100):
        self.c = c
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.plotHistogram(hist)

    def plotHistogram(self, hist):
        ax = self.figure.add_subplot(111)
        
        ax.hist(hist,bins=255,color=self.c)
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())