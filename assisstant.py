import utime
import machine
from basemq import *
from mq2 import *
from dht import *
from gyro import *
from pressure import *
from sdcard import *
from vector3d import *


class card:

    def new_file(files):
        number =0
        need_check = True
        name = "chitti"+str(number)+".csv"

        
        while need_check == True:
            if name in files:
                number = number+1
                name = "chitti"+str(number)+".csv"
            else:
                need_check = False
                return name
      
class dashboard:
    def sendAir(SK=0, LG=0, MN=0,HN=0):
        print("SK:{:.1f}".format(SK)+","+"LG:{:.1f}".format(LG)+","+"MN:{:.1f}".format(MN)+","+"HN:{:.1f}".format(HN))
    
    def sendWoair(Pr=0,temp=32, ax=0, ay=0, az=0, gx=0, gy=0, gz=0):
        Pr=(Pr*0.01)-4.5
        tall = convert.height(Pr) 
        print("P:"+str(Pr)+","+"H:"+str(tall)+","+"T:"+str(temp)+","+"ax:"+str(ax)+","+"ay:"+str(ay)+","+"az:"+str(az)+","+"gx:"+str(gx)+","+"gz:"+str(gy)+","+"gz:"+str(gz))
     
    def sendAll(Pr=0,temp=32,SK=0, LG=0, MN=0, HN=0, ax=0, ay=0, az=0, gx=0, gy=0, gz=0):
        Pr=(Pr*0.01)-4.5
        tall = convert.height(Pr)
        print("SK:{:.1f}".format(SK)+","+"LG:{:.1f}".format(LG)+","+"MN:{:.1f}".format(MN)+","+"HN:{:.1f}".format(HN)+","+"P:"+str(Pr)+","+"H:"+str(tall)+","+"T:"+str(temp)+","+"ax:"+str(ax)+","+"ay:"+str(ay)+","+"az:"+str(az)+","+"gx:"+str(gx)+","+"gz:"+str(gy)+","+"gz:"+str(gz))



    def sendGyro(gx=0, gy=0, gz=0, ax=0, ay=0, az=0):
       print( "ax:"+str(ax)+","+"ay:"+str(ay)+","+"az:"+str(az)+","+"gx:"+str(gx)+","+"gy:"+str(gy)+","+"gz:"+str(gz))
    
    
    def sendPressure(Pr=0,temp=32):
        Pr=(Pr*0.01)-4.5
        tall = convert.height(Pr)
        print("P:"+str(Pr)+","+"H:"+str(tall)+","+"T:"+str(temp))
        
    def sendWeather(Pr=0,temp=32):
        Pr=(Pr*0.01)-4.5
        tall = convert.height(Pr)
        print("P:"+str(Pr)+","+"H:"+str(tall)+","+"T:"+str(temp))
    
class convert:
    def height(pressure):
        local_pressure = pressure   # Unit : hPa
        sea_level_pressure = 1013.25 # Unit : hPa
        pressure_ratio = local_pressure / sea_level_pressure
        altitude = 44330*(1-(pressure_ratio**(1/5.255)))
        return altitude
    
        
class calibrate:
    def pressure(bmp280_object):
        bmp280_object.power_mode = BMP280_POWER_NORMAL

        bmp280_object.oversample = BMP280_OS_HIGH

        bmp280_object.temp_os = BMP280_TEMP_OS_8

        bmp280_object.press_os = BMP280_TEMP_OS_4

        bmp280_object.standby = BMP280_STANDBY_250

        bmp280_object.iir = BMP280_IIR_FILTER_2

