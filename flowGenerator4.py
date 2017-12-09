import numpy as np
import random
import time
import subprocess




def voip(src, dst, time, rand_port):
    print 'VOIP STARTS %s to %s: port:%s' % (src.IP(), dst.IP(), rand_port)
    report = 'reportVOIP_%s_to_%s_port_%s.txt' % (src.IP(), dst.IP(), rand_port)

    cmd_src = 'iperf -c %s -p %s -u -mss 160 -b 6BE_COUNT00 -S 184  -fk -i 3 -t %s &' % (dst.IP(), rand_port, time)
    cmd_dst = 'iperf -s -p %s -u -mss 160 -b 6BE_COUNT00 -S 184 -fk -i 3 | tee %s &' % (rand_port, report)

    src.cmd(cmd_src)
    dst.cmd(cmd_dst)


def voip2(start, src, dst, port, duration, delay):
    if 6000 < port < 7000:
        qos_type = 1
    if 7000 < port < 8000:
        qos_type = 0
    if 999 < port < 2001:
        qos_type = 2

    print 'VOIP STARTS %s to %s: port:%s' % (src.IP(), dst.IP(), port)
    rec_report = './log/%s_reciever_reportVOIP_%s_to_%s_port_%s_%s.log' % (start, src.IP(), dst.IP(), port, qos_type)
    send_report = './log/%s_sender_reportVOIP_%s_to_%s_port_%s_%s.log' % (start, src.IP(), dst.IP(), port, qos_type)

    signal_port = port + 9000

    cmd_src = '../D-ITG/bin/ITGSend -T UDP -rp %s -a %s -c 1000 -d %s -C 200 -t %s -Sdp %s -l %s -x %s &' % (
    port, dst.IP(), delay * 1000, duration * 1000, signal_port, send_report, rec_report)
    cmd_dst = '../D-ITG/bin/ITGRecv -Sp %s &' % (signal_port)

    src.cmd(cmd_src)
    dst.cmd(cmd_dst)


def voip3(src, dst, time, rand_port, delay=0):
    print 'VOIP STARTS %s to %s: port:%s' % (src.IP(), dst.IP(), rand_port)
    # rec_report='./log/reciever_reportVOIP_%s_to_%s_port_%s.log' % (src.IP(), dst.IP(),rand_port)
    rec_report = 'reciever.log'
    send_report = 'sender.log'
    # send_report='./log/sender_reportVOIP_%s_to_%s_port_%s.log' % (src.IP(), dst.IP(),rand_port)

    # cmd_src='iperf -c %s -p %s -u -mss 160 -b 6BE_COUNT00 -S 184  -fk -i 3 -t %s &' % (dst.IP(),rand_port,time)
    # cmd_dst='iperf -s -p %s -u -mss 160 -b 6BE_COUNT00 -S 184 -fk -i 3 | tee %s &' %(rand_port,report)

    cmd_src = '/home/ubuntu/D-ITG/bin/ITGSend -T UDP -rp %s -a %s -d %s-c 1000 -C 1000 -t 20000 -l %s -x %s &' % (
    rand_port, dst.IP(), delay, rsend_ec_report)
    cmd_dst = '/home/ubuntu/D-ITG/bin/ITGRecv &'

    src.cmd(cmd_src)
    dst.cmd(cmd_dst)


def ftp(src, dst, time):
    print 'FTP STARTS %s to %s' % (src.IP(), dst.IP())
    report = 'reportFTP_%s_to_%s.txt' % (src.IP(), dst.IP())

    cmd_src = 'iperf -c %s -p 21 -fk -i 3 -m -t %s &' % (dst.IP(), time)
    cmd_dst = 'iperf -s -p 21 -i 3 -w 8K | tee %s &' % (report)

    src.cmd(cmd_src)
    dst.cmd(cmd_dst)


def scp(src, dst, time):
    print 'SCP STARTS %s to %s' % (src.IP(), dst.IP())
    report = 'reportSCP_%s_to_%s.txt' % (src.IP(), dst.IP())

    cmd_src = 'iperf -c %s -p 22 -fk -i 3 -m -t %s &' % (dst.IP(), time)
    cmd_dst = 'iperf -s -p 22 -i 3 -w 64K | tee %s &' % (report)

    src.cmd(cmd_src)
    dst.cmd(cmd_dst)


def socket_exist(traffic, src_host, dst_host, dst_port):
    # print 'traffic-socket: %s' % (traffic)

    lent = len(traffic)
    for i in range(lent):
        pair = traffic[i]
        (start_time, src, dst, port, duration, delay) = pair
        # src_host == src or
        if [dst_host == dst] and dst_port == port:
            return 'match'

    return 'correct'


####################################################################
####################################################################
####################################################################
####################################################################

