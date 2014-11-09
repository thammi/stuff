# image mount

This script is designed to help you mount disk images. It will parse the
partition table of the image using `sfdisk` and print the mount command for each
partition.

Example usage:

    $ ./image_mount.py test.img
    test.img1
    size:   3000.0 MB
    mount:  mount -o loop,offset=1048576 /tmp/test.img /mnt

    test.img2
    size:   11258.0 MB
    mount:  mount -o loop,offset=3146776576 /tmp/test.img /mnt

You can add the desired mount point as the second option for convenience.

