with open('/home/oracle/files_ready/Date_res.txt', 'w') as output:
	with open('/home/oracle/Tools/DATA/Batch1/Date.txt', 'r') as ins:
	    for line in ins:
	        arr = line.split('|')
	        arr[-1] = '"1"' if arr[-1] == 'true' else '"0"'
	        output.write('|'.join(arr) + '\n')