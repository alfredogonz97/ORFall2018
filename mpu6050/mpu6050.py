###############################################################################
#Created on Sun Oct 28 00:14:40 2018
#
#@author: Alfredo
#
#Module for the MPU6050
###############################################################################

import smbus

# default values for the I2C setup
channel = 1 # channel that the MPU6050 module is connected to
address = 0x68 # i2c address that the MPU6050 module is on
bus = smbus.SMBus(channel) # set the i2c bus that the MPU6050 is connected to

###############################################################################
#Functions to read/write to/from i2c node
###############################################################################

def i2c_read_byte(reg):
    # read a byte of data from a specified register
    global bus, address
    return bus.read_byte_data(address, reg)

def i2c_read_word(reg):
    # read a word (two bytes) from a specified register, assumes the two bytes 
    # that make up the word are in consecutive registers
    high = i2c_read_byte(reg)
    low = i2c_read_byte(reg+1)
    return (high << 8) + low

def i2c_write_byte(reg,val):
    global bus, address
    bus.write_byte_data(address,reg,val)
    
def reverse_2s_compliment(val):
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
    
###############################################################################
# Functions to get and set the i2c properties of the MPU6050
###############################################################################

def get_i2c_channel():
    # read the channel that the MPU6050 module is connected to on the pi
    return channel

def get_i2c_address():
    # read the address that the MPU6050 module is at
    return address

def set_i2c_channel(val):
    global bus, channel
    channel = val
    bus = smbus.SMBus(channel)
    
def set_i2c_address(val):
    global address
    address = val
    
def setup_i2c(channel,addr):
    set_i2c_channel(channel)
    set_i2c_address(addr)

###############################################################################
# Set Gyroscope sample rate, where 
# Sample Rate = GyroscopeOutputRate / (1 + SMPRT_DIV)
# The sample rate for the accelerometer is always 1 KHz
###############################################################################

def set_SMPRT_DIV(val):
    # set SMPLRT_DIV
    i2c_write_byte(0x19,val)
    
def get_SMPRT_DIV():
    return i2c_read_byte(0x19)

def set_CONFIG(val):
    # CONFIG: | Bit 7 | Bit 6 | Bit 5 | Bit 4 | Bit 3 | Bit 2 | Bit 1 | Bit 0 |
    #         |   X   |   X   |    EX_SYNC_SET[2:0]   |     DLPF_CFG[2:0]     |
    # DLPF is the digital low pass filter where the three bits control 
    # the gyroscope output rate, etiher 8 or 1 KHz. Accelerometer sample rate 
    # is always 1 KHz
    i2c_write_byte(0x1A,val)
    
def get_CONFIG():
    return i2c_read_byte(0x1A)

###############################################################################
# Read accelerometer data
###############################################################################

def accel_x():
    return reverse_2s_compliment(i2c_read_word(0x3B))

def accel_y():
    return reverse_2s_compliment(i2c_read_word(0x3D))

def accel_z():
    return reverse_2s_compliment(i2c_read_word(0x3F))

###############################################################################
# Read internal temperature measurements
###############################################################################

def temperatureRaw():
    # Returns the raw data from the registers
    temp = i2c_read_word(0x41)
    if((temp >> 7) == 1): # check if the value is negative
        return -(temp & 0x7F)
    else:
        return temp

def temperatureC():
    # returns temperature in Celsius
    temp = i2c_read_word(0x41) #is a signed value
    if((temp >> 7) == 1): # check if the value is negative
        temp = -(temp & 0x7F)
    return (temp / 340.0) + 36.53

###############################################################################
# Read Gyroscope data
###############################################################################
    
def gyro_x():
    return reverse_2s_compliment(i2c_read_word(0x43))

def gyro_y():
    return reverse_2s_compliment(i2c_read_word(0x45))

def gyro_z():
    return reverse_2s_compliment(i2c_read_word(0x47))

###############################################################################
# Set the PWR_MGMT_1 and PWR_MGMT_2 Register, and some of the individual bits 
# in these registers
###############################################################################
    
def read_PWR_MGMT_1():
    return i2c_read_byte(0x6B)

def set_PWR_MGMT_1(val):
    i2c_write_byte(0x6B,val)
    
def read_PWR_MGMT_2():
    return i2c_read_byte(0x6C)

def set_PWR_MGMT_2(val):
    i2c_write_byte(0x6C,val)

def sleep(val):
    hold = read_PWR_MGMT_1()
    up = hold & 0x80
    low = hold & 0x3F
    if(val == True):
        i2c_write_byte(0x6B, up + (1 << 6) + low) # activate sleep bit
    else:
        i2c_write_byte(0x6B, up + (0 << 6) + low) # turn off sleep bit
        
def enable_temperature_sensor(val):
    hold = read_PWR_MGMT_1()
    up = hold & 0xF0
    low = hold & 0x07
    if(val == True):
        i2c_write_byte(0x6B, up + (1 << 3) + low) # activate 
    else:
        i2c_write_byte(0x6B, up + (0 << 3) + low) # turn off 
        
def enable_reset(val):
    hold = read_PWR_MGMT_1()
    low = hold & 0x7F
    if(val == True):
        i2c_write_byte(0x6B, (1 << 7) + low) # activate 
    else:
        i2c_write_byte(0x6B, (0 << 7) + low) # turn off 
    
###############################################################################
# Default initialization for the MPU 6050
###############################################################################

def default_initialize():
    set_SMPRT_DIV(0)
    set_CONFIG(0)
    set_PWR_MGMT_1(0)
    set_PWR_MGMT_2(0)
    