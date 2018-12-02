load data 
infile 'dimTime.csv' "str '\r\n'"
append
into table DIMTIME
fields terminated by '|'
OPTIONALLY ENCLOSED BY '"' AND '"'
trailing nullcols
           ( SK_TIMEID,
             TIMEVALUE TIMESTAMP "HH24:MI:SS",
             HOURID,
             HOURDESC CHAR(20),
             MINUTEID,
             MINUTEDESC CHAR(20),
             SECONDID,
             SECONDDESC CHAR(20),
             MARKETHOURSFLAG CHAR(1),
             OFFICEHOURSFLAG CHAR(1)
           )
