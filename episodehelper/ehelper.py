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

import sys
import os
import os.path

from subprocess import Popen

#media_player = "smplayer"
media_player = "smplayer '%s'"
error_cmd = "kdialog --msgbox '%s'"
media_extensions = ['.avi', '.mpg', '.mkv', '.rmvb', '.ogg', '.mp3']

class InvalidPointerException(Exception):

    def __init__(self, pointer):
        self.pointer = pointer

    def __str__(self):
        return pointer

class CollectionBoundException(Exception):
    pass

def read_list(path):
    for rel in sorted(os.listdir(path), key=str.lower):
        abs_path = os.path.join(path, rel)
        if os.path.isdir(abs_path):
            for sub in read_list(abs_path):
                yield sub
        elif os.path.splitext(rel)[1].lower() in media_extensions:
            yield abs_path

class Collection:

    def __init__(self, root="."):
        self.root = root
        self.pointer = self.load_pointer()
        self.ls = list(read_list(root))

    def save(self):
        self.save_pointer(self.pointer)

    def load_pointer(self):
        pointer_file = self.pointer_file()
        if os.path.isfile(pointer_file):
            f = open(pointer_file)
            pointer = f.readline().strip()
            f.close()
            return pointer
        else:
            return None

    def save_pointer(self, pointer):
        pointer_file = self.pointer_file()
        if pointer == None:
            if os.path.isfile(pointer_file):
                os.remove(pointer_file)
        else:
            f = open(pointer_file, 'w')
            f.write(pointer + '\n')
            f.close()

    def pointer_file(self):
        return os.path.join(self.root, ".ehelp")

    def pointer_index(self):
        pointer = self.pointer
        ls = self.ls

        if pointer == None:
            return -1
        elif pointer in ls:
            return ls.index(pointer)
        else:
            raise InvalidPointerException(pointer)

    def environment(self, extent):
        index = self.pointer_index()
        ls = self.ls

        for jump in range(-extent, extent + 1):
            cur = index + jump
            if 0 <= cur < len(ls):
                yield jump, ls[cur]

    def move(self, diff=1):
        ls = self.ls

        new = self.pointer_index() + diff

        if 0 <= new < len(self.ls):
            self.pointer = ls[new]
        else:
            raise CollectionBoundException()

    def reset(self):
        self.pointer = None

    def fix(self):
        raise NotImplementedError()

def play(coll):
    return os.system(media_player % coll.pointer)

def error_msg(msg):
    if sys.stdout.isatty():
        print("ERROR: " + msg)
    else:
        return os.system(error_cmd % msg)

def forward(coll):
    try:
        coll.move(1)
    except CollectionBoundException:
        error_msg("End of collection reached. Add new files or reset to keep watching!")
    else:
        coll.save()
        play(coll)

def repeat(coll):
    play(coll)

def jump(coll):
    for diff, file_name in coll.environment(3):
        print("%2i: %s" % (diff, file_name))

    inp = input("Jump to? ")
    coll.move(int(inp))

    coll.save()
    play(coll)

def reset(coll):
    coll.reset()
    coll.save()

def fix(coll):
    coll.fix()
    coll.save()

def main(argv):
    commands = {
            'forward': forward,
            'repeat': repeat,
            'jump': jump,
            'reset': reset,
            'fix': fix,
            }

    cmd = argv[0] if len(argv) else 'forward'

    if cmd in commands:
        coll = Collection()
        commands[cmd](coll)
    else:
        print("Command not known. Try a valid one ;)")
        for cmd in sorted(commands):
            print("-", cmd)

if __name__ == '__main__':
    main(sys.argv[1:])

