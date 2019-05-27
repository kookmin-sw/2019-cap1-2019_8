import json
import numpy as np
import magic
import click
import os

from virus_total_apis import PublicApi

from dreamav.__init__ import __ROOT__
from dreamav.core import predict
from dreamav.util import generate_feature_vector_pdf

@click.command()
def start():
    os.system(f"uwsgi --ini {os.path.join(__ROOT__, 'dream.ini')} --chdir {os.path.join(__ROOT__, 'backends')}")

@click.command()
def stop():
    os.system("pkill uwsgi && pkill dreamav")

@click.command()
@click.argument("path", type=click.Path(exists=True))
def scan(path):
    # Fill in your VirusTotal public api key
    api_key = ''
    if api_key != '':
        try:
            vt = PublicApi(api_key)
            res = vt.scan_file(path)

            if res["response_code"] == 200:
                print("Complete Requesting Scan", path)
            else:
                print("Error")
        except Exception as e:
            print("Error:", e)
    else:
        print("Need VirusTotal API Key")

@click.command()
@click.argument("path", type=click.Path(exists=True))
def submit(path):
    file_name = os.path.basename(path)
    file_magic = magic.from_file(path)

    if "PDF" in file_magic:
        feature = generate_feature_vector_pdf.extract(path)
        output = predict.predict_pdf(feature)
    elif "Composite Document" in file_magic:
        f_list = np.array([path])
        output = predict.predict_msword(f_list, np.zeros((f_list.shape)))
    else:
        print(f"Unsupported file format", path)
        return
    print("#" * 50)
    print(f"File name: {file_name}")
    print(f"File type: {file_magic}")
    print(f"Probability of malicious: {json.dumps(output['result'], indent=4)}")
    print("#" * 50)

# if __name__ == '__main__':
#     main()