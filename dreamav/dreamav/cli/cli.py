import numpy as np
import magic
import click
import os

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
def scan():
    pass

@click.command()
# @click.argument("path")
@click.argument("path", type=click.Path(exists=True))
def submit(path):
    file_name = os.path.basename(path)
    file_magic = magic.from_file(path)

    if "PDF" in file_magic:
        feature = generate_feature_vector_pdf.extract(path)
        output = predict.predict_pdf(feature)
    elif "Microsoft Word" in file_magic:
        f_list = np.array([path])
        output = predict.predict_msword(f_list, np.zeros((f_list)))
    else:
        print(f"Unsupported file format", path)
        return
    print("#" * 30)
    print(f"File name: {file_name}")
    print(f"File type: {file_magic}")
    print(f"Malicious Probability: {output['result']}")
    print("#" * 30)

# if __name__ == '__main__':
#     main()