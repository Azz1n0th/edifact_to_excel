try:
    import xlsxwriter
except ImportError:
    import pip
    pip.main(['install', 'XlsxWriter'])


def line_to_list(line):
    line1 = line.split("'")[0]
    line1 = line1[:4] + line1[4:].replace('+', ':')
    line1 = line1.split(':')
    while line1.count('') > 0:
        line1.remove('')
    return line1


test_line = "NAD+ST+++Companty Name+Address Line1+Address Line2+Addres Line3+Postcode+Country'"

print(line_to_list(test_line))
