import csv

class directionChanger:
    def __init__(self):
        a=1


    def changeDirection(self, ID):
        f = open('/home/pi/teamge/user/josh/trainProperties.txt')
        oldFile = []

        #reader for the CSV file
        reader = csv.reader(f)


        # put old file into list
        for line in reader:
            oldFile.append(line)


        #change direction
        for item in oldFile:
            if item[0] == str(ID):
                if item[2] == "True":
                    item[2] = "False"
                else:
                    item[2] = "True"


        f.close()


        writeFile = open('/home/pi/teamge/user/josh/trainProperties.txt', 'w')
        write = csv.writer(writeFile)
        for line in oldFile:
            write.writerow(line)
        writeFile.close()

        return
