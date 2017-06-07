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
    def calculateTurnDegree(self, distance, x, y) :
    	J = 3
    	p = 5
    	dis = list([x, y, distance[0], distance[-45], distance[45]])
    	#dis = array(dis)
    	bestsolution = list([0.38860274108203824, -16.64268613051349, 40, -30.465689999684397, 22.041653185063804, 8.067029113238913, 23.59760328864479, 23.622834595549246, 15.872019991948816, 3.3888945982025556, 4.775310014018899, 20.736681361721203, 22.986783252499755, 12.142447736334912, 21.95879312289316, 22.41745826618512, 22.801066544157166, 13.537498689758234, 28.28092226214305, 4.75220466200467, 8.675754574452974, 10]




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
            x, y = self._street.x, self._street.y
            '''param={#'front'  : distance[0],
                    'sub'   : distance[-45] - distance[45],
                    'left'  : distance[45],
                    'right' : distance[-45]}
            degree = self.FuzzyRules.derivation(param)'''
            degree = self.calculateTurnDegree(distance, x, y)
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
