# image mount

## What is this?

This script is designed to help you mount disk images. It will parse the
partition table of the image using `sfdisk` and print the mount command for each
partition.

## Usage

Example usage:

    $ ./image_mount.py test.img
    test.img1 (3000.0 MB):
    mount -o loop,offset=1048576 /tmp/test.img /mnt

    test.img2 (11258.0 MB):
    mount -o loop,offset=3146776576 /tmp/test.img /mnt

You can add the desired mount point as the second option for convenience.

## Installation

Check out this repository and run

    ./setup.py install --user

in this directory.

You have to have `sfdisk` installed.

