import urllib3
import sqlite3
import re


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
    conn = sqlite3.connect('segments.sqlite')
    conn.cursor().execute('CREATE TABLE IF NOT EXISTS segments(segment text, description text)')
    i = 0
    for item in container:
        cleared = item.strip('\r\n').strip(' ')
        qualifier = cleared[0:3].strip(' ')
        short_description = cleared[6:].strip(' ')
        conn.cursor().execute('INSERT INTO segments VALUES(?, ?)', (segment+'+'+qualifier, short_description))
        i += 1
    conn.commit()
    print('{} {} added'.format(i, segment))


def initiate_db():
    conn = sqlite3.connect('segments.sqlite')
    conn.cursor().execute('DROP TABLE IF EXISTS segments')
    segment_list('DTM', '\d', 'https://www.unece.org/trade/untdid/d01b/tred/tred2005.htm')
    segment_list('FTX', '[A-Z]', 'https://www.unece.org/trade/untdid/d01b/tred/tred4451.htm')
    segment_list('PRI', '[A-Z]', 'https://www.unece.org/trade/untdid/d01a/tred/tred5375.htm')
    segment_list('PRI', '[A-Z]', 'https://www.unece.org/trade/untdid/d01a/tred/tred5125.htm')
    segment_list('PRI', '[A-Z]', 'https://www.unece.org/trade/untdid/d01a/tred/tred5387.htm')
    segment_list('BGM', '\d', 'https://www.unece.org/trade/untdid/d01a/tred/tred1001.htm')
    segment_list('RFF', '[A-Z]', 'https://www.unece.org/trade/untdid/d01b/tred/tred1153.htm')
    segment_list('NAD', '[A-Z]', 'http://www.unece.org/trade/untdid/d04b/tred/tred3035.htm')
    segment_list('CUX', '\d', 'http://www.unece.org/trade/untdid/d06a/tred/tred6347.htm')
    segment_list('PIA', '\d', 'http://www.unece.org/trade/untdid/d11a/tred/tred4347.htm')
    segment_list('QTY', '\d', 'http://www.unece.org/trade/untdid/d09a/tred/tred6063.htm')
    segment_list('CTA', '[A-Z]', 'http://www.unece.org/trade/untdid/d11a/tred/tred3139.htm')
    segment_list('COM', '[A-Z]', 'https://www.unece.org/trade/untdid/d01a/tred/tred3155.htm')
    segment_list('MOA', '\d', 'https://www.unece.org/trade/untdid/d00a/tred/tred5025.htm')
    segment_list('IMD', '[A-Z]', 'http://www.unece.org/trade/untdid/d08a/tred/tred7077.htm')
    segment_list('LOC', '\d', 'http://www.unece.org/trade/untdid/d10a/tred/tred3227.htm')
    segment_list('GIN', '[A-Z]', 'http://www.unece.org/trade/untdid/d03b/tred/tred7405.htm')
    segment_list('TDT', '\d', 'http://www.unece.org/trade/untdid/d05b/tred/tred8051.htm')
    segment_list('MEA', '[A-Z]', 'https://www.unece.org/trade/untdid/d01a/tred/tred6311.htm')
    segment_list('PAT', '\d', 'https://www.unece.org/trade/untdid/d00a/tred/tred4279.htm')
    segment_list('TAX', '\d', 'https://www.unece.org/trade/untdid/d00a/tred/tred5283.htm')
    segment_list('FII', '[A-Z]', 'https://www.unece.org/trade/untdid/d01a/tred/tred3035.htm')
    segment_list('ALC', '[A-Z]', 'https://www.unece.org/trade/untdid/d00a/tred/tred5463.htm')
    segment_list('GIR', '\d', 'https://www.unece.org/trade/untdid/d00a/tred/tred7297.htm')
    segment_list('PCD', '\d', 'https://www.unece.org/trade/untdid/d00a/tred/tred5245.htm')


initiate_db()
