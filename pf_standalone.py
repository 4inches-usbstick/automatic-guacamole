import cv2
import numpy as np
import glob

files = glob.glob('*.const')
for i in files:
    f = open(i, 'r')
    c = f.read().split('\n')
    f.close()

consts = {}
for i in c:
    try:
        i2 = i.split('->')
        consts[i2[0]] = i2[1]
    except:
        pass

def colorparse(color):
    if len(color) != 6: return 0
    try: return (int(color[4:6],16),int(color[2:4],16),int(color[0:2],16))
    except: return 0

def generate(size, inp):
    global consts
    for i in consts:
        inp = inp.replace(i, consts[i])
    
    try: image = np.zeros((size,round(size * 1.6),3), np.uint8)
    except: return np.zeros((round(100),100,3), np.uint8)
    
    if inp[0] != 'H' and inp[0] != 'V':
        cv2.putText(img=image, text='Pos 0: invalid H/V value', org=(10, 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(255, 255, 255),thickness=2)
        #print('Check 0 failed')
        return image
    if inp[1] != ':':
        #print('Check 1 failed')
        cv2.putText(img=image, text='Pos 1: no colon', org=(10, 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(255, 255, 255),thickness=2)
        return image

    colors = inp[2:].split(',')
    if len(colors) == 0:
        #print('Check 2 failed')
        cv2.putText(img=image, text='Pos [2->...]: zero array elements', org=(10, 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(255, 255, 255),thickness=2)
        return image

    if inp[0] == 'H': onebar = size / len(colors)
    if inp[0] == 'V': onebar = round(size * 1.6) / len(colors)

    ticker = 0
    
    for i in colors:
        if inp[0] == 'V':
            #print(i,onebar)
            #print(f'0:{size},{ticker}:{int(ticker+onebar)}')

            if colorparse(i) == 0:
                #print('Check 3 failed in value:',i)
                cv2.putText(img=image, text=f'Color code {i} is not valid.', org=(10, 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(255, 255, 255),thickness=2)
                return image
            
            image[0:size,int(ticker):int(ticker+onebar)] = colorparse(i)
            ticker = ticker + onebar
        if inp[0] == 'H':
            #print(i,onebar)
            #print(f'{int(ticker+onebar)},0:{size},{ticker}')

            if colorparse(i) == 0:
                #print('Check 3 failed in value:',i)
                cv2.putText(img=image, text=f'Color code {i} is not valid.', org=(10, 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(255, 255, 255),thickness=2)
                return image

            image[int(ticker):int(ticker+onebar),0:round(size * 1.6)] = colorparse(i)
            ticker = ticker + onebar

    return image
            

 
# generate ace flag
x = generate(500,"H:000000,A4A4A4,FFFFFF,810081")
cv2.imshow('title',x)
cv2.waitKey(0)
cv2.destroyAllWindows()
