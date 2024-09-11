# Untitled - By: Odion - 周日 5月 17 2023

import sensor, image, time, pyb, struct, math

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

uart = pyb.UART(3, 115200, timeout_char = 1000)# 初始化串口
#threshold   = [(0, 33, -14, 26, -11, 127)]#电赛平衡车
#threshold =[(56, 69, 14, 90, 21, 92),
               #(0, 37, -9, 13, -12, 127)]
threshold =[(7, 35, -21, 2, -3, 20)]#电赛跟随车

def find_max(blobs):
    max_size=0
    max_blob = None
    for blob in blobs:
        if blob.pixels() > max_size:
            max_blob = blob
            max_size = blob.pixels()
    return max_blob
    import time
from pyb import Pin

trig = Pin('P0', Pin.OUT_PP)
echo = Pin('P1', Pin.IN)

def distance():
    #trig.high()
    #time.sleep_us(10)
    #trig.low()
    #t0 = time.ticks_us()
    #while echo.value() == 0:
        #t = time.ticks_us()
        #if(t-t0 >= 3000):#防超时
            #return 1
    #t1 = time.ticks_us()
    #while echo.value() == 1:
        #t = time.ticks_us()
        #if(t1-t>=580):#10m
            #return 2
    #t2 = time.ticks_us()
    mm = 0
    #mm = (t2 - t1) * 0.17
    return mm

i=leftblob=0
downblob=midblob1=midblob2=160
downline=220
midline=115
sign=bsign=csign=b=0
ECHO=0
in_angle=out_angle=0

