Michael,

The TrainLocation.py file is the program we currently use to keep track of the trains using the pi. Ideally this is the location program we would port to Predix. Currently, it uses an infinite loop to read from the Arduino serial ports as well as update the trains. When it finds a number from the Arduino serial port (indicating that a beam breaker with that ID went off) it calls the activateBreaker method (line 199), which is used initially to get the initial train direction and speed, and is then used after that to make corrections to train speed and location. We are guessing if we ported this code to Predix, we would then have to change this line to instead call a Predix Microservice that would utilize the activateBreaker method.  We are guessing we would also want a Predix Microservice that would be used in place of our UpdateTrains() method (line 205), which is called once every loop to update the location of the trains on the track, as well as check for collisions. Then in order to communicate back to the pi from Predix, we would need to fix the bodies of the methods switchTurnout (line 318) and changeTrainSpeed (line 747) to send messages back to the pi regarding either what turnout needs to be switched, which train needs to have its speed changed and by how much, or what color to change the light to. Specifically, currently the lines of code that actually achieve this are the lines

os.system("sudo python /home/pi/teamge/user/Matt/activatePin.py " + str(pin_num)) (line 1297)
This calls a program which activates the pin (specifically the one passed in as an argument) on the pi necessary to turn a relay to the correct state.

and

os.system("python /home/pi/teamge/user/Matt/changeSpeedOfficial.py " + str(train.train_id) + " " + str(new_speed)) (line 749, 82, and 88)
This changes the speed of a train by running a program which takes in arguments of train_id and new_speed, and then changes the file that controls the train speeds. Lines 82 and 88 are the calls that initially start the trains moving at the beginning. The call at line 749 is the call that changes speed to avoid collisions.

and the lines in lightHandler.py

os.system("sudo python /home/pi/teamge/user/Matt/setGreen.py") (line 23)
os.system("sudo python /home/pi/teamge/user/Matt/setYellow.py") (line 37)
os.system("sudo python /home/pi/teamge/user/Matt/setRed.py") (line 51)
These call various programs on the computer which change the color of the GE Logo light we have.


Currently the program is set up to take in four inputs:

train1_segment: This is the starting segment of train 1. If 0, this means that the train is currently not on the tracks.

train1_speed: This is the starting speed of train 1. The number is a floating point number between 0.0 and 1.0, increasing by tenths (0.0,0.1,0.2,0.3,...,0.9,1.0)

train2_segment: This is the starting segment of train 2. If 0, this means that the train is currently not on the tracks.

train2_speed: This is the starting speed of train 2. The number is a floating point number between 0.0 and 1.0, increasing by tenths (0.0,0.1,0.2,0.3,...,0.9,1.0)


We are not sure how moving this to Predix would affect taking in arguments like this does on command line. If we needed to hardcode the values in for now, the values we would most likely want to use are:

train1_segment: 3
train1_speed: 0.7
train2_segment: 1
train2_speed: 1.0


Please let us know if you have any questions.

Josh Schwallier: 
phone:616-340-6899 
e-mail:schwal10@msu.edu

Matt Sopata
Phone: 708-767-0707
e-mail: sopatama@msu.edu

Lucas Reynolds
Phone: 810-908-0956
e-mail: reyno392@msu.edu