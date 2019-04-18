import hashlib
import os

from dreamav.parser import pdf_parser

def extract(file):
    SIZE_OF_FEATURE_VECTOR = 512

    parsed_data = pdf_parser.get_tag(file)
    md5 = os.path.basename(file).split(".")[0]

    feature_vector = [0 for _ in range(SIZE_OF_FEATURE_VECTOR)]
    version = [-1]

    lines = parsed_data.split("\n")

    for line in lines[:-1]:
        try:
            tag, contents = line.strip().split()

            hash_tag = hashlib.sha256(tag.encode()).hexdigest()

            if tag != "PDF_Header":
                if "(" in contents:
                    feature_vector[int(hash_tag, 16) & (SIZE_OF_FEATURE_VECTOR - 1)] += int(contents[:-3])
                else:
                    feature_vector[int(hash_tag, 16) & (SIZE_OF_FEATURE_VECTOR - 1)] += int(contents)
            else:
                version[0] = float(contents)

        except:
            continue

    feature_vector = version + feature_vector

    return feature_vector


if __name__ == '__main__':
    pass