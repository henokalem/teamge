HOW TO OPERATE:

The TrainLocationFinal.py file is the program we currently use to keep track of the trains using the pi. Before running the file, make sure that:
-The SPROG is plugged in, and JRMI Panel Pro is on (for using JMRI, see the JMRI readme)
-The turnout power source is plugged in
-The Power Box for the large breadboard is plugged in (power source for the relays and beam breakers)
-Set up the trains on the track in the segments you want them to be in

Steps to start the trains running:
1. Set up the trains in the segments you want them to start in (for segment numbers, see the picture of the track). It is recommended that you start trains in non-adjacent segments as this will allow the trains the greatest opportunity to initialize without messing each other up.
2. Start the program. To run the program from the terminal, use the command "sudo python TrainLocationFinal.py <train1startsegment> <train1startSpeed> <train2startsegment> <train2startSpeed>" where you insert the values you want for the train start segments and speed (speed can be in the values of [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]).
3. Run the script ScriptPowerAndFile.py using Panel Pro and going to Panel->Run Script... (Make sure to start the script only after all turnouts are initialized and it is past the wait time used to ignore beam breaker noise from the Arduino. A safe bet is starting the script a little after 10 seconds after the program is started).
