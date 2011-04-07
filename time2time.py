#!/usr/bin/env python

"""
Simple script to convert between GPS, Unix, NTP times and smth. human readable.
The human readable time is your LOCAL time, not GMT, unless -u option is specified
"""

import optparse, time

NTP2UNIX         = 2208988800 # seconds from NTP to UNIX epoch
UNIX2GPS         = 315964800  # seconds from UNIX to GPS epoch
GPS_LEAP_SECONDS = 15         # leap seconds since GPS epoch (as of 6/14/2009)
USE_UTC          = False

def __parse_args():
    import sys
    usage =    """
    %prog [--gh|--uh|--nh|--gu|--nu|--hu|--ug|--ng|--hg|--un|--gn|--hn] time

    Convert between NTP, Unix, GPS and human readable time formats at will.
    Note that human readable times are in your local time zone unless --utc is specified.
    When converting from human readable form, the expected format is
    the default one used by python's strptime, e.g.,
    "Thu Apr 7 18:42:31 2011" and is *always* interpreted in local time zone
    """
    parser = optparse.OptionParser(usage)
    parser.add_option("--gh", dest="gh", action="store_true",
                      help="GPS time to human readable")
    parser.add_option("--uh", dest="uh", action="store_true",
                      help="Unix time to human readable")
    parser.add_option("--nh", dest="nh", action="store_true",
                      help="NTP time to human readable")
    
    parser.add_option("--gu", dest="gu", action="store_true",
                      help="GPS time to Unix time")
    parser.add_option("--nu", dest="nu", action="store_true",
                      help="NTP time to Unix time")
    parser.add_option("--hu", dest="hu", action="store_true",
                      help="human readable to Unix time")

    parser.add_option("--ug", dest="ug", action="store_true",
                      help="Unix time to GPS time")
    parser.add_option("--ng", dest="ng", action="store_true",
                      help="NTP time to GPS time")
    parser.add_option("--hg", dest="hg", action="store_true",
                      help="human readable to GPS time")

    parser.add_option("--un", dest="un", action="store_true",
                      help="Unix time to NTP time")
    parser.add_option("--gn", dest="gn", action="store_true",
                      help="GPS time to NTP time")
    parser.add_option("--hn", dest="hn", action="store_true",
                      help="human readable to NTP time")
    parser.add_option("-u", "--utc", dest="utc", action="store_true",
                      help="Print human-readable times in UTC/GMT instead of local time zone")


    options, args = parser.parse_args()

    if options.utc and (options.hu or options.hn or options.hn):
        raise Exception("Can't use --utc when converting from human readable format")

    if options.utc:
        global USE_UTC
        USE_UTC = True
    del options.__dict__['utc']

    # check that specified options/arguments make sense
    opts_dict = options.__dict__
    opts_values = opts_dict.values()
    opts_values[0] = {True:1,None:0}[opts_values[0]]
    nopts = reduce(lambda x,y: x + {True:1,None:0}[y], opts_values)
    if nopts != 1:
        print "Exactly one of the conversion options must be selected, run with -h for help"
        sys.exit(1)
    if len(args) != 1: 
        print "Exactly one argument must be specified, run with -h for help"
        sys.exit(1)

    return (options, args[0])

def __unixtime_to_string(unixtime):
    if USE_UTC:
        gmtime = time.gmtime(int(unixtime))
        return time.strftime("%a %b %d %H:%M:%S %Y GMT", gmtime)
    else:
        gmtime = time.localtime(int(unixtime))
        return time.strftime("%a %b %d %H:%M:%S %Y %Z", gmtime)

def __human_to_unix(humantime):
    localtime = time.strptime(humantime)
    return int(time.mktime(localtime))

def __unix_to_ntp(unixtime):
    ntptime = int(unixtime) + NTP2UNIX
    return ntptime

def __unix_to_gps(unixtime):
    gpstime = int(unixtime) - UNIX2GPS + GPS_LEAP_SECONDS
    return gpstime

def gps_to_human(gpstime):
    print "GPS to human: ", 
    unixtime = int(gpstime) + UNIX2GPS - GPS_LEAP_SECONDS
    print __unixtime_to_string(unixtime)

def unix_to_human(unixtime):
    print "Unix to human: ",
    print __unixtime_to_string(unixtime)

def ntp_to_human(ntptime):
    print "NTP to human: ",
    unixtime = int(ntptime) - NTP2UNIX
    print __unixtime_to_string(unixtime)

def gps_to_unix(gpstime):
    print "GPS to Unix: ", 
    unixtime = int(gpstime) + UNIX2GPS - GPS_LEAP_SECONDS
    print unixtime

def ntp_to_unix(ntptime):
    print "NTP to Unix: ", 
    unixtime = int(ntptime) - NTP2UNIX
    print unixtime

def human_to_unix(humantime):
    print "Human to Unix: ",
    print __human_to_unix(humantime)

def unix_to_gps(unixtime):
    print "Unix to GPS: ",
    print __unix_to_gps(unixtime)

def ntp_to_gps(ntptime):
    print "NTP to GPS: ",
    gpstime = int(ntptime) - UNIX2GPS - NTP2UNIX + GPS_LEAP_SECONDS
    print gpstime

def human_to_gps(humantime):
    print "Human to GPS: ",
    print __unix_to_gps(__human_to_unix(humantime))

def unix_to_ntp(unixtime):
    print "Unix to NTP: ",
    print __unix_to_ntp(unixtime)

def gps_to_ntp(gpstime):
    print "GPS to NTP: ",
    ntptime = int(gpstime) + UNIX2GPS + NTP2UNIX - GPS_LEAP_SECONDS
    print ntptime

def human_to_ntp(humantime):
    print "Human to NTP: ",
    print __unix_to_ntp(__human_to_unix(humantime))


if __name__ == "__main__":
    options, tm = __parse_args()
    if options.gh:
        gps_to_human(tm)
    elif options.uh:
        unix_to_human(tm)
    elif options.nh:
        ntp_to_human(tm)
    elif options.gu:
        gps_to_unix(tm)
    elif options.nu:
        ntp_to_unix(tm)
    elif options.hu:
        human_to_unix(tm)
    elif options.ug:
        unix_to_gps(tm)
    elif options.ng:
        ntp_to_gps(tm)
    elif options.hg:
        human_to_gps(tm)
    elif options.un:
        unix_to_ntp(tm)
    elif options.gn:
        gps_to_ntp(tm)
    elif options.hn:
        human_to_ntp(tm)
