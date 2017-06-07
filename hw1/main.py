from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from GUI import ControlPanel
from fuzzysystem import *


class AutoCar(ControlPanel) :
    detectDirect = [45, 0, -45]

    def __init__(self, path = './map.json', parent = None) :
        super(AutoCar, self).__init__(path, AutoCar.detectDirect, parent)
        #flarge = FuzzySet([[30, 1], [40, 1]])
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
            ])

    def keyPressEvent(self, event) :
        if event.key() == Qt.Key_PageUp :
            distance = self._GUI.dis
            param={#'front'  : dis[0],
                    'sub'   : distance[-45] - distance[45],
                    'left'  : distance[45],
                    'right' : distance[-45]}
            degree = self.FuzzyRules.derivation(param)
            print 'prediction degree : %f' % degree
            self._GUI.tdeg = degree
            self._GUI.nextStatus()
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