def create_topology(p=0):
    import numpy as np
    print p
    traffic = {}
    print 'hahhahahaa'
    sorted_start = sorted(np.random.randint(RUN_TIME, size=BE_COUNT))


    durations = np.random.randint(low=MIN_DURATION, high=MAX_DURATION, size=BE_COUNT)
    delays = np.random.randint(low=0, high=5, size=BE_COUNT)
    j = 0
    while j < BE_COUNT:
        src = nodes[random.randint(0, 13)]
        dst = nodes[random.randint(0, 13)]
        port = np.random.randint(low=1000, high=2000)

        match = 'false'

        if socket_exist(traffic, src, dst, port) is 'match' or src == dst:
            print 'SOCKET_EXIST ERROR %s %s === j:%s' % (dst, port, j)
        else:

            start_time = sorted_start[j]
            duration = durations[j]
            delay = delays[j]
            traffic[j] = (start_time, src, dst, port, duration, delay)
            j = j + 1
            app = 'voip'
            str = "%s, %s, %s %s, %s, %s, %s, %s\n" % (start_time, src, dst, port, duration, delay, app, match)
            f.write(str)

    print '####################################################################'
    print '####################################################################'

    ####################################################################
    ####################################################################
    # BW traffic port= 6200-6209

    traffic1 = {}
    sorted_start1 = sorted(np.random.randint(RUN_TIME, size=BW_COUNT))
    durations = np.random.randint(low=MIN_DURATION, high=MAX_DURATION, size=BW_COUNT)
    delays = np.random.randint(low=0, high=5, size=BW_COUNT)

    j = 0
    while j < BW_COUNT:
        src = nodes[random.randint(0, 13)]
        dst = nodes[random.randint(0, 13)]
        port = np.random.randint(low=6200, high=6210)

        match = 'false'

        if socket_exist(traffic1, src, dst, port) is 'match' or src == dst:
            print 'SOCKET_EXIST ERROR %s %s === j:%s' % (dst, port, j)
        else:

            start_time = sorted_start1[j]
            duration = durations[j]
            delay = delays[j]
            traffic1[j] = (start_time, src, dst, port, duration, delay)
            j = j + 1
            app = 'voip'
            str = "%s, %s, %s %s, %s, %s, %s, %s\n" % (start_time, src, dst, port, duration, delay, app, match)
            f.write(str)

    print '####################################################################'
    ####################################################################
    # delay traffic port= 7200-7209
    traffic2 = {}
    sorted_start2 = sorted(np.random.randint(RUN_TIME, size=DELAY_COUNT))
    durations = np.random.randint(low=MIN_DURATION, high=MAX_DURATION, size=DELAY_COUNT)
    delays = np.random.randint(low=0, high=5, size=DELAY_COUNT)

    j = 0
    while j < DELAY_COUNT:
        src = nodes[random.randint(0, 13)]
        dst = nodes[random.randint(0, 13)]
        port = np.random.randint(low=7200, high=7210)

        match = 'false'

        if socket_exist(traffic2, src, dst, port) is 'match' or src == dst:
            print 'SOCKET_EXIST ERROR %s %s === j:%s' % (dst, port, j)
        else:

            start_time = sorted_start2[j]
            duration = durations[j]
            delay = delays[j]
            traffic2[j] = (start_time, src, dst, port, duration, delay)
            j = j + 1
            app = 'voip'
            str = "%s, %s, %s %s, %s, %s, %s, %s\n" % (start_time, src, dst, port, duration, delay, app, match)
            f.write(str)

    print '####################################################################'
    f.close()
    print '####################################################################'


####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
def run_simulation():
    # simulation schedule duration is currently 30  sec. Max Simulation 30+30 Sec.
    j = 0  # BE traffic
    k = 0
    m = 0
    print sorted_start
    print sorted_start1
    print sorted_start2
    for i in range(RUN_TIME):
        time.sleep(1)
        print 'Second: %s' % (i)

        if i in sorted_start:
            print '++++++ Best Effort'
            count = sorted_start.count(i)
            while 0 < count:
                (start_time, src, dst, port, duration, delay) = traffic[j]

                voip2(start_time, src, dst, port, duration, delay)
                count = count - 1
                j = j + 1

        if i in sorted_start1:
            print '$$$$$$ BW Traffic'
            count = sorted_start1.count(i)
            while 0 < count:
                (start_time, src, dst, port, duration, delay) = traffic1[k]

                voip2(start_time, src, dst, port, duration, delay)
                count = count - 1
                k = k + 1

        if i in sorted_start2:
            print '###### Delay Traffic'
            count = sorted_start2.count(i)
            while 0 < count:
                (start_time, src, dst, port, duration, delay) = traffic2[m]

                voip2(start_time, src, dst, port, duration, delay)
                count = count - 1
                m = m + 1

    print "flows are done !!!"

    time.sleep(60)
    execfile("ditgDec.py")
    print 'txt conversion completed!'
    time.sleep(5)
    execfile("excel.py")
    ####################################################################


    subprocess.call("rm ./log/*", shell=True)
    subprocess.call("rm ./logtxt/*", shell=True)
    # os.system('rm -rf ./logtxt/ && mkdir ./logtxt/')

    print './log and ./logtxt folders cleaned!'

    f = open('myfile', 'w')


####################################################################
####################################################################
print '####################################################################'

# All mininet Nodes
nodes = [h1, h1a, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h12a]

BE_COUNT = 50
BW_COUNT = 10
DELAY_COUNT = 10
RUN_TIME = 100
MIN_DURATION = 30
MAX_DURATION = 40
sorted_start = {}
sorted_start1 = {}
sorted_start2 = {}
traffic = {}
traffic1 = {}
traffic2 = {}
f = open('myfile', 'w')

print BW_COUNT
# Create Same Traffic Matrix
random.seed(321)
np.random.seed(42)

create_topology(2)
print 'I created topology'

print 'Statistic.csv is created!'
print "Good bye!"





