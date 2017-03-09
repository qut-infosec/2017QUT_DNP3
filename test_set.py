__author__ = 'Nicholas Rodofile'
import csv
import sys
import os
import subprocess

#filename = 'master_control'
proto = '_ws.col.Protocol'
GOOSE = 'GOOSE'
DNP3 = 'DNP 3.0'
TCP = 'TCP'
ARP = 'ARP'
ETH_SRC = 'eth.src'
ATTACKER = '00:10:18:cb:8c:13'


def AnalyseTsharkData(data, filename, directory):
    output = {
        ATTACKER: [],
        GOOSE: [],
        DNP3: [],
        TCP: [],
        ARP: []
    }

    #with open(directory+'/'+filename+'.csv', 'rb') as csvfile:
    frames = csv.DictReader(data)
    for f in frames:
        #print f
        if f[proto] == GOOSE and filename != 'attacker':
            output[GOOSE].append(f)
        if f[proto] == DNP3:
            output[DNP3].append(f)
        if f[proto] == ARP:
            output[ARP].append(f)
        if f[proto] == DNP3 or f[proto] == TCP:
            output[TCP].append(f)
        if f[ETH_SRC] == ATTACKER:
            output[ATTACKER].append(f)

    for o in output:
        times = {}
        for l in output[o]:
            #print int(float(l['frame.time_relative']))
            if int(float(l['frame.time_relative'])) in times:
                times[int(float(l['frame.time_relative']))] += 1
            else:
                times[int(float(l['frame.time_relative']))] = 1
        if not os.path.isdir(directory+'/tshark/'):
            os.makedirs(directory+'/tshark/')

        if len(times) > 0:
            print len(times)
            a = sorted(times.keys())[len(times)-1]
            for tic in range(0, a):
                if tic not in times:
                    times[tic] = 0
            with open(directory+'/tshark/'+filename+'.'+o+'.csv', 'wb') as f:
                for t in sorted(times):
                    f.write(str(t) + " " + str(times[t]) + "\n")

    # for o in output:
    #     with open(filename+'/'+filename+'.'+o+'.csv', 'wb') as f:
    #         writer = csv.writer(f)
    #         for l in output[o]:
    #             writer.writerow([l['frame.time_relative']])

if __name__ == '__main__':
    directory = sys.argv[1]
    # filename = sys.argv[2]
    pcaps = ["slave.pcap", "master.pcap", "attacker.pcap"]
    for p in pcaps:
        filename_ = directory + "/" + p
        tshark = ["tshark", "-T", "fields", "-n", "-r", filename_, "-E", "separator=,", "-E", "header=y", "-e",
                  "frame.time_relative", "-e", "eth.src", "-e", "eth.dst", "-e", "ip.src", "-e", "ip.dst", "-e", "_ws.col.Protocol"]
        print "Tshark Analysis", p
        proc = subprocess.Popen(tshark, stdout=subprocess.PIPE)
        tmp = proc.stdout.read()

        print "Analysing Tshark Output:", p
        AnalyseTsharkData(tmp.splitlines(), p, directory)