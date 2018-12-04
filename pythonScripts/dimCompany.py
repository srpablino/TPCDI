from glob import glob
from collections import defaultdict
from tqdm import tqdm_notebook as tqdm
from datetime import datetime
from pprint import pprint


status_types = {}
with open('../data/Batch1/StatusType.txt', 'r') as f:
    for line in f:
        split = line.split('|')
        status_types[split[0]] = split[1].strip()


industries = {}
with open('../data/Batch1/Industry.txt', 'r') as f:
    for line in f:
        split = line.split('|')
        industries[split[0]] = split[1].strip()


finwire_schema = [
    ['PTS', 15],
    ['RecType', 3],
    ['CompanyName', 60],
    ['CIK', 10],
    ['Status', 4],
    ['IndustryID', 2],
    ['SPrating', 4],
    ['FoundingDate', 8],
    ['AddrLine1', 80],
    ['AddrLine2', 80],
    ['PostalCode', 12],
    ['City', 25],
    ['StateProvince', 20],
    ['Country', 24],
    ['CEOname', 46],
    ['Description', 150]
]


dim_company_map = {
    'SK_CompanyID': [True, ''],
    'CompanyID': [False, 'CIK'],
    'Status': [True, 'status_types[record[\'Status\']]'],
    'Name': [False, 'CompanyName'],
    'Industry': [True, 'industries[record[\'IndustryID\']]'],
    'SPrating': [False, 'SPrating'],
    'isLowGrade': [True, '\'0\' if record[\'SPrating\'] and (record[\'SPrating\'].startswith(\'A\') or record[\'SPrating\'].startswith(\'BBB\')) else \'1\''],
    'CEO': [False, 'CEOname'],
    'AddressLine1': [False, 'AddrLine1'],
    'AddressLine2': [False, 'AddrLine2'],
    'PostalCode': [False, 'PostalCode'],
    'City': [False, 'City'],
    'StateProv': [False, 'StateProvince'],
    'Country': [False, 'Country'],
    'Description': [False, 'Description'],
    'FoundingDate': [True, 'datetime.strptime(record[\'FoundingDate\'].split(\'-\')[0], \'%Y%M%d\').strftime(\'%Y-%M-%d\')'],
    'IsCurrent': [True, '\'0\''],
    'BatchID': [True, '\'0\''],
    'EffectiveDate': [True, 'datetime.strptime(record[\'PTS\'].split(\'-\')[0], \'%Y%M%d\').strftime(\'%Y-%M-%d\')'],
    'EndDate': [True, 'None']
}


dim_companies = defaultdict(list)

for file in tqdm(sorted(glob('../data/Batch1/FINWIRE*'))):
    if '_audit' in file:
        continue
    with open(file, 'r') as f:
        for line in f:
            if not line[15:18] == 'CMP':
                continue
            offset = 0
            record = {}
            company = {}
            for entry in finwire_schema:
                value = line[offset:offset+entry[1]].strip()
                record[entry[0]] = value
                offset+=entry[1]
            for k, v in dim_company_map.items():
                if not v[0]:
                    company[k] = record[v[1]]
                else:
                    try:
                        company[k] = eval(v[1])
                    except:
                        company[k] = ''

            dim_companies[record['CIK']].append(company)


for CIK, entries in tqdm(dim_companies.items()):
    for (old,new) in zip(entries, entries[1:] + [None]):
        if not new:
            old['IsCurrent'] = '1'
            old['EndDate'] = '9999-12-31'
            continue
        old['EndDate'] = new['EffectiveDate']


with open('./generated_data/dimCompany.csv', 'w') as out:
    for CIK, entries in tqdm(dim_companies.items()):
        for entry in entries:
            out.write('|'.join(entry.values()) + '\n')