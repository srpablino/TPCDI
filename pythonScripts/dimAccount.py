from xml.dom import minidom
import csv
from sqlalchemy import create_engine
import cx_Oracle

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

xmldoc = minidom.parse('../inputFiles/Batch1/CustomerMgmt.xml')
itemlist = xmldoc.getElementsByTagName('TPCDI:Actions')[0].childNodes
print(len(itemlist))
with open('../outputANDCtlFiles/dimAccount/dimAccount.csv', 'w', newline='\n') as outputCSV:
    writer = csv.writer(outputCSV, delimiter='|')
    out = {}
    dic = {}
    final = {}
    id = 0
    for s in itemlist:
        if s.nodeType == 1:
            action  = s.getAttribute('ActionType')
            actionDate = s.getAttribute('ActionTS')
            account = s.getElementsByTagName('Account')
            customer = s.getElementsByTagName('Customer')
            endDate = '9999-12-31'
            for a in account:
                if a.nodeType != 1:
                    continue
                C_ID = customer[0].getAttribute('C_ID')

                #CA_B_ID = account[0].getElementsByTagName('CA_B_ID')[0].firstChild.data
                #CA_NAME = account[0].getElementsByTagName('CA_NAME')[0].firstChild.data
                #CA_ID = account[0].getAttribute('CA_ID')
                #CA_TAX_ST = account[0].getAttribute('CA_TAX_ST')

                try:
                    CA_B_ID = a.getElementsByTagName('CA_B_ID')[0].firstChild.data
                except:
                    CA_B_ID = None
                try:
                    CA_NAME = a.getElementsByTagName('CA_NAME')[0].firstChild.data
                except:
                    CA_NAME = None

                CA_ID = a.getAttribute('CA_ID')
                CA_TAX_ST = a.getAttribute('CA_TAX_ST')

                try:
                    BK_SK_ID = engine.execute(
                        "select SK_BrokerID from dimbroker where BrokerID = :filter",
                        filter=CA_B_ID).fetchone()[0]
                except:
                    BK_SK_ID = None
                try:
                    C_SK_ID = engine.execute(
                        "select SK_CustomerID from dimcustomer where CustomerID = :filter",
                        filter=C_ID).fetchone()[0]
                except:
                    C_SK_ID = None

                if action == "NEW" or "ADDACCT":
                    STATUS = "ACTIVE"
                    #id
                    out['id'] = id
                    id = id +1
                    # ACCOUNTID
                    out['CA_ID'] = CA_ID
                    # SK_BROKERID
                    out['BK_SK_ID'] = BK_SK_ID
                    # SK_CUSTOMERID
                    out['C_SK_ID'] = C_SK_ID
                    # STATUS
                    out['STATUS'] = "ACTIVE"
                    # ACCOUNTDESC
                    out['CA_NAME'] = CA_NAME
                    # TAXSTATUS
                    out['CA_TAX_ST'] = CA_TAX_ST
                    # ISCURRENT
                    out['ISCURRENT'] = '1'
                    # BATCHID
                    out['batchid'] = batchid
                    # EFFECTIVEDATE
                    out['EFFECTIVEDATE'] = actionDate
                    # ENDDATE
                    out['ENDDATE'] = endDate

                    dic[CA_ID] = out
                    final[id] = out
                elif action == "UPDACCT":
                    out = dic[CA_ID]
                    newVersion = out.copy()
                    out['ISCURRENT'] = '0'
                    out['ENDDATE'] = actionDate
                    if (CA_B_ID != None):
                        newVersion['CA_B_ID'] = CA_B_ID
                    if (CA_NAME != None):
                        newVersion['CA_NAME'] = CA_NAME
                    if (CA_TAX_ST) != None:
                        newVersion['CA_TAX_ST'] = CA_TAX_ST
                    newVersion['EFFECTIVEDATE'] = actionDate
                    newVersion['id'] = id
                    id = id +1
                    dic[CA_ID] = newVersion
                    final[id] = newVersion
                    final[out['id']] = out
                    writer.writerow(out)
                elif action == "CLOSEACCT":
                    out = dic[CA_ID]
                    newVersion = out.copy()
                    out['ENDDATE'] = actionDate
                    out['ISCURRENT'] = '0'
                    newVersion['STATUS'] = "INACTIVE"
                    newVersion['EFFECTIVEDATE'] = actionDate
                    dic[CA_ID] = newVersion
                    final[id] = newVersion
                    final[out['id']] = out
                    id = id +1

                elif action == "UPDCUST":
                    out = dic[CA_ID]
                    # SK_CUSTOMERID
                    newVersion = out.copy()
                    out['ENDDATE'] = actionDate
                    out['ISCURRENT'] = '0'
                    newVersion['C_SK_ID'] = C_SK_ID
                    newVersion['EFFECTIVEDATE'] = actionDate
                    dic[CA_ID] = newVersion
                    final[id] = newVersion
                    final[out['id']] = out
                    id = id + 1
                elif action == "INACT":
                    out = dic[CA_ID]
                    # SK_CUSTOMERID
                    newVersion = out.copy()
                    out['ENDDATE'] = actionDate
                    out['ISCURRENT'] = '0'
                    newVersion['C_SK_ID'] = C_SK_ID
                    newVersion['STATUS'] = "INACTIVE"
                    newVersion['EFFECTIVEDATE'] = actionDate
                    dic[CA_ID] = newVersion
                    final[id] = newVersion
                    final[out['id']] = out
                    id = id + 1
    for accountFinal in final:
        writer.writerow(accountFinal)
