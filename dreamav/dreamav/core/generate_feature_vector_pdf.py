import hashlib
import os

from dreamav.parser import pdf_parser

def extract(file):
    keywords = {'obj': 0,
                'endobj': 1,
                'stream': 2,
                'endstream': 3,
                'xref': 4,
                'trailer': 5,
                'startxref': 6,
                '/Page': 7,
                '/Encrypt': 8,
                '/ObjStm': 9,
                '/JS': 10,
                '/JavaScript': 11,
                '/AA': 12,
                '/OpenAction': 13,
                '/AcroForm': 14,
                '/JBIG2Decode': 15,
                '/RichMedia': 16,
                '/Launch': 17,
                '/EmbeddedFile': 18,
                '/XFA': 19,
                '/Type': 20,
                '/Catalog': 21,
                '/Version': 22,
                '/Pages': 23,
                '/rovers': 24,
                '/abdula': 25,
                '/Kids': 26,
                '/Count': 27,
                '/S': 28,
                '/Filter': 29,
                '/FlateDecode': 30,
                '/Length': 31,
                '/ASCIIHexDecode': 32,
                '/ASCII85Decode': 33,
                '/LZWDecode': 34,
                '/RunLengthDecode': 35,
                '/CCITTFaxDecode': 36,
                '/DCTDecode': 37,
                '/JPXDecode': 38,
                '/Crypt': 39
                }

    SIZE_OF_FEATURE_VECTOR = 128

    parsed_data = pdf_parser.get_tag(file)
    md5 = os.path.basename(file).split(".")[0]

    fixed_vector = [0 for _ in range(40)]
    feature_vector = [0 for _ in range(SIZE_OF_FEATURE_VECTOR)]
    version = [-1]

    lines = parsed_data.split("\n")

    for line in lines[:-1]:
        try:
            tag, contents = line.strip().split()

            hash_tag = hashlib.sha256(tag.encode()).hexdigest()

            if tag in keywords:
                fixed_vector[keywords[tag]] += contents

            elif tag != "PDF_Header":
                if "(" in contents:
                    feature_vector[int(hash_tag, 16) & (SIZE_OF_FEATURE_VECTOR - 1)] += int(contents[:-3])
                else:
                    feature_vector[int(hash_tag, 16) & (SIZE_OF_FEATURE_VECTOR - 1)] += int(contents)
            else:
                version[0] = float(contents)

        except:
            continue

    feature_vector = version + fixed_vector + feature_vector

    return feature_vector