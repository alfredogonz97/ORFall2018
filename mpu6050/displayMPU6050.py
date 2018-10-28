
# Created on Sat Oct 27 20:47:19 2018
#
# @author: Alfredo
#
# Python program that reads acceleration and gyroscope data from 
# the MPU 6050

import mpu6050
from time import sleep

mpu6050.setup_i2c(1,0x68)
mpu6050.default_initialize()

while True:
    # write header
    print("MPU 6050 Data\n")
    print("---------------------\n\n")
    
    print("Addr:\t{}\n".format(mpu6050.get_i2c_address()))
    print("Channel:\t{}\n\n".format(mpu6050.get_i2c_channel()))
    
    # read gyroscope datasu
    gyro_x = mpu6050.gyro_x()
    gyro_y = mpu6050.gyro_y()
    gyro_z = mpu6050.gyro_z()
                      
    # read accelerometer data
    accel_x = mpu6050.accel_x()
    accel_y = mpu6050.accel_y()
    accel_z = mpu6050.accel_z()
    
    # print data
    print("Gyro X:\t{}\n".format(gyro_x))
    print("Gyro Y:\t{}\n".format(gyro_y))
    print("Gyro Z:\t{}\n\n".format(gyro_z))
    
    print("Accel X:\t{}\n".format(accel_x))
    print("Accel Y:\t{}\n".format(accel_y))
    print("Accel Z:\t{}\n\n".format(accel_z))
    sleep(1)