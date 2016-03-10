#!/usr/bin/env python

import datetime
import calendar
import os

from operator import itemgetter

if 'COLUMNSORT' in os.environ:
    sortcol=int(os.environ['COLUMNSORT'])
else:
    sortcol=3

data = []

'''
hostname,filesystem,fstype,size,mountcount,maxmounts,interval,checkafterdate
host19.example.com,/dev/sda1,ext3,99,41,-1,0,
host32.example.com,/dev/mapper/VolGroup01-LV_FPCMPRR1,ext4,2016,
host65.example.com,/dev/mapper/ofhpcdvg1-LV_DVFHPCD1,ext3,75596,2,32,15552000,Mon Jun 15 18:09:20 2015,
host197.example.com,/dev/mapper/ofhpcsvg1-LV_DVFHPCS1,ext3,40318,2,39,15552000,Mon Jun 15 18:09:44 2015,
host53.example.com,/dev/mapper/vg00-bladelogic,ext4,1952,4,-1,0,
'''

MAINTENANCE_DAY = "Sun Jan 17 23:01:02 2016"
mds = datetime.datetime.strptime(MAINTENANCE_DAY, "%a %b %d %H:%M:%S %Y")


with open('small-data.txt', 'r+') as f:
    for line in f:
        if line.strip():
            parts = line.strip().split(',')

            # ignore bad data
            if len(parts) < 7:
                continue

            maxmount_disabled = False
            mnt_fsck_date_old = False
            mnt_interval_invalid = False
            mnt_count_exceeded = False
            mnt_date_empty = False

	    for idx,x in enumerate(parts):
		if x.isdigit():
		    parts[idx] = int(x)
	    parts[3] = int(parts[3])
            mntcount = int(parts[4])
            maxmount = int(parts[5])
            interval = int(parts[6])
            datestr = parts[7]

            if mntcount >= maxmount:
                mnt_count_exceeded = True

            if maxmount == 0 or maxmount == -1:
                maxmount_disabled = True

            if int(interval) == 0:
                mnt_interval_invalid = True

            if datestr == "":
                mnt_date_empty = True

            if not mnt_date_empty:
                # https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
                try:
                    ds = datetime.datetime.strptime(datestr, "%a %b %d %H:%M:%S %Y")
                except:
                    print "bad date: %s" % datestr
                    import pdb; pdb.set_trace()

                if calendar.timegm(ds.timetuple()) < calendar.timegm(mds.timetuple()):
                    mnt_fsck_date_old = True



            fsck = False
            if not mnt_date_empty:
                if (not maxmount_disabled) and (not mnt_interval_invalid):
                    if mnt_count_exceeded or mnt_fsck_date_old:
                        fsck = True
            if fsck:
                #print "#################################################"
                #print parts[0],parts[1]
		#data.append(','.join(parts))
		data.append(parts)
		#import pdb; pdb.set_trace()
data.sort(key=itemgetter(sortcol),reverse=True)
for row in data:
    tmprow = [str(x) for x in row]
    if int(row[3]) > 100000:
        print '\033[91m' + ",".join(tmprow) + '\033[0m'
    else:
        print ",".join(tmprow)
