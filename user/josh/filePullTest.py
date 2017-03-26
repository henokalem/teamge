import os
path="/home/pi/Desktop/JMRI/lib"  # insert the path to the directory of interest here
dirList=os.listdir(path)
for fname in dirList:
    #print fname
    if(".jar" in fname):
        print fname
