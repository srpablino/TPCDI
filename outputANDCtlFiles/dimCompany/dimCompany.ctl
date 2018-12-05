LOAD DATA
INFILE 'dimCompany.csv'
APPEND
INTO TABLE dimCompany
FIELDS TERMINATED BY '|'
TRAILING NULLCOLS
(
   SK_CompanyID,
   CompanyID,
   Status,
   Name,
   Industry,
   SPrating,
   isLowGrade,
   CEO,
   AddressLine1,
   AddressLine2,
   PostalCode,
   City,
   StateProv,
   Country,
   Description,
   FoundingDate DATE "YYYY-MM-DD",
   IsCurrent,
   BatchID,
   EffectiveDate DATE "YYYY-MM-DD HH24:MI:SS",
   EndDate DATE "YYYY-MM-DD HH24:MI:SS"
)
