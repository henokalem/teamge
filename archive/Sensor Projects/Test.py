#!/usr/bin/env python
import i2clibraries
import Adafruit_BMP.BMP085 as BMP085
from i2clibraries import i2c_hmc5883l
import time
hmc5883l = i2c_hmc5883l.i2c_hmc5883l(1)
bmp085 = BMP085.BMP085()

if __name__ == '__main__':
    hmc5883l.setContinuousMode()
    hmc5883l.setDeclination(0,6)
    print(hmc5883l)
    print(bmp085)
