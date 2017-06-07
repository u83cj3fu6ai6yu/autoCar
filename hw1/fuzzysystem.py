class FuzzySet :
    def __init__(self, points = None) :
        self.rule = []
        if points :
            self.addLines([float(points[0][1])], float(points[0][0]))
            for i in range(len(points)-1) :
                m = [float(x) for x in points[i]]
                n = [float(x) for x in points[i+1]]
                a = (n[1] - m[1]) / (n[0] - m[0])
                b = (n[0] * m[1] - m[0] * n[1]) / (n[0] - m[0])
                if a == 0 :
                    self.addLines([b], n[0])
                else :
                    self.addLines([a, b], n[0])
            self.addLines([float(points[-1][1])])

    def addLines(self, poly, n = float('inf')) :
        self.rule.append({'judge' : n, 'poly' : poly})
        sorted(self.rule, key = lambda x : x['judge'])

    def get(self, x) :
        for rule in self.rule :
            n, poly = rule['judge'], rule['poly']
            if x < n :
                return reduce(lambda y, a : y * x + a, poly)
        raise Exception('FuzzySet get error')


class ParamFuzzySet :
    def __init__(self, func, Name) :
        self.func = FuzzySet()
        self.func.rule = func.rule[:]
        self.Name = Name

    def __str__(self) :
        return 'ParamFuzzySet{name : %s}' % self.Name

    def get(self, param) :
        alpha = param[self.Name]
        return self.func.get(alpha)


class WakeFuzzySet :
    def __init__(self, func, alpha) :
        self.originfunc = func
        self.setRuleAfterWake(alpha)

    def setRuleAfterWake(self, alpha) :
        self.alpha = alpha
        currentfunc = FuzzySet()
        for rule in self.originfunc.rule :
            judge, poly = rule['judge'], rule['poly']
            if len(poly) == 1 :
                currentfunc.addLines([min(poly[0], alpha)], judge)
            elif len(poly) == 2 and poly[0] != 0 :
                x = (alpha - poly[1]) / poly[0]
                if poly[0] > 0 :
                    currentfunc.addLines(poly, x)
                    currentfunc.addLines([alpha], judge)
                else :
                    currentfunc.addLines([alpha], x)
                    currentfunc.addLines(poly, judge)
            else :
                raise 'can not reaction poly > 2'
        self.currentfunc = currentfunc

    def midpointaverage(self) :
        count = 0
        num = 0
        last = -40
        print 'WakeFuzzySet rule : %s' % self.currentfunc.rule
        for rule in self.currentfunc.rule :
            judge, poly = rule['judge'], rule['poly']
            if last and len(poly) == 1 and poly[0] != 0 :
                num = num + last + (40 if judge > 40 else judge)
                count = count + 2
            last = judge
        return num / count if count > 0 else 0 #any is 0 so can return any

    def get(self, x) :
        return self.currentfunc.get(x)


class RuleEngine :
    def __init__(self, rules) :
        self.der = rules

    def derivation(self, param) :
        print 'input param : %s' % param
        maybeList = []
        for case in self.der :
            circumstance, reaction = case['circumstance'], case['reaction']
            print 'check circumstance : %s' % circumstance
            alphaList = map(lambda x : x.get(param), circumstance)
            print '%s' % circumstance[0].func.rule
            print 'get alpha list : %s' % alphaList
            alpha = min(float(s) for s in alphaList)
            print 'get minimum alpha : %f' % alpha
            maybeList.append(WakeFuzzySet(reaction, alpha))
        num, count = 0, 0
        for maybe in maybeList :
            x = maybe.midpointaverage()
            y = maybe.get(x)
            print 'x : %s, y : %s' % (x, y)
            num, count = num + x * y, count + y
        return num / count if count > 0 else None
