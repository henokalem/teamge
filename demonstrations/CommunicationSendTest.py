import socket   
import sys  
import struct
import time

#main function
if __name__ == "__main__":

    if(len(sys.argv) < 2) :
        print 'Usage : need python client.py hostname'
        sys.exit()
    elif(len(sys.argv) < 3):
        print 'Usage : need pin to activate'
        sys.exit()

    host = sys.argv[1]
    port = 8888


    #create an INET, STREAMing socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print 'Failed to create socket'
        sys.exit()

    print 'Socket Created'

    try:
        remote_ip = socket.gethostbyname( host )
        s.connect((host, port))

    except socket.gaierror:
        print 'Hostname could not be resolved. Exiting'
        sys.exit()

    print 'Socket Connected to ' + host + ' on ip ' + remote_ip

    #Send some data to remote server
    message = str(sys.argv[2])

    try :
        #Set the whole string
        #while True:
        s.send(message)
        print 'Message sent successfully'
            #print 'Closing socket'
            #s.close()
            #sys.exit()
    ##        time.sleep(1)
    ##        print 'Sending...'
            #get reply and print
            #print recv_timeout(s)
##        recieve = s.recv(1024)
##        while(recieve != "Completed"):
##            if(recieve != ""):
##                print recieve
##            recieve = s.recv(1024)
##        print recieve
        print 'Closing Socket'
        s.close()
        sys.exit()
            
            #break
    except socket.error:
        #Send failed
        print 'Send failed'
        sys.exit()





##def recv_timeout(the_socket,timeout=2):
##    #make socket non blocking
##    the_socket.setblocking(0)
##
##    #total data partwise in an array
##    total_data=[];
##    data='';
##
##    #beginning time
##    begin=time.time()
##    while 1:
##        #if you got some data, then break after timeout
##        if total_data and time.time()-begin > timeout:
##            break
##
##        #if you got no data at all, wait a little longer, twice the timeout
##        elif time.time()-begin > timeout*2:
##            break
##
##        #recv something
##        try:
##            data = the_socket.recv(8192)
##            if data:
##                total_data.append(data)
##                #change the beginning time for measurement
##                begin=time.time()
##            else:
##                #sleep for sometime to indicate a gap
##                time.sleep(0.1)
##        except:
##            pass
##
##    #join all parts to make final string
####    s.close()
##    return ''.join(total_data)






