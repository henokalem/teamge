import jarray
import jmri

class MovementTest(jmri.jmrit.automat.AbstractAutomaton):

    def init(self):
        print "Inside init(self, id)"
        self.throttle = self.getThrottle(1, False)
        return

    def handle(self):
        print "Inside handle(self)"
        # set loco to forward
        print "Set Loco Forward"
        self.throttle.setIsForward(True)
        
        # wait 1 second for engine to be stopped, then set speed
        self.waitMsec(1000)                 
        print "Set Speed"
        self.throttle.setSpeedSetting(0.7)

        # wait for run time in forward direction
        print "Wait for forward time"
        self.waitMsec(10000)
        
        # stop the engine
        print "Set Speed Stop"
        self.throttle.setSpeedSetting(0)

        return 0

print "Starting"
MovementTest().start()
