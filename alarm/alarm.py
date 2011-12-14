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
# ./alarm.py TIME[h/m/s] [..] [-- finish message]

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

def message(msg):
    system(MSG_CMD % msg)

start = time()

# get a time
if len(argv) > 1:
    raw = argv[1:]
else:
    raw = raw_input("Enter time to wait: ").split()

# do we have a message?
if "--" in raw:
    split = raw.index("--")

    msg = " ".join(raw[split+1:])
    raw = raw[:split]

    msg += " " * max(0, 8 - len(msg))
else:
    msg = "Time is up!"

# available time factors
factors = {
        's': 1,
        'm': 60,
        'h': 60 * 60,
        }

wait = 0

for part in raw:
    # factor parsing, if any (defaults to seconds)
    if part[-1] in factors:
        factor = factors[part[-1]]
        number = part[:-1]
    else:
        factor = 1
        number = part

    # determine end point (TODO: parsing might fail with an exception)
    wait += int(number) * factor

if wait <= 0:
    message("Did not have to wait at all")
    sys.exit(1)

target = start + wait

try:
    while time() < target:
        # get a nice output
        left = int(target - time() + 0.1)
        parts = (left / 60 / 60, left / 60 % 60, left % 60)
        display("%02i:%02i:%02i " % parts)

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
    message(msg)

