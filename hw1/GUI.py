import sys, json, math
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Data :
    __b=6
    car_size=3
    def __init__(self, path, detectDirect) :
        self.data=self.__load(path)
        self.dir=detectDirect
        s=self.data['start']
        self.x, self.y=float(s[0]), float(s[1])
        self.cdeg, self.tdeg=90, 0
        self.dis={}
        for d in self.dir :
            self.dis.update({d : self.getDistanceByDeg(d)})
        self.path=[]
        self.__savePath()
    def __savePath(self) :
        case=[self.x, self.y, self.cdeg]
        case.extend(self.dis[d] for d in self.dir)
        case.append(self.tdeg)
        self.path.append(case)
    def save(self, path4, path6) :
        print path4, path6
        with open(path4, 'w') as f :
            for case in self.path :
                f.write('%.7f %.7f %.7f %.7f\n' % (case[0], case[1], case[2], case[-1]))
        with open(path6, 'w') as f :
            m='%.7f '*len(self.path[0])+'\n'
            for case in self.path :
                f.write(m % tuple(case))
    def __load(self, path) :
        data=None
        with open(path) as f :
            data=json.load(f)
        return data
    @staticmethod
    def standDeg(d) :
        d=d+360 if d<-90 else d
        d=d-360 if d>270 else d
        return d
    @staticmethod
    def plDistance(x0, y0, x1, y1, x2, y2) :
        # p : (x0, y0)
        # L : (x1, y1) -> (x2, y2)
        # (y2-y1)x-(x2-x1)y+x2y1-x1y2=0
        a=y2-y1
        b=x1-x2
        return abs(a*x0+b*y0+x2*y1-x1*y2)/math.sqrt(a*a+b*b)
    @staticmethod
    def sin(d) :
        return math.sin(d*math.pi/180)
    @staticmethod
    def cos(d) :
        return math.cos(d*math.pi/180)
    @staticmethod
    def tan(d) :
        return math.tan(d*math.pi/180)
    @staticmethod
    def asin(d) :
        return math.asin(d)*180/math.pi
    def tdegPlus(self) :
        if self.tdeg<40 :
            self.tdeg=self.tdeg+1
    def tdegSub(self) :
        if self.tdeg>-40 :
            self.tdeg=self.tdeg-1
    def nextStatus(self) :
        c=self.cdeg
        t=self.tdeg
        self.x=self.x+Data.cos(c+t)+Data.sin(t)*Data.sin(c)
        self.y=self.y+Data.sin(c+t)-Data.sin(t)*Data.cos(c)
        self.cdeg=Data.standDeg(c-Data.asin(2*Data.sin(t)/Data.__b))
        for d in self.dir :
            self.dis.update({d : self.getDistanceByDeg(d)})
        self.__savePath()
        if self.__Goal():
            QMessageBox.about(self, "Finish!!!", "Congratulation!!!")
        elif self.__collision() :
            print 'Boom!!!'
    def lastStatus(self) :
        if len(self.path)>1 :
            self.path.pop()
            last=self.path[-1]
            self.x, self.y=last[0], last[1]
            self.cdeg, self.tdeg=last[2], last[-1]
            for i, d in enumerate(self.dir) :
                self.dis.update({d : last[i-3]})
            #print self.x, self.y
            #print last
            #print self.path
    def __collision(self) :
        x0, y0=self.x, self.y
        for wall in self.data['wall'] :
            x1, y1=wall[0][0], wall[0][1]
            x2, y2=wall[1][0], wall[1][1]
            d=Data.plDistance(x0, y0, x1, y1, x2, y2)
            if d>Data.car_size :
                continue
            xd, yd=(x1+x2)/2, (y1+y2)/2
            r=math.sqrt(pow((x2-x1)/2, 2)+pow((y2-y1)/2, 2)+pow(Data.car_size, 2))
            d=math.sqrt(pow(x0-xd, 2)+pow(y0-yd, 2))
            if d<r :
                return True
            d=math.sqrt(pow(x1-x0, 2)+pow(y1-y0, 2))
            if d<Data.car_size :
                return True
            d=math.sqrt(pow(x2-x0, 2)+pow(y2-y0, 2))
            if d<Data.car_size :
                return True
        return False
    def __Goal(self) :
        x0, y0=self.x, self.y
        dx, dy = x0 - 24, y0 - 37
        d = math.sqrt(dx**2 + dy**2)
        if d > 3:
            return False
        else:
            return True
    @staticmethod
    def __det(a, b, c, d) :
        return a*d-b*c
    @staticmethod
    def __getDirection(x1, y1, x2, y2, x0, y0, d) :
        # x = (x2-x1)t + x1
        # y = (y2-y1)t + y1     0<=t<=1
        # x = cos(d)k  + x0
        # y = sin(d)k  + y0     0<=k
        # a1 = x2-x1    b1 = -cos(d)    c1 = x0-x1
        # a2 = y2-y1    b2 = -sin(d)    c2 = y0-y1
        # a1t + b1k = c1
        # a2t + b2k = c2    0<=t<=1, 0<=k
        a1, a2=x2-x1, y2-y1
        b1, b2=-1*Data.cos(d), -1*Data.sin(d)
        c1, c2=x0-x1, y0-y1
        D=Data.__det(a1, b1, a2, b2)
        Da=Data.__det(c1, b1, c2, b2)
        Db=Data.__det(a1, c1, a2, c2)
        if D==0 or Da/D<0 or Da/D>1 or Db/D<0 :
            return None
        return Db/D
    def getDistanceByDeg(self, t) :
        deg=self.cdeg+t
        min_d=None
        x0, y0=self.x, self.y
        for wall in self.data['wall'] :
            x1, y1=wall[0][0], wall[0][1]
            x2, y2=wall[1][0], wall[1][1]
            d=self.__getDirection(x1, y1, x2, y2, x0, y0, deg)
            if d and (not min_d or d<min_d) :
                min_d=d
        return min_d if min_d else 100
