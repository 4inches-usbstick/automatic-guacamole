import cv2
from math import *
print('Graphing API imported...')
graph = cv2.imread('source.png')
graph = cv2.resize(graph, (700,700) )
from numpy import *

def fileio(name, mode, contents = ""):
    f = open(name, mode)
    if mode == 'r':
        tr = f.read()
    if mode == 'rb':
        tr = f.read()
    if mode == 'a' or mode == 'w':
        f.write(contents)
        tr = None
    if mode == 'ab' or mode == 'wb':
        f.write(contents)
        tr = None
    f.close()
    return tr
    
def blast():
    print('Blasting graph...')
    global graph
    graph = cv2.imread('source.png')
    graph = cv2.resize(graph, (700,700) )

def undefline(x = 0, color = (255,255,255) ):
    x = 0
    y = range(-700,700)
    for i in y:
        plot(x,i, color)
    
def decirange(start, stop, step):
    rt = []
    pnt = start
    while pnt < stop:
        rt.append(pnt)
        pnt = pnt + step

    return rt
        
def setnothelper(inp):
    start = 0
    stop = 0
    if inp[0] == '[':
        startmod = 0
    if inp[0] == '(':
        startmod = 1

    if inp[-1:] == ']':
        endmod = 1
    if inp[-1:] == ')':
        endmod = 0

    inpref = inp.replace('[','').replace(']','').replace('(','').replace(')','').replace('*', '9223372036854775808')
    se = inpref.split(',')
    return list( range(int(se[0]) + startmod, int(se[1]) + endmod) )

def pointshelperx(inp):
    inp = inp.replace(' ','')
    inps = inp.split(';')
    tr = []
    for i in inps:
        i2 = i.replace('(','').replace(')','')
        i3 = i2.split(',')
        tr.append( int(i3[0]) )
    return tr

def plot(x,y,color = (255,255,255),thick = 1 ):
    x = x
    y = y
    realx = (700 / 2) + x
    realy = (700 / 2) - y

    f = 1
    global graph
    #print('Plotting:',x,y,', real =',realx,realy,color,thick)
    #print(color)
    try: graph[(int(realy)-thick)*f:(int(realy)+thick)*f,(int(realx)-thick)*f:(int(realx)+thick)*f] = color
    except: print('valuerror')


def show():
    global graph
    cv2.imshow('graph', graph)
    cv2.waitKey(0)

def write(filename = 'out.png'):
    global graph
    cv2.imwrite(filename, graph)
    
class contFunction:
    def __init__(self, expr, domain = 'A[]', color = (255,255,255), pre1 = 10, pre2 = 0.1, exece = False ):
        print(expr,domain,color)
        expr = ''+expr+''
        self.xpoints = []
        self.ypoints = []
        self.valuedict = {}
        self.pointdict = {}
        self.dm = domain
        self.pre1 = pre1
        self.pre2 = pre2
        self.expression = expr
        self.arn = False
        self.ex = exece
        
        self.color = color
        if domain[0] == 'A':
            self.xpoints = list(decirange(-700 , 700, 0.05))
            self.xintpoints = list(decirange(-700 , 700, 1))
            self.arn = True
        if domain[0] == 'R':
            self.xpoints = setnothelper(domain[1:])
            self.xintpoints = setnothelper(domain[1:])

        for i in self.xintpoints:
            try: endval =  eval(expr .replace( 'x', ''+str(i) ))
            except: endval = 10000 # in case you run square root function and a negative is plugged in
            self.ypoints.append(endval)
            self.valuedict[i] = endval

        for i in self.xpoints:
            try: endval = eval(f'{pre1}*('+expr.replace('x', f'({pre2}*'+str(i)+')')+')'   )
            except: endval = 10000
            self.pointdict[i] = endval
            #this one dilates the image both horizantally and vertically so overall the line shape is the same but the image is larger


    def get(self, val):
        val = int(val)
        if not self.arn and not self.ex:
            try: return self.valuedict[val]
            except KeyError: return 'KeyError in self.valuedict'
        if self.arn and not self.ex:
            return eval(self.expression.replace('x', str(val)))
            
        if self.ex:
            #print('UNDERLYING LIB:',self.expression[2:-2])
            a = self.expression[2:-2].replace("'", "")
            ass = a.split(', ')
            for i in ass:
                i = i.split(':')
                print(i)
                no1 = i[0].replace('(','').replace(')','').replace('[','').replace(']','').split(',')[0]
                no2 = i[0].replace('(','').replace(')','').replace('[','').replace(']','').split(',')[1]
                no1 = int(no1)
                no2 = int(no2)
                print('GET CALL',no1,no2,i[0][0], i[0][-1])
                if i[0][0] == '[' and i[0][-1] == ']':
                    if val >= no1 and val <= no2:
                        return float(eval(i[1].replace('x', str(val))))
                if i[0][0] == '[' and i[0][-1] == ')':
                    if val >= no1 and val < no2:
                        return float(eval(i[1].replace('x', str(val))))
                if i[0][0] == '(' and i[0][-1] == ']':
                    if val >= no1 and val <= no2:
                        return float(eval(i[1].replace('x', str(val))))
                if i[0][0] == '(' and i[0][-1] == ')':
                    if val > no1 and val < no2:
                        return float(eval(i[1].replace('x', str(val))))

    def place(self, color = (255,255,255) ):
        print('Graphing...')
        print(self.expression, self.color)
        counter = 0
        for i in self.pointdict:
            if self.pointdict[i] <= 351 and self.pointdict[i] >= -351:
                plot(i, self.pointdict[i], self.color)
            counter = counter + 1
        print('Counter:',counter)
        
 
    def report(self):

        try: yint = eval( self.expression.replace('x', str(0) ) )
        except: yint = 'null'
        
        xints = []
        for i in range(-700, 700):
            #print(self.expression.replace('x', str(i) ))
            #print( eval(self.expression.replace('x', str(i) )) )
            #if eval(self.expression.replace('x', str(i) )) == 0:
                #xints.append(self.xpoints[i])
            #print(i)
            #if i == 0:
             #   index0 = self.ypoints.index(i)
              #  xints.append(self.xpoints[i])
              
            if eval(self.expression.replace('x', str(i) )) == 0 and False:
                xints.append(i)
        
        #ticker = 0
        #while ticker < len(self.ypoints):
         #   #print(self.xpoints[ticker],self.ypoints[ticker])
          #  if floor(self.ypoints[ticker]) == 0 or ceil(self.ypoints[ticker]) == 0 or round(self.ypoints[ticker]) == 0:
           #     xints.append(self.xpoints[ticker])
            #ticker = ticker + 1
                
        #xints = str(xints)
        
        domain = self.dm.replace('R','')
        
        if domain == 'A[]':
            domain = 'All Real Numbers'
        maxint = max(self.ypoints)
        minint = min(self.ypoints)
        
        print(eval(self.expression.replace('x', str(699) )))
        print(eval(self.expression.replace('x', str(-700) )))
        
        arns = self.arn
        f = open('tmp.txt','w')
        f.write(str(self.valuedict).replace(',','\n'))
        f.close
        
        ro = f'```REPORT:\n expression: {self.expression}\n color: R={self.color[2]},G={self.color[1]},B={self.color[0]}\n y intercept: {yint}\n domain: {domain}\n min: {minint}\n max: {maxint}\n all-real-numbers function: {arns}\n [note that max/min does NOT apply to all functions]```'
        
        return ro
        
undefline(0, (0,255,255) )
xaxis = contFunction('0', 'A[]', (0,255,255) )
xaxis.place()
