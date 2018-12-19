#path_to_dt = '/Users/epozdeev/Desktop/ms/DataWarehouses/tpc-di/Tools/dt/Batch1/'
#path_to_res = '/Users/epozdeev/Desktop/ms/DataWarehouses/tpc-di/files_ready/'

path_to_dt = '/home/oracle/Tools/DATA/Batch1/'
path_to_res = '/home/oracle/files_ready/'


import xml.etree.ElementTree


def get_phone(n, cph_cc, cph_ac, cph_l, cph_ce):
	if (cph_cc is not None) and (cph_ac is not None) and (cph_l is not None):
		return '+' + cph_cc + ' (' + cph_ac + ') '+ cph_l
	if (cph_cc is None) and (cph_ac is not None) and (cph_l is not None):
		return '(' + cph_ac + ') ' + cph_l
	if (cph_ac is None) and (cph_l is not None):
		return cph_l
	if (cph_ce is not None):
		return 'Phone' + str(n) + cph_ce
	return ''

def get_mn(NetWorth, Income, NumberChildren, NumberCreditCards, Age, CreditRating, NumberCars):
	res = []

	#• HighValue: NetWorth > 1000000 or Income > 200000
	if ((NetWorth != '') and (NetWorth > 1000000)) or ((Income != '') and (Income > 200000)):
		res.append('HighValue')
	
	#• Expenses: NumberChildren > 3 or NumberCreditCards > 5
	if ((NumberChildren != '') and (NumberChildren > 3)) or ((NumberCreditCards != '') and (NumberCreditCards > 5)):
		res.append('Expenses')

	#• Boomer: Age > 45
	if (Age != '') and (Age > 45):
		res.append('Boomer')

	#• MoneyAlert: Income < 50000 or CreditRating < 600 or NetWorth < 100000
	if ((Income != '') and (Income < 50000)) or ((CreditRating != '') and (CreditRating < 600)) or ((NetWorth != '') and (NetWorth < 100000)):
		res.append('MoneyAlert')

	#• Spender: NumberCars > 3 or NumberCreditCards > 7
	if ((NumberCars != '') and (NumberCars > 3)) or ((NumberCreditCards != '') and (NumberCreditCards > 7)):
		res.append('Spender')

	#• Inherited: Age < 25 and NetWorth > 1000000
	if ((Age != '') and (Age < 25)) and ((NetWorth != '') and (NetWorth > 1000000)):
		res.append('Inherited')

	return '+'.join(res)

tax_dict = {}
with open(path_to_dt + 'TaxRate.txt', 'r') as ins:
	for line in ins:
		arr = line.split('|')
		tax_dict[arr[0]] = (arr[1], float(arr[2]))

prospect_dict = {}
with open(path_to_dt + 'Prospect.csv', 'r') as ins:
	for line in ins:
		arr = line.split(',')
		key = str(arr[1]).upper() + str(arr[2]).upper() + str(arr[5]).upper() + str(arr[6]).upper() + str(arr[7]).upper()

		NetWorth = int(arr[21]) if arr[21].isdigit() else ''
		Income = int(arr[12]) if arr[12].isdigit() else '' 
		NumberChildren = int(arr[14]) if arr[14].isdigit() else '' 
		NumberCreditCards = int(arr[20]) if arr[20].isdigit() else '' 
		Age = int(arr[16]) if arr[16].isdigit() else '' 
		CreditRating = int(arr[18]) if arr[18].isdigit() else '' 
		NumberCars = int(arr[13]) if arr[13].isdigit() else ''		
		
		val = (arr[0], arr[17], arr[21], get_mn(NetWorth, Income, NumberChildren, NumberCreditCards, Age, CreditRating, NumberCars))
		prospect_dict[key] = val

actions = xml.etree.ElementTree.parse(path_to_dt + 'CustomerMgmt.xml').getroot()

updcust_dict = {}

