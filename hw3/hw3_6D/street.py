import sys, json, math
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from car import *

class Street(QWidget, Car) :
    __scale=8
    def __init__(self, path, detectDirect, parent=None) :
        super(Street, self).__init__(parent)
        Car.__init__(self, path, detectDirect)
        self.resize(500, 500)
    def __drawCar(self, qp, x, y, deg, r) :
        tx, ty=self.getXY([x, y])
        qp.drawEllipse(tx-r, ty-r, 2*r, 2*r)
        qp.drawLine(tx, ty, tx+Car.cos(deg)*r*2, ty-Car.sin(deg)*r*2)
    def paintEvent(self, event):
        qp=QPainter()
        qp.begin(self)
        qp.setPen(QPen(Qt.blue, 2, Qt.SolidLine))
        for wall in self.data['wall'] :
            x1, y1=self.getXY(wall[0])
            x2, y2=self.getXY(wall[1])
            qp.drawLine(x1, y1, x2, y2)
        qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        qp.drawRect(0, 0, 500, 500)

        qp.setPen(QPen(Qt.green, 1, Qt.DotLine))
        for p in self.path[:-1] :
            x, y, deg=p[0], p[1], p[2]
            self.__drawCar(qp, x, y, deg, 1*Street.__scale)

        qp.setPen(QPen(Qt.red, 5, Qt.SolidLine))
        for p in ['start', 'end'] :
            x, y=self.getXY(self.data[p])
            qp.drawPoint(x, y)
        self.__drawCar(qp, self.x, self.y, self.cdeg, Car.car_size*Street.__scale)
        qp.end()
    def getXY(self, li) :
        x=Street.__scale*(li[0]+12)
        y=450-Street.__scale*li[1]
        return x, y
class ParamPanel(QWidget) :
    def __init__(self, street, parent=None) :
        super(ParamPanel, self).__init__(parent)
        self.__street=street

        pLabel=QLabel(self)
        pLabel.setText('postion:')
        cLabel=QLabel(self)
        cLabel.setText('current degree:')
        tLabel=QLabel(self)
        tLabel.setText('turn degree:')

        self.__pLabel=QLabel(self)
        self.__cLabel=QLabel(self)
        self.__tLabel=QLabel(self)

        layout=QHBoxLayout(self)
        layout.addWidget(pLabel)
        layout.addWidget(self.__pLabel)
        layout.addWidget(cLabel)
        layout.addWidget(self.__cLabel)
        layout.addWidget(tLabel)
        layout.addWidget(self.__tLabel)
        self.setLayout(layout)
    def update(self) :
        x, y=self.__street.x, self.__street.y
        self.__pLabel.setText('(%.3f, %.3f)' % (self.__street.x, self.__street.y))
        self.__cLabel.setText('%.3f' % self.__street.cdeg)
        self.__tLabel.setText('%d' % self.__street.tdeg)
class DistancePanel(QWidget) :
    def __init__(self, street, detectDirect, parent=None) :
        super(DistancePanel, self).__init__(parent)
        self.__street=street
        self.dir=detectDirect
        self.lDict={}

        layout=QHBoxLayout(self)
        for d in self.dir :
            label=QLabel(self)
            label.setText('%3d : ' % d)
            layout.addWidget(label)
            label=QLabel(self)
            layout.addWidget(label)
            self.lDict.update({d : label})
        self.setLayout(layout)
    def update(self) :
        for d in self.dir :
            self.lDict[d].setText('%f' % self.__street.dis[d])
class ControlPanel(QWidget) :
    def __init__(self, path, detectDirect, parent=None) :
        super(ControlPanel, self).__init__(parent)
        self._street=Street(path, detectDirect, self)
        self.__param=ParamPanel(self._street, self)
        self.__distance=DistancePanel(self._street, detectDirect, self)
        save=QPushButton('Save', self)
        save.clicked.connect(self.save)
        save.setFocusPolicy(Qt.NoFocus)

        layout=QGridLayout()
        #layout=QVBoxLayout(self)
        layout.addWidget(self._street, 0, 0, 50, 50)
        layout.addWidget(self.__param, 60, 0, 1 , 50)
        layout.addWidget(self.__distance, 70, 0, 1 , 50)
        layout.addWidget(save, 80, 0, 1, 20)
        self.setLayout(layout)

        self._changeStrate()
    def save(self) :
        self._street.save('./train4D.txt', './train6D.txt')
        mbox=QMessageBox()
        mbox.setIcon(QMessageBox.Information)
        mbox.setText('Save Success')
        mbox.setWindowTitle('Save')
        mbox.exec_()
    def _changeStrate(self) :
        self._street.update()
        self.__param.update()
        self.__distance.update()
        if self._street.game=='collision' :
            mbox=QMessageBox()
            mbox.setIcon(QMessageBox.Information)
            mbox.setText('Boom!!!')
            mbox.setWindowTitle('Game Over')
            mbox.exec_()
        elif self._street.game=='success' :
            mbox=QMessageBox()
            mbox.setIcon(QMessageBox.Information)
            mbox.setText('Success!!!')
            mbox.setWindowTitle('Game Over')
            mbox.exec_()
    def keyPressEvent(self, event) :
        if event.key()==Qt.Key_Up :
            self._street.nextStatus()
            self._changeStrate()
        #elif event.key()==Qt.Key_Down :
        #    self._street.lastStatus()
        #    self._changeStrate()
        else :
            if event.key()==Qt.Key_Left :
                self._street.tdegSub()
                self._changeStrate()
            elif event.key()==Qt.Key_Right :
                self._street.tdegPlus()
                self._changeStrate()
if __name__=='__main__' :
    #s.resize(200, 150)
    #s.move(500, 400)
    app=QApplication(sys.argv)
    c=ControlPanel('./map.json', [45, 0, -45])
    c.setWindowTitle("Car")
    c.resize(550, 650)
    c.show()
    app.exec_()
