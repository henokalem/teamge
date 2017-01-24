#include <wiringPi.h>
#include <wiringPiI2C.h>
#include <stdio.h>
#include <pcf8591.h>
#define TEMPSENSORPIN 2
#define PCF 120
int ANALOGCONTROL = 0x48;
int AC;
int main(void) {
	pinMode(TEMPSENSORPIN, INPUT);
	pcf8591Setup(PCF, 0x48);
	if(wiringPiSetup() == -1) {
		printf("Setup failed.");
		return(1);
	}
	float val,degC,degF;
	while(1) {
		int read = digitalRead(TEMPSENSORPIN);
		printf("Digital Reading: %d\n",read);
		val = analogRead(PCF+0);
		degC = (val - 0.5) * 100.0;
		degF = degC * (9.0/5.0) + 32.0;
		printf("Analog:%f3 *C (%f3 *F)\n",degC,degF);
		delay(1000);
	}
}