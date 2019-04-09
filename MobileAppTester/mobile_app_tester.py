import os
import sys
import shutil
import csv
import subprocess
import datetime
import xml.etree.ElementTree as ET
import random
import re
import time

FLAGS = None


def setup_android(path):
    command = 'adb shell su -c cp {0} /sbin/tcpdump'.format(path)
    command_check(command)
    command = 'adb shell su -c chmod +x /sbin/tcpdump'
    command_check(command)


def check_binary(binaries):
    for binary in binaries:
        if shutil.which(binary) is None:
            raise FileNotFoundError


def check_dirs(dirs):
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)


def clear_env(pss):
    for ps in pss:
        command = 'adb shell "ps | grep {0}"'.format(ps)
        try:
            output = command_output(command)
        except subprocess.CalledProcessError:
            continue
        psnum = re.findall('\d+', output)[0]
        command = 'adb shell su -c kill -9 {0}'.format(psnum)
        command_check(command)


def terminate_env(pss):
    for ps in pss:
        command = 'adb shell "ps | grep {0}"'.format(ps)
        try:
            output = command_output(command)
        except subprocess.CalledProcessError:
            continue
        psnum = re.findall('\d+', output)[0]
        command = 'adb shell su -c kill -2 {0}'.format(psnum)
        command_check(command)


def command_popen(command):
    return subprocess.Popen(command, shell=True)


def command_check(command):
    return subprocess.check_call(command, shell=True)


def command_output(command):
    return subprocess.check_output(command, shell=True).decode('utf-8')


def write_relative_timing(start_time):
    pass


def send_ping():
    command = 'adb shell su -c ping -c 1 -w 1 -I wlan0 127.0.0.1'
    return command_popen(command)


def terminate_ping(ping_proc):
    try:
        ping_proc.communicate(timeout=1)
    except subprocess.TimeoutExpired:
        ping_proc.kill()
        ping_proc.communicate()


def get_second_from_start(start_time):
    return abs(int((start_time - datetime.datetime.now()).total_seconds()))


def parse_xml_log(path):
    tree = ET.parse(path)
    root = tree.getroot()
    it = root.iter()
    size = 0
    bounds = list()
    for item in it:
        size = size+1
        if item.get('clickable') == 'true':
            bounds.append(item.get('bounds'))

    try:
        choose = random.choice(bounds)
        axes = re.findall('\d+', choose)
        point = (random.randrange(int(axes[0]), int(axes[2])),
                 random.randrange(int(axes[1]), int(axes[3])))
    except ValueError:
        point = (random.randrange(0, 1080),
                 random.randrange(0, 1920))
    except IndexError:
        point = (random.randrange(0, 1080),
                 random.randrange(0, 1920))
    return size, point


