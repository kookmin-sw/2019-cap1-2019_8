import hashlib
import xml.dom.minidom
import traceback
import sys
import zipfile
import urllib.request as urllib23
import os

def _c2bip3(string):
    if sys.version_info[0] > 2:
        return bytes([ord(x) for x in string])
    else:
        return string


class BinaryFile:
    def __init__(self, file):
        self.file = file
        if file == '':
            self.infile = sys.stdin
        elif file.lower().startswith('http://') or file.lower().startswith('https://'):
            try:
                if sys.hexversion >= 0x020601F0:
                    self.infile = urllib23.urlopen(file, timeout=5)
                else:
                    self.infile = urllib23.urlopen(file)
            except urllib23.HTTPError:
                print('Error accessing URL %s' % file)
                print(sys.exc_info()[1])
                sys.exit()
        elif file.lower().endswith('.zip'):
            try:
                self.zipfile = zipfile.ZipFile(file, 'r')
                self.infile = self.zipfile.open(self.zipfile.infolist()[0], 'r', _c2bip3('infected'))
            except:
                print('Error opening file %s' % file)
                print(sys.exc_info()[1])
                sys.exit()
        else:
            try:
                self.infile = open(file, 'rb')
            except:
                print('Error opening file %s' % file)
                print(sys.exc_info()[1])
                sys.exit()
        self.ungetted = []

    def byte(self):
        if len(self.ungetted) != 0:
            return self.ungetted.pop()
        inbyte = self.infile.read(1)
        if not inbyte or inbyte == '':
            self.infile.close()
            return None
        return ord(inbyte)

    def bytes(self, size):
        if size <= len(self.ungetted):
            result = self.ungetted[0:size]
            del self.ungetted[0:size]
            return result
        inbytes = self.infile.read(size - len(self.ungetted))
        if inbytes == '':
            self.infile.close()
        if type(inbytes) == type(''):
            result = self.ungetted + [ord(b) for b in inbytes]
        else:
            result = self.ungetted + [b for b in inbytes]
        self.ungetted = []
        return result

    def unget(self, byte):
        self.ungetted.append(byte)

    def ungets(self, bytes):
        bytes.reverse()
        self.ungetted.extend(bytes)


def _find_pdf_header_relaxed(binary_file_object):
    bytes = binary_file_object.bytes(1024)
    index = ''.join([chr(byte) for byte in bytes]).find('%PDF')
    if index == -1:
        binary_file_object.ungets(bytes)
        return ([], None)
    for end_header in range(index + 4, index + 4 + 10):
        if bytes[end_header] == 10 or bytes[end_header] == 13:
            break
    binary_file_object.ungets(bytes[end_header:])
    return (bytes[0:end_header], ''.join([chr(byte) for byte in bytes[index:end_header]]))


def _hexcode_2_string(char):
    if type(char) == int:
        return '#%02x' % char
    else:
        return char


def _swap_case(char):
    if type(char) == int:
        return ord(chr(char).swapcase())
    else:
        return char.swapcase()


def _hex_2_string(hex_name):
    return ''.join(map(_hexcode_2_string, hex_name))


def _swap_name(word_extract):
    return map(_swap_case, word_extract)


def _update_words(word, word_extract, slash, words, hexcode, names, last_name, inside_stream, entropy, f_out):
    if word != '':
        if slash + word in words:
            words[slash + word][0] += 1
            if hexcode:
                words[slash + word][1] += 1
        elif slash == '/' and names:
            words[slash + word] = [1, 0]
            if hexcode:
                words[slash + word][1] += 1
        if slash == '/':
            last_name = slash + word
        if slash == '':
            if word == 'stream':
                inside_stream = True
            if word == 'endstream':
                if inside_stream == True and entropy != None:
                    for char in 'endstream':
                        entropy.removeInsideStream(ord(char))
                inside_stream = False
        if f_out != None:
            if slash == '/' and '/' + word in (
            '/JS', '/JavaScript', '/AA', '/OpenAction', '/JBIG2Decode', '/RichMedia', '/Launch'):
                word_extractSwapped = _hex_2_string(_swap_name(word_extract))
                f_out.write(_c2bip3(word_extractSwapped))
                print('/%s -> /%s' % (_hex_2_string(word_extract), word_extractSwapped))
            else:
                f_out.write(_c2bip3(_hex_2_string(word_extract)))
    return ('', [], False, last_name, inside_stream)


class CVE_2009_3459:
    def __init__(self):
        self.count = 0

    def check(self, last_name, word):
        if (last_name == '/Colors' and word.isdigit() and int(
                word) > 2 ^ 24):  # decided to alert when the number of colors is expressed with more than 3 bytes
            self.count += 1


