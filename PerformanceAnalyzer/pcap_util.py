import os
import csv
import subprocess


class PcapToCSV(object):
    def __init__(self, pcap_path, remove=False):
        self.pcap_path = pcap_path
        self.csv_path = self._execute_tshark()
        self.remove = remove

    def __del__(self):
        if self.remove:
            if os.path.exists(self.csv_path):
                os.remove(self.csv_path)

    def _execute_tshark(self):
        pcap_path = self.pcap_path
        csv_path = '.'.join((pcap_path.split('.'))[:-1]) + '.csv'
        command = ('tshark -Y "tcp or udp" -T fields '
                   '-e frame.time_relative -e ip.proto -e ip.src '
                   '-e ip.len '
                   '-e tcp.srcport -e udp.srcport -e ip.dst -e tcp.dstport -e udp.dstport '
                   '-e tcp.flags.syn -e tcp.flags.ack -e tcp.flags.fin '
                   '-e ssl.handshake '
                   '-e dns.a -e dns.qry.name '
                   '-E header=y -E separator=, '
                   '-E quote=d '
                   '-r {0} > {1}').format(self.pcap_path, csv_path)
        subprocess.run(command, shell=True)
        return csv_path

    def get_csv_path(self):
        return self.csv_path


def parse_pcap_csv(csv_path):
    times = list()
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            times.append(float(row['frame.time_relative']))
    return times