def main(_):
    # Check binaries
    binaries = ['adb']
    check_binary(binaries)
    # Check dirs
    dirs = ['./output/xml',
            './output/pcap',
            './output/mp4',
            './output/top']
    check_dirs(dirs)
    # Clear env
    print('checked all binaries, dirs')

    # Setup android (tcpdump)
    #setup_android('/sdcard/tcpdump')

    # Get list of target apps
    if not os.path.exists('app_list.csv'):
        raise Exception('Need app_list.csv')
    app_list = list()
    with open('app_list.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row['package_name'])
            app_list.append(row['package_name'])
    # package_name = app_list[0]

    for package_name in app_list:
        pss = ['tcpdump',
               'screenrecord']
        clear_env(pss)
        # clear cache without user data
        # adb shell pm clear APKNAME
        # adb shell run-as APKNAME rm -rf /data/data/APKNAME/cache/*
        # adb shell su - c rm - rf /data/data/com.amazon.mShop.android.shopping/cache/*
        command = 'adb shell su -c rm -rf /data/data/{0}/cache/*'.format(package_name)
        try:
            command_check(command)
        except subprocess.CalledProcessError:
            pass
        command = 'adb shell su -c rm /sdcard/*.xml'
        try:
            command_check(command)
        except subprocess.CalledProcessError:
            pass
        command = 'adb shell su -c rm /sdcard/*.mp4'
        try:
            command_check(command)
        except subprocess.CalledProcessError:
            pass
        command = 'adb shell su -c rm /sdcard/*.pcap'
        try:
            command_check(command)
        except subprocess.CalledProcessError:
            pass
        print('removed cache')

        # create XML dir
        os.makedirs('./output/xml/{0}'.format(package_name),
                    exist_ok=True)
        os.makedirs('./output/top/{0}'.format(package_name),
                    exist_ok=True)

        # time_list
        timing_list = list()

        # execute tcpdump
        timing_list.append((time.time(), 'execute tcpdump'))
        command = 'adb shell su -c tcpdump -i wlan0 -w /sdcard/{0}.pcap'.format(package_name)
        tcpdump_proc = command_popen(command)

        # execute screenrecord
        command = 'adb shell screenrecord /sdcard/{0}.mp4'.format(package_name)
        screenrecord_proc = command_popen(command)

        # launch app
        start_time = datetime.datetime.now()
        ping_proc = send_ping()
        command = 'adb shell monkey -p {0} -c android.intent.category.LAUNCHER 1'.format(package_name)
        command_check(command)
        terminate_ping(ping_proc)

        # insert event
        for index in range(0, 10):
            size_list = list()
            # wait for rendering
            while True:
                if len(size_list) > 5:
                    size_list.pop(0)
                if len(size_list) == 5 and len(set(size_list)) == 1:
                    break
                print('size_list', size_list)
                # export XML log
                dump_time = get_second_from_start(start_time)
                if dump_time >= (index+1)*60:
                    break
                command = 'adb shell \'top -n 1 | grep {0}\' > ./output/top/{0}/{1}.txt'.format(package_name, dump_time)
                command_check(command)
                dump_time = get_second_from_start(start_time)
                command = 'adb shell uiautomator dump /sdcard/{0}.xml'.format(dump_time)
                dump_output = command_output(command)
                print('dump', dump_output)
                if not dump_output.startswith('UI hierchary dumped to:'):
                    # break
                    # raise Exception
                    size_list.append(0)
                    point = (random.randrange(0, 1080),
                             random.randrange(0, 1920))
                    continue
                # pull XML log
                command = 'adb pull /sdcard/{0}.xml ./output/xml/{1}/'.format(dump_time, package_name)
                command_check(command)
                last_xml = './output/xml/{0}/{1}.xml'.format(
                    package_name, dump_time)
                size, point = parse_xml_log(last_xml)
                size_list.append(size)
            print('touch', point)
            if point[0] != point[1]:
                command = 'adb shell input tap {0} {1}'.format(point[0], point[1])
            else:
                command = 'adb shell input keyevent KEYCODE_BACK'
            ping_proc = send_ping()
            command_check(command)
            terminate_ping(ping_proc)

        # stop app
        ping_proc = send_ping()
        for index in range(0, 5):
            command = 'adb shell input keyevent KEYCODE_BACK'
            command_check(command)
        command = 'adb shell am force-stop {0}'.format(package_name)
        command_check(command)
        terminate_ping(ping_proc)

        # terminate tcpdump
        tcpdump_proc.terminate()
        tcpdump_proc.kill()

        # terminate screenrecord
        screenrecord_proc.terminate()
        screenrecord_proc.kill()

        # why?
        pss = ['tcpdump',
               'screenrecord']
        terminate_env(pss)

        # pull tcpdump
        command = 'adb pull /sdcard/{0}.pcap ./output/pcap/'.format(package_name)
        command_check(command)

        # pull mp4
        command = 'adb pull /sdcard/{0}.mp4 ./output/mp4/'.format(package_name)
        command_check(command)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
      description='Mobile App Tester',
      formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-d', '--device', type=str,
      help=('the testing device id'))
    parser.add_argument('-r', '--root', action='store_true',
      help=('set a flag if the testing device was rooted'))
    parser.add_argument('-i', '--input', type=str,
      default='./applist.csv',
      help=('list of app package names to test(default: ./applist.csv)'))
    parser.add_argument('-o', '--output', type=str,
      default='./output',
      help=('output directory(default: ./output)'))
    parser.add_argument('-e', '--event', type=int,
      default=10,
      help=('the number of generated user event(default: 10)'))

    FLAGS, _ = parser.parse_known_args()

    main(_)

# ERROR
# adb: failed to install Gmail_v8.8.26.211559306.release_apkpure.com.apk: Failure [INSTALL_FAILED_ALREADY_EXISTS: Attempt to re-install com.google.android.gm without first uninstalling.]
