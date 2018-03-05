import httplib
from urlparse import urlparse
from datetime import datetime
import time
import signal
import urllib2
from stripogram import html2text
import codecs


class Timeout():
    """Timeout class using ALARM signal."""
    class Timeout(Exception):
        pass
 
    def __init__(self, sec):
        self.sec = sec
 
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)
 
    def __exit__(self, *args):
        signal.alarm(0)    # disable alarm
 
    def raise_timeout(self, *args):
        raise Timeout.Timeout()

def checkUrl(url):
    try:
	    p = urlparse(url)
	    
	    #data = conn.getresponse()
	    try:
		with Timeout(2):
			conn = httplib.HTTPConnection(p.netloc)
	    		conn.request('HEAD', p.path)
    			data = conn.getresponse()
    	    except:
		return False
           
	 	
	    return data.status < 400	
	    
	    	
    except:
	    return False

if __name__ == '__main__':
	f = open('uk2002-spamlabels1.txt')
	f1 = open('uk2002-working.txt',"wb")
	line = f.readline()
	i = 0;
	while line:
		print i
		i = i + 1;
		space = line.split()
		site = 'http://'+ space[0];
		##print site;
		##print checkUrl(site)
		now = time.time()
		if(checkUrl(site)):
				later = time.time()
				difference = int(later - now)
				try:
					with Timeout(5):
						file("docs/"+space[0]+".txt", "w").write(html2text(urllib2.urlopen(site).read()))
					print site + " " + str(difference)
					f1.write(site + " " + space[1]+" "+str(difference)+"\n")
				except:
					print(site + " " + "non-responsive\n")
    		line = f.readline()
	f.close()
	f1.close()


