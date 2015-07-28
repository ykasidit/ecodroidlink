#!/bin/bash

exit_if_failed() {
    if [ $? -ne 0 ]; then
	echo "ABORT: Previous step failed"
	exit 1
    fi
}

mount -o remount,rw /
exit_if_failed
cp related_scripts/systemd_networkd/* /etc/systemd/network/
exit_if_failed
echo "SUCCESS"
