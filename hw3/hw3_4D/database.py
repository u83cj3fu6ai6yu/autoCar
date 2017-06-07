import json

def save(data, path='database.json') :
    with open(path, 'w') as f :
        json.dump(data, f)

def load(path='database.json') :
    with open(path, 'r') as f :
        d=json.load(f,sort_keys = True ,indent = 4)
        return d
    raise Exception('can not open database.json')

def toStand(d, g, t) :
    data=dict(d)
    log=g.log
    data.update({ 'data' : [{
        'log_size' : len(log),
        'log' : log,
        'time' : t,
        'gene' : g.best.data
        }]})
    return data
