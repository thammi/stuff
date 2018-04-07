#!/usr/bin/env python3

import sys
import re
import os.path
import subprocess

def find_parted():
    locations = ['/sbin/parted']

    for location in locations:
        if os.path.exists(location):
            return location

    return None

def get_partitions(path):
    parted = find_parted()

    # run fsdisk

    cmd = [parted, '-sm', path, 'unit', 'B', 'print']
    raw = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
    out = raw.decode('utf-8').strip()

    lines = list(map(str.strip, out.split('\n')))

    # verify

    if lines[0] != 'BYT;':
        raise Exception("Unable to parse output, unexpected start")

    partitions = []

    for line in lines[2:]:
        parts = line.split(':')

        name = parts[0]

        data = {
            'start': int(parts[1][:-1]),
            'size': int(parts[2][:-1]),
            'fs': parts[4]
        }

        if data['size'] == 0:
            continue

        partitions.append((name, data))

    return partitions

def print_partitions(path, mount_point='/mnt/', loop_dev='/dev/loop1'):
    partitions = get_partitions(path)

    abs_path = os.path.abspath(path)

    for name, data in partitions:
        start = data['start']
        size = data['size']
        fs = data['fs']

        mount = 'mount -o loop,offset={},sizelimit={} {} {}'.format(start, size, abs_path, mount_point)
        losetup = 'losetup -o {} --sizelimit {} {} {}'.format(start, size, loop_dev, abs_path)

        print('{} ({}, {} MB):'.format(name, fs, round(size / 1024 / 1024, 1)))
        print(mount)
        print(losetup)
        print()

def main():
    if len(sys.argv) < 2:
        print("Usage: {} IMAGE [MOUNT_POINT]".format(sys.argv[0]))
        sys.exit(1)

    path = sys.argv[1]
    mount_point = sys.argv[2] if len(sys.argv) > 2 else '/mnt'

    try:
        print_partitions(path, mount_point)
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == '__main__':
    main()