class Street(QWidget, Data) :
    __scale=10
    def __init__(self, path, detectDirect, parent=None) :
        super(Street, self).__init__(parent)
        Data.__init__(self, path, detectDirect)
        self.resize(500, 500)
    def __drawCar(self, qp, x, y, deg, r) :
        tx, ty=self.getXY([x, y])
        qp.drawEllipse(tx-r, ty-r, 2*r, 2*r)
        qp.drawLine(tx, ty, tx+Data.cos(deg)*r*2, ty-Data.sin(deg)*r*2)
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
        self.__drawCar(qp, self.x, self.y, self.cdeg, Data.car_size*Street.__scale)
        qp.end()
    def getXY(self, li) :
        x=Street.__scale*(li[0]+12)
        y=450-Street.__scale*li[1]
        return x, y
class ParamPanel(QWidget) :
    def __init__(self, street, parent=None) :
        super(ParamPanel, self).__init__(parent)
        self.__GUI=street

        pLabel=QLabel(self)
        pLabel.setText('position:')
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
        x, y=self.__GUI.x, self.__GUI.y
        self.__pLabel.setText('(%.3f, %.3f)' % (self.__GUI.x, self.__GUI.y))
        self.__cLabel.setText('%.3f' % self.__GUI.cdeg)
        self.__tLabel.setText('%d' % self.__GUI.tdeg)
class DistancePanel(QWidget) :
    def __init__(self, street, detectDirect, parent=None) :
        super(DistancePanel, self).__init__(parent)
        self.__GUI=street
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
            self.lDict[d].setText('%f' % self.__GUI.dis[d])
class ControlPanel(QWidget) :
    def __init__(self, path, detectDirect, parent=None) :
        super(ControlPanel, self).__init__(parent)
        self._GUI=Street(path, detectDirect, self)
        self.__param=ParamPanel(self._GUI, self)
        self.__distance=DistancePanel(self._GUI, detectDirect, self)
        save=QPushButton('Save', self)
        save.clicked.connect(self.save)

        layout=QGridLayout()
        #layout=QVBoxLayout(self)
        layout.addWidget(self._GUI, 0, 0, 50, 50)
        layout.addWidget(self.__param, 60, 0, 1 , 50)
        layout.addWidget(self.__distance, 70, 0, 1 , 50)
        layout.addWidget(save, 80, 0, 1, 20)
        self.setLayout(layout)

        self._changeStrate()
    def save(self) :
        self._GUI.save('./train4D.txt', './train6D.txt')
    def _changeStrate(self) :
        self._GUI.update()
        self.__param.update()
        self.__distance.update()
    def keyPressEvent(self, event) :
        if event.key()==Qt.Key_Up :
            self._GUI.nextStatus()
            self._changeStrate()
        #elif event.key()==Qt.Key_Down :
        #    self._GUI.lastStatus()
        #    self._changeStrate()
        else :
            if event.key()==Qt.Key_Left :
                self._GUI.tdegSub()
                self._changeStrate()
            elif event.key()==Qt.Key_Right :
                self._GUI.tdegPlus()
                self._changeStrate()
