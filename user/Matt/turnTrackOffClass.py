import csv

#sets the train config file to turn off the track when read next
class trainOff:
    def __init__(self):
        a=0


    def turnTrainOff(self):
        f = open('/home/pi/teamge/user/josh/trainProperties.txt')
        oldFile = []

        #reader for the CSV file
        reader = csv.reader(f)


        # put old file into list
        for line in reader:
            oldFile.append(line)


        f.close()
        oldFile[0][0] = "False"

        writeFile = open('/home/pi/teamge/user/josh/trainProperties.txt', 'w')
        write = csv.writer(writeFile)
        for line in oldFile:
            write.writerow(line)
        writeFile.close()

        return
