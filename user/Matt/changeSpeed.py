import csv


class speedChanger:
    def __init__(self):
        a=0

    def changeSpeed(self, ID, speed):
        f = open('/home/pi/teamge/user/josh/trainProperties.txt')
        oldFile = []

        #reader for the CSV file
        reader = csv.reader(f)


        # put old file into list
        for line in reader:
            oldFile.append(line)

        #print oldFile

        #change speed
        for item in oldFile:
            if item[0] == str(ID):
                item[1] = str(speed)
        
        f.close()


        ## Write to file
        writeFile = open('/home/pi/teamge/user/josh/trainProperties.txt', 'w')
        write = csv.writer(writeFile)
        for line in oldFile:
            write.writerow(line)
        writeFile.close()

        return


