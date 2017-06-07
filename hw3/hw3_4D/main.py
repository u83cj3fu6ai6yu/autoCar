from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
#from GUI import ControlPanel
from street import *
#from fuzzysystem import *

from numpy import *
from math import exp


class AutoCar(ControlPanel) :
    detectDirect = [45, 0, -45]

    def __init__(self, path = './map.json', parent = None) :
        super(AutoCar, self).__init__(path, AutoCar.detectDirect, parent)
        '''#flarge = FuzzySet([[30, 1], [40, 1]])
        small  = FuzzySet([ [0, 1], [4, 1], [5, 0] ])
        large  = FuzzySet([ [8, 0], [16, 1], [30, 1] ])
        turnRL = FuzzySet([ [ 20, 0], [ 40, 1] ])
        turn0  = FuzzySet([ [-40, 0], [-20, 1], [ 20, 1], [40, 0] ])
        turnLL = FuzzySet([ [-40, 1], [-20, 0] ])
        self.FuzzyRules = RuleEngine([
            {'circumstance' : [ParamFuzzySet(large, 'right')],
             'reaction'     :  turnRL},

            {'circumstance' : [ParamFuzzySet(large, 'left')], 
             'reaction'     :  turnLL},

            {'circumstance' : [ParamFuzzySet(small, 'right')],
             'reaction'     :  turnLL},

            {'circumstance' : [ParamFuzzySet(small, 'left')],
             'reaction'     :  turnRL},

            {'circumstance' : [#ParamFuzzySet(flarge, 'front'), 
                               ParamFuzzySet(small, 'sub')],
             'reaction'     :  turn0}
            ])'''
    def calculateTurnDegree(self, distance) :
        J = 3
        p = 3
        dis = list([distance[0], distance[-45], distance[45]])
        #dis = array(dis)
        bestsolution = list([0.6434388429202277, -38.943620337036634, 5.405875345132818, 40, 24.742813412188877, 13.297751524739287, 24.936064581253216, 11.384949686617997, 19.160414256726238, 25.920189337514145, 21.94348618602635, 23.272093106761695, 7.5326689019082504, 10, 3.6875771118591127, 10]
)
        phi = list()
        
        for j in range(J):
            summ = 0
            for smallp in range(p):
                summ = summ + pow( (dis[smallp] - bestsolution[1+J+j*p+smallp]) , 2)
            summ = summ / (2 * (pow(bestsolution[(1+J+p*J+j)], 2)))
            summ = summ * (-1)
            phi.append( exp(summ) )
        Fx = bestsolution[0]
        for i in range(1, 1+J):
            Fx =  Fx + (bestsolution[i] * phi[i-1])
        #Fx = Fx * 80 - 40
        return Fx
    def keyPressEvent(self, event) :
        if event.key() == Qt.Key_PageUp :
            distance = self._street.dis
            '''param={#'front'  : distance[0],
                    'sub'   : distance[-45] - distance[45],
                    'left'  : distance[45],
                    'right' : distance[-45]}
            degree = self.FuzzyRules.derivation(param)'''
            degree = self.calculateTurnDegree(distance)
            print 'prediction degree : %f' % degree
            self._street.tdeg = degree
            self._street.nextStatus()
            self._changeStrate()
        else :
            super(AutoCar, self).keyPressEvent(event)


if __name__ == '__main__' :
    app = QApplication(sys.argv)
    car = AutoCar()
    car.setWindowTitle("AutoCar")
    car.resize(550, 650)
    car.show()
    app.exec_()
