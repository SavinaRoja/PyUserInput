# -*- coding: iso-8859-1 -*-

#   Copyright 2010 Pepijn de Vos
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from pymouse import PyMouse
import random, time
try:
    from pymouse import PyMouseEvent

    class event(PyMouseEvent):
        def move(self, x, y):
            print "Mouse moved to", x, y

        def click(self, x, y, button, press):
            if press:
                print "Mouse pressed at", x, y, "with button", button
            else:
                print "Mouse released at", x, y, "with button", button

    e = event()
    #e.capture = True
    e.start()

except ImportError:
    print "Mouse events are not yet supported on your platform"

m = PyMouse()
try:
	size = m.screen_size()
	print "size: %s" % (str(size))

	pos = (random.randint(0, size[0]), random.randint(0, size[1]))
except:
	pos = (random.randint(0, 250), random.randint(0, 250))

print "Position: %s" % (str(pos))

m.move(pos[0], pos[1])

time.sleep(2)

m.click(pos[0], pos[1], 1)

time.sleep(2)

m.click(pos[0], pos[1], 2)

time.sleep(2)

m.click(pos[0], pos[1], 3)

try:
    e.stop()
except:
    pass
