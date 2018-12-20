import csv
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import select
from sqlalchemy import or_
from datetime import datetime



import cx_Oracle

#SID = ORCL
#conn = cx_Oracle.connect('username/pass@//host:port/SID')

host=''
port=''
sid=''
user=''
password=''
sid = cx_Oracle.makedsn(host, port, sid=sid)

cstr = 'oracle://{user}:{password}@{sid}'.format(
    user=user,
    password=password,
    sid=sid
)

engine =  create_engine(
    cstr,
    convert_unicode=False,
    pool_recycle=10,
    pool_size=50,
    echo=True
)

with open("../inputFiles/Batch1_audit.csv") as batch_file:
    batch_reader = csv.reader(batch_file, delimiter=',')
    # [0]DataSet, [1]BatchID, [2]Date, [3]Attribute, [4]Value, [5]DValue
    batchRow = next(batch_reader)
    batchRow = next(batch_reader)
    # date1 = datetime.strptime(batchRow[2], formatDate).date()
    date1 = batchRow[2]
    batchRow = next(batch_reader)
    date2 = batchRow[2]
    batchid = batchRow[1]

    dateId1 = engine.execute(
        "select SK_DateID from dimdate where DateValue = to_Date(:filter,'yyyy-mm-dd')",
        filter=date1).fetchone()[0]
    dateId2 = engine.execute(
        "select SK_DateID from dimdate where DateValue = to_Date(:filter,'yyyy-mm-dd')",
        filter=date2).fetchone()[0]


with open("../inputFiles/Batch1/Prospect.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    with open('../outputANDCtlFiles/dimProspect/dimProspect.csv', 'w', newline='\n') as outputCSV:
        writer = csv.writer(outputCSV, delimiter='|')
        for row in csv_reader:
            out = row[0:1]
            out.append(dateId1)
            out.append(dateId2)
            out.append(batchid)
            out.append('0')
            out = out[0:] + row[1:]
            writer.writerow(out)