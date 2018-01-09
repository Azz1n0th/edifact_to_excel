try:
    import xlsxwriter
except ImportError:
    import pip
    pip.main(['install', 'XlsxWriter'])
import sqlite3

conn = sqlite3.connect("segments.sqlite")
workbook = xlsxwriter.Workbook('Report.xlsx')
worksheet = workbook.add_worksheet()


def line_to_list(line):
    if "'" in line:
        line1 = line.split("'")[0]
    else:
        line1 = line
    line1 = line1[:4] + line1[4:].replace('+', ':')
    line1 = line1.split(':')
    while line1.count('') > 0:
        line1.remove('')
    if "COM+" in line1[0]:
        line1[1] = "COM+" + line1[1]
        line1[1], line1[0] = line1
        line1[1] = line1[1].strip("COM+")
        return line1
    else:
        return line1


# open file translation file. File must be with Start BGM and finish before UNT+

with open("test_semple.txt", 'r') as test_file:
    segment_to_description = dict()
    header = []
    for line in test_file:
        line = line_to_list(line)
        if line[0] not in segment_to_description.keys() and "LIN+" not in line[0]:
            description = conn.cursor().execute("SELECT description FROM segments WHERE segment=?",
                                                (line[0],)).fetchone()[0]
            segment_to_description[line[0]] = description
            header.append(description)

workbook.close()
