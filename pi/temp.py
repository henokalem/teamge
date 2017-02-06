from Adafruit_BMP import BMP085

bmp085 = BMP085.BMP085()
print("{}".format(bmp085.read_temperature()))