with open(path_to_res + 'dimcustomer.csv', 'w') as output:
	for action in actions:
		
		ACTION_TYPE = action.attrib['ActionType']
		arr_res = []

	
		cid = action.find('Customer').attrib['C_ID']
		ctaxid = action.find('Customer').attrib['C_TAX_ID'] if 'C_TAX_ID' in action.find('Customer').attrib else ''
		cln = action.find('Customer').find('Name').find('C_L_NAME').text if action.find('Customer').find('Name') is not None else ''
		cfn = action.find('Customer').find('Name').find('C_F_NAME').text if action.find('Customer').find('Name') is not None else ''
		cmn = action.find('Customer').find('Name').find('C_M_NAME').text if action.find('Customer').find('Name') is not None else ''
		cmn = cmn if cmn is not None else ''
		ct = action.find('Customer').attrib['C_TIER'] if 'C_TIER' in action.find('Customer').attrib else ''
		cdob = action.find('Customer').attrib['C_DOB'] if 'C_DOB' in action.find('Customer').attrib else ''
		cpe = action.find('Customer').find('ContactInfo').find('C_PRIM_EMAIL') if action.find('Customer').find('ContactInfo') is not None else ''
		cpe = cpe.text if ((cpe is not None) and (cpe != '')) else ''
		cae = action.find('Customer').find('ContactInfo').find('C_ALT_EMAIL') if action.find('Customer').find('ContactInfo') is not None else ''
		cae = cae.text if ((cae is not None) and (cae != '')) else ''
		cg = 'U' if 'C_GNDR' not in action.find('Customer').attrib else 'M' if action.find('Customer').attrib['C_GNDR'] == 'M' else 'F' if action.find('Customer').attrib['C_GNDR'] == 'F' else 'U'
		cs = 'ACTIVE'
		cal1 = action.find('Customer').find('Address').find('C_ADLINE1') if action.find('Customer').find('Address') is not None else ''
		cal1 = cal1.text if ((cal1 is not None) and (cal1 != '')) else ''
		cal2 = action.find('Customer').find('Address').find('C_ADLINE2') if action.find('Customer').find('Address') is not None else ''
		cal2 = cal2.text if ((cal2 is not None) and (cal2 != '')) else ''
		czip = action.find('Customer').find('Address').find('C_ZIPCODE') if action.find('Customer').find('Address') is not None else ''
		czip = czip.text if ((czip is not None) and (czip != '')) else ''
		ccit = action.find('Customer').find('Address').find('C_CITY') if action.find('Customer').find('Address') is not None else ''
		ccit = ccit.text if ((ccit is not None) and (ccit != '')) else ''
		csp = action.find('Customer').find('Address').find('C_STATE_PROV') if action.find('Customer').find('Address') is not None else ''
		csp = csp.text if ((csp is not None) and (csp != '')) else ''
		ccoun = action.find('Customer').find('Address').find('C_CTRY') if action.find('Customer').find('Address') is not None else ''
		ccoun = ccoun.text if ((ccoun is not None) and (ccoun != '')) else ''
		ccoun = ccoun if ccoun is not None else ''
		cph1cc = action.find('Customer').find('ContactInfo').find('C_PHONE_1').find('C_CTRY_CODE').text if action.find('Customer').find('ContactInfo') is not None else ''
		cph1ac = action.find('Customer').find('ContactInfo').find('C_PHONE_1').find('C_AREA_CODE').text if action.find('Customer').find('ContactInfo') is not None else ''
		cph1l = action.find('Customer').find('ContactInfo').find('C_PHONE_1').find('C_LOCAL').text if action.find('Customer').find('ContactInfo') is not None else ''
		cph1ce = action.find('Customer').find('ContactInfo').find('C_PHONE_1').find('C_EXT').text if action.find('Customer').find('ContactInfo') is not None else ''
		cph1 = get_phone(1, cph1cc, cph1ac, cph1l, cph1ce)
		cph1 = cph1 if cph1 is not None else ''
		cph2cc = action.find('Customer').find('ContactInfo').find('C_PHONE_2').find('C_CTRY_CODE').text if action.find('Customer').find('ContactInfo') is not None else ''
		cph2ac = action.find('Customer').find('ContactInfo').find('C_PHONE_2').find('C_AREA_CODE').text if action.find('Customer').find('ContactInfo') is not None else ''
		cph2l = action.find('Customer').find('ContactInfo').find('C_PHONE_2').find('C_LOCAL').text if action.find('Customer').find('ContactInfo') is not None else ''
		cph2ce = action.find('Customer').find('ContactInfo').find('C_PHONE_2').find('C_EXT').text if action.find('Customer').find('ContactInfo') is not None else ''
		cph2 = get_phone(2, cph2cc, cph2ac, cph2l, cph2ce)
		cph2 = cph2 if cph2 is not None else ''
		cph3cc = action.find('Customer').find('ContactInfo').find('C_PHONE_3').find('C_CTRY_CODE').text if action.find('Customer').find('ContactInfo') is not None else ''
		cph3ac = action.find('Customer').find('ContactInfo').find('C_PHONE_3').find('C_AREA_CODE').text if action.find('Customer').find('ContactInfo') is not None else '' 
		cph3l = action.find('Customer').find('ContactInfo').find('C_PHONE_3').find('C_LOCAL').text if action.find('Customer').find('ContactInfo') is not None else ''
		cph3ce = action.find('Customer').find('ContactInfo').find('C_PHONE_3').find('C_EXT').text if action.find('Customer').find('ContactInfo') is not None else ''
		cph3 = get_phone(3, cph3cc, cph3ac, cph3l, cph3ce)
		cph3 = cph3 if cph3 is not None else ''
		cntaxid = action.find('Customer').find('TaxInfo').find('C_NAT_TX_ID').text if action.find('Customer').find('TaxInfo') is not None else ''
		cltaxid = action.find('Customer').find('TaxInfo').find('C_LCL_TX_ID').text if action.find('Customer').find('TaxInfo') is not None else ''
		ntrd = tax_dict[cntaxid][0] if cntaxid != '' else ''
		ntr = tax_dict[cntaxid][1] if cntaxid != '' else ''
		ltrd = tax_dict[cltaxid][0] if cltaxid != '' else ''
		ltr = tax_dict[cltaxid][1] if cltaxid != '' else ''

		prospect_match_key = str(cln).upper()+str(cfn).upper()+str(cal1).upper()+str(cal2).upper()+str(czip).upper()

		if prospect_match_key in prospect_dict:
			prospect_match = prospect_dict[prospect_match_key]
			caid = prospect_match[0]
			ccr = prospect_match[1]
			cnw = prospect_match[2]
			cmt = prospect_match[3]
		else:
			caid = ''
			ccr = ''
			cnw = ''
			cmt = ''

		#arr_res.append('') #SK_CustomerID
		arr_res.append(cid) #CustomerID
		arr_res.append(ctaxid) #TaxID
		arr_res.append(cs) #Status
		arr_res.append(cln) #LastName 3
		arr_res.append(cfn) #FirstName 4
		arr_res.append(cmn) #MiddleInitial
		arr_res.append(cg) #Gender
		arr_res.append(ct) #Tier
		arr_res.append(cdob) #DOB
		arr_res.append(cal1) #AddressLine1 9 
		arr_res.append(cal2) #AddressLine2 10
		arr_res.append(czip) #PostalCode 11
		arr_res.append(ccit) #City
		arr_res.append(csp) #StateProv
		arr_res.append(ccoun) #Country
		arr_res.append(cph1) #Phone1
		arr_res.append(cph2) #Phone2
		arr_res.append(cph3) #Phone3
		arr_res.append(cpe) #Email1
		arr_res.append(cae) #Email2
		arr_res.append(ntrd) #NationalTaxRateDesc
		arr_res.append(ntr) #NationalTaxRate
		arr_res.append(ltrd) #LocalTaxRateDesc
		arr_res.append(ltr) #LocalTaxRate
		arr_res.append(caid) #AgencyID
		arr_res.append(ccr) #CreditRating
		arr_res.append(cnw) #NetWorth
		arr_res.append(cmt) #MarketingNameplate
		arr_res.append(1) #IsCurrent
		arr_res.append(0) #BatchID
		arr_res.append('2018-12-02') #EffectiveDate
		arr_res.append('9999-12-31') #EndDate

		if ACTION_TYPE == 'NEW':
			output.write(','.join([str(x) for x in arr_res]).replace('\n', '') + '\n')

		elif ACTION_TYPE == 'UPDCUST':
			if cid in updcust_dict:
				updcust_dict[cid].append(['UPDCUST'] + (','.join([str(x) for x in arr_res]).replace('\n', '') + '\n').split(','))
			else:
				updcust_dict[cid] = []
				updcust_dict[cid].append(['UPDCUST'] + (','.join([str(x) for x in arr_res]).replace('\n', '') + '\n').split(','))


		elif ACTION_TYPE == 'INACT':
			if cid in updcust_dict:
				updcust_dict[cid].append(['INACT'] + (','.join([str(x) for x in arr_res]).replace('\n', '') + '\n').split(','))
			else:
				updcust_dict[cid] = []
				updcust_dict[cid].append(['INACT'] + (','.join([str(x) for x in arr_res]).replace('\n', '') + '\n').split(','))

