# encoding: UTF-8
import Image
import numpy
import math
import os
import time

#三维空间中球坐标转换为直角坐标
#徑向距離、天頂角、方位角，分別標記為 (r,\ \theta,\ \phi)
def Spherical2Cartesian (r, theta, phi):
    x = r  * math.sin(theta) * math.cos(phi)
    y = r  * math.sin(theta) * math.sin(phi)
    z = r * math.cos(theta)
    return (x, y, z)

#三维空间中直角坐标转球面坐标
def Cartesian2Spherical (x, y, z):
    r = math.sqrt(x**2 + y**2 + z**2)
    theta = math.atan2(math.sqrt(x**2 + y**2), z)
    phi = math.atan2(y, x)
    return (r, theta, phi)

def f ((x, y, z), R):
    (r, theta, phi) = Cartesian2Spherical(x, y, z)
    H = int(math.pi * R)
    (E, N) = (R * phi, R * theta)
    (E, N) = (int(E) % (2*H), int(N) % H)
    return (E, N)

for root, dirs, files in os.walk("./TraImg/"):
    for filename in files:
        Img = Image.open("./TraImg/"+filename) #读取原图，得到图像高度信息
        #Img.save('./Fronts/'+ os.path.splitext(filename)[0]+'.jpg')
        H = Img.size[1]
        R = int(H / math.pi)
        ImgClip = Image.new('RGBA',(2 * R, 2 * R)) #实例一张新画布，尺寸为2R*2R
        #右手坐标系，编码如下
        #0 法向量为(0,0,1)的平面 5 法向量为(0,0,-1) 顶面和底面
        #1->(1,0,0); 3->(-1,0,0) 垂直于x轴的面
        #2->(0,1,0); 4->(0,-1,0) 垂直于y轴的面
        ImgClipArr = numpy.array(ImgClip)
        dataArr = numpy.array(Img)
        print str(Img.mode) + "  " + str(Img.size) + "  " + str(Img.format) + "  R=" + str(R) + " Begin " + str(time.ctime())
        for i in range (0, 6):
            #xx和yy 用于指定画布上的像素坐标
            for yy in range(0, 2*R):
                for xx in range(0 , 2*R):
                    if    i == 0:    z = R;           x = xx - R;             y = yy - R
                    elif i == 5:    z = -1 * R;    x = -1 * (xx - R);             y = yy - R
                    elif i == 1:    x = R;           y = xx - R;             z = yy - R
                    elif i == 3:    x = -1 * R;    y = -1 * (xx - R);      z = yy - R
                    elif i == 2:    y = R;           x = -1 * (xx - R);      z = yy - R
                    elif i == 4:    y = -1 * R;    x = xx - R;             z = yy - R
                    EN = f((x,y,z),R)
                    #print str((x,y,z)) + " => " + str(EN)
                    (E, N) = EN
                    #print EN
                    for j in range(0, 3):
                        ImgClipArr[(2*R-1) - yy, xx, j] = dataArr[N, E, j]
            ImgClip = Image.fromarray(ImgClipArr)
            print "       " + os.path.splitext(filename)[0]+'_'+str(i)+'.jpg    ' + str(time.ctime())
            ImgClip.save('./Fronts/'+ os.path.splitext(filename)[0]+'_'+str(i)+'.jpg')