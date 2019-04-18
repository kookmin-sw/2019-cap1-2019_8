import json
import os
import csv

_report_path = r''


def walk_dir(input_path):
    file_list = list()
    for path, dirs, files in os.walk(input_path):
        for file in files:
            file_path = os.path.join(path, file)
            file_list.append(file_path)
    return file_list


def file_parsing(report_list):
    file_dict = {}

    for file in report_list:
        file_name = os.path.basename(file).split('.')[0]

        with open(file, "r") as r:
            report = json.load(r)
        try:
            if report["results"]["positives"] >= 10:
                file_dict[file_name] = 1

            elif report["results"]["positives"] == 0:
                file_dict[file_name] = 0

        except Exception as ep:
            print("error: ", ep)

        finally:
            pass

    return file_dict


def csv_write(report_result_set):
    with open('output.csv', 'w', encoding='utf-8', newline='') as f:
        for i in list(report_result_set.keys()):
            wr = csv.writer(f)
            wr.writerow([i, report_result_set[i]])


if __name__ == '__main__':
    r_list = walk_dir(_report_path)
    f_dict = file_parsing(r_list)
    csv_write(f_dict)