def _xml_add_attribute(xmlDoc, name, value=None):
    att = xmlDoc.createAttribute(name)
    xmlDoc.documentElement.setAttributeNode(att)
    if value != None:
        att.nodeValue = value

    return att


def _pdf_2_string(xmlDoc, nozero=False):
    result = 'PDFiD %s %s\n' % (
    xmlDoc.documentElement.getAttribute('Version'), xmlDoc.documentElement.getAttribute('Filename'))
    if xmlDoc.documentElement.getAttribute('ErrorOccured') == 'True':
        return result + '***Error occured***\n%s\n' % xmlDoc.documentElement.getAttribute('ErrorMessage')

    result = f' PDF_Header {xmlDoc.documentElement.getAttribute("Header").split("-")[-1]}\n'
    for node in xmlDoc.documentElement.getElementsByTagName('Keywords')[0].childNodes:
        if not nozero or nozero and int(node.getAttribute('Count')) > 0:
            result += ' %s %d' % (node.getAttribute('Name'), int(node.getAttribute('Count')))

            if int(node.getAttribute('HexcodeCount')) > 0:
                result += '(%d)' % int(node.getAttribute('HexcodeCount'))
            result += '\n'

    if xmlDoc.documentElement.getAttribute('CountEOF') != '':
        result += ' %s %d\n' % ('%%EOF', int(xmlDoc.documentElement.getAttribute('CountEOF')))

    if xmlDoc.documentElement.getAttribute('CountCharsAfterLastEOF') != '':
        result += ' %s %d\n' % (
        'After last %%EOF', int(xmlDoc.documentElement.getAttribute('CountCharsAfterLastEOF')))

    for node in xmlDoc.documentElement.getElementsByTagName('Dates')[0].childNodes:
        result += ' %s %s\n' % (node.getAttribute('Value'), node.getAttribute('Name'))

    if xmlDoc.documentElement.getAttribute('TotalEntropy') != '':
        result += ' Total entropy:           %s (%10s bytes)\n' % (
        xmlDoc.documentElement.getAttribute('TotalEntropy'), xmlDoc.documentElement.getAttribute('TotalCount'))

    if xmlDoc.documentElement.getAttribute('StreamEntropy') != '':
        result += ' Entropy inside streams:  %s (%10s bytes)\n' % (
        xmlDoc.documentElement.getAttribute('StreamEntropy'), xmlDoc.documentElement.getAttribute('StreamCount'))

    if xmlDoc.documentElement.getAttribute('NonStreamEntropy') != '':
        result += ' Entropy outside streams: %s (%10s bytes)\n' % (
        xmlDoc.documentElement.getAttribute('NonStreamEntropy'), xmlDoc.documentElement.getAttribute('NonStreamCount'))

    return result


