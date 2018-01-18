try:
    import xlsxwriter
except ImportError:
    import pip
    pip.main(['install', 'XlsxWriter'])
import sqlite3

input_file = input("Input File Name: ")
output_file = input("Output File Name: ")
line_separator = input("Please indicate PO Line Separator: ")

conn = sqlite3.connect("segments.sqlite")
workbook = xlsxwriter.Workbook(output_file)
worksheet = workbook.add_worksheet()


# convert an EDIFACT line to a list
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
        line1[1] = "COM+" + line1[-1]
        line1 = line1[1], line1[0][4:]
    elif "LIN+" in line1[0]:
        try:
            line1[-1] = int(line1[-1])
        except:
            pass
        if type(line1[-1]) is int:
            line1.remove(line1[-1])
        line1[0] = "LIN+" + line1[-1]
        line1.remove(line1[-1])
    else:
        pass
    return line1


# open file for translation.
with open(input_file, 'r') as test_file:
    segment_to_description = {}
    header = []
    column = 1
    skip_elements = ['UNA' ,'UNB', 'UNH', 'INV', 'UNT', 'UNZ']
    for line in test_file:
        content = ""
        line = line_to_list(line)
        if line_separator in line[0]:
            column += 1
        if line[0] not in segment_to_description.keys():
            try:
                description = conn.cursor().execute("SELECT description FROM segments WHERE segment=?",
                                                                                        (line[0],)).fetchone()[0]
                segment_to_description[line[0]] = description
                header.append(description)
                worksheet.write(0, header.index(description), description)
            except:
                pass
        for current in line[1:]:
            content += current + " "
        try:
            worksheet.write(int(column), int(header.index(segment_to_description[line[0]])), content)
        except:
            pass

workbook.close()
