LOAD DATA
INFILE '/home/oracle/files_ready/dimcustomer_FINAL.csv'
APPEND
INTO TABLE dimcustomer
FIELDS TERMINATED BY ','
TRAILING NULLCOLS
(
      CustomerID,
      TaxID,
      Status,
      LastName,
      FirstName,
      MiddleInitial,
      Gender,
      Tier,
      DOB DATE "YYYY-MM-DD",
      AddressLine1,
      AddressLine2,
      PostalCode,
      City,
      StateProv,
      Country,
      Phone1,
      Phone2,
      Phone3,
      Email1,
      Email2,
      NationalTaxRateDesc,
      NationalTaxRate,
      LocalTaxRateDesc,
      LocalTaxRate,
      AgencyID,
      CreditRating,
      NetWorth,
      MarketingNameplate,
      IsCurrent,
      BatchID,
      EffectiveDate DATE "YYYY-MM-DD",
      EndDate DATE "YYYY-MM-DD"
)
