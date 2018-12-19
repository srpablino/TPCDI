#/Users/epozdeev/Desktop/ms/DataWarehouses/tpc-di/Tools/dt/Batch1/

#/home/oracle/files_ready/HR_res.csv 
#/home/oracle/Tools/DATA/Batch1/HR.csv

cntr = 0

with open('/Users/epozdeev/Desktop/ms/DataWarehouses/tpc-di/files_ready/HR_res.csv', 'w') as output:
	with open('/Users/epozdeev/Desktop/ms/DataWarehouses/tpc-di/Tools/dt/Batch1/HR.csv', 'r') as ins:
		for line in ins:
			arr = line.split(',')
			arr_res = [str(cntr)]
			cntr += 1

			for i in range(9):
				if i != 5 :
					arr_res.append(arr[i].replace('\n', ''))
			arr_res.append('1')
			arr_res.append('0')
			arr_res.append('9999-12-31')

			output.write(','.join(arr_res) + '\n')