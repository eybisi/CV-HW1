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


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.title = 'Histogram Equalization'
        self.inputLoaded = False
        self.targetLoaded = False

        self.inputBGR_b = []
        self.inputBGR_r = []
        self.inputBGR_g = []
        self.targetBGR_b = []
        self.targetBGR_r = []
        self.targetBGR_g = []
        self.initUI()
        
    def openInputImage(self):
        if self.inputLoaded :
            QMessageBox.question(self, 'Error', "Input image already loaded", QMessageBox.Yes | QMessageBox.Yes, QMessageBox.Yes)
        else:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;PNG Files (*.png)", options=options)
            if fileName:
                self.setImage(fileName,self.left,"Input")


    def openTargetImage(self):
        if self.targetLoaded :
            QMessageBox.question(self, 'Error', "Target image already loaded", QMessageBox.Yes | QMessageBox.Yes, QMessageBox.Yes)
        else:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;PNG Files (*.png)", options=options)
            if fileName:
                self.setImage(fileName,self.mid,"Target")
 
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

    def histogramButtonClicked(self):

        if not self.inputLoaded and not self.targetLoaded:
            QMessageBox.question(self, 'Error', "First load input and target images", QMessageBox.Yes | QMessageBox.Yes, QMessageBox.Yes)
        elif not self.inputLoaded:
            QMessageBox.question(self, 'Error', "Load input image", QMessageBox.Yes | QMessageBox.Yes, QMessageBox.Yes)
        elif not self.targetLoaded:
            QMessageBox.question(self, 'Error', "Load target image", QMessageBox.Yes | QMessageBox.Yes, QMessageBox.Yes)
        else:
            input_img = cv2.imread(self.inputFile)
            target_img = cv2.imread(self.targetFile)
            i_b = self.inputBGR_b
            i_g = self.inputBGR_g
            i_r = self.inputBGR_r


            #Get BLUE,GREEN,RED pixels of target file
            t_b = self.targetBGR_b
            t_g = self.targetBGR_g
            t_r = self.targetBGR_r
            
            #Calculate LUT
            LUT_b = calcLUT(i_b,t_b)
            LUT_g = calcLUT(i_g,t_g)
            LUT_r = calcLUT(i_r,t_r)

            for i in range(len(input_img)):
                for j in range(len(input_img[i])):
                    
                    input_img[i][j][0] = LUT_b[input_img[i][j][0]]
                    input_img[i][j][1] = LUT_g[input_img[i][j][1]]
                    input_img[i][j][2] = LUT_r[input_img[i][j][2]]

            r_b = [x[0] for y in input_img for x in y]
            r_r = [x[2] for y in input_img for x in y]
            r_g = [x[1] for y in input_img for x in y]
            
            b =PlotCanvas(hist=r_b,c="b")
            g =PlotCanvas(hist=r_g,c="g")
            r =PlotCanvas(hist=r_r,c="r")
  
            cv2.imwrite("result.png",   input_img)
            pixmap = QPixmap("result.png")
            res = QLabel()
            res.setPixmap(pixmap)
            right_layout = QVBoxLayout()
            right_layout.addWidget(res)

            #right_layout.addWidget(res)
            right_layout.addWidget(b)
            right_layout.addWidget(g)
            right_layout.addWidget(r)

            #right_layout.addWidget(f_b)
            self.right.setLayout(right_layout)
    def setImage(self,fileName,loc,filetype):
        
        try:
            pixmap = QPixmap(fileName)
        except:
            raise ValueError("Cant read file")

        if filetype == "Input": 
            self.inputFile = fileName
            self.inputLoaded = True
        elif filetype == "Target":
            self.targetFile = fileName
            self.targetLoaded = True
        res = QLabel()
        res.setPixmap(pixmap)
        layout = QVBoxLayout()
        layout.addWidget(res)
        layout.setAlignment(res,Qt.AlignHCenter)
        layout.addStretch()
        
        input_img = cv2.imread(fileName)
        
        i_b = [x[0] for y in input_img for x in y]
        i_g = [x[1] for y in input_img for x in y]
        i_r = [x[2] for y in input_img for x in y]
        if filetype == "Input": 
            self.inputBGR_b = i_b
            self.inputBGR_g = i_g
            self.inputBGR_r = i_r
        elif filetype == "Target":
            self.targetBGR_b = i_b
            self.targetBGR_g = i_g
            self.targetBGR_r = i_r
        
        b =PlotCanvas(hist=i_b,c="b")
        g = PlotCanvas(hist=i_g,c="g")
        r = PlotCanvas(hist=i_r,c="r")
        layout.addWidget(r)
        layout.addWidget(g)
        layout.addWidget(b)
        loc.setLayout(layout)

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


def calcLUT(i,t):
    num_bins = 256
    counts1, bin_edges1 = np.histogram(i, bins=num_bins)
    cdf1 = np.cumsum(counts1)
    counts2, bin_edges2 = np.histogram(t, bins=num_bins)
    cdf2 = np.cumsum(counts2)
    LUT = np.zeros((256,1))
    j = 0
    for i in range(256):       
        for j in range(0,256):
            if cdf1[i] <= cdf2[j]:
                break
        LUT[i] = j
    return LUT


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())