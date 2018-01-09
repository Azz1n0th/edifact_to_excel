import tkinter
try:
    import urllib3
except ModuleNotFoundError:
        try:
            import importlib
            importlib.import_module('urllib3')
        except ImportError:
            import pip
            pip.main(['install', 'urllib3'])
            
import sqlite3
import re
import os
conn = sqlite3.connect('segments.sqlite')


def get_url_contents(url):
    http = urllib3.PoolManager()
    site = http.request('GET', url)
    try:
        return site.data.decode('utf-8')
    except UnicodeDecodeError:
        return site.data.decode('windows-1252')


# this one returns a list of all values of segments
def get_segments(segment_type, url):
    regex = '\r*\n\r*\n\s{' + '5,' + '}' + segment_type + '+\s+.*'
    target_url = get_url_contents(url)
    applied_regex = re.compile(regex)
    return applied_regex.findall(target_url)


def segment_list(segment, segm_type, url):
    container = get_segments(segm_type, url)
    conn.cursor().execute('CREATE TABLE IF NOT EXISTS segments(segment text, description text)')
    i = 0
    for item in container:
        cleared = item.strip('\r\n').strip(' ')
        qualifier = cleared[0:3].strip(' ')
        short_description = cleared[6:].strip(' ')
        conn.cursor().execute('INSERT INTO segments VALUES(?, ?)', (segment+'+'+qualifier, short_description))
        i += 1
    output_box.insert(tkinter.END, '{} {} added'.format(i, segment) + os.linesep)


def initiate_db():
    conn.cursor().execute('DROP TABLE IF EXISTS segments')
    segment_list('DTM', '\d', 'http://www.unece.org/trade/untdid/d01b/tred/tred2005.htm')
    segment_list('FTX', '[A-Z]', 'http://www.unece.org/trade/untdid/d01b/tred/tred4451.htm')
    segment_list('PRI', '[A-Z]', 'http://www.unece.org/trade/untdid/d01a/tred/tred5375.htm')
    segment_list('PRI', '[A-Z]', 'http://www.unece.org/trade/untdid/d01a/tred/tred5125.htm')
    segment_list('PRI', '[A-Z]', 'http://www.unece.org/trade/untdid/d01a/tred/tred5387.htm')
    segment_list('BGM', '\d', 'http://www.unece.org/trade/untdid/d01a/tred/tred1001.htm')
    segment_list('RFF', '[A-Z]', 'http://www.unece.org/trade/untdid/d01b/tred/tred1153.htm')
    segment_list('NAD', '[A-Z]', 'http://www.unece.org/trade/untdid/d04b/tred/tred3035.htm')
    segment_list('CUX', '\d', 'http://www.unece.org/trade/untdid/d06a/tred/tred6347.htm')
    segment_list('PIA', '\d', 'http://www.unece.org/trade/untdid/d11a/tred/tred4347.htm')
    segment_list('QTY', '\d', 'http://www.unece.org/trade/untdid/d09a/tred/tred6063.htm')
    segment_list('CTA', '[A-Z]', 'http://www.unece.org/trade/untdid/d11a/tred/tred3139.htm')
    segment_list('COM', '[A-Z]', 'http://www.unece.org/trade/untdid/d01a/tred/tred3155.htm')
    segment_list('MOA', '\d', 'http://www.unece.org/trade/untdid/d00a/tred/tred5025.htm')
    segment_list('IMD', '[A-Z]', 'http://www.unece.org/trade/untdid/d08a/tred/tred7077.htm')
    segment_list('LOC', '\d', 'http://www.unece.org/trade/untdid/d10a/tred/tred3227.htm')
    segment_list('GIN', '[A-Z]', 'http://www.unece.org/trade/untdid/d03b/tred/tred7405.htm')
    segment_list('TDT', '\d', 'http://www.unece.org/trade/untdid/d05b/tred/tred8051.htm')
    segment_list('MEA', '[A-Z]', 'http://www.unece.org/trade/untdid/d01a/tred/tred6311.htm')
    segment_list('PAT', '\d', 'http://www.unece.org/trade/untdid/d00a/tred/tred4279.htm')
    segment_list('TAX', '\d', 'http://www.unece.org/trade/untdid/d00a/tred/tred5283.htm')
    segment_list('FII', '[A-Z]', 'http://www.unece.org/trade/untdid/d01a/tred/tred3035.htm')
    segment_list('ALC', '[A-Z]', 'http://www.unece.org/trade/untdid/d00a/tred/tred5463.htm')
    segment_list('GIR', '\d', 'http://www.unece.org/trade/untdid/d00a/tred/tred7297.htm')
    segment_list('PCD', '\d', 'http://www.unece.org/trade/untdid/d00a/tred/tred5245.htm')
    conn.commit()



def translate_line(line):
    current_line = line.split(":")
    #try:
    current_line = current_line[0].split('+') + current_line[1:]
    #except ValueError:
    #   pass

    if len(current_line[0]) >= 3 and current_line[0] != 'COM' and current_line[0] != 'LIN':
        current_line = current_line[0] + '+' + current_line[1]
    elif current_line[0] == 'COM':
        current_line = current_line[0] + '+' + current_line[-1][0:2]
    elif current_line[0] == 'LIN':
        product_line = 'Product Line ' + current_line[1]
        current_line = line.replace(current_line[0] + '+' + current_line[1], product_line)
        return current_line
    else:
        current_line = current_line[0]
    try:
        line_description = conn.cursor().execute("SELECT description FROM segments WHERE segment=?", (current_line,)).fetchone()
    except sqlite3.InterfaceError:
        pass
    except sqlite3.OperationalError:
        output_box.insert(tkinter.END, 'Please update/retrieve Database')
    if line_description is not None and 'COM' not in current_line:
        line = line.replace(current_line, line_description[0])
        return line
    elif 'COM' in current_line:
        line = line.replace('COM', line_description[0])
        line = line.replace(line[-4:-1], "")
        return line
        print(line)
        print(current_line)
        print(line)
    else:
        return line


def get_input():
    # ADD a variable for the query strings at later stage
    text_value = entry_box.get('1.0', tkinter.END)
    output_box.delete('1.0', tkinter.END)
    split_output = text_value.split("\n")
    for output in split_output:
        output_box.insert(tkinter.END, translate_line(output) + os.linesep)


# initialize the main working window
window = tkinter.Tk(className='_EDIFACT Translator_')
window.geometry("1200x700")

input_box = tkinter.Frame(window, width=500, height=640)
input_box.grid(row=1, column=0)

output_box = tkinter.Frame(window, width=400, height=640)
output_box.grid(row=1, column=2)
# init the input box
label1 = tkinter.Label(input_box, text='EDI Message')
label1.grid(row=0, column=0)
entry_box = tkinter.Text(input_box, borderwidth=2, height=40, width=60, padx=2, pady=2)
entry_box.grid(row=1, column=0)
# translate button setup
button1 = tkinter.Button(window, height=1, width=8, text='Translate', command=get_input)
button1.grid(row=1, column=1, sticky='nse')
button2_text = 'Update' + os.linesep + 'or' + os.linesep + 'Retrieve' + os.linesep + 'Database'
button2 = tkinter.Button(window, height=1, width=6, text=button2_text, command=lambda: initiate_db())
button2.grid(row=1, column=4, sticky='nse')
# init an empty output box
label2 = tkinter.Label(output_box, text='Translated Message')
label2.grid(row=0, column=3)
output_box = tkinter.Text(output_box, height=40, width=60)
output_box.grid(row=1, column=3)


window.mainloop()
