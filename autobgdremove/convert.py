import cv2
import numpy as np

globaldir = {}
globaldir['color'] = []

def show_color(event,x = 0,y = 0,flags = 0,param = None):
    B=param[y,x][0]
    G=param[y,x][1]
    R=param[y,x][2]
	#print('\b' * len(str(B) + str(G) + str(R)),end="")
	#print(B,G,R)

    #cv2.putText(imgc, f'{R}, {G}, {B}', (0,0), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 2, cv2.LINE_AA)

    if event == cv2.EVENT_LBUTTONDOWN:
        print('  Added color:',B,G,R)
        globaldir['color'].append( (B,G,R) )
	#set the color so when the user closes out the color will be in the global dict

def AutoRemove(fn, dfn, moe = 3, top = 2):
    im = cv2.imread(fn, cv2.IMREAD_UNCHANGED)
    im = cv2.resize(im, (50, 50))
    #cv2.imshow('see', im)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    height, width, depth = im.shape
    instances = {}

    print(f'  AUTO {fn}->{dfn}')
    for i in range(0,height):
        for j in range(0,width):
            x = str(im[i,j][0])+'/'+str(im[i,j][1])+'/'+str(im[i,j][2])
            try: instances[x] = instances[x] + 1
            except: instances[x] = 1

    #print(len(instances))
    instances = {v: k for k, v in instances.items()}
    #reverse the key and the value

    #print(instances)
    #print(len(instances))
    globaldir['color'] = []
    for i in range(0, top):
        print(f'  Sweep {i}')
        print('   Selected: '+str(max(instances))+ '->' +str(instances[max(instances)]))
        del instances[max(instances)]

        b,g,r = instances[max(instances)].split('/')[0],instances[max(instances)].split('/')[1],instances[max(instances)].split('/')[2]
        globaldir['color'].append((int(b),int(g),int(r)))


    print('  Sending control to ManualRemove...')
    ManualRemove(fn, dfn, moe, False)
    print('  AUTO complete.')

            

    
def ManualRemove(fn, dfn, moe = 3, pick = True):
    #get image		
    img = cv2.imread(fn, cv2.IMREAD_UNCHANGED)
    print(f' {fn}->{dfn}')

    #create AC
    try:
        print(' Attempting to create Alpha channel.')
        bc, gc, rc = cv2.split(img) 
        ac = np.full(bc.shape, 255, dtype=bc.dtype)
        imgc = cv2.merge( (bc, gc, rc, ac) )
        #print(imgc[0,4])
    except:
        print(' Alpha channel may already exist.')
        bc, gc, rc, ac = cv2.split(img)
        imgc = img

    #let user choose a color
    print(' Select the background color.')

    # give object over
    if pick:
        cv2.imshow('pick',imgc)
        param = imgc
        cv2.setMouseCallback('pick',show_color, param)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    #go ahead with transparenting
    height, width, depth = imgc.shape
    print(f'  Colors: {globaldir["color"]}')
    print(f'  High: {height} Wide: {width} SafetyMargin: {moe}')
    total = height * width
    onetenth = total // 10
    iters = 0

    #for each color that is to be removed
    for k in globaldir['color']:
        print(f' Working on color: {k}')
        print(' Progress: [',end='')

        #instead of getting margin every time, get it once and sub in
        r1 = range(k[0]-moe,k[0]+moe)
        r2 = range(k[1]-moe,k[1]+moe)
        r3 = range(k[2]-moe,k[2]+moe)
        
        for i in range(0,height):
            for j in range(0,width):
                iters = iters + 1
                if imgc[i,j][0] in r1 and imgc[i,j][1] in r2 and imgc[i,j][2] in r3:
                    imgc[i,j][3] = 0
                if iters % onetenth == 0:
                    print('+', end='')

        print(']')

    print('  Completed, writing to file.')
    cv2.imwrite(dfn, imgc)

AutoRemove('test.png', 'out.png', 4)
