import sys
import csv
import json
import statistics

from scipy import stats


def main(argv):
    print(argv)
    with open(argv[1], 'r') as f:
        data = json.load(f)
    si = data['si']
    fp = data['fp']
    ll = data['ll']
    cs = data['cs']
    rt = data['rt']
    new_items = list()
    with open(argv[2], 'r') as f:
        reader = csv.reader(f)
        sii_dict = dict()
        sir_dict = dict()
        fpi_dict = dict()
        fpr_dict = dict()
        lli_dict = dict()
        llr_dict = dict()
        csi_dict = dict()
        csr_dict = dict()
        rti_dict = dict()
        rtr_dict = dict()
        for row in reader:
            scene = eval(row[1])
            if scene[0] == 0:
                sii_dict[row[0]] = float(row[2])
                fpi_dict[row[0]] = float(row[4])
                lli_dict[row[0]] = float(row[5])
                csi_dict[row[0]] = float(row[6])
                rti_dict[row[0]] = float(row[7])
            else:
                sir_list = sir_dict.get(row[0], list())
                sir_list.append(float(row[2]))
                sir_dict[row[0]] = sir_list
                fpr_list = fpr_dict.get(row[0], list())
                fpr_list.append(float(row[4]))
                fpr_dict[row[0]] = fpr_list
                llr_list = llr_dict.get(row[0], list())
                llr_list.append(float(row[5]))
                llr_dict[row[0]] = llr_list
                csr_list = csr_dict.get(row[0], list())
                csr_list.append(float(row[6]))
                csr_dict[row[0]] = csr_list
                rtr_list = rtr_dict.get(row[0], list())
                rtr_list.append(float(row[7]))
                rtr_dict[row[0]] = rtr_list
        for key in sii_dict.keys():
            if key not in sir_dict.keys():
                si_value = sii_dict[key]
                fp_value = fpi_dict[key]
                ll_value = lli_dict[key]
                cs_value = csi_dict[key]
                rt_value = rti_dict[key]
            else:
                si_value = sii_dict[key] * 0.7 + statistics.mean(sir_dict[key]) * 0.3
                fp_value = fpi_dict[key] * 0.7 + statistics.mean(fpr_dict[key]) * 0.3
                ll_value = lli_dict[key] * 0.7 + statistics.mean(llr_dict[key]) * 0.3
                cs_value = csi_dict[key] * 0.7 + statistics.mean(csr_dict[key]) * 0.3
                rt_value = rti_dict[key] * 0.7 + statistics.mean(rtr_dict[key]) * 0.3
            si_score = 100-stats.percentileofscore(si, si_value)
            fp_score = 100-stats.percentileofscore(fp, fp_value)
            ll_score = 100-stats.percentileofscore(ll, ll_value)
            cs_score = 100-stats.percentileofscore(cs, cs_value)
            rt_score = 100-stats.percentileofscore(rt, rt_value)
            ps_score = si_score*0.6 + fp_score*0.1 + ll_score*0.1 + cs_score*0.1 + rt_score*0.1
            new_items.append([key, si_score, fp_score, ll_score, cs_score, rt_score, ps_score])

    with open(argv[3], 'w') as f:
        writer = csv.writer(f)
        for entry in new_items:
            writer.writerow(entry)


if __name__ == '__main__':
    main(sys.argv)
    

