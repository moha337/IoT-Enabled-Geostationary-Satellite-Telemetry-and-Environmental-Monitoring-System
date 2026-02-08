import machine
import utime
import uos
from mq2 import MQ2
from gyro import MPU6050
from assistant import *
from pressure import *
from sdcard import *

# UART Communication to ESP32
uart = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))

#i2c configuration
i2c=machine.I2C(0, scl=machine.Pin(1), sda =machine.Pin(0))
devices = i2c.scan()
if devices:
    print(devices)
    
#Mq2 sensor
sensor =MQ2(pinData = 26)
sensor.calibrate()

   #gyro
mpu6050 =MPU6050(i2c)
#pressure
bmp =BMP280(i2c)
calibrate.pressure(bmp)

#Sdcard
spi=machine.SPI(1,sck=machine.Pin(14),mosi=machine.Pin(15),miso=machine.Pin(12))
sd=SDCard(spi)
uos.mount(sd,'/sd')
print("sd card connected")
print(uos.listdir('/sd'))
#creating file name
#myfile = card.newFile(uso.listdir('/sd'))
file_count = len(uos.listdir('/sd'))
myfile = "/sd/data_" + str(file_count) + ".csv"
with open (myfile,"w") as f:
    f.write("Time")
    f.write(",")
    f.write("Pressure")
    f.write(",")
    f.write("Temperature")
    f.write(",")
    f.write("Smoke")
    f.write(",")
    f.write("LPG")
    f.write(",")
    f.write("Methane")
    f.write(",")
    f.write("Hydrogen")
    f.write(",")
    f.write("Ax")
    f.write(",")
    f.write("Ay")
    f.write(",")
    f.write("Az")
    f.write(",")
    f.write("Gx")
    f.write(",")
    f.write("Gy")
    f.write(",")
    f.write("Gz")
    f.write(",")
    f.write("\n")
    while True:
        t =time.ticks_ms()/1000
        pressure = bmp.pressure
        temperature=bmp.temperature
        smoke= sensor.readSmoke()
        LPG = sensor.readLPG()
        Methane = sensor.readMethane()
        Hydrogen = sensor.readHydrogen()
       
        ax=round(mpu6050.accel.x,2)
        ay=round(mpu6050.accel.y,2)
        az=round(mpu6050.accel.z,2)
        gx=round(mpu6050.gyro.x,2)
        gy=round(mpu6050.gyro.y,2)
        gz=round(mpu6050.gyro.z,2)
            # -------- SEND DATA TO ESP32 --------
    send_data = "P:{}|T:{}|S:{}|L:{}|M:{}|H:{}|AX:{}|AY:{}|AZ:{}|GX:{}|GY:{}|GZ:{}\n".format(
        pressure,
        temperature,
        smoke,
        LPG,
        Methane,
        Hydrogen,
        ax,
        ay,
        az,
        gx,
        gy,
        gz
    )

    uart.write(send_data)

    print("Sent to ESP32:", send_data)

        f.write(str(t))
        f.write(",")
        f.write(str(pressure))
        f.write(",")
        f.write(str(temperature))
        f.write(",")
        f.write(str(smoke))
        f.write(",")
        f.write(str(LPG))
        f.write(",")
        f.write(str(Methane))
        f.write(",")
        f.write(str(Hydrogen))
        f.write(",")
        f.write(str(ax))
        f.write(",")
        f.write(str(ay))
        f.write(",")
        f.write(str(az))
        f.write(",")
        f.write(str(gx))
        f.write(",")
        f.write(str(gy))
        f.write(",")
        f.write(str(gz))
        f.write(",")
        f.write("\n")
        f.flush()
        print("our data saved:",t,pressure,temperature,smoke,LPG,Methane,Hydrogen,ax,ay,az,gx,gy,gz)
