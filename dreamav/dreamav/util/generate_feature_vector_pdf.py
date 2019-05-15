import hashlib
import os

from dreamav.parser import pdf_parser

SIZE_OF_FEATURE_VECTOR = 128

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
    parsed_data = pdf_parser.get_tag(file)

    fixed_vector = [0 for _ in range(40)]
    feature_vector = [0 for _ in range(SIZE_OF_FEATURE_VECTOR)]
    version = [-1]

    lines = parsed_data.split("\n")

    for line in lines[:-1]:
        try:
            tag = "_".join(line.strip().split()[:-1])
            contents = line.strip().split()[-1]

            if tag in keywords:
                if "(" in contents:
                    fixed_vector[keywords[tag]] += int(contents[:contents.index("(")])
                else:
                    fixed_vector[keywords[tag]] += int(contents)

            elif tag != "PDF_Header":
                hash_tag = hashlib.sha256(tag.encode()).hexdigest()

                if "(" in contents:
                    feature_vector[int(hash_tag, 16) & (SIZE_OF_FEATURE_VECTOR - 1)] += int(
                        contents[:contents.index("(")])
                else:
                    feature_vector[int(hash_tag, 16) & (SIZE_OF_FEATURE_VECTOR - 1)] += int(contents)
            else:
                version[0] = float(contents)

        except Exception as e:
            print(line)
            print(e)
            print()
            continue

    feature_vector = version + fixed_vector + feature_vector

    return feature_vector