#!/usr/bin/python

import logging
import daemon
from socket import gethostname;
from pymouse import PyMouse
import random, time
from signal import signal, SIGINT

with daemon.DaemonContext():

    def stop(signum, frame):
	cleanup_stop_thread();
	sys.exit()
    signal(SIGINT, stop)

    try:
	from pymouse import PyMouseEvent

	class event(PyMouseEvent):
	    def __init__(self):
		super(event, self).__init__()
		FORMAT = '%(asctime)-15s ' + gethostname() + ' touchlogger %(levelname)s %(message)s'
		logging.basicConfig(filename='/var/log/mouse.log', level=logging.DEBUG, format=FORMAT)

	    def move(self, x, y):
		pass

	    def click(self, x, y, button, press):
		if press:
		    logging.info('{ "event": "click", "type": "press", "x": "' + str(x) + '", "y": "' + str(y) + '"}') 
		else:
		    logging.info('{ "event": "click", "type": "release", "x": "' + str(x) + '", "y": "' + str(y) + '"}') 

	e = event()
	e.capture = False
	e.daemon = False
	e.start()

    except ImportError:
	logging.info('{ "event": "exception", "type": "ImportError", "value": "Mouse events unsupported"}') 
	sys.exit()

    m = PyMouse()
    try:
	    size = m.screen_size()
	    logging.info('{ "event": "start", "type": "size", "value": "' + str(size) + '"}') 
    except:
	    logging.info('{ "event": "exception", "type": "size", "value": "undetermined problem"}') 
	    sys.exit()

    try:
	    e.join()
    except KeyboardInterrupt:
	    e.stop()
	    sys.exit()

