#!/bin/bash

#to simulate disk corruption: unmount it first then: dd if=/dev/urandom of=/dev/mmcblk0p3 bs=64 count=100

EDL_DISK_DEV="/dev/mmcblk0p3"

exit_if_failed() {
    if [ $? -ne 0 ]; then
	echo "ABORT: Previous step failed"
	exit 1
    fi
}

df | grep ecodroidlink_data

if [ $? = 0 ]; then
    echo "edl_data_prepare: test ecodroidlink_data parition pass - exit."
    exit 0
fi

#below two would normally fail but it's not a problem
rmdir /ecodroidlink_data
mkdir /ecodroidlink_data

echo 'edl_data_prepare: try mount it'
mount -t ext4 "$EDL_DISK_DEV" /ecodroidlink_data

if [ $? = 0 ]; then
    echo "edl_data_prepare: mount success - exit."
    #below for cases after re-format of parition and the folder is not there
    #linked from /var/lib/bluetooth
    mkdir /ecodroidlink_data/bluetooth
    exit 0
fi

echo "edl_data_prepare: mount failed - format the partition again then remount..."
#if control reaches here then htis means the mount fialed

mkfs.ext4 "$EDL_DISK_DEV"

if [ $? = 0 ]; then
    echo "edl_data_prepare: format parition success."
fi

echo 'edl_data_prepare: try mount it again'
mount -t ext4 "$EDL_DISK_DEV" /ecodroidlink_data

if [ $? = 0 ]; then
    echo "edl_data_prepare: mount success after format - exit."
    #below for cases after re-format of parition and the folder is not there
    #linked from /var/lib/bluetooth
    mkdir /ecodroidlink_data/bluetooth
    exit 0
fi

echo "edl_data_prepare: mount still failed - abort"