while(True):
    clock.tick()
    img = sensor.snapshot()
    #print(clock.fps())
    blobs = img.find_blobs(threshold, roi=(40,downline-20,200,40), x_stride=20, pixels_threshold=100)#下边
    max_blob = find_max(blobs)
    if max_blob is not None:
        downblob=max_blob.cx()
        #print(max_blob.w())

        if(max_blob.w()>=85):#标识识别发送blob.roundness()可以测圆度，若循迹实在不稳定可以缩小色块宽度限制加入大半径圆判定（在感兴趣区域内画线前判定效果更佳）
            w = max_blob.w()
            while(w >= 85):
                img = sensor.snapshot()
                c = img.find_circles(threshold = 3000, x_margin = 10, y_margin = 10, r_margin = 10,r_min = 30, r_max = 40, r_step = 4)
                if c is not None:
                    i=1
                    #img.draw_circle(c.x(), c.y(), c.r(), color = (255, 0, 0))

                blobs = img.find_blobs(threshold, roi=(40,downline-20,200,40), x_stride=20, pixels_threshold=100,margin = 15)#下边
                max_blob = find_max(blobs)
                if max_blob is not None:
                    downblob=max_blob.cx()
                    #print(max_blob.w())
                    w = max_blob.w()
                else:
                    w = 85
                blobs = img.find_blobs(threshold, roi=(40,midline-15,240,30), x_stride=12, pixels_threshold=80, margin = 15)#中边
                m_max_blob = find_max(blobs)
                if m_max_blob is not None:
                    midblob1=m_max_blob.cx()
                    #print(blobs.w())
                    if m_max_blob in blobs:
                        blobs.remove(m_max_blob)
                        if blobs is not None:
                            m_max_blob = find_max(blobs)
                            if m_max_blob is not None:
                                img.draw_cross(m_max_blob.cx(),midline)
                                midblob2=m_max_blob.cx()
                            else:
                                midblob2=0
                        else:
                            midblob2=0
                    else:
                        midblob2=0
                else:
                    midblob1=666#md跑丢了真的6
                if(midblob1 == 666):
                    in_angle = 666 #md跑丢了真的6
                else:
                    if(midblob2==0):
                        dx1 = downblob - midblob1
                        in_angle = round(math.atan2(105, dx1) * 180 / math.pi)
                        out_angle=0
                        img.draw_string(midblob1,100,str(in_angle))
                        img.draw_arrow(downblob,downline,midblob1,midline)
                    elif(midblob1<midblob2):
                        dx1 = downblob - midblob1
                        in_angle = round(math.atan2(105, dx1) * 180 / math.pi)# Calculate line angle
                        dx2 = downblob - midblob2
                        out_angle = round(math.atan2(105, dx2) * 180 / math.pi)
                        img.draw_string(midblob1,100,str(in_angle))
                        img.draw_string(midblob2,100,str(out_angle))
                        img.draw_arrow(downblob,downline,midblob1,midline)
                        img.draw_arrow(downblob,downline,midblob2,midline)
                    elif(midblob1>midblob2):
                        dx2 = downblob - midblob2
                        in_angle = round(math.atan2(105, dx2) * 180 / math.pi)
                        dx1 = downblob - midblob1
                        out_angle = round(math.atan2(105, dx1) * 180 / math.pi)
                        img.draw_string(midblob2,100,str(in_angle))
                        img.draw_string(midblob1,100,str(out_angle))
                        img.draw_arrow(downblob,downline,midblob1,midline)
                        img.draw_arrow(downblob,downline,midblob2,midline)
                    #print(in_angle,out_angle)
                    ECHO = int(distance())
                    road = struct.pack('IBBBB', in_angle , out_angle, downblob, ECHO, sign)

                    uart.write(road)
                    img.draw_string(260,10,str(ECHO)+"mm")
            if(i==1):
                sign+=1
            print(sign)

    blobs = img.find_blobs(threshold, roi=(40,midline-15,240,30), x_stride=12, pixels_threshold=80, margin = 15)#中边
    m_max_blob = find_max(blobs)
    if m_max_blob is not None:
        midblob1=m_max_blob.cx()
        #print(blobs.w())
        if m_max_blob in blobs:
            blobs.remove(m_max_blob)
            if blobs is not None:
                m_max_blob = find_max(blobs)
                if m_max_blob is not None:
                    img.draw_rectangle(m_max_blob.rect(),(0,0,0),thickness=3)
                    img.draw_cross(m_max_blob.cx(),midline)
                    midblob2=m_max_blob.cx()
                else:
                    midblob2=0
            else:
                midblob2=0
        else:
            midblob2=0
    else:
        midblob1=666#md跑丢了真的6
    img.draw_rectangle(40,midline-15,240,30, (250,0,0), thickness=1)
    img.draw_rectangle(40,downline-20, 240, 40, (250,0,0), thickness=1)

    #for blob in img.find_blobs(threshold, roi=(0,0,40,200), y_stride=5, pixels_threshold=80, merge=True):#左边
        #img.draw_rectangle(blob.rect(),(0,0,0),thickness=3)
        #img.draw_cross(20,blob.cy())
        #leftblob=blob.cy()
        #img.draw_rectangle(0,0 , 40, 200, (250,0,0), thickness=1)



    #img.draw_rectangle(0,100,320,30, (250,0,0), thickness=1, fill=True)
    #0,0 , 40, 240左
    #0,0 , 320, 20上
    #0,100,320,30中
    #0,200 , 320, 40下

    #数据处理和通讯
    if(sign==csign):
        b=0
    elif(b==0 and sign!=csign):
        time_data0 = pyb.millis()
        bsign=sign
        b=1
    if(b==1):
        time_data1 = pyb.millis()
    if(b==1 and (time_data1-time_data0)>1000):
        csign=bsign
        b=0
    else:
        sign=bsign
    if(midblob1 == 666):
        in_angle = 666 #md跑丢了真的6
    else:
        if(midblob2==0):
            dx1 = downblob - midblob1
            in_angle = round(math.atan2(105, dx1) * 180 / math.pi)
            out_angle=0
            img.draw_string(midblob1,100,str(in_angle))
            img.draw_arrow(downblob,downline,midblob1,midline)
        elif(midblob1<midblob2):
            dx1 = downblob - midblob1
            in_angle = round(math.atan2(105, dx1) * 180 / math.pi)# Calculate line angle
            dx2 = downblob - midblob2
            out_angle = round(math.atan2(105, dx2) * 180 / math.pi)
            img.draw_string(midblob1,100,str(in_angle))
            img.draw_string(midblob2,100,str(out_angle))
            img.draw_arrow(downblob,downline,midblob1,midline)
            img.draw_arrow(downblob,downline,midblob2,midline)
        elif(midblob1>midblob2):
            dx2 = downblob - midblob2
            in_angle = round(math.atan2(105, dx2) * 180 / math.pi)
            dx1 = downblob - midblob1
            out_angle = round(math.atan2(105, dx1) * 180 / math.pi)
            img.draw_string(midblob2,100,str(in_angle))
            img.draw_string(midblob1,100,str(out_angle))
            img.draw_arrow(downblob,downline,midblob1,midline)
            img.draw_arrow(downblob,downline,midblob2,midline)
        #print(in_angle,out_angle)
        ECHO = int(distance())
        road = struct.pack('IBBBB', in_angle , out_angle, downblob, ECHO, sign)
        uart.write(road)
        img.draw_string(260,10,str(ECHO)+"mm")

