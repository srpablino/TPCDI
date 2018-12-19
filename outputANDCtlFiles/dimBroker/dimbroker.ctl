LOAD DATA
INFILE '/home/oracle/files_ready/HR_res.csv'
APPEND
INTO TABLE dimbroker
FIELDS TERMINATED BY ','
TRAILING NULLCOLS
(
   SK_BrokerID,
   BrokerID,
   ManagerID,
   FirstName,
   LastName,
   MiddleInitial,
   Branch,
   Office,
   Phone,
   IsCurrent,
   BatchID,
   EffectiveDate expression "(select min(datevalue) from dimdate)",
   EndDate DATE "YYYY-MM-DD"
)
