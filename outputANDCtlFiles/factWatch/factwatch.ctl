LOAD DATA
INFILE '/home/oracle/files_ready/WatchHistory_RES.csv'
APPEND
INTO TABLE factwatch
FIELDS TERMINATED BY ','
TRAILING NULLCOLS
(
      SK_CustomerID,
      SK_SecurityID,
      SK_DateID_DatePlaced DATE "YYYY-MM-DD",
      SK_DateID_DateRemoved DATE "YYYY-MM-DD",
      BatchID
)