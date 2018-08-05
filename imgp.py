import numpy as np
import cv2 as cv
import os

dir = 'img/'

def symButterfly(fname):
    img = cv.imread(fname)
    h = img.shape[0]
    w = img.shape[1]
    imgRight = img[0:h,int(0.52*w):w]
    imgLeft = cv.flip(imgRight,1)
    img = np.concatenate((imgLeft,imgRight),1)
    img = cv.resize(img,(128,128),interpolation=cv.INTER_CUBIC)
    return img

def main():
    for roots,dirs,files in os.walk(dir):
        for file in files:
            try:
                rimg = symButterfly(dir+str(file))
                cv.imwrite('data/'+file.replace('png','jpg'),rimg)
            except:
                print(file)
if __name__ == '__main__':
    main()
