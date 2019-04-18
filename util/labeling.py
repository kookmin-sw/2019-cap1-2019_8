import os
import shutil
import json
import glob
import magic

report_list = []
for path, dirs, files in os.walk(VT_REPORT_PATH):
    for file in files:
        if file.split(".")[-1] == "json":
            report_list.append(os.path.join(path, file))


print(len(report_list))
with open(CSV_PATH, "w") as f:
    f.write("file,label\n")
    for file in report_list:
        with open(file, "r") as r:
            report = json.load(r)

        try:
            file_hash = report["results"]["md5"]
            label = -1

            try:
                f_sec = report["results"]["scans"]["F-Secure"]["detected"]
            except:
                f_sec = None

            try:
                kas = report["results"]["scans"]["Kaspersky"]["detected"]
            except:
                kas = None

            try:
                sym = report["results"]["scans"]["Symantec"]["detected"]
            except:
                sym = None

            if (f_sec or kas or sym) is True:
                label = 1

            elif report["results"]["positives"] == 0:
                label = 0

            if label > -1:
                f.write(f"{file_hash},{label}\n")

        except Exception as e:
            print(e)
            pass




