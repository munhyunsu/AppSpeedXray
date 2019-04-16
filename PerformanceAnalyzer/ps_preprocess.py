import sys
import csv

from file_util import get_files, parse_xml_log, parse_top_log
from image_util import get_ssim, is_white
from pcap_util import PcapToCSV, parse_pcap_csv

FPS = 1


def get_sp_si(path):
    apps = dict()
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            # if float(row[2]) <= 100 and eval(row[1])[0] == 0:
            if float(row[2]) <= 100:
                # print(row)
                continue
            item = apps.get(row[0], list())
            item.append([eval(row[1]), float(row[2])])
            apps[row[0]] = item
    return apps


def get_si(apps):
    for key in apps.keys():
        item = apps[key]
        new_item = list()
        for entry in item:
            new_item.append(entry+[(entry[0][1]+1-entry[0][0])/FPS])
        apps[key] = new_item
    return apps


def get_fp(snap_path, apps):
    for key in apps.keys():
        files = get_files(snap_path + key)
        files.sort()
        item = apps[key]
        new_item = list()
        # for split, speedindex in item:
        for entry in item:
            white_scene = False
            fp = entry[0][1]
            for index in range(entry[0][0], entry[0][1]+1):
                white_result = is_white(files[index])
                if not white_result and white_scene:
                    fp = index
                    break
                if white_result:
                    white_scene = True
            if fp == entry[0][1]:
                for index in range(entry[0][0], entry[0][1]):
                    sim_result = get_ssim(files[index], files[index + 1])
                    if sim_result <= 0.9:
                        fp = index+1
                        break
            fp = fp-entry[0][0]
            new_item.append(entry+[(fp+1)/FPS])
        apps[key] = new_item
    return apps


def get_ll(xml_path, apps):
    for key in apps.keys():
        files = get_files(xml_path + key)
        item = apps[key]
        cuts_t = dict()
        for path in files:
            sec = int((path.split('/')[-1]).split('.')[0])
            ln = parse_xml_log(path)
            cuts_t[sec] = ln
        new_item = list()
        for entry in item:
            ll = 0
            xml_count = 0
            for index in range(entry[0][1], entry[0][0]-1, -1):
                if index in cuts_t.keys():
                    if xml_count != cuts_t[index] and xml_count != 0:
                        ll = index
                        break
                    else:
                        xml_count = cuts_t[index]
            if ll != 0:
                ll = ll-(entry[0][0])/FPS
            new_item.append(entry+[ll])
        apps[key] = new_item
    return apps


def get_cs(top_path, apps):
    for key in apps.keys():
        files = get_files(top_path + key)
        item = apps[key]
        top_t = dict()
        for path in files:
            sec = int((path.split('/')[-1]).split('.')[0])
            tv = parse_top_log(path)
            top_t[sec] = tv
        new_item = list()
        for entry in item:
            cs = 0
            for index in range(entry[0][1], entry[0][0]-1, -1):
                if index in top_t.keys():
                    if top_t[index] == 0:
                        cs = index
                        break
            if cs == 0:
                cs = entry[0][1]+1
            cs = cs-(entry[0][0])/FPS
            new_item.append(entry+[cs])
        apps[key] = new_item
    return apps


def get_rt(pcap_path, apps):
    for key in apps.keys():
        item = apps[key]
        path = pcap_path+key+'.pcap'
        pcap_reader = PcapToCSV(path)
        csv_path = pcap_reader.get_csv_path()
        times = parse_pcap_csv(csv_path)
        new_item = list()
        for entry in item:
            ltime = 0
            for ctime in times:
                if ctime > (entry[0][1]+1)/FPS:
                    break
                else:
                    ltime = ctime
            rt = (entry[0][1]+1)/FPS - ltime
            new_item.append(entry+[rt])
        apps[key] = new_item
    return apps


def export_csv(path, apps):
    with open(path, 'w') as f:
        writer = csv.writer(f)
        for key in apps.keys():
            for scene in apps[key]:
                writer.writerow([key] + scene)


def main(_):
    print(FLAGS, _)
    apps = get_sp_si(FLAGS.speedindex)
    # print(apps)
    apps = get_si(apps)
    # print(apps)
    apps = get_fp(FLAGS.temp, apps)
    # print(apps)
    apps = get_ll(FLAGS.xmldir, apps)
    # print(apps)
    apps = get_cs(FLAGS.topdir, apps)
    # print(apps)
    apps = get_rt(FLAGS.pcapdir, apps)
    # print(apps)
    export_csv(FLAGS.outputfile, apps)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='Root directory of experiment files')
    parser.add_argument('-t', '--temp', type=str, required=True,
                        help='Snapshots directory')
    parser.add_argument('-s', '--speedindex', type=str, required=True,
                        help='Speedindex result file')
    parser.add_argument('-o', '--output', type=str, required=True,
                        help='Output directory')
    parser.add_argument('-f', '--fps', type=int, default=30,
                        help='Frame per second of snapshot')

    FLAGS, _ = parser.parse_known_args()

    FLAGS.input = os.path.abspath(os.path.expanduser(FLAGS.input))
    FLAGS.xmldir = os.path.join(FLAGS.input, 'xml')
    FLAGS.topdir = os.path.join(FLAGS.input, 'top')
    FLAGS.pcapdir = os.path.join(FLAGS.input, 'pcap')
    FLAGS.temp = os.path.abspath(os.path.expanduser(FLAGS.temp))
    FLAGS.speedindex = os.path.abspath(os.path.expanduser(FLAGS.speedindex))
    FLAGS.output = os.path.abspath(os.path.expanduser(FLAGS.output))
    FLAGS.outputfile = os.path.join(FLAGS.output, 'ps-raw.csv')

    main(_)

