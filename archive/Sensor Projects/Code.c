#include <stdio.h>
#include <wiringPi.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <wiringPiI2C.h>
#include <time.h>
#define MAXTIMINGS 85
#define DHTPIN 0
char outputFile[] = "/tmp/humiture.csv";
FILE *outFile;
int LCDAddr = 0x27;
int fd;
int dht11_dat[5] = {0,0,0,0,0};
int validData = 0;
int BLEN = 1;
float fahrenheit;

void write_word(int data){
	int temp = data;
	if ( BLEN == 1 )
		temp |= 0x08;
	else
		temp &= 0xF7;
	wiringPiI2CWrite(fd, temp);
}

void send_command(int comm){
	int buf;
	// Send bit7-4 firstly
	buf = comm & 0xF0;
	buf |= 0x04;			// RS = 0, RW = 0, EN = 1
	write_word(buf);
	delay(2);
	buf &= 0xFB;			// Make EN = 0
	write_word(buf);

	// Send bit3-0 secondly
	buf = (comm & 0x0F) << 4;
	buf |= 0x04;			// RS = 0, RW = 0, EN = 1
	write_word(buf);
	delay(2);
	buf &= 0xFB;			// Make EN = 0
	write_word(buf);
}

void send_data(int data){
	int buf;
	// Send bit7-4 firstly
	buf = data & 0xF0;
	buf |= 0x05;			// RS = 1, RW = 0, EN = 1
	write_word(buf);
	delay(2);
	buf &= 0xFB;			// Make EN = 0
	write_word(buf);

	// Send bit3-0 secondly
	buf = (data & 0x0F) << 4;
	buf |= 0x05;			// RS = 1, RW = 0, EN = 1
	write_word(buf);
	delay(2);
	buf &= 0xFB;			// Make EN = 0
	write_word(buf);
}

void init(){
	send_command(0x33);	// Must initialize to 8-line mode at first
	delay(5);
	send_command(0x32);	// Then initialize to 4-line mode
	delay(5);
	send_command(0x28);	// 2 Lines & 5*7 dots
	delay(5);
	send_command(0x0C);	// Enable display without cursor
	delay(5);
	send_command(0x01);	// Clear Screen
	wiringPiI2CWrite(fd, 0x08);
}

void clear(){
	send_command(0x01);	//clear Screen
}

void write(int x, int y, char data[]){
	int addr, i;
	int tmp;
	if (x < 0)  x = 0;
	if (x > 15) x = 15;
	if (y < 0)  y = 0;
	if (y > 1)  y = 1;

	// Move cursor
	addr = 0x80 + 0x40 * y + x;
	send_command(addr);
	
	tmp = strlen(data);
	for (i = 0; i < tmp; i++){
		send_data(data[i]);
	}
}

void read_dht11_dat() {
	uint8_t laststate = HIGH;
	uint8_t counter = 0;
	uint8_t j = 0, i;
	float f; // fahrenheit

	dht11_dat[0] = dht11_dat[1] = dht11_dat[2] = dht11_dat[3] = dht11_dat[4] = 0;

	// pull pin down for 18 milliseconds
	pinMode(DHTPIN, OUTPUT);
	digitalWrite(DHTPIN, LOW);
	delay(18);
	// then pull it up for 40 microseconds
	digitalWrite(DHTPIN, HIGH);
	delayMicroseconds(40); 
	// prepare to read the pin
	pinMode(DHTPIN, INPUT);

	// detect change and read data
	for ( i=0; i< MAXTIMINGS; i++) {
		counter = 0;
		while (digitalRead(DHTPIN) == laststate) {
			counter++;
			delayMicroseconds(1);
			if (counter == 255) {
				break;
			}
		}
		laststate = digitalRead(DHTPIN);

		if (counter == 255) break;

		// ignore first 3 transitions
		if ((i >= 4) && (i%2 == 0)) {
			// shove each bit into the storage bytes
			dht11_dat[j/8] <<= 1;
			if (counter > 16)
				dht11_dat[j/8] |= 1;
			j++;
		}
	}

	// check we read 40 bits (8bit x 5 ) + verify checksum in the last byte
	// print it out if data is good
	if ((j >= 40) && 
			(dht11_dat[4] == ((dht11_dat[0] + dht11_dat[1] + dht11_dat[2] + dht11_dat[3]) & 0xFF)) ) {
		validData=1;
		f = dht11_dat[2] * 9. / 5. + 32;
		fahrenheit = f;
	}
	else
	{
		validData=0;
	}
}

int main(void) {
	int analogVal;
	fd = wiringPiI2CSetup(LCDAddr);
	init();
	outFile = fopen(outputFile, "w");
	fputs("Date-Time,SensorID,Humidity%,Dig-TemperatureC\n",outFile);
	fclose(outFile);
	clear();
	if(wiringPiSetup() == -1) {
		printf("Set up failed");
		exit(1);
	}
	write(0,0,"Initializing...");
	write(0,1,"Temp. & Humid.");	
	delay(2000);
	while (1) 
	{
		read_dht11_dat();
		if(validData==1) {
			outFile = fopen(outputFile, "a");
			clear();
			char dtetme[100];
			time_t now = time(NULL);
			struct tm *t = gmtime(&now);
			strftime(dtetme, sizeof(dtetme)-1, "%m/%d/%Y %H:%M:%S",t);
			printf("%s:Humidity = %d.%d %% Temperature = %d.%d *C (%g *F)\n",dtetme, dht11_dat[0], dht11_dat[1], dht11_dat[2], dht11_dat[3], fahrenheit);
			printf("%d\n",dht11_dat[2]);
			char str[1024];
			snprintf(str, sizeof(str), "H=%d.%d%% T=%d.%d*C\n", dht11_dat[0], dht11_dat[1], dht11_dat[2], dht11_dat[3]);
			write(0,0,"Temp. & Humid.");
			write(0,1, str);
			char data[1024];
			snprintf(data, sizeof(data),"%s,%s,%d.%d%%,%d.%d\n",dtetme,"001",dht11_dat[0],dht11_dat[1],dht11_dat[2], dht11_dat[3]);
			fputs(data,outFile);
			fclose(outFile);
		}
		delay(1200); // wait 1sec to refresh
	}
}