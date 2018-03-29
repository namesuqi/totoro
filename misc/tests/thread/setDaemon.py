import time
import random
import threading


def run(i):
    t = random.randint(1, 10)
    time.sleep(t)
    print str(i) +" ;I sleep %d second." % (t)


tsk = []
for i in xrange(0, 5):
    time.sleep(0.1)
    t = threading.Thread(target=run, args=(i, ))
    t.setDaemon(True)


    t.start()

time.sleep(10)
print "This is the end of main thread."