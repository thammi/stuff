#!/usr/bin/env python3

import sys
import re
import os.path
import subprocess

def find_sfdisk():
    locations = ['/sbin/sfdisk']

    for location in locations:
        if os.path.exists(location):
            return location

    return None

def parse_line(line):
    start = line.find(':')

    name = line[:start].strip()

    obj = {}

    for part in line[start+1:].split(','):
        parts = [i.strip() for i in part.split('=', 1)]

        if len(parts) == 2:
            key, raw = parts

            if re.match('\d+', raw):
                value = int(raw)
            else:
                value = raw

            obj[key] = value
        else:
            key = parts[0]
            obj[key] = True

    return name, obj

def to_bytes(value):
    return value * 512

def get_partitions(path):
    sfdisk = find_sfdisk()

    # run fsdisk

    cmd = [sfdisk, '-ld', path]
    raw = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    out = raw.decode('utf-8').strip()

    # looks like actual output?

    if not re.search('^# partition table of ', out):
        raise Exception("sfdisk seems to be unable to read the image")

    # find start of table

    start = out.index('\n\n')

    if start == -1:
        raise Exception("Unable to parse output, cannot find start of table")

    # parse table

    lines = out[start:].split('\n')[2:]

    partitions = []

    for line in lines:
        name, data = parse_line(line)

        if data['size'] == 0:
            continue

        partitions.append((name, data))

    return partitions

def print_partitions(path, mount_point):
    partitions = get_partitions(path)

    abs_path = os.path.abspath(path)

    for name, data in partitions:
        mount = 'mount -o loop,offset={} {} {}'.format(to_bytes(data['start']), abs_path, mount_point)
        size = to_bytes(data['size']) / 1024 / 1024

        print('{} ({} MB):'.format(name, size))
        print(mount)
        print()

def main(args):
    if len(args) < 2:
        print("Usage: {} IMAGE [MOUNT_POINT]".format(args[0]))
        return 1

    path = args[1]
    mount_point = args[2] if len(args) > 2 else '/mnt'

    try:
        print_partitions(path, mount_point)
    except Exception as e:
        print(e)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

