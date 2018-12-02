import csv
with open("../inputFiles/Batch1/Time.txt") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|')
    with open('../outputANDCtlFiles/dimTime/dimTime.csv', 'w', newline='\n') as outputCSV:
        writer = csv.writer(outputCSV, delimiter='|')
        for row in csv_reader:
            # SK_TIMEID row[0] OK
            # TIMEVALUE row[1] Need to
            # HOURID row[2]
            # HOURDESC row[3]
            # MINUTEID row[4]
            # MINUTEDESC row[5]
            # SECONDID row[6]
            # SECONDDESC row[7]
            # MARKETHOURSFLAG row[8]
            # OFFICEHOURSFLAG row[9]
            i = 8
            while i<10:
                if row[i] == "false":
                    row[i] = "f"
                elif row[i] == "true":
                    row[i] = "t"
                i+=1
            writer.writerow(row)