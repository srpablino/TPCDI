from tqdm import tqdm_notebook as tqdm
from collections import defaultdict
from glob import glob
from datetime import datetime
import cx_Oracle

ORACLE_USER = 'system'
ORACLE_PASS = 'oracle'
ORACLE_HOST = 'localhost'
ORACLE_PORT = '1521'
ORACLE_SN = 'xe'

status_types = {}
with open('../../data/Batch1/StatusType.txt', 'r') as f:
    for line in f:
        split = line.split('|')
        status_types[split[0]] = split[1].strip()

finwire_schema = [
    ['PTS', 15],
    ['RecType', 3],
    ['Symbol', 15],
    ['IssueType', 6],
    ['Status', 4],
    ['Name', 70],
    ['ExID', 6],
    ['ShOut', 13],
    ['FirstTradeDate', 8],
    ['FirstTradeExchg', 8],
    ['Dividend', 12],
    ['CoNameOrCIK', None]
]

dim_security_map = {
    'SK_SecurityID': [True, ''],
    'Symbol': [False, 'Symbol'],
    'Issue': [False, 'IssueType'],
    'Status': [True, 'status_types[record[\'Status\']]'],
    'Name': [False, 'Name'],
    'ExchangeID': [False, 'ExID'],
    'SK_CompanyID': [False, 'CoNameOrCIK'],
    'SharesOutstanding': [False, 'ShOut'],
    'FirstTrade': [True, 'datetime.strptime(record[\'FirstTradeDate\'].split(\'-\')[0], \'%Y%M%d\').strftime(\'%Y-%M-%d\')'],
    'FirstTradeOnExchange': [True, 'datetime.strptime(record[\'FirstTradeExchg\'].split(\'-\')[0], \'%Y%M%d\').strftime(\'%Y-%M-%d\')'],
    'Dividend': [False, 'Dividend'],
    'IsCurrent': [True, '\'0\''],
    'BatchID': [True, '\'0\''],
    'EffectiveDate': [True, 'datetime.strptime(record[\'PTS\'], \'%Y%m%d-%H%M%S\').strftime(\'%Y-%m-%d %H:%M:%S\')'],
    'EndDate': [True, '']
}

conn = cx_Oracle.connect('{}/{}@{}:{}/{}'.format(ORACLE_USER, ORACLE_PASS, ORACLE_HOST, ORACLE_PORT, ORACLE_SN))
cr = conn.cursor()

dim_security = defaultdict(list)

for file in tqdm(sorted(glob('../../data/Batch1/FINWIRE*'))):
    if '_audit' in file:
        continue
    with open(file, 'r') as f:
        for line in f:
            if not line[15:18] == 'SEC':
                continue
                
            is_name = True if len(line) > 171 else False
            finwire_schema[-1][1] = 60 if is_name else 10
                
            offset = 0
            record = {}
            security = {}
            for entry in finwire_schema:
                value = line[offset:offset+entry[1]].strip()
                record[entry[0]] = value
                offset+=entry[1]
            for k, v in dim_security_map.items():
                if not v[0]:
                    security[k] = record[v[1]]
                else:
                    try:
                        security[k] = eval(v[1])
                    except:
                        if k == 'EffectiveDate':
                            eval(v[1])
                        security[k] = ''
            
            cond = 'name = \'{}\'' if is_name else 'companyId = {}'
            q = ('Select SK_CompanyID, CompanyID from dimCompany where {} '
                             'and to_date(\'{}\', \'YY-MM-DD HH24:MI:SS\') >= effectiveDate '
                             'and to_date(\'{}\', \'YY-MM-DD HH24:MI:SS\') < endDate')\
                             .format(cond.format(security['SK_CompanyID']),
                             security['EffectiveDate'],
                             security['EffectiveDate'])
            res = cr.execute(q).fetchone()
            
            security['SK_CompanyID'] = str(res[0])
            dim_security[res[1]].append(security)

cr.close()
conn.close()

for CIK, entries in tqdm(dim_security.items()):
    for (old,new) in zip(entries, entries[1:] + [None]):
        if not new:
            old['IsCurrent'] = '1'
            old['EndDate'] = '9999-12-31'
            continue
        old['EndDate'] = new['EffectiveDate']

with open('../generated_data/dimSecurity.csv', 'w') as out:
    for CIK, entries in tqdm(dim_security.items()):
        for entry in entries:
            try:
                out.write('|'.join(entry.values()) + '\n')
            except:
                print(entry.values())
                raise ValueError('')
