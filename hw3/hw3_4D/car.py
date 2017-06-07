import math, json
class Car :
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
        self.game='run'
    def __savePath(self) :
        case=[self.x, self.y, self.cdeg]
        case.extend(self.dis[d] for d in self.dir)
        case.append(self.tdeg)
        self.path.append(case)
    def save(self, path4, path6) :
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
        if self.game!='run' :
            return
        c=self.cdeg
        t=self.tdeg
        self.x=self.x+Car.cos(c+t)+Car.sin(t)*Car.sin(c)
        self.y=self.y+Car.sin(c+t)-Car.sin(t)*Car.cos(c)
        self.cdeg=Car.standDeg(c-Car.asin(2*Car.sin(t)/Car.__b))
        for d in self.dir :
            self.dis.update({d : self.getDistanceByDeg(d)})
        self.__savePath()
        if self.__collision() :
            self.game='collision'
            return
        terminal=self.data['terminal']
        x1, x2=terminal[0][0], terminal[0][1]
        y1, y2=terminal[1][0], terminal[1][1]
        if self.x>x1 and self.x<x2 and self.y>y1 and self.y<y2 :
            self.game='success'
            return
    def lastStatus(self) :
        if len(self.path)>1 :
            self.path.pop()
            last=self.path[-1]
            self.x, self.y=last[0], last[1]
            self.cdeg, self.tdeg=last[2], last[-1]
            for i, d in enumerate(self.dir) :
                self.dis.update({d : last[i-3]})
    def __collision(self) :
        x0, y0=self.x, self.y
        for wall in self.data['wall'] :
            x1, y1=wall[0][0], wall[0][1]
            x2, y2=wall[1][0], wall[1][1]
            d=Car.plDistance(x0, y0, x1, y1, x2, y2)
            if d>Car.car_size :
                continue
            xd, yd=(x1+x2)/2, (y1+y2)/2
            r=math.sqrt(pow((x2-x1)/2, 2)+pow((y2-y1)/2, 2)+pow(Car.car_size, 2))
            d=math.sqrt(pow(x0-xd, 2)+pow(y0-yd, 2))
            if d<r :
                return True
            d=math.sqrt(pow(x1-x0, 2)+pow(y1-y0, 2))
            if d<Car.car_size :
                return True
            d=math.sqrt(pow(x2-x0, 2)+pow(y2-y0, 2))
            if d<Car.car_size :
                return True
        return False
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
        b1, b2=-1*Car.cos(d), -1*Car.sin(d)
        c1, c2=x0-x1, y0-y1
        D=Car.__det(a1, b1, a2, b2)
        Da=Car.__det(c1, b1, c2, b2)
        Db=Car.__det(a1, c1, a2, c2)
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
