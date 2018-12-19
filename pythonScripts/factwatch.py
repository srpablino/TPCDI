import cx_Oracle
from tqdm import tqdm

ORACLE_USER = 'usr'
ORACLE_PASS = 'passwd'
ORACLE_HOST = 'localhost'
ORACLE_PORT = '1521'
ORACLE_SN = 'xe'

conn = cx_Oracle.connect('{}/{}@{}:{}/{}'.format(ORACLE_USER, ORACLE_PASS, ORACLE_HOST, ORACLE_PORT, ORACLE_SN))
cr = conn.cursor()

path_to_dt = '/Users/epozdeev/Desktop/ms/DataWarehouses/tpc-di/Tools/dt/Batch1/'
path_to_res = '/Users/epozdeev/Desktop/ms/DataWarehouses/tpc-di/files_ready/'

#path_to_dt = '/home/oracle/Tools/DATA/Batch1/'
#path_to_res = '/home/oracle/files_ready/'

q = 'Select CUSTOMERID, SK_CustomerID from dimCustomer'
res = cr.execute(q).fetchall()
CUSTOMERID_SK_CustomerID_dict = {}
cnt = 0
for i in res:
	CUSTOMERID_SK_CustomerID_dict[i[0]] = i[1]

q = 'Select SYMBOL, SK_SecurityID from dimSecurity'
res = cr.execute(q).fetchall()

SYMBOL_SK_SecurityID = {}
cnt = 0
for i in res:
	SYMBOL_SK_SecurityID[i[0]] = i[1]



res_dict = {}

with open(path_to_dt + 'WatchHistory.txt', 'r') as inp:

	for line in tqdm(inp):
		line_vals = line.replace('\n', '').split('|')

		if line_vals[-1] == 'ACTV':

			if int(line_vals[0]) not in CUSTOMERID_SK_CustomerID_dict:
				continue
			SK_CustomerID = str(CUSTOMERID_SK_CustomerID_dict[int(line_vals[0])])

			if line_vals[1] not in SYMBOL_SK_SecurityID:
				continue
			SK_SecurityID = str(SYMBOL_SK_SecurityID[line_vals[1]])

			SK_DateID_DatePlaced = line_vals[2].split(' ')[0]

			SK_DateID_DateRemoved = ''

			BatchID = 0

			#outp.write(','.join([SK_CustomerID, SK_SecurityID, SK_DateID_DatePlaced, SK_DateID_DateRemoved, BatchID]) + '\n')

			res_dict[str(SK_CustomerID) + ',' + str(SK_SecurityID)] = [SK_DateID_DatePlaced, SK_DateID_DateRemoved, BatchID]

		elif line_vals[-1] == 'CNCL':

			if int(line_vals[0]) not in CUSTOMERID_SK_CustomerID_dict:
				continue
			SK_CustomerID = str(CUSTOMERID_SK_CustomerID_dict[int(line_vals[0])])

			if line_vals[1] not in SYMBOL_SK_SecurityID:
				continue
			SK_SecurityID = str(SYMBOL_SK_SecurityID[line_vals[1]])

			to_change = res_dict[str(SK_CustomerID) + ',' + str(SK_SecurityID)]

			to_change[1] = line_vals[2].split(' ')[0]
			to_change[2] = 1

			res_dict[str(SK_CustomerID) + ',' + str(SK_SecurityID)] = to_change
cr.close()
conn.close()

with open(path_to_res + 'WatchHistory_RES.csv', 'w') as outp:
	for i in res_dict:
		SK_CustomerID = i.split(',')[0]
		SK_SecurityID = i.split(',')[1]
		outp.write(','.join([SK_CustomerID, SK_SecurityID, str(res_dict[i][0]), str(res_dict[i][1]), str(res_dict[i][2])]) + '\n')

print('D O N E')
