with open(path_to_res + 'dimcustomer.csv', 'r') as inp:
	with open(path_to_res + 'dimcustomer_FINAL.csv', 'w') as output:
		for line in inp:

			values = line.split(',')
			current_cid = values[0]

			if current_cid in updcust_dict:

				for st in updcust_dict[current_cid]:
					if st[0] == 'UPDCUST':

						stat = st[1:]
						new_values = []
						new_values.append(values[0])

						for i in range(1, len(stat)):
							if (stat[i] != ''):
								new_values.append(stat[i])
							else:
								new_values.append(values[i])

						prospect_match_key = str(stat[3]).upper()+str(stat[4]).upper()+str(stat[9]).upper()+str(stat[10]).upper()+str(stat[11]).upper()

						if prospect_match_key in prospect_dict:

							prospect_match = prospect_dict[prospect_match_key]
							new_values[24] = prospect_match[0]
							new_values[25] = prospect_match[1]
							new_values[26] = prospect_match[2]
							new_values[27] = prospect_match[3]
					
					elif st[0] == 'INACT':
						new_values = values.copy()
						new_values[2] = 'INACTIVE'

						stat = st[1:]
						prospect_match_key = str(stat[3]).upper()+str(stat[4]).upper()+str(stat[9]).upper()+str(stat[10]).upper()+str(stat[11]).upper()

						if prospect_match_key in prospect_dict:
							prospect_match = prospect_dict[prospect_match_key]
							new_values[24] = prospect_match[0]
							new_values[25] = prospect_match[1]
							new_values[26] = prospect_match[2]
							new_values[27] = prospect_match[3]

					new_values[29] = str(int(new_values[29]) + 1) if (int(new_values[29]) + 1) < 3 else new_values[29]


			else:
				new_values = values.copy()

			output.write(','.join([str(x) for x in new_values]).replace('\n', '') + '\n')

print('DONE')







