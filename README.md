# This is my portfolio of work as I begin learning python

# realcheck2.py
The first file I've uploaded is "realcheck2.py" which is a tool that was written to help analyze which file systems are due for a file system check (fsck). In preparing to patch all our hosts we realized that the maintenance window may be impacted if there were larger file systems that would require a fsck on the next reboot.

Fsck happens based on either the time (180 days after creation) or number of mounts (vs. a maximum number of mounts) and the time it will take to run is variable based on the file system type, size, and other factors.  The time had too many variables to consider so I just tried to indicate which would fsck and organize the output to highlight the larger file systems.

It was designed to read in a comma seperated file and refine/highlight which are set for fsck.  The data it reviews should be in this format:
hostname,filesystem,fstype,size,mountcount,maxmounts,interval,checkafterdate

In order to get the data, the following command was executed on all the hosts and consolidated into a file:

for i in $(df -PlT -B 1M -t ext2 -t ext3 -t ext4 | grep -v Filesystem | awk '{OFS=","; print $1,$2,$3}'); do echo ${i},$(tune2fs -l ${i%%,*} | awk -F ": +" '/ount count|Check interval|Next check after/ {ORS=",";gsub(/ \(.*\)/, "", $2);print $2}'); done

NOTE: I need to update it because I was using a hard coded MAINTENANCE_DAY = "Sun Jan 17 23:01:02 2016", but should probably make the MAINTENANCE_DAY = current date/time so manual changes to realcheck2.py aren't needed for future runs.
