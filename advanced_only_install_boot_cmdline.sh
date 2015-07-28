#!/bin/bash

exit_if_failed() {
    if [ $? -ne 0 ]; then
	echo "ABORT: Previous step failed"
	exit 1
    fi
}

mount -o remount,rw /boot
exit_if_failed
if [ -f /boot/cmdline.bk ]; then
    echo "omit bk old cmdline - already exists"
else    
    cp /boot/cmdline.txt /boot/cmdline.bk
fi
cp related_scripts/cmdline.txt /boot/cmdline.txt
exit_if_failed
echo "SUCCESS"