def get_tag(file, names=True):
    word = ''
    word_extract = []
    hexcode = False
    last_name = ''
    inside_stream = False
    keywords = ['obj',
                'endobj',
                'stream',
                'endstream',
                'xref',
                'trailer',
                'startxref',
                '/Page',
                '/Encrypt',
                '/ObjStm',
                '/JS',
                '/JavaScript',
                '/AA',
                '/OpenAction',
                '/AcroForm',
                '/JBIG2Decode',
                '/RichMedia',
                '/Launch',
                '/EmbeddedFile',
                '/XFA',
                '/Type',
                '/Catalog',
                '/Version',
                '/Pages',
                '/rovers',
                '/abdula',
                '/Kids',
                '/Count',
                '/S',
                '/Filter',
                '/FlateDecode',
                '/Length',
                '/ASCIIHexDecode',
                '/ASCII85Decode',
                '/LZWDecode',
                '/RunLengthDecode',
                '/CCITTFaxDecode',
                '/DCTDecode',
                '/JPXDecode',
                '/Crypt'
                ]
    words = {}
    dates = []

    for keyword in keywords:
        words[keyword] = [0, 0]
    slash = ''
    xmlDoc = xml.dom.minidom.getDOMImplementation().createDocument(None, 'PDFiD', None)
    _xml_add_attribute(xmlDoc, 'Filename', file)
    att_error_occured = _xml_add_attribute(xmlDoc, 'ErrorOccured', 'False')
    att_error_message = _xml_add_attribute(xmlDoc, 'ErrorMessage', '')

    pdf_date = None
    entropy = None
    pdf_eof = None
    cve_2009_3459 = CVE_2009_3459()
    try:
        att_is_pdf = xmlDoc.createAttribute('IsPDF')
        xmlDoc.documentElement.setAttributeNode(att_is_pdf)
        binary_file_object = BinaryFile(file)
        (bytes_header, pdf_header) = _find_pdf_header_relaxed(binary_file_object)
        f_out = None
        if entropy != None:
            for byteHeader in bytes_header:
                entropy.add(byteHeader, inside_stream)

        if pdf_header == None:
            att_is_pdf.nodeValue = 'False'

            return _pdf_2_string(xmlDoc)

        else:
            if pdf_header == None:
                att_is_pdf.nodeValue = 'False'
                pdf_header = ''

            else:
                att_is_pdf.nodeValue = 'True'
            att = xmlDoc.createAttribute('Header')
            att.nodeValue = repr(pdf_header[0:10]).strip("'")
            xmlDoc.documentElement.setAttributeNode(att)
        byte = binary_file_object.byte()
        while byte != None:
            char = chr(byte)
            charUpper = char.upper()
            if charUpper >= 'A' and charUpper <= 'Z' or charUpper >= '0' and charUpper <= '9':
                word += char
                word_extract.append(char)

            elif slash == '/' and char == '#':
                d1 = binary_file_object.byte()
                if d1 != None:
                    d2 = binary_file_object.byte()

                    if d2 != None and (chr(d1) >= '0' and chr(d1) <= '9' or chr(d1).upper() >= 'A' and chr(
                            d1).upper() <= 'F') and (
                            chr(d2) >= '0' and chr(d2) <= '9' or chr(d2).upper() >= 'A' and chr(d2).upper() <= 'F'):
                        word += chr(int(chr(d1) + chr(d2), 16))
                        word_extract.append(int(chr(d1) + chr(d2), 16))
                        hexcode = True

                        if entropy != None:
                            entropy.add(d1, inside_stream)
                            entropy.add(d2, inside_stream)

                        if pdf_eof != None:
                            pdf_eof.parse(d1)
                            pdf_eof.parse(d2)
                    else:
                        binary_file_object.unget(d2)
                        binary_file_object.unget(d1)
                        (word, word_extract, hexcode, last_name, inside_stream) = _update_words(word, word_extract,
                                                                                                slash, words, hexcode,
                                                                                                names, last_name,
                                                                                                inside_stream, entropy,
                                                                                                f_out)
                else:
                    binary_file_object.unget(d1)
                    (word, word_extract, hexcode, last_name, inside_stream) = _update_words(word, word_extract, slash,
                                                                                            words, hexcode, names,
                                                                                            last_name, inside_stream,
                                                                                            entropy, f_out)
            else:
                cve_2009_3459.check(last_name, word)

                (word, word_extract, hexcode, last_name, inside_stream) = _update_words(word, word_extract, slash,
                                                                                        words, hexcode, names,
                                                                                        last_name, inside_stream,
                                                                                        entropy, f_out)
                if char == '/':
                    slash = '/'
                else:
                    slash = ''

            if pdf_date != None and pdf_date.parse(char) != None:
                dates.append([pdf_date.date, last_name])

            if entropy != None:
                entropy.add(byte, inside_stream)

            if pdf_eof != None:
                pdf_eof.parse(char)

            byte = binary_file_object.byte()
        (word, word_extract, hexcode, last_name, inside_stream) = _update_words(word, word_extract, slash, words,
                                                                                hexcode, names, last_name,
                                                                                inside_stream, entropy, f_out)

        # check to see if file ended with %%EOF.  If so, we can reset charsAfterLastEOF and add one to EOF count.  This is never performed in
        # the parse function because it never gets called due to hitting the end of file.
        if byte == None and pdf_eof != None:
            if pdf_eof.token == '%%EOF':
                pdf_eof.cntEOFs += 1
                pdf_eof.cntCharsAfterLastEOF = 0
                pdf_eof.token = ''

    except SystemExit:
        sys.exit()
    except:
        att_error_occured.nodeValue = 'True'
        att_error_message.nodeValue = traceback.format_exc()

    att_entropy_all = xmlDoc.createAttribute('TotalEntropy')
    xmlDoc.documentElement.setAttributeNode(att_entropy_all)
    att_count_all = xmlDoc.createAttribute('TotalCount')
    xmlDoc.documentElement.setAttributeNode(att_count_all)
    att_entropy_stream = xmlDoc.createAttribute('StreamEntropy')
    xmlDoc.documentElement.setAttributeNode(att_entropy_stream)
    att_count_stream = xmlDoc.createAttribute('StreamCount')
    xmlDoc.documentElement.setAttributeNode(att_count_stream)
    att_entropy_non_stream = xmlDoc.createAttribute('NonStreamEntropy')
    xmlDoc.documentElement.setAttributeNode(att_entropy_non_stream)
    att_count_non_stream = xmlDoc.createAttribute('NonStreamCount')
    xmlDoc.documentElement.setAttributeNode(att_count_non_stream)
    if entropy != None:
        (countAll, entropyAll, countStream, entropyStream, countNonStream, entropyNonStream) = entropy.calc()
        att_entropy_all.nodeValue = '%f' % entropyAll
        att_count_all.nodeValue = '%d' % countAll
        if entropyStream == None:
            att_entropy_stream.nodeValue = 'N/A     '

        else:
            att_entropy_stream.nodeValue = '%f' % entropyStream
        att_count_stream.nodeValue = '%d' % countStream
        att_entropy_non_stream.nodeValue = '%f' % entropyNonStream
        att_count_non_stream.nodeValue = '%d' % countNonStream

    else:
        att_entropy_all.nodeValue = ''
        att_count_all.nodeValue = ''
        att_entropy_stream.nodeValue = ''
        att_count_stream.nodeValue = ''
        att_entropy_non_stream.nodeValue = ''
        att_count_non_stream.nodeValue = ''
    att_count_eof = xmlDoc.createAttribute('CountEOF')
    xmlDoc.documentElement.setAttributeNode(att_count_eof)

    att_count_chars_after_last_eof = xmlDoc.createAttribute('CountCharsAfterLastEOF')
    xmlDoc.documentElement.setAttributeNode(att_count_chars_after_last_eof)

    if pdf_eof != None:
        att_count_eof.nodeValue = '%d' % pdf_eof.cntEOFs
        if pdf_eof.cntEOFs > 0:
            att_count_chars_after_last_eof.nodeValue = '%d' % pdf_eof.cntCharsAfterLastEOF
        else:
            att_count_chars_after_last_eof.nodeValue = ''
    else:
        att_count_eof.nodeValue = ''
        att_count_chars_after_last_eof.nodeValue = ''

    ele_keywords = xmlDoc.createElement('Keywords')
    xmlDoc.documentElement.appendChild(ele_keywords)
    for keyword in keywords:
        ele_keyword = xmlDoc.createElement('Keyword')
        ele_keywords.appendChild(ele_keyword)
        att = xmlDoc.createAttribute('Name')
        att.nodeValue = keyword
        ele_keyword.setAttributeNode(att)
        att = xmlDoc.createAttribute('Count')
        att.nodeValue = str(words[keyword][0])
        ele_keyword.setAttributeNode(att)
        att = xmlDoc.createAttribute('HexcodeCount')
        att.nodeValue = str(words[keyword][1])
        ele_keyword.setAttributeNode(att)
    ele_keyword = xmlDoc.createElement('Keyword')
    ele_keywords.appendChild(ele_keyword)
    att = xmlDoc.createAttribute('Name')
    att.nodeValue = '/Colors_2^24'
    ele_keyword.setAttributeNode(att)
    att = xmlDoc.createAttribute('Count')
    att.nodeValue = str(cve_2009_3459.count)
    ele_keyword.setAttributeNode(att)
    att = xmlDoc.createAttribute('HexcodeCount')
    att.nodeValue = str(0)
    ele_keyword.setAttributeNode(att)
    if names:
        keys = sorted(words.keys())
        for word in keys:
            if not word in keywords:
                ele_keyword = xmlDoc.createElement('Keyword')
                ele_keywords.appendChild(ele_keyword)
                att = xmlDoc.createAttribute('Name')
                att.nodeValue = word
                ele_keyword.setAttributeNode(att)
                att = xmlDoc.createAttribute('Count')
                att.nodeValue = str(words[word][0])
                ele_keyword.setAttributeNode(att)
                att = xmlDoc.createAttribute('HexcodeCount')
                att.nodeValue = str(words[word][1])
                ele_keyword.setAttributeNode(att)
    ele_dates = xmlDoc.createElement('Dates')
    xmlDoc.documentElement.appendChild(ele_dates)
    dates.sort(key=lambda x: x[0])
    for date in dates:
        ele_date = xmlDoc.createElement('Date')
        ele_dates.appendChild(ele_date)
        att = xmlDoc.createAttribute('Value')
        att.nodeValue = date[0]
        ele_date.setAttributeNode(att)
        att = xmlDoc.createAttribute('Name')
        att.nodeValue = date[1]
        ele_date.setAttributeNode(att)
    return _pdf_2_string(xmlDoc)


