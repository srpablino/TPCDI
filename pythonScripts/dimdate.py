with open('../outputANDCtlFiles/dimDate/Date_res.txt', 'w') as output:
	with open('../inputFiles/Batch1/Date.txt', 'r') as ins:
		for line in ins:
			arr = line.split('|')
			arr[-1] = '1'	 if arr[-1] == 'true' else '0'
			output.write('|'.join(arr) + '\n')