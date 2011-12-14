#!/usr/bin/env python
##############################################################################
##
##  Copyright (C) 2010 Thammi
##  
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##  
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##  
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
##############################################################################

# Usage:
# ./alarm.py TIME[h/m/s] [finish message]

from sys import argv, exit, stdout
from time import time, sleep
from os import system

# change to your favorite sound
SOUND_FILE = "/usr/share/sounds/k3b_success1.wav"

# obvious dependencies ;)
SOUND_CMD = "mplayer '%s' > /dev/null &"
#MSG_CMD = "zenity --info --text '%s'"
MSG_CMD = "kdialog --msgbox '%s'"

def display(txt):
    stdout.write("\r")
    stdout.write(txt)
    stdout.flush()

start = time()

# get a time
if len(argv) > 1:
    raw = argv[1]
else:
    raw = raw_input("Enter time to wait: ")

# do we have a message?
if len(argv) > 2:
    msg = " ".join(argv[2:])
    msg += " " * max(0, 8 - len(msg))
else:
    msg = "Time is up!"

# available time factors
factors = {
        's': 1,
        'm': 60,
        'h': 60 * 60,
        }

# factor parsing, if any (defaults to seconds)
if raw[-1] in factors:
    factor = factors[raw[-1]]
    raw = raw[:-1]
else:
    factor = 1

# determine end point (TODO: parsing might fail with an exception)
wait = int(raw) * factor
target = start + wait

try:
    while time() < target:
        # get a nice output
        left = int(target - time() + 0.1)
        parts = (left / 60 / 60, left / 60 % 60, left % 60)
        display("\r%02i:%02i:%02i " % parts)

        # wait for the next full second
        sleep((target - time()) % 1)
except KeyboardInterrupt:
    display("Interrupted by the user!")
    print

    exit(1)
else:
    display(msg)
    print

    system(SOUND_CMD % SOUND_FILE)
    system(MSG_CMD % msg)

