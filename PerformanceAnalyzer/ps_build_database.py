import sys
import csv
import statistics
import json


def main(argv):
    print(argv)
    si = list()
    fp = list()
    ll = list()
    cs = list()
    rt = list()
    for file_path in argv[1:]:
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            sii_dict = dict()
            sir_dict = dict()
            for row in reader:
                scene = eval(row[1])
                if scene[0] == 0:
                    sii_dict[row[0]] = float(row[2])
                else:
                    sir_list = sir_dict.get(row[0], list())
                    sir_list.append(float(row[2]))
                    sir_dict[row[0]] = sir_list
                fp.append(float(row[4]))
                ll.append(float(row[5]))
                cs.append(float(row[6]))
                rt.append(float(row[7]))
            for key in sii_dict.keys():
                if key not in sir_dict.keys():
                    si.append(sii_dict[key])
                else:
                    si_value = sii_dict[key]*0.7 + statistics.mean(sir_dict[key])*0.3
                    si.append(si_value)
    result = {'si': si,
              'fp': fp,
              'll': ll,
              'cs': cs,
              'rt': rt}
    with open('performance_score_database.json', 'w') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main(sys.argv)
