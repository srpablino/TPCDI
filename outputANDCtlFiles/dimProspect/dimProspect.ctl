load data 
infile '/home/pablo/BDMA/datawarehouses/tpcdi/git/TPCDI/outputANDCtlFiles/dimProspect/dimProspect.csv' "str '\r\n'"
append
into table DIMPROSPECT
fields terminated by '|'
OPTIONALLY ENCLOSED BY '"' AND '"'
trailing nullcols
           ( AGENCYID CHAR(30),
             SK_RECORDDATEID,
             SK_UPDATEDATEID,
             BATCHID,
             ISCUSTOMER CHAR(1),
             LASTNAME CHAR(30),
             FIRSTNAME CHAR(30),
             MIDDLEINITIAL CHAR(1),
             GENDER CHAR(1),
             ADDRESSLINE1 CHAR(80),
             ADDRESSLINE2 CHAR(80),
             POSTALCODE CHAR(12),
             CITY CHAR(25),
             STATE CHAR(20),
             COUNTRY CHAR(24),
             PHONE CHAR(30),
             INCOME,
             NUMBERCARS,
             NUMBERCHILDREN,
             MARITALSTATUS CHAR(1),
             AGE,
             CREDITRATING,
             OWNORRENTFLAG CHAR(1),
             EMPLOYER CHAR(30),
             NUMBERCREDITCARDS,
             NETWORTH,
             MARKETINGNAMEPLATE CHAR(100)
           )
